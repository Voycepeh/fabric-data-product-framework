from __future__ import annotations
import pandas as pd
from typing import Any

def build_dq_rules_metadata_df(table_name:str, rules:list[dict[str,Any]], version:int=1)->pd.DataFrame:
    """Build append-only active metadata rows for approved DQ rules."""
    return pd.DataFrame([{'table_name':table_name,'rule_id':r['rule_id'],'rule_json':r,'version':version,'is_active':True,'deactivation_reason':None} for r in rules])

def build_dq_rule_deactivation_metadata_df(existing_metadata:pd.DataFrame, rule_id:str, reason:str)->pd.DataFrame:
    """Append an inactive metadata version for a rule deactivation action."""
    latest=int(existing_metadata[existing_metadata.rule_id==rule_id]['version'].max()) if not existing_metadata.empty else 0
    return pd.DataFrame([{'table_name':existing_metadata.iloc[0]['table_name'],'rule_id':rule_id,'rule_json':None,'version':latest+1,'is_active':False,'deactivation_reason':reason}])

def get_latest_dq_rule_versions_from_metadata(metadata_df:pd.DataFrame)->pd.DataFrame:
    """Return latest row per rule_id."""
    return metadata_df.sort_values('version').groupby('rule_id',as_index=False).tail(1)

def load_latest_active_dq_rules_from_metadata(metadata_df:pd.DataFrame)->list[dict[str,Any]]:
    """Load latest active approved rules only."""
    latest=get_latest_dq_rule_versions_from_metadata(metadata_df)
    return [r for r in latest['rule_json'].tolist() if isinstance(r,dict) and bool(latest[latest['rule_json']==r]['is_active'].iloc[0])]

def load_latest_active_dq_rule_metadata(metadata_df:pd.DataFrame)->pd.DataFrame:
    """Return latest active metadata rows."""
    latest=get_latest_dq_rule_versions_from_metadata(metadata_df)
    return latest[latest['is_active']==True].reset_index(drop=True)
