"""Compile AI layman DQ candidates into executable framework quality rules."""

from __future__ import annotations

from .quality import SUPPORTED_RULE_TYPES


def _skipped(candidate, message):
    return {
        "status": "skipped",
        "can_compile": False,
        "compiler_warning": True,
        "compiler_message": message,
        "layman_rule": candidate.get("layman_rule"),
        "quality_rule": None,
        "candidate": candidate,
    }


def compile_layman_rule_to_quality_rule(candidate):
    """Compile layman rule to quality rule.

    Execute `compile_layman_rule_to_quality_rule`.

    Parameters
    ----------
    candidate : Any
        Value for `candidate`.

    Returns
    -------
    result : Any
        Result returned by `compile_layman_rule_to_quality_rule`.

    Examples
    --------
    >>> compile_layman_rule_to_quality_rule(candidate)
    """
    rule_type = str(candidate.get("rule_type", "")).strip().lower()
    if rule_type not in SUPPORTED_RULE_TYPES:
        return _skipped(candidate, f"Unsupported rule_type: {rule_type}")

    config = candidate.get("rule_config") if isinstance(candidate.get("rule_config"), dict) else {}
    rule = {"rule_id": candidate.get("rule_id") or "AI_COMPILED", "rule_type": rule_type, "severity": candidate.get("severity", "warning"), "reason": candidate.get("layman_rule") or candidate.get("reason")}

    if rule_type in {"not_null", "unique", "accepted_values", "range_check", "regex_check", "freshness_check"}:
        if not candidate.get("column"):
            return _skipped(candidate, f"Missing required field column for {rule_type}")
        rule["column"] = candidate["column"]
    if rule_type == "unique_combination":
        if not candidate.get("columns"):
            return _skipped(candidate, "Missing required field columns for unique_combination")
        rule["columns"] = candidate["columns"]

    if rule_type == "accepted_values":
        vals = config.get("accepted_values")
        if not isinstance(vals, list) or not vals:
            return _skipped(candidate, "accepted_values requires rule_config.accepted_values list")
        rule["accepted_values"] = vals
    elif rule_type == "range_check":
        if "min_value" not in config and "max_value" not in config:
            return _skipped(candidate, "range_check requires min_value and/or max_value")
        if "min_value" in config:
            rule["min_value"] = config["min_value"]
        if "max_value" in config:
            rule["max_value"] = config["max_value"]
    elif rule_type == "regex_check":
        if not config.get("pattern"):
            return _skipped(candidate, "regex_check requires rule_config.pattern")
        rule["pattern"] = config["pattern"]
    elif rule_type == "freshness_check":
        if "max_age_days" not in config:
            return _skipped(candidate, "freshness_check requires rule_config.max_age_days")
        rule["max_age_days"] = config["max_age_days"]
    elif rule_type == "row_count_min":
        if "min_count" not in config:
            return _skipped(candidate, "row_count_min requires rule_config.min_count")
        rule["min_count"] = config["min_count"]
    elif rule_type == "row_count_between":
        if "min_count" not in config or "max_count" not in config:
            return _skipped(candidate, "row_count_between requires rule_config.min_count and max_count")
        rule["min_count"] = config["min_count"]
        rule["max_count"] = config["max_count"]

    return {"status": "compiled", "can_compile": True, "compiler_warning": False, "compiler_message": "compiled", "layman_rule": candidate.get("layman_rule"), "quality_rule": rule, "candidate": candidate}


def compile_layman_rules_to_quality_rules(candidates):
    """Compile layman rules to quality rules.

    Execute `compile_layman_rules_to_quality_rules`.

    Parameters
    ----------
    candidates : Any
        Value for `candidates`.

    Returns
    -------
    result : Any
        Result returned by `compile_layman_rules_to_quality_rules`.

    Examples
    --------
    >>> compile_layman_rules_to_quality_rules(candidates)
    """
    records = [compile_layman_rule_to_quality_rule(c) for c in candidates]
    return {"compiled_rules": [r["quality_rule"] for r in records if r["status"] == "compiled"], "records": records, "summary": {"total": len(records), "compiled": sum(r["status"] == "compiled" for r in records), "skipped": sum(r["status"] == "skipped" for r in records)}}


def build_rule_registry_records(compiled_rules, run_id, dataset_name, table_name):
    """Build rule registry records.

    Execute `build_rule_registry_records`.

    Parameters
    ----------
    compiled_rules : Any
        Value for `compiled_rules`.
    run_id : Any
        Value for `run_id`.
    dataset_name : Any
        Value for `dataset_name`.
    table_name : Any
        Value for `table_name`.

    Returns
    -------
    result : Any
        Result returned by `build_rule_registry_records`.

    Examples
    --------
    >>> build_rule_registry_records(compiled_rules, run_id)
    """
    return [{"run_id": run_id, "dataset_name": dataset_name, "table_name": table_name, "rule_id": r.get("rule_id"), "rule_type": r.get("rule_type"), "severity": r.get("severity"), "column": r.get("column"), "columns": r.get("columns"), "reason": r.get("reason"), "rule_json": r} for r in compiled_rules]
