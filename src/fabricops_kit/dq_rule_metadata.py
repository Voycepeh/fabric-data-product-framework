from __future__ import annotations
import json
from datetime import datetime, timezone
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def build_dq_rules_metadata_df(spark, table_name:str, approved_rules:list[dict], action_by:str="notebook_user", rule_source:str="ai_widget_approval", action_reason:str="Approved after human review."):
    """Build append-only active DQ metadata versions for approved rules."""
    ts=datetime.now(timezone.utc).isoformat(); rows=[]
    for rule in approved_rules:
        cols=rule.get("columns",[]); rows.append({"table_name":table_name,"rule_id":str(rule["rule_id"]),"rule_type":str(rule["rule_type"]),"columns":",".join(cols),"rule_key":f"{table_name}|{rule['rule_id']}|{rule['rule_type']}|{','.join(cols)}","is_active":True,"action_type":"approved","action_by":action_by,"action_ts":ts,"action_reason":action_reason,"rule_source":rule_source,"rule_json":json.dumps(rule)})
    return spark.createDataFrame(rows)

def build_dq_rule_deactivation_metadata_df(spark, table_name:str, deactivations:list[dict], action_by:str="notebook_user", rule_source:str="rule_deactivation_widget"):
    """Build append-only inactive DQ metadata rows; each deactivation requires a reason."""
    ts=datetime.now(timezone.utc).isoformat(); rows=[]
    for i in deactivations:
        reason=str(i["action_reason"]).strip(); rule=i["rule"]
        if not reason: raise ValueError("Deactivation reason is required.")
        cols=rule.get("columns",[]); rows.append({"table_name":table_name,"rule_id":str(rule["rule_id"]),"rule_type":str(rule["rule_type"]),"columns":",".join(cols),"rule_key":f"{table_name}|{rule['rule_id']}|{rule['rule_type']}|{','.join(cols)}","is_active":False,"action_type":"deactivated","action_by":action_by,"action_ts":ts,"action_reason":reason,"rule_source":rule_source,"rule_json":json.dumps(rule)})
    return spark.createDataFrame(rows)

def get_latest_dq_rule_versions_from_metadata(metadata_df, table_name:str):
    w=Window.partitionBy("rule_key").orderBy(F.col("action_ts").desc())
    return metadata_df.filter(F.col("table_name")==table_name).withColumn("_rn",F.row_number().over(w)).filter(F.col("_rn")==1).drop("_rn")

def load_latest_active_dq_rules_from_metadata(metadata_df, table_name:str)->list[dict]:
    """Load latest active approved rules after suppressing rule_keys with newer deactivation versions."""
    rows=get_latest_dq_rule_versions_from_metadata(metadata_df,table_name).filter(F.col("is_active")==True).select("rule_json").collect()
    return [json.loads(r["rule_json"]) for r in rows]

def load_latest_active_dq_rule_metadata(metadata_df, table_name:str):
    """Return latest active metadata rows for governance UIs."""
    return get_latest_dq_rule_versions_from_metadata(metadata_df,table_name).filter(F.col("is_active")==True)
