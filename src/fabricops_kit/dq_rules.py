"""Canonical Data Quality rule workflow helpers."""
from __future__ import annotations
import ast, json, re
from typing import Any

AI_SUGGESTABLE_DQ_RULE_TYPES=("not_null","unique_key","accepted_values","value_range","regex_format")
DQ_RULE_SUGGESTION_PROMPT_TEMPLATE=("Suggest one DQ rule for this profiled column. Return JSON dict only with keys: rule_id, rule_type, columns, description and optional allowed_values,min_value,max_value,regex_pattern. Allowed rule_type: {rule_types}. Table={table_name}. Business context={business_context}. Profile row={profile_row}.")

def profile_dataframe_for_dq(df: Any)->list[dict[str,Any]]:
    """Profile a DataFrame into per-column rows used for DQ suggestion prompts.

    Parameters
    ----------
    df : Any
        Pandas DataFrame or Spark DataFrame.

    Returns
    -------
    list[dict[str, Any]]
        Row-wise profile entries.
    """
    if hasattr(df,'toPandas'): pdf=df.toPandas()
    else: pdf=df
    rows=[]
    for c in pdf.columns:
      s=pdf[c]
      rows.append({'column_name':c,'data_type':str(s.dtype),'null_count':int(s.isna().sum()),'distinct_count':int(s.nunique(dropna=True)),'row_count':int(len(pdf))})
    return rows

def suggest_dq_rules_with_fabric_ai(profile_rows:list[dict[str,Any]], table_name:str, business_context:str="", fabric_ai_generate=None)->list[str]:
    """Generate one AI response per profile row."""
    if fabric_ai_generate is None: raise ValueError('fabric_ai_generate callable is required.')
    out=[]
    for row in profile_rows:
      prompt=DQ_RULE_SUGGESTION_PROMPT_TEMPLATE.format(rule_types=', '.join(AI_SUGGESTABLE_DQ_RULE_TYPES),table_name=table_name,business_context=business_context or 'none',profile_row=json.dumps(row,default=str))
      out.append(fabric_ai_generate(prompt,row))
    return out

def parse_dq_rules_dict_from_text(text:str)->dict[str,Any]:
    """Parse a dictionary payload from AI text."""
    try: return json.loads(text)
    except Exception:
      m=re.search(r"\{.*\}",text,re.S)
      if not m: raise ValueError('No dictionary found in response text.')
      return ast.literal_eval(m.group(0))

def extract_candidate_rules_from_responses(responses:list[str])->list[dict[str,Any]]:
    """Extract and flatten candidate rules from AI response texts."""
    rules=[]
    for t in responses:
      parsed=parse_dq_rules_dict_from_text(t)
      if isinstance(parsed,dict) and 'DQ_RULES' in parsed:
        for v in parsed['DQ_RULES'].values(): rules.extend(v)
      elif isinstance(parsed,dict): rules.append(parsed)
    return rules

def validate_dq_rules(rules:list[dict[str,Any]])->list[dict[str,Any]]:
    """Validate canonical DQ rules."""
    for r in rules:
      if r.get('rule_type') not in AI_SUGGESTABLE_DQ_RULE_TYPES: raise ValueError('Unsupported rule_type')
      if not r.get('columns'): raise ValueError('columns required')
    return rules

def run_dq_rules(df:Any,rules:list[dict[str,Any]])->list[dict[str,Any]]:
    """Run deterministic DQ rules and return failure evidence rows."""
    if hasattr(df,'toPandas'): pdf=df.toPandas()
    else: pdf=df.copy()
    validate_dq_rules(rules)
    fails=[]
    for _,row in pdf.iterrows():
      for rule in rules:
        c=rule['columns'][0]; typ=rule['rule_type']; ok=True
        v=row.get(c)
        if typ=='not_null': ok= v is not None and not (hasattr(v,'item') and v!=v)
        elif typ=='unique_key': pass
        elif typ=='accepted_values': ok=(v is None) or (v in set(rule.get('allowed_values',[])))
        elif typ=='value_range':
          ok=(v is None) or ((rule.get('min_value') is None or v>=rule.get('min_value')) and (rule.get('max_value') is None or v<=rule.get('max_value')))
        elif typ=='regex_format': ok=(v is None) or re.match(rule.get('regex_pattern',''),str(v)) is not None
        if not ok: fails.append({'rule_id':rule.get('rule_id'),'rule_type':typ,'column_name':c,'failed_value':v})
    if any(r['rule_type']=='unique_key' for r in rules):
      for rule in [r for r in rules if r['rule_type']=='unique_key']:
        dup=pdf.duplicated(subset=rule['columns'],keep=False)
        for _,rw in pdf[dup].iterrows(): fails.append({'rule_id':rule.get('rule_id'),'rule_type':'unique_key','column_name':','.join(rule['columns']),'failed_value':{c:rw[c] for c in rule['columns']}})
    return fails

def assert_dq_passed(failure_evidence:list[dict[str,Any]])->None:
    """Raise when DQ failures exist after evidence creation."""
    if failure_evidence: raise ValueError(f'DQ failed with {len(failure_evidence)} evidence rows.')
