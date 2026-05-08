"""Data quality configuration, execution, and AI suggestion helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

from .fabric_io import lakehouse_table_write


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


def get_default_dq_rule_templates() -> dict[str, list[dict[str, Any]]]:
    """Return editable data quality rule templates for common rule patterns.

    Returns
    -------
    dict[str, list[dict[str, Any]]]
        Mapping of sample table names to reusable rule dictionaries.

    Notes
    -----
    These templates are examples only and are intended for human editing in
    ``00_env_config`` or an equivalent config module.
    """

    return {
        "EMAIL_LOGS": [
            {
                "rule_id": "EMAIL_LOGS_NOT_NULL_MESSAGE_ID",
                "rule_type": "not_null",
                "columns": ["message_id"],
                "severity": "error",
                "description": "Every email message row must have a message identifier.",
            },
            {
                "rule_id": "EMAIL_LOGS_UNIQUE_MESSAGE_ID",
                "rule_type": "unique_key",
                "columns": ["message_id"],
                "severity": "error",
                "description": "Message identifier must be unique.",
            },
        ]
    }


def validate_dq_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate data quality rule dictionaries before runtime enforcement.

    Parameters
    ----------
    rules : list[dict[str, Any]]
        Rule definitions to validate.

    Returns
    -------
    list[dict[str, Any]]
        The same rule list when validation succeeds.

    Raises
    ------
    ValueError
        Raised when any rule is structurally invalid.
    """

    if not isinstance(rules, list):
        raise ValueError("rules must be provided as a list of dictionaries.")

    required_fields = ["rule_id", "rule_type", "columns", "severity", "description"]

    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError(f"Rule at index {idx} must be a dictionary.")
        for field in required_fields:
            if field not in rule:
                raise ValueError(f"Rule '{rule.get('rule_id', idx)}' is missing required field '{field}'.")

        rule_type = str(rule["rule_type"]).strip()
        if rule_type not in SUPPORTED_RULE_TYPES:
            raise ValueError(f"Rule '{rule['rule_id']}' has unsupported rule_type '{rule_type}'.")

        columns = rule.get("columns")
        if not isinstance(columns, list) or any(not isinstance(c, str) or not c for c in columns):
            raise ValueError(f"Rule '{rule['rule_id']}' must include columns as a non-empty list of strings.")

        if rule_type in {"accepted_values", "regex_format", "value_range", "schema_data_type"} and len(columns) != 1:
            raise ValueError(f"Rule '{rule['rule_id']}' supports exactly one column in v1.")
        if rule_type == "accepted_values" and "allowed_values" not in rule:
            raise ValueError(f"Rule '{rule['rule_id']}' requires allowed_values.")
        if rule_type == "value_range" and ("min_value" not in rule or "max_value" not in rule):
            raise ValueError(f"Rule '{rule['rule_id']}' requires min_value and max_value.")
        if rule_type == "regex_format" and "regex_pattern" not in rule:
            raise ValueError(f"Rule '{rule['rule_id']}' requires regex_pattern.")
        if rule_type == "row_count_between" and ("min_rows" not in rule or "max_rows" not in rule):
            raise ValueError(f"Rule '{rule['rule_id']}' requires min_rows and max_rows.")
        if rule_type == "schema_data_type" and "expected_types" not in rule:
            raise ValueError(f"Rule '{rule['rule_id']}' requires expected_types mapping.")

    return rules


def run_dq_rules(df, table_name: str, rules: list[dict[str, Any]], fail_on_error: bool = True):
    """Run configured DQ rules against a Spark DataFrame.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Spark DataFrame to validate.
    table_name : str
        Logical output table name used in result records.
    rules : list[dict[str, Any]]
        Rule dictionaries validated by ``validate_dq_rules``.
    fail_on_error : bool, default=True
        Raise after execution when an ``error`` severity rule fails.

    Returns
    -------
    pyspark.sql.DataFrame
        One-row-per-rule Spark DataFrame of DQ execution results.

    Raises
    ------
    ValueError
        Raised when an error-severity rule fails and ``fail_on_error`` is true.
    """

    validate_dq_rules(rules)
    total_count = df.count()
    cols = set(df.columns)
    rows = []

    for rule in rules:
        rtype = rule["rule_type"]
        selected_cols = rule["columns"]
        failed_count = 0
        details = ""

        if rtype == "not_null":
            condition = None
            for c in selected_cols:
                condition = df[c].isNull() if condition is None else (condition | df[c].isNull())
            failed_count = df.filter(condition).count()
        elif rtype == "unique_key":
            failed_count = total_count - df.dropDuplicates(selected_cols).count()
        elif rtype == "accepted_values":
            column = selected_cols[0]
            allowed_values = rule["allowed_values"]
            failed_count = df.filter(~df[column].isin(allowed_values)).count()
        elif rtype == "value_range":
            column = selected_cols[0]
            min_value = rule["min_value"]
            max_value = rule["max_value"]
            failed_count = df.filter((df[column] < min_value) | (df[column] > max_value)).count()
        elif rtype == "regex_format":
            column = selected_cols[0]
            pattern = rule["regex_pattern"]
            failed_count = df.filter(~df[column].rlike(pattern)).count()
        elif rtype == "row_count_between":
            min_rows = int(rule["min_rows"])
            max_rows = int(rule["max_rows"])
            failed_count = 0 if min_rows <= total_count <= max_rows else 1
            details = f"Observed row count={total_count}; expected between {min_rows} and {max_rows}."
        elif rtype == "schema_required_columns":
            missing = sorted(set(selected_cols) - cols)
            failed_count = 0 if not missing else 1
            details = "" if not missing else f"Missing columns: {', '.join(missing)}"
        elif rtype == "schema_data_type":
            expected_types = rule["expected_types"]
            schema_map = {f.name: f.dataType.simpleString() for f in df.schema.fields}
            mismatches = []
            for col in selected_cols:
                expected = str(expected_types[col]).lower()
                actual = str(schema_map.get(col, "missing")).lower()
                if actual != expected:
                    mismatches.append(f"{col}: expected={expected}, actual={actual}")
            failed_count = 0 if not mismatches else 1
            details = "; ".join(mismatches)

        status = "PASS" if failed_count == 0 else "FAIL"
        failed_percent = 0.0 if total_count == 0 else (failed_count / total_count) * 100.0
        rows.append(
            {
                "table_name": table_name,
                "rule_id": rule["rule_id"],
                "rule_type": rtype,
                "columns": ",".join(selected_cols),
                "severity": rule["severity"],
                "status": status,
                "failed_count": int(failed_count),
                "total_count": int(total_count),
                "failed_percent": float(round(failed_percent, 4)),
                "description": rule["description"],
                "run_timestamp": datetime.now(timezone.utc).isoformat(),
                "details": details,
            }
        )

    result_df = df.sparkSession.createDataFrame(rows)
    error_failures = [r for r in rows if str(r["severity"]).lower() == "error" and r["status"] == "FAIL"]
    if fail_on_error and error_failures:
        msg = ", ".join(f"{r['rule_id']}({r['failed_count']})" for r in error_failures)
        raise ValueError(f"Data quality failed for error-severity rules: {msg}")
    return result_df


def write_dq_results(dq_result_df, lh, table_name: str = "DQ_RESULTS", mode: str = "append") -> None:
    """Write DQ rule execution results to a Fabric lakehouse table.

    Parameters
    ----------
    dq_result_df : pyspark.sql.DataFrame
        Spark DataFrame produced by ``run_dq_rules``.
    lh : Housepath
        Lakehouse target from framework path config.
    table_name : str, default="DQ_RESULTS"
        Destination table name.
    mode : str, default="append"
        Spark write mode.
    """

    lakehouse_table_write(dq_result_df, lh=lh, tablename=table_name, mode=mode)


def suggest_dq_rules_prompt(profile_df, table_name: str, business_context: str = "", output_format: str = "python_config") -> str:
    """Build a Copilot prompt for candidate DQ rule suggestions.

    Parameters
    ----------
    profile_df : pandas.DataFrame or pyspark.sql.DataFrame
        Profiling output containing per-column metadata.
    table_name : str
        Table name for which candidate rules are requested.
    business_context : str, default=""
        Optional plain-language business purpose.
    output_format : str, default="python_config"
        Requested candidate output format.

    Returns
    -------
    str
        Plain text prompt instructing Copilot to produce candidate rules only.
    """

    profile_records = profile_df.toPandas().to_dict("records") if hasattr(profile_df, "toPandas") else profile_df.to_dict("records")
    profile_json = json.dumps(profile_records, indent=2, default=str)
    return (
        f"You are helping draft candidate data quality rules for table '{table_name}'.\n"
        "IMPORTANT: Output is suggestion-only and must NOT be auto-enforced. "
        "A human must review and approve rules before copying into DQ_RULES in 00_env_config.\n\n"
        f"Business context:\n{business_context or 'No business context supplied.'}\n\n"
        f"Profile metadata:\n{profile_json}\n\n"
        f"Return candidate rules in {output_format} format as a Python dictionary shaped like "
        "DQ_RULES = {\"TABLE_NAME\": [<rule dictionaries>]}."
    )
