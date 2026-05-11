import pandas as pd
import pytest
from fabricops_kit.dq_rules import *
from fabricops_kit.dq_rule_metadata import *
from fabricops_kit.quarantine import split_valid_quarantine_and_failures
from fabricops_kit.contract_guardrails import *


def test_rule_types():
    assert set(AI_SUGGESTABLE_DQ_RULE_TYPES)=={'not_null','unique_key','accepted_values','value_range','regex_format'}

def test_ai_row_by_row_extraction():
    profile=[{'column_name':'a','data_type':'int','null_count':0,'distinct_count':2,'row_count':2}]
    responses=suggest_dq_rules_with_fabric_ai(profile,'t',fabric_ai_generate=lambda p,r:'{"rule_id":"R1","rule_type":"not_null","columns":["a"],"description":"x"}')
    rules=extract_candidate_rules_from_responses(responses)
    assert rules[0]['rule_id']=='R1'

def test_metadata_latest_active_and_deactivation():
    m1=build_dq_rules_metadata_df('t',[{'rule_id':'R1','rule_type':'not_null','columns':['a'],'description':'x'}],version=1)
    m2=build_dq_rule_deactivation_metadata_df(m1,'R1','no longer needed')
    allm=pd.concat([m1,m2],ignore_index=True)
    assert load_latest_active_dq_rules_from_metadata(allm)==[]

def test_dq_quarantine_and_evidence_multiple_failures_per_row():
    df=pd.DataFrame({'id':[1,1],'x':[None,5],'code':['BAD','OK']})
    rules=[{'rule_id':'r1','rule_type':'not_null','columns':['x'],'description':'x'}, {'rule_id':'r2','rule_type':'accepted_values','columns':['code'],'allowed_values':['OK'],'description':'c'}]
    evidence=run_dq_rules(df,rules)
    valid,quar,fail=split_valid_quarantine_and_failures(df,evidence)
    assert len(quar)==1 and len(fail)>=2
    with pytest.raises(ValueError): assert_dq_passed(evidence)

def test_contract_guardrails_separate():
    df=pd.DataFrame({'a':[1,2]})
    out=run_contract_guardrails(df,[{'rule_type':'row_count_between','min_count':3,'max_count':10}])
    assert out and out[0]['rule_type']=='row_count_between'
