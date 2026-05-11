"""AI-assistance helpers for governance and handover generation."""
from __future__ import annotations
import json
from .config import FrameworkConfig

DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE="Generate governance suggestions as JSON. Context={business_context}."
DEFAULT_HANDOVER_SUMMARY_TEMPLATE="Generate handover summary as JSON. Context={business_context}."

def _resolve_prompt_template(config: FrameworkConfig | None, template_name: str, fallback_template: str) -> str:
    if config is None: return fallback_template
    ai_prompt_config=getattr(config,'ai_prompt_config',None)
    configured=getattr(ai_prompt_config,template_name,'') if ai_prompt_config else ''
    return configured or fallback_template

def build_governance_candidate_prompt(business_context="", dataset_name=None, config: FrameworkConfig | None = None) -> str:
    return _resolve_prompt_template(config,'governance_candidate_template',DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE).replace('{business_context}',business_context or '').replace('{dataset_name}',dataset_name or 'unknown')

def build_handover_summary_prompt(business_context="", config: FrameworkConfig | None = None) -> str:
    return _resolve_prompt_template(config,'handover_summary_template',DEFAULT_HANDOVER_SUMMARY_TEMPLATE).replace('{business_context}',business_context or '')

def parse_manual_ai_json_response(response_text:str)->dict:
    return json.loads(response_text)
