"""Canonical Spark/Fabric data-quality workflow helpers for notebook users."""

from __future__ import annotations

import ast
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from pyspark.sql import functions as F
from pyspark.sql.window import Window

AI_SUGGESTABLE_DQ_RULE_TYPES = {"not_null", "unique_key", "accepted_values", "value_range", "regex_format"}


def profile_for_dq(df, table_name: str, business_context: str = "", sample_value_limit: int = 20):
    """Profile a Spark DataFrame into one row per source column for DQ rule suggestion.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Source Spark DataFrame.
    table_name : str
        Logical table name to include in profile rows.
    business_context : str, default=""
        Domain context carried into profile rows and AI prompts.
    sample_value_limit : int, default=20
        Maximum number of distinct non-null sample values per column.

    Returns
    -------
    pyspark.sql.DataFrame
        Spark profile DataFrame with one row per input column.
    """
    row_count = df.count()
    rows = []
    for column_name, data_type in df.dtypes:
        null_count = df.filter(F.col(column_name).isNull()).count()
        distinct_count = df.select(column_name).distinct().count()
        min_value = None
        max_value = None
        if data_type in {"int", "bigint", "double", "float", "date", "timestamp"} or data_type.startswith("decimal"):
            mm = df.select(F.min(F.col(column_name)).cast("string").alias("min_value"), F.max(F.col(column_name)).cast("string").alias("max_value")).collect()[0]
            min_value, max_value = mm["min_value"], mm["max_value"]
        observed = [str(r[column_name]) for r in df.select(column_name).where(F.col(column_name).isNotNull()).distinct().limit(sample_value_limit).collect()]
        rows.append({"table_name": table_name, "column_name": column_name, "data_type": data_type, "row_count": int(row_count), "null_count": int(null_count), "null_percent": round((null_count / row_count) * 100, 4) if row_count else 0.0, "distinct_count": int(distinct_count), "distinct_percent": round((distinct_count / row_count) * 100, 4) if row_count else 0.0, "min_value": min_value, "max_value": max_value, "observed_values_sample": ", ".join(observed), "business_context": business_context, "profile_timestamp": datetime.now(timezone.utc).isoformat()})
    return df.sparkSession.createDataFrame(rows)


def suggest_dq_rules(profile_df, prompt_template: str | None = None, output_col: str = "response"):
    """Generate row-wise AI DQ suggestions using Fabric AI Functions.

    Parameters
    ----------
    profile_df : pyspark.sql.DataFrame
        Output of :func:`profile_for_dq`.
    prompt_template : str | None, optional
        Prompt template from ``config.ai_prompt_config.dq_rule_candidate_template``.
    output_col : str, default="response"
        Output column for AI text responses.

    Returns
    -------
    pyspark.sql.DataFrame
        Spark DataFrame including AI response text.
    """
    if not prompt_template:
        raise ValueError("prompt_template must be provided from config.ai_prompt_config.dq_rule_candidate_template.")
    active_prompt = prompt_template
    return profile_df.ai.generate_response(prompt=active_prompt, output_col=output_col)


def _parse_dq_rules_dict_from_text(text: str) -> dict[str, list[dict[str, Any]]]:
    cleaned = str(text or "").strip()
    match = re.search(r"DQ_RULES\s*=\s*(\{.*\})", cleaned, flags=re.DOTALL)
    payload = match.group(1) if match else cleaned
    try:
        parsed = ast.literal_eval(payload)
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def extract_dq_rules(response_df, table_name: str, response_col: str = "response") -> list[dict[str, Any]]:
    """Extract notebook-shaped AI responses and deduplicate candidate DQ rules by ``rule_id``."""
    candidates: list[dict[str, Any]] = []
    for row in response_df.select(response_col).collect():
        candidates.extend(_parse_dq_rules_dict_from_text(row[response_col]).get(table_name, []))
    deduped: dict[str, dict[str, Any]] = {}
    for rule in candidates:
        rid = rule.get("rule_id")
        if rid:
            deduped[rid] = rule
    return list(deduped.values())


def validate_dq_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate canonical DQ rules before enforcement.

    Notes
    -----
    Supported canonical ``rule_type`` values are ``not_null``, ``unique_key``,
    ``accepted_values``, ``value_range``, and ``regex_format``.

    Raises
    ------
    ValueError
        If a rule type, severity, column binding, or required field is invalid.
    """
    if not isinstance(rules, list):
        raise ValueError("DQ rules must be a list of dictionaries.")
    required = {"rule_id", "rule_type", "columns", "severity", "description"}
    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError(f"DQ rule at index {i} must be a dictionary.")
        missing = required.difference(rule)
        if missing:
            raise ValueError(f"DQ rule '{rule.get('rule_id', i)}' is missing fields: {sorted(missing)}")
        if rule["rule_type"] not in AI_SUGGESTABLE_DQ_RULE_TYPES:
            raise ValueError(f"DQ rule '{rule['rule_id']}' has unsupported rule_type '{rule['rule_type']}'.")
        if str(rule["severity"]).lower() not in {"warning", "error"}:
            raise ValueError(f"DQ rule '{rule['rule_id']}' severity must be warning or error.")
        cols = rule.get("columns")
        if not isinstance(cols, list) or not cols:
            raise ValueError(f"DQ rule '{rule['rule_id']}' columns must be a non-empty list.")
        if rule["rule_type"] in {"not_null", "accepted_values", "value_range", "regex_format"} and len(cols) != 1:
            raise ValueError(f"DQ rule '{rule['rule_id']}' requires exactly one column.")
        if rule["rule_type"] == "accepted_values" and "allowed_values" not in rule:
            raise ValueError(f"DQ rule '{rule['rule_id']}' requires allowed_values.")
        if rule["rule_type"] == "value_range" and "min_value" not in rule and "max_value" not in rule:
            raise ValueError(f"DQ rule '{rule['rule_id']}' requires min_value or max_value.")
        if rule["rule_type"] == "regex_format" and "regex_pattern" not in rule:
            raise ValueError(f"DQ rule '{rule['rule_id']}' requires regex_pattern.")
    return rules


def build_dq_rule_history(spark, table_name: str, approved_rules: list[dict], action_by: str = "notebook_user", rule_source: str = "ai_widget_approval", action_reason: str = "Approved after human review."):
    """Build append-only active metadata rows for approved DQ rules.

    Parameters
    ----------
    spark : pyspark.sql.SparkSession
        Active Spark session used to create metadata DataFrame.
    table_name : str
        Logical table name for the governed rules.
    approved_rules : list[dict]
        Human-approved canonical DQ rules to append as active versions.
    action_by : str, default="notebook_user"
        Actor identity for audit tracking.
    rule_source : str, default="ai_widget_approval"
        Source label for audit tracking.
    action_reason : str, default="Approved after human review."
        Human-readable reason for approval action.

    Returns
    -------
    pyspark.sql.DataFrame
        Append-only metadata rows with ``is_active=True`` and ``action_type=approved``.
    """
    ts = datetime.now(timezone.utc).isoformat(); rows = []
    for rule in approved_rules:
        cols = rule.get("columns", [])
        rows.append({"table_name": table_name, "rule_id": str(rule["rule_id"]), "rule_type": str(rule["rule_type"]), "columns": ",".join(cols), "rule_key": f"{table_name}|{rule['rule_id']}|{rule['rule_type']}|{','.join(cols)}", "is_active": True, "action_type": "approved", "action_by": action_by, "action_ts": ts, "action_reason": action_reason, "rule_source": rule_source, "rule_json": json.dumps(rule)})
    return spark.createDataFrame(rows)


def build_dq_rule_deactivations(spark, table_name: str, deactivations: list[dict], action_by: str = "notebook_user", rule_source: str = "rule_deactivation_widget"):
    """Build append-only inactive metadata rows for governed DQ rule deactivation.

    Parameters
    ----------
    spark : pyspark.sql.SparkSession
        Active Spark session used to create metadata DataFrame.
    table_name : str
        Logical table name for the governed rules.
    deactivations : list[dict]
        Items shaped as ``{"rule": <rule dict>, "action_reason": <str>}``.
    action_by : str, default="notebook_user"
        Actor identity for audit tracking.
    rule_source : str, default="rule_deactivation_widget"
        Source label for audit tracking.

    Returns
    -------
    pyspark.sql.DataFrame
        Append-only metadata rows with ``is_active=False`` and ``action_type=deactivated``.

    Raises
    ------
    ValueError
        If any deactivation record has an empty reason.
    """
    ts = datetime.now(timezone.utc).isoformat(); rows = []
    for item in deactivations:
        reason = str(item["action_reason"]).strip(); rule = item["rule"]
        if not reason:
            raise ValueError(f"Deactivation reason is required for rule '{rule['rule_id']}'.")
        cols = rule.get("columns", [])
        rows.append({"table_name": table_name, "rule_id": str(rule["rule_id"]), "rule_type": str(rule["rule_type"]), "columns": ",".join(cols), "rule_key": f"{table_name}|{rule['rule_id']}|{rule['rule_type']}|{','.join(cols)}", "is_active": False, "action_type": "deactivated", "action_by": action_by, "action_ts": ts, "action_reason": reason, "rule_source": rule_source, "rule_json": json.dumps(rule)})
    return spark.createDataFrame(rows)


def _latest_dq_rule_versions(metadata_df, table_name: str):
    """Resolve latest metadata row per rule key."""
    w = Window.partitionBy("rule_key").orderBy(F.col("action_ts").desc())
    return metadata_df.filter(F.col("table_name") == table_name).withColumn("_rn", F.row_number().over(w)).filter(F.col("_rn") == 1).drop("_rn")


def load_active_dq_rules(metadata_df, table_name: str) -> list[dict[str, Any]]:
    """Load latest active approved rules from append-only metadata history.

    Parameters
    ----------
    metadata_df : pyspark.sql.DataFrame
        Append-only metadata table containing active and inactive versions.
    table_name : str
        Logical table name to resolve.

    Returns
    -------
    list[dict[str, Any]]
        Latest active rule payloads deserialized from ``rule_json``.

    Notes
    -----
    Latest-version resolution is done per ``rule_key``; a newer inactive version suppresses older active versions.
    """
    rows = _latest_dq_rule_versions(metadata_df, table_name).filter(F.col("is_active") == True).select("rule_json").collect()
    return [json.loads(r["rule_json"]) for r in rows]


# removed public metadata-row loader
def _load_active_dq_rule_metadata(metadata_df, table_name: str):
    """Return latest active metadata rows for governance review screens.

    Parameters
    ----------
    metadata_df : pyspark.sql.DataFrame
        Append-only metadata table containing active and inactive versions.
    table_name : str
        Logical table name to resolve.

    Returns
    -------
    pyspark.sql.DataFrame
        Latest active metadata versions per ``rule_key``.
    """
    return _latest_dq_rule_versions(metadata_df, table_name).filter(F.col("is_active") == True)


def split_dq_rows(df, rules: list[dict[str, Any]], dq_run_id: str | None = None, row_id_columns: list[str] | None = None):
    """Split source rows into valid rows, quarantine rows, and one-row-per-failure evidence.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Source Spark DataFrame to evaluate.
    rules : list[dict[str, Any]]
        Canonical approved DQ rules to enforce.
    dq_run_id : str | None, optional
        Optional run identifier; auto-generated when omitted.
    row_id_columns : list[str] | None, optional
        Optional stable business-key columns used for deterministic row IDs.

    Returns
    -------
    tuple[pyspark.sql.DataFrame, pyspark.sql.DataFrame, pyspark.sql.DataFrame]
        ``(valid_rows, quarantine_rows, quarantine_failure_evidence)``.

    Raises
    ------
    ValueError
        If rules fail canonical DQ validation.

    Notes
    -----
    A single source row may generate multiple failure-evidence rows when multiple rules fail.
    """
    validate_dq_rules(rules)
    dq_run_id = dq_run_id or str(uuid.uuid4())
    run_ts = datetime.now(timezone.utc).isoformat()
    if row_id_columns:
        df_with_ids = df.withColumn("dq_row_id", F.sha2(F.concat_ws("||", *[F.coalesce(F.col(c).cast("string"), F.lit("<NULL>")) for c in row_id_columns]), 256))
    else:
        df_with_ids = df.withColumn("dq_row_id", F.sha2(F.concat_ws("||", *[F.coalesce(F.col(c).cast("string"), F.lit("<NULL>")) for c in df.columns], F.monotonically_increasing_id().cast("string")), 256))
    working = df_with_ids.withColumn("dq_run_id", F.lit(dq_run_id))
    failure_dfs = []
    for rule in rules:
        rid, rtype, cols = str(rule["rule_id"]), str(rule["rule_type"]), rule["columns"]
        col_name = cols[0] if cols else None
        if rtype == "not_null":
            failed = F.col(col_name).isNull() | (F.trim(F.col(col_name).cast("string")) == "")
        elif rtype == "unique_key":
            dup_col = f"__dq_duplicate_count_{rid}"; working = working.withColumn(dup_col, F.count(F.lit(1)).over(Window.partitionBy(*[F.col(c) for c in cols]))); failed = F.col(dup_col) > F.lit(1)
        elif rtype == "accepted_values":
            failed = F.col(col_name).isNotNull() & ~F.col(col_name).isin(rule["allowed_values"])
        elif rtype == "value_range":
            cond = F.lit(False)
            if rule.get("min_value") is not None: cond = cond | (F.col(col_name).cast("double") < F.lit(float(rule["min_value"])))
            if rule.get("max_value") is not None: cond = cond | (F.col(col_name).cast("double") > F.lit(float(rule["max_value"])))
            failed = F.col(col_name).isNotNull() & cond
        elif rtype == "regex_format":
            failed = F.col(col_name).isNotNull() & ~F.col(col_name).rlike(rule["regex_pattern"])
        else:
            continue
        failure_dfs.append(working.filter(F.coalesce(failed, F.lit(False))).select(F.col("dq_run_id"), F.col("dq_row_id"), F.lit(rid).alias("rule_id"), F.lit(rtype).alias("rule_type"), F.lit(",".join(cols)).alias("failed_columns"), F.lit(str(rule.get("severity", "warning"))).alias("severity"), F.lit(str(rule.get("description", ""))).alias("description"), F.lit(run_ts).alias("dq_failed_ts")))
        if rtype == "unique_key":
            working = working.drop(dup_col)
    if not failure_dfs:
        empty = df.sparkSession.createDataFrame([], "dq_run_id string, dq_row_id string, dq_quarantine_id string, rule_id string, rule_type string, failed_columns string, severity string, description string, dq_failed_ts string")
        return working, working.limit(0), empty
    failures = failure_dfs[0]
    for x in failure_dfs[1:]:
        failures = failures.unionByName(x)
    quarantine_ids = failures.select("dq_run_id", "dq_row_id").distinct().withColumn("dq_quarantine_id", F.sha2(F.concat_ws("||", F.col("dq_run_id"), F.col("dq_row_id")), 256))
    failures = failures.join(quarantine_ids, on=["dq_run_id", "dq_row_id"], how="left").select("dq_run_id", "dq_row_id", "dq_quarantine_id", "rule_id", "rule_type", "failed_columns", "severity", "description", "dq_failed_ts")
    quarantine_rows = working.join(quarantine_ids, on=["dq_run_id", "dq_row_id"], how="inner").withColumn("dq_quarantine_ts", F.lit(run_ts))
    valid = working.join(quarantine_ids.select("dq_run_id", "dq_row_id"), on=["dq_run_id", "dq_row_id"], how="left_anti")
    return valid, quarantine_rows, failures


def run_dq_rules(df, table_name: str, rules: list[dict[str, Any]]):
    """Run canonical DQ rules and return Spark rule-level PASS/FAIL evidence for all rules.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Source Spark DataFrame to evaluate.
    table_name : str
        Logical table name included in output evidence rows.
    rules : list[dict[str, Any]]
        Canonical approved DQ rules to enforce.

    Returns
    -------
    pyspark.sql.DataFrame
        Rule-level evidence including PASS and FAIL rows for every approved rule.

    Raises
    ------
    ValueError
        If rules fail canonical DQ validation.
    """
    validate_dq_rules(rules)
    _, _, failures = split_dq_rows(df, rules)
    total = df.count()
    failure_counts = {r["rule_id"]: int(r["failed_count"]) for r in failures.groupBy("rule_id").agg(F.count(F.lit(1)).alias("failed_count")).collect()}
    rows = []
    for rule in rules:
        failed_count = failure_counts.get(rule["rule_id"], 0)
        rows.append({"table_name": table_name, "rule_id": rule["rule_id"], "rule_type": rule["rule_type"], "columns": ",".join(rule["columns"]), "severity": str(rule["severity"]).lower(), "status": "PASS" if failed_count == 0 else "FAIL", "failed_count": int(failed_count), "total_count": int(total), "failed_percent": float(round((failed_count / total) * 100, 4)) if total else 0.0, "description": rule.get("description", ""), "run_timestamp": datetime.now(timezone.utc).isoformat()})
    return df.sparkSession.createDataFrame(rows)


def assert_dq_passed(dq_result_df) -> None:
    """Raise only after evidence materialization when error-severity rules fail.

    Parameters
    ----------
    dq_result_df : pyspark.sql.DataFrame
        Materialized rule-level DQ results DataFrame.

    Raises
    ------
    ValueError
        If any row has ``severity=error`` and ``status=FAIL``.
    """
    if dq_result_df.filter("lower(severity) = 'error' AND status = 'FAIL'").count() > 0:
        raise ValueError("Data quality failed for error-severity rules.")


# Backward-compatible aliases (not exported)
profile_dataframe_for_dq = profile_for_dq
suggest_dq_rules_with_fabric_ai = suggest_dq_rules
extract_candidate_rules_from_responses = extract_dq_rules
build_dq_rules_metadata_df = build_dq_rule_history
build_dq_rule_deactivation_metadata_df = build_dq_rule_deactivations
load_latest_active_dq_rules_from_metadata = load_active_dq_rules
split_valid_quarantine_and_failures = split_dq_rows
