from __future__ import annotations
from typing import Any
from pyspark.sql import functions as F
CONTRACT_GUARDRAIL_RULE_TYPES={"row_count_between","schema_required_columns","schema_data_type"}

def validate_contract_guardrails(rules:list[dict[str,Any]])->list[dict[str,Any]]:
    if not isinstance(rules,list): raise ValueError("Contract guardrails must be a list.")
    for r in rules:
        if r.get("rule_type") not in CONTRACT_GUARDRAIL_RULE_TYPES: raise ValueError("unsupported guardrail rule_type")
    return rules

def run_contract_guardrails(df, guardrails:list[dict[str,Any]]):
    """Run contract guardrails separately and return Spark evidence rows."""
    validate_contract_guardrails(guardrails); rows=[]; cnt=df.count(); schema={c:t for c,t in df.dtypes}
    for g in guardrails:
        t=g["rule_type"]; status="PASS"; details=""
        if t=="row_count_between":
            mn,mx=g.get("min_value"),g.get("max_value"); status="FAIL" if (mn is not None and cnt<mn) or (mx is not None and cnt>mx) else "PASS"
        elif t=="schema_required_columns":
            miss=[c for c in g.get("required_columns",[]) if c not in df.columns]; status="FAIL" if miss else "PASS"; details=",".join(miss)
        elif t=="schema_data_type":
            c=g.get("column"); exp=g.get("expected_type"); status="FAIL" if schema.get(c)!=exp else "PASS"; details=f"actual={schema.get(c)}"
        rows.append({"rule_id":g.get("rule_id"),"rule_type":t,"status":status,"details":details})
    return df.sparkSession.createDataFrame(rows)
