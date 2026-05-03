"""Microsoft Fabric AI Functions helpers for optional AI-in-the-loop workflows."""
from __future__ import annotations

import json


def check_fabric_ai_functions_available() -> dict:
    try:
        import synapse.ml.spark.aifunc as _aifunc  # noqa: F401
        return {"available": True, "runtime": "fabric_pyspark", "message": "Microsoft Fabric AI Functions import check passed."}
    except Exception as exc:  # pragma: no cover
        return {"available": False, "runtime": "local_or_unknown", "message": f"Microsoft Fabric AI Functions are unavailable. Require Fabric PySpark runtime and feature enablement. Import error: {exc}"}


def configure_fabric_ai_functions(deployment_name: str | None = None, temperature: float = 0.0) -> dict:
    try:
        import synapse.ml.spark.aifunc as aifunc
    except Exception as exc:  # pragma: no cover
        return {"available": False, "configured": False, "message": f"Microsoft Fabric AI Functions are unavailable. Import error: {exc}"}
    conf = getattr(aifunc, "default_conf", None)
    if conf is None:
        return {"available": True, "configured": False, "message": "aifunc.default_conf is not available in this runtime."}
    if deployment_name and hasattr(conf, "set_deployment_name"):
        conf.set_deployment_name(deployment_name)
    if hasattr(conf, "set_temperature"):
        conf.set_temperature(float(temperature))
    return {"available": True, "configured": True, "message": "Microsoft Fabric AI Functions default configuration applied."}


def build_dq_rule_candidate_prompt(business_context="", dataset_name=None) -> str:
    dataset_context = dataset_name or "unknown"
    business_context_text = business_context or ""
    return (
        "Generate candidate data quality rules from row-level profile metadata. "
        "Return JSON only with: rule_id, table_name, column_name, rule_type, severity, reason, evidence, needs_human_review. "
        "Suggestions are for human review and are not deterministic enforcement. "
        f"Dataset name: {dataset_context}. Business context: {business_context_text}. "
        "Row profile fields: column_name={column_name}, data_type={data_type}, null_count={null_count}, distinct_count={distinct_count}, row_count={row_count}."
    )


def build_governance_candidate_prompt(business_context="", dataset_name=None) -> str:
    dataset_context = dataset_name or "unknown"
    business_context_text = business_context or ""
    return (
        "Generate governance label suggestions from profile metadata. "
        "Return JSON only with: table_name, column_name, candidate_label, reason, evidence, needs_human_review. "
        "Allowed candidate_label: public, internal, confidential_candidate, restricted_candidate, unknown. "
        "Suggestions are for human review and are not deterministic enforcement. "
        f"Dataset name: {dataset_context}. Business context: {business_context_text}. "
        "Row profile fields: table_name={table_name}, column_name={column_name}, data_type={data_type}, profile_summary={profile_summary}."
    )


def build_handover_summary_prompt(business_context="") -> str:
    business_context_text = business_context or ""
    return (
        "Generate handover summary suggestions. "
        "Return JSON only with: pipeline_summary, important_transformations, business_reason, handover_notes, risks_or_open_questions. "
        "Suggestions are for human review and are not deterministic enforcement. "
        f"Business context: {business_context_text}. "
        "Row summary field: summary={summary}."
    )


def _require_fabric_ai_dataframe(df, helper_name: str):
    ai = getattr(df, "ai", None)
    if ai is None or not hasattr(ai, "generate_response"):
        raise RuntimeError(f"{helper_name} requires Fabric DataFrame.ai.generate_response in AI Functions-enabled runtime.")


def generate_dq_rule_candidates_with_fabric_ai(profile_df, business_context="", dataset_name=None, output_col="ai_dq_rule_candidate", error_col="ai_dq_rule_error", response_format="json_object", concurrency=20):
    _require_fabric_ai_dataframe(profile_df, "generate_dq_rule_candidates_with_fabric_ai")
    prompt = build_dq_rule_candidate_prompt(business_context=business_context, dataset_name=dataset_name)
    return profile_df.ai.generate_response(prompt=prompt, is_prompt_template=True, output_col=output_col, error_col=error_col, response_format=response_format, concurrency=concurrency)


def generate_governance_candidates_with_fabric_ai(profile_df, business_context="", dataset_name=None, output_col="ai_governance_candidate", error_col="ai_governance_error", response_format="json_object", concurrency=20):
    _require_fabric_ai_dataframe(profile_df, "generate_governance_candidates_with_fabric_ai")
    prompt = build_governance_candidate_prompt(business_context=business_context, dataset_name=dataset_name)
    return profile_df.ai.generate_response(prompt=prompt, is_prompt_template=True, output_col=output_col, error_col=error_col, response_format=response_format, concurrency=concurrency)


def generate_handover_summary_with_fabric_ai(summary_df, business_context="", output_col="ai_handover_summary", error_col="ai_handover_error", response_format="json_object", concurrency=20):
    _require_fabric_ai_dataframe(summary_df, "generate_handover_summary_with_fabric_ai")
    prompt = build_handover_summary_prompt(business_context=business_context)
    return summary_df.ai.generate_response(prompt=prompt, is_prompt_template=True, output_col=output_col, error_col=error_col, response_format=response_format, concurrency=concurrency)


def _compact_sample_rows(sample_rows=None) -> str:
    if sample_rows is None:
        return ""
    try:
        return json.dumps(sample_rows, ensure_ascii=False)[:3000]
    except Exception:
        return str(sample_rows)[:3000]


def build_manual_dq_rule_prompt_package(sample_rows=None, business_context="", dataset_name=None) -> dict:
    return {
        "mode": "manual_prompt_ferry",
        "target_use": "dq_rule_candidates",
        "prompt": build_dq_rule_candidate_prompt(business_context=business_context, dataset_name=dataset_name),
        "expected_output_schema": ["rule_id", "table_name", "column_name", "rule_type", "severity", "reason", "evidence", "needs_human_review"],
        "notes": "Paste prompt into Copilot or another LLM, then review before storing approved deterministic rules.",
        "sample_rows": _compact_sample_rows(sample_rows),
    }


def build_manual_governance_prompt_package(sample_rows=None, business_context="", dataset_name=None) -> dict:
    return {
        "mode": "manual_prompt_ferry",
        "target_use": "governance_candidates",
        "prompt": build_governance_candidate_prompt(business_context=business_context, dataset_name=dataset_name),
        "expected_output_schema": ["table_name", "column_name", "candidate_label", "reason", "evidence", "needs_human_review"],
        "notes": "Paste prompt into Copilot or another LLM, then review before storing approved governance labels.",
        "sample_rows": _compact_sample_rows(sample_rows),
    }


def build_manual_handover_prompt_package(sample_rows=None, business_context="") -> dict:
    return {
        "mode": "manual_prompt_ferry",
        "target_use": "handover_summary",
        "prompt": build_handover_summary_prompt(business_context=business_context),
        "expected_output_schema": ["pipeline_summary", "important_transformations", "business_reason", "handover_notes", "risks_or_open_questions"],
        "notes": "Paste prompt into Copilot or another LLM, then review before storing handover summaries.",
        "sample_rows": _compact_sample_rows(sample_rows),
    }


def parse_manual_ai_json_response(text):
    try:
        return json.loads(text)
    except Exception as exc:
        raise ValueError("Failed to parse manual AI response as JSON.") from exc
