import pytest
from pyspark.sql import SparkSession
from fabricops_kit.dq_rules import validate_dq_rules, extract_candidate_rules_from_responses, assert_dq_passed
from fabricops_kit.contract_guardrails import validate_contract_guardrails
from fabricops_kit.dq_rule_metadata import build_dq_rules_metadata_df, build_dq_rule_deactivation_metadata_df, load_latest_active_dq_rules_from_metadata
from fabricops_kit.quarantine import split_valid_quarantine_and_failures

@pytest.fixture(scope='module')
def spark():
    s=SparkSession.builder.master('local[1]').appName('dq').getOrCreate(); yield s; s.stop()

def test_dq_rule_types_only_canonical():
    validate_dq_rules([{"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}])
    with pytest.raises(ValueError): validate_dq_rules([{"rule_id":"x","rule_type":"custom_condition","columns":["a"],"severity":"error","description":"d"}])

def test_contract_guardrails_separate_validation():
    validate_contract_guardrails([{"rule_type":"row_count_between"}])
    with pytest.raises(ValueError): validate_contract_guardrails([{"rule_type":"not_null"}])

def test_extract_candidates_shape(spark):
    df=spark.createDataFrame([{"response":"DQ_RULES = {'T':[{'rule_id':'r1','rule_type':'not_null','columns':['a'],'severity':'error','description':'d'}]}"},{"response":"DQ_RULES = {'T':[{'rule_id':'r1','rule_type':'not_null','columns':['a'],'severity':'error','description':'d'}]}"}])
    out=extract_candidate_rules_from_responses(df,'T')
    assert len(out)==1 and out[0]['rule_id']=='r1'

def test_metadata_approval_deactivation_latest(spark):
    rule={"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}
    a=build_dq_rules_metadata_df(spark,'T',[rule],action_by='u')
    d=build_dq_rule_deactivation_metadata_df(spark,'T',[{"rule":rule,"action_reason":"bad"}],action_by='u2')
    meta=a.unionByName(d)
    assert load_latest_active_dq_rules_from_metadata(meta,'T')==[]

def test_quarantine_multi_fail_and_traceability(spark):
    df=spark.createDataFrame([{"a":"","b":"x"},{"a":"ok","b":"x"}])
    rules=[{"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"},{"rule_id":"r2","rule_type":"unique_key","columns":["b"],"severity":"error","description":"d"}]
    valid,q,f=split_valid_quarantine_and_failures(df,rules,dq_run_id='run1')
    assert q.filter("dq_run_id='run1'").count()==2
    assert f.filter("dq_row_id is not null and dq_quarantine_id is not null").count()==f.count()
    assert f.filter("rule_id='r1'").count()==1 and f.filter("rule_id='r2'").count()==2
    res=spark.createDataFrame([{"severity":"error","status":"FAIL"}])
    with pytest.raises(ValueError): assert_dq_passed(res)
