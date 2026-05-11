import pytest
from pyspark.sql import SparkSession
from fabricops_kit.dq import (
    validate_dq_rules,
    extract_candidate_rules_from_responses,
    build_dq_rules_metadata_df,
    build_dq_rule_deactivation_metadata_df,
    load_latest_active_dq_rules_from_metadata,
    split_valid_quarantine_and_failures,
    run_dq_rules,
)

@pytest.fixture(scope='module')
def spark():
    s=SparkSession.builder.master('local[1]').appName('dq').getOrCreate(); yield s; s.stop()

def test_validation_canonical_types_and_fields():
    validate_dq_rules([{"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}])
    with pytest.raises(ValueError): validate_dq_rules([{"rule_id":"x","rule_type":"custom_condition","columns":["a"],"severity":"error","description":"d"}])
    with pytest.raises(ValueError): validate_dq_rules([{"rule_id":"x","rule_type":"accepted_values","columns":["a"],"severity":"error","description":"d"}])
    with pytest.raises(ValueError): validate_dq_rules([{"rule_id":"x","rule_type":"not_null","columns":[],"severity":"bad","description":"d"}])

def test_extract_candidates_shape(spark):
    df=spark.createDataFrame([{"response":"DQ_RULES = {'T':[{'rule_id':'r1','rule_type':'not_null','columns':['a'],'severity':'error','description':'d'}]}"}])
    assert extract_candidate_rules_from_responses(df,'T')[0]['rule_id']=='r1'

def test_metadata_approval_deactivation_latest(spark):
    rule={"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}
    a=build_dq_rules_metadata_df(spark,'T',[rule],action_by='u')
    d=build_dq_rule_deactivation_metadata_df(spark,'T',[{"rule":rule,"action_reason":"bad"}],action_by='u2')
    assert load_latest_active_dq_rules_from_metadata(a.unionByName(d),'T')==[]

def test_quarantine_and_run_results_include_pass(spark):
    df=spark.createDataFrame([{"a":"","b":"x"},{"a":"ok","b":"x"},{"a":"ok","b":"y"}])
    rules=[
      {"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"},
      {"rule_id":"r2","rule_type":"unique_key","columns":["b"],"severity":"error","description":"d"},
      {"rule_id":"r3","rule_type":"regex_format","columns":["a"],"regex_pattern":"^[a-z]{2}$","severity":"warning","description":"fmt"}
    ]
    valid,q,f=split_valid_quarantine_and_failures(df,rules,dq_run_id='run1')
    assert f.filter("rule_id='r2'").count()==2 and f.filter("rule_id='r1'").count()==1
    assert f.filter("dq_run_id is not null and dq_row_id is not null and dq_quarantine_id is not null").count()==f.count()
    out=run_dq_rules(df,'T',rules)
    by={r['rule_id']:r['status'] for r in out.collect()}
    assert set(by)=={'r1','r2','r3'} and by['r3']=='PASS'
