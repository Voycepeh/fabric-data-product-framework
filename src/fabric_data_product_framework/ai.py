"""Microsoft Fabric AI Functions helpers for optional AI-in-the-loop workflows."""
from __future__ import annotations


def check_fabric_ai_functions_available() -> dict:
    """Best-effort check for Fabric AI Functions availability."""
    try:
        import synapse.ml.spark.aifunc as _aifunc  # noqa: F401
        return {"available": True, "runtime": "fabric_pyspark", "message": "Microsoft Fabric AI Functions import check passed."}
    except Exception as exc:  # pragma: no cover
        return {
            "available": False,
            "runtime": "local_or_unknown",
            "message": (
                "Microsoft Fabric AI Functions are unavailable in this environment. "
                "They require Fabric PySpark runtime and Microsoft Fabric AI feature availability. "
                f"Import error: {exc}"
            ),
        }


def configure_fabric_ai_functions(deployment_name: str | None = None, temperature: float = 0.0) -> dict:
    """Configure Fabric AI Functions default settings when available."""
    try:
        import synapse.ml.spark.aifunc as aifunc
    except Exception as exc:  # pragma: no cover
        return {
            "available": False,
            "configured": False,
            "message": (
                "Microsoft Fabric AI Functions are unavailable in this environment. "
                "They require Fabric PySpark runtime and Microsoft Fabric AI feature availability. "
                f"Import error: {exc}"
            ),
        }
    conf = getattr(aifunc, "default_conf", None)
    if conf is None:
        return {"available": True, "configured": False, "message": "aifunc.default_conf is not available in this runtime."}
    if deployment_name and hasattr(conf, "set_deployment_name"):
        conf.set_deployment_name(deployment_name)
    if hasattr(conf, "set_temperature"):
        conf.set_temperature(float(temperature))
    return {"available": True, "configured": True, "message": "Microsoft Fabric AI Functions default configuration applied."}


def _require_fabric_ai_dataframe(df, helper_name: str):
    ai = getattr(df, "ai", None)
    if ai is None or not hasattr(ai, "generate_response"):
        raise RuntimeError(
            f"{helper_name} requires a Fabric PySpark DataFrame with AI Functions enabled and DataFrame.ai.generate_response available."
        )
    return ai


def generate_dq_rule_candidates_with_fabric_ai(profile_df, business_context="", dataset_name=None, output_col="ai_dq_rule_candidate", error_col="ai_dq_rule_error", response_format="json_object", concurrency=20):
    """Generate DQ candidate suggestions as an enriched DataFrame."""
    _require_fabric_ai_dataframe(profile_df, "generate_dq_rule_candidates_with_fabric_ai")
    dataset_context = dataset_name or "unknown"
    business_context_text = business_context or ""
    prompt = (
        "You are generating candidate data quality rules from profile metadata rows. "
        "Return JSON only with keys: rule_id, table_name, column_name, rule_type, severity, reason, evidence, needs_human_review. "
        "These are suggestions only and must not be treated as enforced checks. "
        f"Dataset name: {dataset_context}. Business context: {business_context_text}. "
        "Use this row profile: column_name={column_name}, data_type={data_type}, null_count={null_count}, distinct_count={distinct_count}, row_count={row_count}."
    )
    return profile_df.ai.generate_response(
        prompt=prompt,
        is_prompt_template=True,
        output_col=output_col,
        error_col=error_col,
        response_format=response_format,
        concurrency=concurrency,
    )


def generate_governance_candidates_with_fabric_ai(profile_df, business_context="", output_col="ai_governance_candidate", error_col="ai_governance_error", response_format="json_object", concurrency=20):
    """Generate governance label candidate suggestions as an enriched DataFrame."""
    _require_fabric_ai_dataframe(profile_df, "generate_governance_candidates_with_fabric_ai")
    business_context_text = business_context or ""
    prompt = (
        "Return JSON only with keys: table_name, column_name, candidate_label, reason, evidence, needs_human_review. "
        "Allowed candidate_label values: public, internal, confidential_candidate, restricted_candidate, unknown. "
        f"Business context: {business_context_text}. "
        "Evaluate row details table_name={table_name}, column_name={column_name}, data_type={data_type}, profile_summary={profile_summary}."
    )
    return profile_df.ai.generate_response(
        prompt=prompt,
        is_prompt_template=True,
        output_col=output_col,
        error_col=error_col,
        response_format=response_format,
        concurrency=concurrency,
    )


def generate_handover_summary_with_fabric_ai(summary_df, business_context="", output_col="ai_handover_summary", error_col="ai_handover_error", response_format="json_object", concurrency=20):
    """Generate handover summary suggestions as an enriched DataFrame.

    Notes
    -----
    ``summary_df`` should include a ``summary`` column for row-level context when
    using prompt templates.
    """
    _require_fabric_ai_dataframe(summary_df, "generate_handover_summary_with_fabric_ai")
    business_context_text = business_context or ""
    prompt = (
        "Return JSON only with keys: pipeline_summary, important_transformations, business_reason, handover_notes, risks_or_open_questions. "
        f"These are suggestions for human review. Business context: {business_context_text}. "
        "Use row context summary={summary}."
    )
    return summary_df.ai.generate_response(
        prompt=prompt,
        is_prompt_template=True,
        output_col=output_col,
        error_col=error_col,
        response_format=response_format,
        concurrency=concurrency,
    )
