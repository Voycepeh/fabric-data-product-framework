"""Notebook-friendly data quality wrappers built on top of quality.py."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

from .quality import run_quality_rules

SUPPORTED_RULE_TYPES = {
    "not_null",
    "unique_key",
    "accepted_values",
    "value_range",
    "regex_format",
    "row_count_between",
    "schema_required_columns",
    "schema_data_type",
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
- row_count_between
- schema_required_columns
- schema_data_type

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
    elif rtype == "row_count_between":
        mapped.update({"rule_type": "row_count_between", "min_count": int(rule["min_rows"]), "max_count": int(rule["max_rows"])})
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
        if rtype == "row_count_between" and ("min_rows" not in rule or "max_rows" not in rule):
            raise ValueError(f"Rule '{rule['rule_id']}' requires min_rows and max_rows.")
        if rtype == "schema_data_type":
            expected = rule.get("expected_types")
            if not isinstance(expected, dict):
                raise ValueError(f"Rule '{rule['rule_id']}' requires expected_types mapping.")
            missing = [c for c in cols if c not in expected]
            if missing:
                raise ValueError(f"Rule '{rule['rule_id']}' expected_types missing columns: {', '.join(missing)}")
    return rules


def run_dq_rules(df, table_name: str, rules: list[dict[str, Any]], fail_on_error: bool = True):
    """Run notebook-facing DQ rules and return a Spark DataFrame result."""
    validate_dq_rules(rules)
    quality_compatible = [_to_quality_rule(r) for r in rules if r["rule_type"] not in {"schema_required_columns", "schema_data_type"}]
    qres = run_quality_rules(df, quality_compatible, dataset_name=table_name, table_name=table_name, engine="spark") if quality_compatible else {"results": []}
    by_id = {r["rule_id"]: r for r in qres.get("results", [])}
    total_count = df.count()
    schema_map = {f.name: f.dataType.simpleString().lower() for f in df.schema.fields}
    result_schema = "table_name string, rule_id string, rule_type string, columns string, severity string, status string, failed_count long, total_count long, failed_percent double, description string, run_timestamp string, details string"
    if not rules:
        return df.sparkSession.createDataFrame([], schema=result_schema)

    rows=[]
    for rule in rules:
        rtype=rule["rule_type"]
        details=""
        if rtype == "schema_required_columns":
            missing = sorted(set(rule["columns"]) - set(df.columns))
            failed = 0 if not missing else 1
            details = "" if not missing else f"Missing columns: {', '.join(missing)}"
        elif rtype == "schema_data_type":
            mismatches=[]
            for c in rule["columns"]:
                actual = schema_map.get(c, "missing")
                expected = str(rule["expected_types"][c]).lower()
                if actual != expected:
                    mismatches.append(f"{c}: expected={expected}, actual={actual}")
            failed = 0 if not mismatches else 1
            details = "; ".join(mismatches)
        else:
            item = by_id.get(rule["rule_id"], {})
            failed = int(item.get("failed_count", 1))
            details = item.get("message", "")
        status = "PASS" if failed == 0 else "FAIL"
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
