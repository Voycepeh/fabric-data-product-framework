import pytest
import sys
import types
from pyspark.sql import SparkSession
from fabricops_kit.config import AIPromptConfig
from fabricops_kit.data_quality import (
    validate_dq_rules,
    extract_dq_rules,
    build_dq_rule_history,
    build_dq_rule_deactivations,
    load_active_dq_rules,
    split_dq_rows,
    run_dq_rules,
    suggest_dq_rules,
)

@pytest.fixture(scope='module')
def spark():
    s=SparkSession.builder.master('local[1]').appName('dq').getOrCreate(); yield s; s.stop()

def test_configured_prompt_contains_canonical_sections():
    prompt=AIPromptConfig(
        dq_rule_suggestion_prompt_template="Suggest candidate DQ rules as JSON. Profile: {profile}",
        governance_candidate_prompt_template="g",
        handover_summary_prompt_template="h",
    ).dq_rule_suggestion_prompt_template
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
    out=suggest_dq_rules(df,prompt_template=prompt,output_col='resp')
    assert out["prompt"]==prompt and out["output_col"]=='resp' and df.ai.prompt==prompt

def test_validation_canonical_types_and_fields():
    validate_dq_rules([{"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}])
    with pytest.raises(ValueError): validate_dq_rules([{"rule_id":"x","rule_type":"custom_condition","columns":["a"],"severity":"error","description":"d"}])

def test_extract_candidates_shape(spark):
    df=spark.createDataFrame([{"response":"DQ_RULES = {'T':[{'rule_id':'r1','rule_type':'not_null','columns':['a'],'severity':'error','description':'d'}]}"}])
    assert extract_dq_rules(df,'T')[0]['rule_id']=='r1'

def test_metadata_approval_deactivation_latest(spark):
    rule={"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}
    a=build_dq_rule_history(spark,'T',[rule],action_by='u')
    d=build_dq_rule_deactivations(spark,'T',[{"rule":rule,"action_reason":"bad"}],action_by='u2')
    assert load_active_dq_rules(a.unionByName(d),'T')==[]

def test_action_by_resolves_from_runtime_context_and_explicit_override(spark, monkeypatch):
    rule={"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"}

    runtime_mod = types.SimpleNamespace(context={"userName": "fabric_user", "userId": "id_1"})
    monkeypatch.setitem(sys.modules, "notebookutils.runtime", runtime_mod)
    rows = build_dq_rule_history(spark, "T", [rule]).collect()
    assert rows[0]["action_by"] == "fabric_user"

    runtime_mod = types.SimpleNamespace(context={"userId": "id_only"})
    monkeypatch.setitem(sys.modules, "notebookutils.runtime", runtime_mod)
    rows = build_dq_rule_history(spark, "T", [rule]).collect()
    assert rows[0]["action_by"] == "id_only"

    rows = build_dq_rule_history(spark, "T", [rule], action_by="explicit_user").collect()
    assert rows[0]["action_by"] == "explicit_user"

    deact = [{"rule": rule, "action_reason": "bad"}]
    rows = build_dq_rule_deactivations(spark, "T", deact).collect()
    assert rows[0]["action_by"] == "id_only"

def test_quarantine_and_run_results_include_pass(spark):
    df=spark.createDataFrame([{"a":"","b":"x"},{"a":"ok","b":"x"},{"a":"ok","b":"y"}])
    rules=[{"rule_id":"r1","rule_type":"not_null","columns":["a"],"severity":"error","description":"d"},{"rule_id":"r2","rule_type":"unique_key","columns":["b"],"severity":"error","description":"d"},{"rule_id":"r3","rule_type":"regex_format","columns":["a"],"regex_pattern":"^[a-z]{2}$","severity":"warning","description":"fmt"}]
    _,_,f=split_dq_rows(df,rules,dq_run_id='run1')
    assert f.filter("rule_id='r2'").count()==2 and f.filter("rule_id='r1'").count()==1
    out=run_dq_rules(df,'T',rules)
    by={r['rule_id']:r['status'] for r in out.collect()}
    assert set(by)=={'r1','r2','r3'} and by['r3']=='PASS'
