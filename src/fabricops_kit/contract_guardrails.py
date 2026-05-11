from __future__ import annotations
CONTRACT_GUARDRAIL_RULE_TYPES=("row_count_between","schema_required_columns","schema_data_type")

def validate_contract_guardrails(guardrails:list[dict])->list[dict]:
    """Validate supported contract guardrails."""
    for g in guardrails:
      if g.get('rule_type') not in CONTRACT_GUARDRAIL_RULE_TYPES: raise ValueError('Unsupported contract guardrail.')
    return guardrails

def run_contract_guardrails(df, guardrails:list[dict])->list[dict]:
    """Run contract guardrails separately from DQ rules."""
    import pandas as pd
    pdf=df.toPandas() if hasattr(df,'toPandas') else df
    validate_contract_guardrails(guardrails)
    out=[]
    for g in guardrails:
      t=g['rule_type']
      if t=='row_count_between':
        rc=len(pdf); ok=g['min_count']<=rc<=g['max_count']
        if not ok: out.append({'rule_type':t,'message':'row_count out of range'})
      elif t=='schema_required_columns':
        miss=[c for c in g.get('required_columns',[]) if c not in pdf.columns]
        if miss: out.append({'rule_type':t,'message':f'missing columns: {miss}'})
      elif t=='schema_data_type':
        for c,expected in g.get('expected_types',{}).items():
          if c in pdf.columns and expected not in str(pdf[c].dtype): out.append({'rule_type':t,'message':f'type mismatch: {c}'})
    return out
