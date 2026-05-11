from __future__ import annotations
import ast, re
from datetime import datetime, timezone
from typing import Any
from pyspark.sql import functions as F

AI_SUGGESTABLE_DQ_RULE_TYPES={"not_null","unique_key","accepted_values","value_range","regex_format"}
DQ_RULE_SUGGESTION_PROMPT_TEMPLATE="""You are helping draft candidate FabricOps data quality rules for a pipeline contract notebook.\nThese suggestions are advisory only. A human reviewer must approve every rule before enforcement.\nUse only rule_type values: not_null, unique_key, accepted_values, value_range, regex_format.\nReturn only Python dictionary output named DQ_RULES in shape DQ_RULES={\"{table_name}\":[...]}.\nColumn profile row: Column name: {column_name} Data type: {data_type} Row count: {row_count} Null count: {null_count} Null percent: {null_percent} Distinct count: {distinct_count} Distinct percent: {distinct_percent} Minimum value: {min_value} Maximum value: {max_value} Observed values sample: {observed_values_sample} Business context: {business_context}"""

def profile_dataframe_for_dq(df, table_name:str, business_context:str="", sample_value_limit:int=20):
    """Create one Spark profile row per source column for Fabric AI prompting.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Source DataFrame to profile.
    table_name : str
        Logical table name.
    business_context : str, default=""
        Extra context propagated into each profile row.
    sample_value_limit : int, default=20
        Maximum distinct non-null samples per column.
    """
    rows=[]; row_count=df.count()
    for c,t in df.dtypes:
        null_count=df.filter(F.col(c).isNull()).count(); distinct_count=df.select(c).distinct().count(); min_value=max_value=None
        if t in {"int","bigint","double","float","date","timestamp"} or t.startswith("decimal"):
            mm=df.select(F.min(F.col(c)).cast("string").alias("min_value"),F.max(F.col(c)).cast("string").alias("max_value")).collect()[0]; min_value=mm["min_value"]; max_value=mm["max_value"]
        observed=[str(r[c]) for r in df.select(c).where(F.col(c).isNotNull()).distinct().limit(sample_value_limit).collect()]
        rows.append({"table_name":table_name,"column_name":c,"data_type":t,"row_count":int(row_count),"null_count":int(null_count),"null_percent":round((null_count/row_count)*100,4) if row_count else 0.0,"distinct_count":int(distinct_count),"distinct_percent":round((distinct_count/row_count)*100,4) if row_count else 0.0,"min_value":min_value,"max_value":max_value,"observed_values_sample":", ".join(observed),"business_context":business_context,"profile_timestamp":datetime.now(timezone.utc).isoformat()})
    return df.sparkSession.createDataFrame(rows)

def suggest_dq_rules_with_fabric_ai(profile_df,prompt_template:str=DQ_RULE_SUGGESTION_PROMPT_TEMPLATE,output_col:str="response"):
    """Generate advisory DQ suggestions with Fabric AI Functions on a Spark DataFrame."""
    return profile_df.ai.generate_response(prompt=prompt_template, output_col=output_col)

def parse_dq_rules_dict_from_text(text:str)->dict[str,list[dict[str,Any]]]:
    cleaned=str(text or "").strip(); m=re.search(r"DQ_RULES\s*=\s*(\{.*\})", cleaned, flags=re.DOTALL); payload=m.group(1) if m else cleaned
    try: parsed=ast.literal_eval(payload)
    except Exception: return {}
    return parsed if isinstance(parsed,dict) else {}

def extract_candidate_rules_from_responses(response_df, table_name:str, response_col:str="response"):
    """Extract row-by-row Fabric AI responses and deduplicate candidates by rule_id."""
    rules=[]
    for r in response_df.select(response_col).collect(): rules.extend(parse_dq_rules_dict_from_text(r[response_col]).get(table_name,[]))
    out={}; [out.setdefault(x.get("rule_id"),x) for x in rules if x.get("rule_id")]
    return list(out.values())

def validate_dq_rules(rules:list[dict[str,Any]])->list[dict[str,Any]]:
    """Validate canonical DQ rules and enforce supported types and required fields."""
    if not isinstance(rules,list): raise ValueError("DQ rules must be a list of dictionaries.")
    for i,r in enumerate(rules):
        if not isinstance(r,dict): raise ValueError(f"DQ rule at index {i} must be a dictionary.")
        for f in ["rule_id","rule_type","columns","severity","description"]:
            if f not in r: raise ValueError(f"DQ rule '{r.get('rule_id',i)}' is missing field '{f}'.")
        if r["rule_type"] not in AI_SUGGESTABLE_DQ_RULE_TYPES: raise ValueError("unsupported rule_type")
    return rules

def run_dq_rules(df, table_name:str, rules:list[dict[str,Any]]):
    """Run canonical DQ rules and return Spark DataFrame rule-level evidence."""
    from .quarantine import split_valid_quarantine_and_failures
    validate_dq_rules(rules)
    _,_,f=split_valid_quarantine_and_failures(df,rules)
    total=df.count()
    agg=(f.groupBy("rule_id","rule_type","severity").agg(F.count(F.lit(1)).alias("failed_count")).withColumn("table_name",F.lit(table_name)).withColumn("total_count",F.lit(total)).withColumn("status",F.when(F.col("failed_count")==0,F.lit("PASS")).otherwise(F.lit("FAIL"))))
    return agg.select("table_name","rule_id","rule_type","severity","status","failed_count","total_count")

def assert_dq_passed(dq_result_df)->None:
    """Raise only after evidence exists when any error-severity DQ rule failed."""
    if dq_result_df.filter("lower(severity)='error' and status='FAIL'").count()>0: raise ValueError("Data quality failed for error-severity rules.")
