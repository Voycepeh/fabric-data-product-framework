import pytest
from pyspark.sql import SparkSession
from fabricops_kit.config import create_ai_prompt_config
from fabricops_kit.dq import (
    validate_dq_rules,
    extract_candidate_rules_from_responses,
    build_dq_rules_metadata_df,
    build_dq_rule_deactivation_metadata_df,
    load_latest_active_dq_rules_from_metadata,
    split_valid_quarantine_and_failures,
    run_dq_rules,
    suggest_dq_rules_with_fabric_ai,
)

@pytest.fixture(scope='module')
def spark():
    s=SparkSession.builder.master('local[1]').appName('dq').getOrCreate(); yield s; s.stop()

def test_configured_prompt_contains_canonical_sections():
    prompt=create_ai_prompt_config().dq_rule_candidate_template
    for snippet in [
        "1. not_null", "2. unique_key", "Heuristics:",
        "Do not return Great Expectations, Deequ, DQX, SQL, or pseudocode syntax.",
        "DQ_RULES = {", "Column profile row:", "Business context:",
    ]:
        assert snippet in prompt

def test_suggest_uses_config_prompt():
    class AIFake:
        def __init__(self): self.prompt=None
        def generate_response(self, prompt, output_col): self.prompt=prompt; return {"prompt":prompt,"output_col":output_col}
    class DFFake:
        def __init__(self): self.ai=AIFake()
    df=DFFake(); prompt="PROMPT_FROM_CONFIG"
    out=suggest_dq_rules_with_fabric_ai(df,prompt_template=prompt,output_col='resp')
    assert out["prompt"]==prompt and out["output_col"]=='resp' and df.ai.prompt==prompt

def test_validation_canonical_types_and_fields():
    validate_dq_rules([{"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}])
    with pytest.raises(ValueError): validate_dq_rules([{"rule_id":"x","rule_type":"custom_condition","columns":["a"],"severity":"error","description":"d"}])

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
    rules=[{"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"},{"rule_id":"r2","rule_type":"unique_key","columns":["b"],"severity":"error","description":"d"},{"rule_id":"r3","rule_type":"regex_format","columns":["a"],"regex_pattern":"^[a-z]{2}$","severity":"warning","description":"fmt"}]
    _,_,f=split_valid_quarantine_and_failures(df,rules,dq_run_id='run1')
    assert f.filter("rule_id='r2'").count()==2 and f.filter("rule_id='r1'").count()==1
    out=run_dq_rules(df,'T',rules)
    by={r['rule_id']:r['status'] for r in out.collect()}
    assert set(by)=={'r1','r2','r3'} and by['r3']=='PASS'
