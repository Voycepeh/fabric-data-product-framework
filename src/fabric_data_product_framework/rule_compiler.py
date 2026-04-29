"""Compile AI layman DQ candidates into executable framework quality rules."""

from __future__ import annotations

from typing import Any

from .quality import SUPPORTED_RULE_TYPES


def compile_layman_rule_to_quality_rule(candidate):
    rule_type = str(candidate.get("rule_type", "")).strip().lower()
    if rule_type not in SUPPORTED_RULE_TYPES:
        return {"status": "skipped", "can_compile": False, "compiler_message": f"Unsupported rule_type: {rule_type}", "compiler_warning": True, "quality_rule": None, "candidate": candidate}

    config = candidate.get("rule_config") if isinstance(candidate.get("rule_config"), dict) else {}
    rule = {
        "rule_id": candidate.get("rule_id") or "AI_COMPILED",
        "rule_type": rule_type,
        "severity": candidate.get("severity", "warning"),
        "reason": candidate.get("layman_rule") or candidate.get("reason"),
    }

    if rule_type in {"not_null", "unique", "accepted_values", "range_check", "regex_check", "freshness_check"}:
        if not candidate.get("column"):
            return {"status": "skipped", "can_compile": False, "compiler_message": f"Missing required field column for {rule_type}", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        rule["column"] = candidate["column"]
    if rule_type == "unique_combination":
        if not candidate.get("columns"):
            return {"status": "skipped", "can_compile": False, "compiler_message": "Missing required field columns for unique_combination", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        rule["columns"] = candidate["columns"]

    if rule_type == "accepted_values":
        vals = config.get("accepted_values")
        if not isinstance(vals, list) or not vals:
            return {"status": "skipped", "can_compile": False, "compiler_message": "accepted_values requires rule_config.accepted_values list", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        rule["accepted_values"] = vals
    elif rule_type == "range_check":
        if "min_value" not in config and "max_value" not in config:
            return {"status": "skipped", "can_compile": False, "compiler_message": "range_check requires min_value and/or max_value", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        if "min_value" in config:
            rule["min_value"] = config["min_value"]
        if "max_value" in config:
            rule["max_value"] = config["max_value"]
    elif rule_type == "regex_check":
        if not config.get("pattern"):
            return {"status": "skipped", "can_compile": False, "compiler_message": "regex_check requires rule_config.pattern", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        rule["pattern"] = config["pattern"]
    elif rule_type == "freshness_check":
        if "max_age_days" not in config:
            return {"status": "skipped", "can_compile": False, "compiler_message": "freshness_check requires rule_config.max_age_days", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        rule["max_age_days"] = config["max_age_days"]
    elif rule_type == "row_count_min":
        if "min_count" not in config:
            return {"status": "skipped", "can_compile": False, "compiler_message": "row_count_min requires rule_config.min_count", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        rule["min_count"] = config["min_count"]
    elif rule_type == "row_count_between":
        if "min_count" not in config or "max_count" not in config:
            return {"status": "skipped", "can_compile": False, "compiler_message": "row_count_between requires rule_config.min_count and max_count", "compiler_warning": True, "quality_rule": None, "candidate": candidate}
        rule["min_count"] = config["min_count"]
        rule["max_count"] = config["max_count"]

    return {"status": "compiled", "can_compile": True, "compiler_message": "compiled", "compiler_warning": False, "quality_rule": rule, "candidate": candidate}


def compile_layman_rules_to_quality_rules(candidates):
    records = [compile_layman_rule_to_quality_rule(c) for c in candidates]
    return {
        "compiled_rules": [r["quality_rule"] for r in records if r["status"] == "compiled"],
        "records": records,
        "summary": {"total": len(records), "compiled": sum(r["status"] == "compiled" for r in records), "skipped": sum(r["status"] == "skipped" for r in records)},
    }


def build_rule_registry_records(compiled_rules, run_id, dataset_name, table_name):
    records = []
    for rule in compiled_rules:
        records.append(
            {
                "run_id": run_id,
                "dataset_name": dataset_name,
                "table_name": table_name,
                "rule_id": rule.get("rule_id"),
                "rule_type": rule.get("rule_type"),
                "severity": rule.get("severity"),
                "column": rule.get("column"),
                "columns": rule.get("columns"),
                "reason": rule.get("reason"),
                "rule_json": rule,
            }
        )
    return records
