"""Notebook-friendly data quality wrappers built on top of quality.py."""

from __future__ import annotations


from datetime import datetime, timezone
import difflib
import json
from typing import Any

from .quality import run_quality_rules

SUPPORTED_RULE_TYPES = {
    "not_null",
    "unique_key",
    "accepted_values",
    "value_range",
    "regex_format",
    "accepted_values_ref",
    "string_length_between",
}

DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE = """You are helping draft candidate data quality rules for table '{table_name}'.
IMPORTANT: AI output is advisory only. A human must review and approve every suggestion before copying into DQ_RULES in 00_config.py.

Business context:
{business_context}

Profile metadata:
{profile_json}

Supported rule types (use only these):
- not_null
- unique_key
- accepted_values
- value_range
- regex_format
- accepted_values_ref
- string_length_between

Hard constraints:
- Return only Python dictionary output named DQ_RULES.
- Do not include Great Expectations, Deequ, DQX, SQL, pseudocode, markdown, or explanatory text.
- Do not invent unsupported rule types.

Output format: {output_format}
Required shape: DQ_RULES = {"TABLE_NAME": [<rule dictionaries>]}."""

def _to_quality_rule(rule: dict[str, Any]) -> dict[str, Any]:
    """Map notebook-friendly DQ rule shape to quality.py rule shape."""
    mapped = {
        "rule_id": rule["rule_id"],
        "severity": "critical" if str(rule.get("severity", "warning")).lower() == "error" else "warning",
        "reason": rule.get("description"),
    }
    rtype = rule["rule_type"]
    cols = rule["columns"]
    if rtype == "not_null":
        if len(cols) == 1:
            mapped.update({"rule_type": "not_null", "column": cols[0]})
        else:
            mapped.update({"rule_type": "not_null", "column": cols[0]})
    elif rtype == "unique_key":
        mapped.update({"rule_type": "unique_combination", "columns": cols})
    elif rtype == "accepted_values":
        mapped.update({"rule_type": "accepted_values", "column": cols[0], "accepted_values": rule["allowed_values"]})
    elif rtype == "value_range":
        mapped.update({"rule_type": "range_check", "column": cols[0], "min_value": rule.get("min_value"), "max_value": rule.get("max_value")})
    elif rtype == "regex_format":
        mapped.update({"rule_type": "regex_check", "column": cols[0], "pattern": rule["regex_pattern"]})
    elif rtype == "accepted_values_ref":
        mapped.update({"rule_type": "accepted_values_ref", "column": cols[0], "reference_table": rule["reference_table"], "reference_column": rule["reference_column"]})
    elif rtype == "string_length_between":
        mapped.update({"rule_type": "string_length_between", "column": cols[0], "min_length": int(rule["min_length"]), "max_length": int(rule["max_length"])})
    return mapped


def get_default_dq_rule_templates() -> dict[str, list[dict[str, Any]]]:
    """Return editable example data quality rules."""
    return {"EMAIL_LOGS": [{"rule_id": "EMAIL_LOGS_NOT_NULL_MESSAGE_ID", "rule_type": "not_null", "columns": ["message_id"], "severity": "error", "description": "Every email message row must have a message identifier."}]}


def validate_dq_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate notebook-facing DQ rules."""
    if not isinstance(rules, list):
        raise ValueError("rules must be provided as a list of dictionaries.")
    required = ["rule_id", "rule_type", "columns", "severity", "description"]
    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError(f"Rule at index {i} must be a dictionary.")
        for key in required:
            if key not in rule:
                raise ValueError(f"Rule '{rule.get('rule_id', i)}' is missing required field '{key}'.")
        rtype = rule["rule_type"]
        cols = rule["columns"]
        if rtype not in SUPPORTED_RULE_TYPES:
            raise ValueError(f"Rule '{rule['rule_id']}' has unsupported rule_type '{rtype}'.")
        if not isinstance(cols, list) or not cols:
            raise ValueError(f"Rule '{rule['rule_id']}' must include a non-empty columns list.")
        if rtype in {"not_null", "accepted_values", "regex_format", "value_range"} and len(cols) != 1:
            raise ValueError(f"Rule '{rule['rule_id']}' supports exactly one column in v1.")
        if rtype == "accepted_values" and "allowed_values" not in rule:
            raise ValueError(f"Rule '{rule['rule_id']}' requires allowed_values.")
        if rtype == "value_range" and ("min_value" not in rule and "max_value" not in rule):
            raise ValueError(f"Rule '{rule['rule_id']}' requires min_value or max_value.")
        if rtype == "regex_format" and "regex_pattern" not in rule:
            raise ValueError(f"Rule '{rule['rule_id']}' requires regex_pattern.")
        if rtype == "accepted_values_ref" and ("reference_table" not in rule or "reference_column" not in rule):
            raise ValueError(f"Rule '{rule['rule_id']}' requires reference_table and reference_column.")
        if rtype == "string_length_between" and ("min_length" not in rule or "max_length" not in rule):
            raise ValueError(f"Rule '{rule['rule_id']}' requires min_length and max_length.")
    return rules


def run_dq_rules(df, table_name: str, rules: list[dict[str, Any]], fail_on_error: bool = True):
    """Run notebook-facing DQ rules and return a Spark DataFrame result."""
    validate_dq_rules(rules)
    quality_compatible = [_to_quality_rule(r) for r in rules]
    qres = run_quality_rules(df, quality_compatible, dataset_name=table_name, table_name=table_name, engine="spark") if quality_compatible else {"results": []}
    by_id = {r["rule_id"]: r for r in qres.get("results", [])}
    total_count = df.count()
    result_schema = "table_name string, rule_id string, rule_type string, columns string, severity string, status string, failed_count long, total_count long, failed_percent double, description string, run_timestamp string, details string"
    if not rules:
        return df.sparkSession.createDataFrame([], schema=result_schema)

    rows=[]
    for rule in rules:
        rtype=rule["rule_type"]
        details=""
        item = by_id.get(rule["rule_id"], {})
        lower_status = str(item.get("status", "failed")).lower()
        failed = int(item.get("failed_count", 1))
        details = item.get("message", "")
        status = "PASS" if lower_status == "passed" and failed == 0 else "FAIL"
        rows.append({"table_name": table_name, "rule_id": rule["rule_id"], "rule_type": rtype, "columns": ",".join(rule["columns"]), "severity": rule["severity"], "status": status, "failed_count": failed, "total_count": int(total_count), "failed_percent": float(round((failed / total_count) * 100.0, 4)) if total_count else 0.0, "description": rule["description"], "run_timestamp": datetime.now(timezone.utc).isoformat(), "details": details})
    result_df = df.sparkSession.createDataFrame(rows)
    if fail_on_error:
        failures = [r for r in rows if str(r["severity"]).lower() == "error" and r["status"] == "FAIL"]
        if failures:
            msg = ", ".join(f"{r['rule_id']}({r['failed_count']})" for r in failures)
            raise ValueError(f"Data quality failed for error-severity rules: {msg}")
    return result_df


def assert_dq_passed(dq_result_df) -> None:
    """Raise when any error-severity DQ rule failed after results are logged."""
    failed = dq_result_df.filter("lower(severity) = 'error' AND status = 'FAIL'").collect()
    if failed:
        msg = ", ".join(f"{r['rule_id']}({r['failed_count']})" for r in failed)
        raise ValueError(f"Data quality failed for error-severity rules: {msg}")


def suggest_dq_rules_prompt(
    profile_df,
    table_name: str,
    business_context: str = "",
    output_format: str = "python_config",
    prompt_template: str | None = None,
) -> str:
    """Build a prompt for candidate DQ rule suggestions."""
    profile_records = profile_df.toPandas().to_dict("records") if hasattr(profile_df, "toPandas") else profile_df.to_dict("records")
    profile_json = json.dumps(profile_records, indent=2, default=str)
    template = prompt_template or DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE
    return template.format(
        table_name=table_name,
        business_context=business_context or "No business context supplied.",
        profile_json=profile_json,
        output_format=output_format,
    )



def suggest_accepted_value_mapping_prompt(source_value: str, approved_values: list[str]) -> str:
    """Build a constrained prompt for accepted-value mapping suggestions.

    Parameters
    ----------
    source_value : str
        Invalid source value that failed an ``accepted_values`` check.
    approved_values : list[str]
        Approved canonical values that suggestions must choose from.

    Returns
    -------
    str
        Prompt text constraining output to JSON-only mapping suggestions.

    Raises
    ------
    ValueError
        If ``source_value`` is blank or ``approved_values`` is empty.
    """
    if not isinstance(source_value, str) or not source_value.strip():
        raise ValueError("source_value must be a non-empty string.")
    if not isinstance(approved_values, list) or not approved_values:
        raise ValueError("approved_values must be a non-empty list of strings.")
    cleaned = [str(v) for v in approved_values if str(v).strip()]
    if not cleaned:
        raise ValueError("approved_values must contain at least one non-empty value.")

    return (
        "You are helping standardize organization names for a governed Fabric data pipeline.\n\n"
        "Task:\n"
        "Suggest a mapping from the invalid source value to one approved canonical value.\n\n"
        "Rules:\n"
        "- Only choose from the approved values provided.\n"
        "- Do not invent new canonical values.\n"
        "- If confidence is low, return \"needs_review\".\n"
        "- Return JSON only with:\n"
        "  source_value,\n"
        "  suggested_value,\n"
        "  confidence,\n"
        "  reason.\n\n"
        "Invalid source value:\n"
        f"{source_value}\n\n"
        "Approved values:\n"
        f"{cleaned}"
    )


def suggest_closest_accepted_value(source_value: str, approved_values: list[str], *, min_score: float = 0.75) -> dict[str, Any]:
    """Suggest a deterministic closest accepted value using ``difflib``.

    Parameters
    ----------
    source_value : str
        Source value requiring normalization.
    approved_values : list[str]
        Canonical approved values.
    min_score : float, default=0.75
        Minimum similarity score required to return a candidate suggestion.

    Returns
    -------
    dict[str, Any]
        Mapping payload with source value, suggested value, confidence,
        review flag, and method metadata.

    Raises
    ------
    ValueError
        If ``source_value`` is blank, ``approved_values`` is empty, or
        ``min_score`` is outside the inclusive [0.0, 1.0] range.
    """
    if not isinstance(source_value, str) or not source_value.strip():
        raise ValueError("source_value must be a non-empty string.")
    if not isinstance(approved_values, list) or not approved_values:
        raise ValueError("approved_values must be a non-empty list of strings.")
    if not (0.0 <= float(min_score) <= 1.0):
        raise ValueError("min_score must be between 0.0 and 1.0.")

    cleaned = [str(v) for v in approved_values if str(v).strip()]
    if not cleaned:
        raise ValueError("approved_values must contain at least one non-empty value.")

    source_norm = source_value.strip().lower()
    scores = []
    for candidate in cleaned:
        score = difflib.SequenceMatcher(None, source_norm, candidate.strip().lower()).ratio()
        scores.append((candidate, float(score)))
    best_value, best_score = max(scores, key=lambda x: x[1])
    if best_score < float(min_score):
        return {"source_value": source_value, "suggested_value": None, "confidence": round(best_score, 4), "needs_review": True, "method": "difflib"}
    return {"source_value": source_value, "suggested_value": best_value, "confidence": round(best_score, 4), "needs_review": True, "method": "difflib"}


def split_valid_and_quarantine(df, rules: list[dict[str, Any]], engine: str = "auto"):
    """Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.

    Parameters
    ----------
    df : Any
        Input DataFrame, currently Spark DataFrame is supported.
    rules : list[dict[str, Any]]
        Notebook-facing DQ rules in the same shape accepted by ``run_dq_rules``.
    engine : str, default="auto"
        Execution engine selector. ``auto`` resolves based on input type.

    Returns
    -------
    tuple[Any, Any]
        ``(df_pass, df_quarantine)`` where quarantine rows include metadata
        columns: ``dq_failed_rule_ids``, ``dq_failed_rule_types``,
        ``dq_failed_columns``, ``dq_failed_severities``, and ``dq_quarantine_ts``.

    Raises
    ------
    ValueError
        If rules are invalid or no row-level rule can be evaluated.
    NotImplementedError
        If a pandas DataFrame is provided.
    """
    validate_dq_rules(rules)
    resolved = engine
    if engine == "auto":
        resolved = "spark" if df.__class__.__module__.startswith("pyspark") else "pandas"
    if resolved == "pandas":
        raise NotImplementedError("split_valid_and_quarantine currently supports Spark DataFrames only.")
    if resolved != "spark":
        raise ValueError("engine must be 'auto' or 'spark' for this helper.")

    from pyspark.sql import functions as F
    from pyspark.sql.window import Window

    supported = {"not_null", "unique_key", "accepted_values", "value_range", "regex_format", "string_length_between"}
    eval_rules = [r for r in rules if r.get("rule_type") in supported]
    if not eval_rules:
        raise ValueError("No row-level quarantine rules found. Supported rule types: not_null, unique_key, accepted_values, value_range, regex_format, string_length_between.")

    working = df.withColumn("__dq_failed_rule_ids", F.array().cast("array<string>"))                .withColumn("__dq_failed_rule_types", F.array().cast("array<string>"))                .withColumn("__dq_failed_columns", F.array().cast("array<string>"))                .withColumn("__dq_failed_severities", F.array().cast("array<string>"))

    for rule in eval_rules:
        rid = str(rule["rule_id"])
        rtype = str(rule["rule_type"])
        col = rule["columns"][0]
        sev = str(rule.get("severity", "warning"))
        if rtype == "not_null":
            failed = F.col(col).isNull()
        elif rtype == "unique_key":
            dup_ct_col = f"__dq_dup_count_{rid}"
            key_cols = [F.col(c) for c in rule.get("columns", [])]
            working = working.withColumn(dup_ct_col, F.count(F.lit(1)).over(Window.partitionBy(*key_cols)))
            failed = F.col(dup_ct_col) > F.lit(1)
        elif rtype == "accepted_values":
            vals = rule.get("allowed_values", [])
            failed = F.col(col).isNotNull() & ~F.col(col).isin(vals)
        elif rtype == "value_range":
            min_v, max_v = rule.get("min_value"), rule.get("max_value")
            cond = F.lit(False)
            if min_v is not None:
                cond = cond | (F.col(col) < F.lit(min_v))
            if max_v is not None:
                cond = cond | (F.col(col) > F.lit(max_v))
            failed = F.col(col).isNotNull() & cond
        elif rtype == "regex_format":
            failed = F.col(col).isNotNull() & ~F.col(col).rlike(rule["regex_pattern"])
        else:  # string_length_between
            min_len, max_len = int(rule["min_length"]), int(rule["max_length"])
            failed = F.col(col).isNotNull() & ((F.length(F.col(col).cast("string")) < F.lit(min_len)) | (F.length(F.col(col).cast("string")) > F.lit(max_len)))

        working = working.withColumn("__dq_failed_rule_ids", F.when(failed, F.array_union(F.col("__dq_failed_rule_ids"), F.array(F.lit(rid)))).otherwise(F.col("__dq_failed_rule_ids")))
        working = working.withColumn("__dq_failed_rule_types", F.when(failed, F.array_union(F.col("__dq_failed_rule_types"), F.array(F.lit(rtype)))).otherwise(F.col("__dq_failed_rule_types")))
        working = working.withColumn("__dq_failed_columns", F.when(failed, F.array_union(F.col("__dq_failed_columns"), F.array(F.lit(col)))).otherwise(F.col("__dq_failed_columns")))
        working = working.withColumn("__dq_failed_severities", F.when(failed, F.array_union(F.col("__dq_failed_severities"), F.array(F.lit(sev)))).otherwise(F.col("__dq_failed_severities")))
        if rtype == "unique_key":
            working = working.drop(f"__dq_dup_count_{rid}")

    fail_cond = F.size(F.col("__dq_failed_rule_ids")) > F.lit(0)
    df_pass = working.filter(~fail_cond).drop("__dq_failed_rule_ids", "__dq_failed_rule_types", "__dq_failed_columns", "__dq_failed_severities")
    df_quarantine = working.filter(fail_cond).withColumn("dq_failed_rule_ids", F.concat_ws(",", F.col("__dq_failed_rule_ids")))        .withColumn("dq_failed_rule_types", F.concat_ws(",", F.col("__dq_failed_rule_types")))        .withColumn("dq_failed_columns", F.concat_ws(",", F.col("__dq_failed_columns")))        .withColumn("dq_failed_severities", F.concat_ws(",", F.col("__dq_failed_severities")))        .withColumn("dq_quarantine_ts", F.lit(datetime.now(timezone.utc).isoformat()))        .drop("__dq_failed_rule_ids", "__dq_failed_rule_types", "__dq_failed_columns", "__dq_failed_severities")
    return df_pass, df_quarantine
