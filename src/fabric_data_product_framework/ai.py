"""Microsoft Fabric AI Functions helpers for optional AI-in-the-loop workflows."""
from __future__ import annotations

import json


def check_fabric_ai_functions_available() -> dict:
    """Check whether Fabric AI Functions can be imported in the current runtime.

    Returns
    -------
    dict
        Status payload with ``available``, ``runtime``, and ``message`` keys.

    Notes
    -----
    This is a best-effort import check only. It does not validate tenant switches,
    Fabric capacity, or deployment readiness.

    Examples
    --------
    >>> check_fabric_ai_functions_available()["available"] in {True, False}
    True
    """
    try:
        import synapse.ml.spark.aifunc as _aifunc  # noqa: F401
        return {"available": True, "runtime": "fabric_pyspark", "message": "Microsoft Fabric AI Functions import check passed."}
    except Exception as exc:  # pragma: no cover
        return {"available": False, "runtime": "local_or_unknown", "message": f"Microsoft Fabric AI Functions are unavailable. Require Fabric PySpark runtime and feature enablement. Import error: {exc}"}


def configure_fabric_ai_functions(deployment_name: str | None = None, temperature: float = 0.0) -> dict:
    """Apply optional default Fabric AI Function configuration.

    Parameters
    ----------
    deployment_name : str | None, optional
        Optional deployment name applied through ``aifunc.default_conf`` when
        supported by the runtime.
    temperature : float, default=0.0
        Optional generation temperature applied when supported.

    Returns
    -------
    dict
        Configuration result with availability and message fields.

    Notes
    -----
    This helper configures runtime defaults only; it does not execute model calls.
    """
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
    """Build standardized prompt text for AI-assisted DQ candidate generation.

    Parameters
    ----------
    business_context : str, optional
        Static business context embedded directly into the prompt text.
    dataset_name : str | None, optional
        Static dataset name embedded directly into the prompt text.

    Returns
    -------
    str
        Prompt template string for use with Fabric ``DataFrame.ai.generate_response``.

    Notes
    -----
    Hardcoded sections define expected JSON output schema and review posture.
    Row placeholders injected from DataFrame rows are ``{column_name}``,
    ``{data_type}``, ``{null_count}``, ``{distinct_count}``, and ``{row_count}``.
    Output is suggestion-oriented and not deterministic enforcement.
    """
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
    """Build standardized prompt text for AI-assisted governance suggestions.

    Parameters
    ----------
    business_context : str, optional
        Static business context embedded directly into the prompt text.
    dataset_name : str | None, optional
        Static dataset name embedded directly into the prompt text.

    Returns
    -------
    str
        Prompt template string for use with Fabric ``DataFrame.ai.generate_response``.

    Notes
    -----
    Hardcoded sections define allowed candidate labels and output keys.
    Row placeholders injected from DataFrame rows are ``{table_name}``,
    ``{column_name}``, ``{data_type}``, and ``{profile_summary}``.
    Output is suggestion-oriented and requires human review.
    """
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
    """Build standardized prompt text for AI-assisted handover summary suggestions.

    Parameters
    ----------
    business_context : str, optional
        Static business context embedded directly into the prompt text.

    Returns
    -------
    str
        Prompt template string for use with Fabric ``DataFrame.ai.generate_response``.

    Notes
    -----
    Hardcoded sections define expected JSON keys for handover summaries.
    Row placeholder injected from DataFrame rows is ``{summary}``.
    Output is suggestion-oriented and requires human review.
    """
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
    return ai


def generate_dq_rule_candidates_with_fabric_ai(profile_df, business_context="", dataset_name=None, output_col="ai_dq_rule_candidate", error_col="ai_dq_rule_error", response_format="json_object", concurrency=20):
    """Execute Fabric AI Functions to append DQ candidate suggestions to a DataFrame.

    Parameters
    ----------
    profile_df : Any
        Fabric PySpark DataFrame with an ``.ai.generate_response`` extension.
        Expected row columns include ``column_name``, ``data_type``, ``null_count``,
        ``distinct_count``, and ``row_count`` for prompt placeholders.
    business_context : str, optional
        Static context embedded in prompt text.
    dataset_name : str | None, optional
        Static dataset name embedded in prompt text.
    output_col : str, default="ai_dq_rule_candidate"
        Output column for generated JSON text.
    error_col : str, default="ai_dq_rule_error"
        Error column written by AI Functions.
    response_format : str, default="json_object"
        Fabric AI response format.
    concurrency : int, default=20
        Fabric AI row-level concurrency setting.

    Returns
    -------
    Any
        Enriched DataFrame containing AI suggestion output columns.

    Notes
    -----
    This helper executes AI generation only and does not enforce deterministic
    quality rules.
    """
    _require_fabric_ai_dataframe(profile_df, "generate_dq_rule_candidates_with_fabric_ai")
    prompt = build_dq_rule_candidate_prompt(business_context=business_context, dataset_name=dataset_name)
    return profile_df.ai.generate_response(prompt=prompt, is_prompt_template=True, output_col=output_col, error_col=error_col, response_format=response_format, concurrency=concurrency)


def generate_governance_candidates_with_fabric_ai(profile_df, business_context="", dataset_name=None, output_col="ai_governance_candidate", error_col="ai_governance_error", response_format="json_object", concurrency=20):
    """Execute Fabric AI Functions to append governance suggestions to a DataFrame.

    Parameters
    ----------
    profile_df : Any
        Fabric PySpark DataFrame with an ``.ai.generate_response`` extension.
        Expected row columns include ``table_name``, ``column_name``, ``data_type``,
        and ``profile_summary`` for prompt placeholders.
    business_context : str, optional
        Static context embedded in prompt text.
    dataset_name : str | None, optional
        Static dataset name embedded in prompt text.
    output_col, error_col, response_format, concurrency
        Fabric AI execution options.

    Returns
    -------
    Any
        Enriched DataFrame containing AI suggestion output columns.
    """
    _require_fabric_ai_dataframe(profile_df, "generate_governance_candidates_with_fabric_ai")
    prompt = build_governance_candidate_prompt(business_context=business_context, dataset_name=dataset_name)
    return profile_df.ai.generate_response(prompt=prompt, is_prompt_template=True, output_col=output_col, error_col=error_col, response_format=response_format, concurrency=concurrency)


def generate_handover_summary_with_fabric_ai(summary_df, business_context="", output_col="ai_handover_summary", error_col="ai_handover_error", response_format="json_object", concurrency=20):
    """Execute Fabric AI Functions to append handover summary suggestions.

    Parameters
    ----------
    summary_df : Any
        Fabric PySpark DataFrame with an ``.ai.generate_response`` extension.
        Expected row column includes ``summary`` for prompt placeholders.
    business_context : str, optional
        Static context embedded in prompt text.
    output_col, error_col, response_format, concurrency
        Fabric AI execution options.

    Returns
    -------
    Any
        Enriched DataFrame containing AI suggestion output columns.
    """
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
    """Build copy/paste prompt package for manual DQ candidate generation.

    Parameters
    ----------
    sample_rows : Any, optional
        Optional small sample context serialized compactly for prompt ferry usage.
    business_context : str, optional
        Static context embedded in prompt text.
    dataset_name : str | None, optional
        Static dataset name embedded in prompt text.

    Returns
    -------
    dict
        Manual package containing reusable prompt text, schema expectations, and
        notes. Output is advisory and requires human review.
    """
    prompt = build_dq_rule_candidate_prompt(business_context=business_context, dataset_name=dataset_name)
    compact = _compact_sample_rows(sample_rows)
    return {
        "mode": "manual_prompt_ferry",
        "target_use": "dq_rule_candidates",
        "prompt": prompt,
        "full_prompt_text": f"{prompt}\n\nSample rows:\n{compact}" if compact else prompt,
        "expected_output_schema": ["rule_id", "table_name", "column_name", "rule_type", "severity", "reason", "evidence", "needs_human_review"],
        "notes": "Paste prompt into Copilot or another LLM, then review before storing approved deterministic rules.",
        "sample_rows": compact,
    }


def build_manual_governance_prompt_package(sample_rows=None, business_context="", dataset_name=None) -> dict:
    """Build copy/paste prompt package for manual governance suggestion generation.

    Parameters
    ----------
    sample_rows : Any, optional
        Optional small sample context serialized compactly for prompt ferry usage.
    business_context : str, optional
        Static context embedded in prompt text.
    dataset_name : str | None, optional
        Static dataset name embedded in prompt text.

    Returns
    -------
    dict
        Manual package containing reusable prompt text, schema expectations, and
        notes. Output is advisory and requires human review.
    """
    prompt = build_governance_candidate_prompt(business_context=business_context, dataset_name=dataset_name)
    compact = _compact_sample_rows(sample_rows)
    return {
        "mode": "manual_prompt_ferry",
        "target_use": "governance_candidates",
        "prompt": prompt,
        "full_prompt_text": f"{prompt}\n\nSample rows:\n{compact}" if compact else prompt,
        "expected_output_schema": ["table_name", "column_name", "candidate_label", "reason", "evidence", "needs_human_review"],
        "notes": "Paste prompt into Copilot or another LLM, then review before storing approved governance labels.",
        "sample_rows": compact,
    }


def build_manual_handover_prompt_package(sample_rows=None, business_context="") -> dict:
    """Build copy/paste prompt package for manual handover summary generation.

    Parameters
    ----------
    sample_rows : Any, optional
        Optional small sample context serialized compactly for prompt ferry usage.
    business_context : str, optional
        Static context embedded in prompt text.

    Returns
    -------
    dict
        Manual package containing reusable prompt text, schema expectations, and
        notes. Output is advisory and requires human review.
    """
    prompt = build_handover_summary_prompt(business_context=business_context)
    compact = _compact_sample_rows(sample_rows)
    return {
        "mode": "manual_prompt_ferry",
        "target_use": "handover_summary",
        "prompt": prompt,
        "full_prompt_text": f"{prompt}\n\nSample rows:\n{compact}" if compact else prompt,
        "expected_output_schema": ["pipeline_summary", "important_transformations", "business_reason", "handover_notes", "risks_or_open_questions"],
        "notes": "Paste prompt into Copilot or another LLM, then review before storing handover summaries.",
        "sample_rows": compact,
    }


def parse_manual_ai_json_response(text):
    """Parse manual AI JSON output into Python objects.

    Parameters
    ----------
    text : str
        Raw text expected to contain JSON.

    Returns
    -------
    Any
        Parsed JSON payload.

    Raises
    ------
    ValueError
        Raised when parsing fails.
    """
    try:
        return json.loads(text)
    except Exception as exc:
        raise ValueError("Failed to parse manual AI response as JSON.") from exc
