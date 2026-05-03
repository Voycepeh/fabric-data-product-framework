"""Lightweight data quality rule execution for pandas and Spark."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import math
from pathlib import Path
import re
from typing import Any

import pandas as pd
import yaml

from fabric_data_product_framework.drift import (
    build_and_write_partition_snapshot,
    build_and_write_schema_snapshot,
    check_partition_drift,
    check_schema_drift,
    load_latest_partition_snapshot,
    load_latest_schema_snapshot,
    summarize_drift_results,
)
from fabric_data_product_framework.lineage import build_lineage_records
from fabric_data_product_framework.metadata import build_dataset_run_record, write_metadata_records
from fabric_data_product_framework.profiling import flatten_profile_for_metadata, profile_dataframe
from fabric_data_product_framework.governance import (
    build_governance_classification_records,
    classify_columns,
    summarize_governance_classifications,
    write_governance_classifications,
)
from fabric_data_product_framework.run_summary import build_run_summary, build_run_summary_record
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.technical_columns import add_audit_columns, add_hash_columns, default_technical_columns

SUPPORTED_RULE_TYPES = {
    "not_null",
    "unique",
    "unique_combination",
    "accepted_values",
    "range_check",
    "regex_check",
    "row_count_min",
    "row_count_between",
    "freshness_check",
}
SEVERITY_TO_ACTION = {"info": "allow", "warning": "warn", "critical": "block"}


class DataQualityError(Exception):
    """Dataqualityerror.

    Public class used by the framework API for `DataQualityError`.

    Examples
    --------
    >>> DataQualityError(... )
    """


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def _resolve_engine(df: Any, engine: str) -> str:
    if engine not in {"auto", "pandas", "spark"}:
        raise ValueError("engine must be one of: auto, pandas, spark")
    if engine != "auto":
        return engine
    if isinstance(df, pd.DataFrame):
        return "pandas"
    if df.__class__.__module__.startswith("pyspark"):
        return "spark"
    raise ValueError("Unable to auto-detect engine; please pass engine='pandas' or engine='spark'.")


def _normalize_severity(rule: dict[str, Any]) -> tuple[str, str | None]:
    severity = str(rule.get("severity", "critical")).lower()
    if severity not in SEVERITY_TO_ACTION:
        return "critical", "Invalid severity; defaulted to critical"
    return severity, None


def _result_from_counts(rule: dict[str, Any], severity: str, failed_count: int, total_count: int, threshold: Any, message: str) -> dict[str, Any]:
    status = "failed" if failed_count > 0 else "passed"
    return {
        "rule_id": rule.get("rule_id", "unknown"),
        "rule_type": rule.get("rule_type", "unknown"),
        "column_name": rule.get("column"),
        "columns": rule.get("columns"),
        "severity": severity,
        "status": status,
        "action": SEVERITY_TO_ACTION[severity] if status == "failed" else "allow",
        "failed_count": int(failed_count),
        "total_count": int(total_count),
        "failed_pct": float((failed_count / total_count) * 100.0) if total_count > 0 else 0.0,
        "threshold": _to_jsonable(threshold),
        "message": message,
        "reason": rule.get("reason"),
    }


def _pandas_rule(df: pd.DataFrame, rule: dict[str, Any], row_count: int) -> tuple[int, int, Any, str]:
    rtype = rule["rule_type"]
    if rtype == "not_null":
        c = rule["column"]
        return int(df[c].isna().sum()), row_count, {"not_null": True}, f"Column '{c}' contains nulls"
    if rtype == "unique":
        c = rule["column"]
        return int(df[c].duplicated(keep=False).sum()), row_count, {"unique": True}, f"Column '{c}' has duplicates"
    if rtype == "unique_combination":
        cols = rule["columns"]
        return int(df.duplicated(subset=cols, keep=False).sum()), row_count, {"unique_combination": cols}, f"Combination {cols} has duplicates"
    if rtype == "accepted_values":
        c = rule["column"]
        vals = rule.get("accepted_values", [])
        mask = df[c].notna() & ~df[c].isin(vals)
        return int(mask.sum()), row_count, {"accepted_values": vals}, f"Column '{c}' has unexpected values"
    if rtype == "range_check":
        c = rule["column"]
        min_v, max_v = rule.get("min_value"), rule.get("max_value")
        if min_v is None and max_v is None:
            raise ValueError("range_check requires at least one of min_value or max_value")
        s = df[c]
        out_of_range = pd.Series(False, index=df.index)
        if min_v is not None:
            out_of_range |= s.notna() & (s < min_v)
        if max_v is not None:
            out_of_range |= s.notna() & (s > max_v)
        return int(out_of_range.sum()), row_count, {"min_value": min_v, "max_value": max_v}, f"Column '{c}' is out of range"
    if rtype == "regex_check":
        c = rule["column"]
        pattern = rule["pattern"]
        non_null = df[c].dropna().astype(str)
        return int((~non_null.str.match(pattern, na=False)).sum()), row_count, {"pattern": pattern}, f"Column '{c}' failed regex check"
    if rtype == "row_count_min":
        min_count = int(rule["min_count"])
        return (1 if row_count < min_count else 0), row_count, {"min_count": min_count}, "Row count below minimum"
    if rtype == "row_count_between":
        min_count = int(rule["min_count"])
        max_count = int(rule["max_count"])
        fail = row_count < min_count or row_count > max_count
        return (1 if fail else 0), row_count, {"min_count": min_count, "max_count": max_count}, "Row count outside expected range"
    if rtype == "freshness_check":
        c = rule["column"]
        max_age = int(rule["max_age_days"])
        s = pd.to_datetime(df[c], errors="coerce", utc=True).dropna()
        if s.empty:
            return 1, row_count, {"max_age_days": max_age}, "No valid timestamps found for freshness check"
        max_ts = s.max()
        age_days = (pd.Timestamp.now(tz="UTC") - max_ts).total_seconds() / 86400
        return (1 if age_days > max_age else 0), row_count, {"max_age_days": max_age}, "Data is stale"
    raise ValueError("Unsupported rule type")


def _spark_rule(df: Any, rule: dict[str, Any], row_count: int) -> tuple[int, int, Any, str]:
    from pyspark.sql import functions as F

    rtype = rule["rule_type"]
    if rtype == "not_null":
        c = rule["column"]
        return df.filter(F.col(c).isNull()).count(), row_count, {"not_null": True}, f"Column '{c}' contains nulls"
    if rtype == "unique":
        c = rule["column"]
        failed = df.groupBy(c).count().filter(F.col("count") > 1).agg(F.sum("count").alias("failed")).collect()[0]["failed"] or 0
        return int(failed), row_count, {"unique": True}, f"Column '{c}' has duplicates"
    if rtype == "unique_combination":
        cols = rule["columns"]
        failed = df.groupBy(*cols).count().filter(F.col("count") > 1).agg(F.sum("count").alias("failed")).collect()[0]["failed"] or 0
        return int(failed), row_count, {"unique_combination": cols}, f"Combination {cols} has duplicates"
    if rtype == "accepted_values":
        c = rule["column"]
        vals = rule.get("accepted_values", [])
        failed = df.filter(F.col(c).isNotNull() & ~F.col(c).isin(vals)).count()
        return failed, row_count, {"accepted_values": vals}, f"Column '{c}' has unexpected values"
    if rtype == "range_check":
        c = rule["column"]
        min_v, max_v = rule.get("min_value"), rule.get("max_value")
        cond = F.lit(False)
        if min_v is not None:
            cond = cond | (F.col(c) < F.lit(min_v))
        if max_v is not None:
            cond = cond | (F.col(c) > F.lit(max_v))
        failed = df.filter(F.col(c).isNotNull() & cond).count()
        return failed, row_count, {"min_value": min_v, "max_value": max_v}, f"Column '{c}' is out of range"
    if rtype == "regex_check":
        c = rule["column"]
        pattern = rule["pattern"]
        failed = df.filter(F.col(c).isNotNull() & ~F.col(c).rlike(pattern)).count()
        return failed, row_count, {"pattern": pattern}, f"Column '{c}' failed regex check"
    if rtype == "row_count_min":
        min_count = int(rule["min_count"])
        return (1 if row_count < min_count else 0), row_count, {"min_count": min_count}, "Row count below minimum"
    if rtype == "row_count_between":
        min_count = int(rule["min_count"])
        max_count = int(rule["max_count"])
        return (1 if row_count < min_count or row_count > max_count else 0), row_count, {"min_count": min_count, "max_count": max_count}, "Row count outside expected range"
    if rtype == "freshness_check":
        c = rule["column"]
        max_age = int(rule["max_age_days"])
        max_ts = df.select(F.max(F.col(c)).alias("max_ts")).collect()[0]["max_ts"]
        if max_ts is None:
            return 1, row_count, {"max_age_days": max_age}, "No valid timestamps found for freshness check"
        now_utc = datetime.now(timezone.utc)
        if max_ts.tzinfo is None:
            max_ts = max_ts.replace(tzinfo=timezone.utc)
        age_days = (now_utc - max_ts).total_seconds() / 86400
        return (1 if age_days > max_age else 0), row_count, {"max_age_days": max_age}, "Data is stale"
    raise ValueError("Unsupported rule type")


def run_quality_rules(df: Any, rules: list[dict], *, dataset_name: str = "unknown", table_name: str = "unknown", engine: str = "auto") -> dict:
    """Run quality rules.

    Run `run_quality_rules`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    rules : list[dict]
        Parameter `rules`.
    dataset_name : str, optional
        Parameter `dataset_name`.
    table_name : str, optional
        Parameter `table_name`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `run_quality_rules`.

    Examples
    --------
    >>> run_quality_rules(df, rules)
    """
    resolved_engine = _resolve_engine(df, engine)
    row_count = len(df) if resolved_engine == "pandas" else df.count()
    results = []

    for idx, rule in enumerate(rules):
        severity, sev_msg = _normalize_severity(rule)
        rule = dict(rule)
        rule_id = rule.get("rule_id", f"DQ{idx + 1:03d}")
        rule_type = rule.get("rule_type")
        base = {
            "rule_id": rule_id,
            "rule_type": rule_type or "unknown",
            "column_name": rule.get("column"),
            "columns": rule.get("columns"),
            "severity": severity,
            "status": "failed",
            "action": SEVERITY_TO_ACTION[severity],
            "failed_count": 1,
            "total_count": int(row_count),
            "failed_pct": 100.0 if row_count else 0.0,
            "threshold": None,
            "message": "Invalid rule",
            "reason": rule.get("reason"),
        }
        if not rule_type:
            base["message"] = "Missing required key: rule_type"
            results.append(base)
            continue
        if rule_type not in SUPPORTED_RULE_TYPES:
            base.update({"status": "skipped", "action": "allow", "failed_count": 0, "failed_pct": 0.0, "message": "Unsupported rule type"})
            results.append(base)
            continue

        required = {
            "not_null": ["column"],
            "unique": ["column"],
            "unique_combination": ["columns"],
            "accepted_values": ["column", "accepted_values"],
            "range_check": ["column"],
            "regex_check": ["column", "pattern"],
            "row_count_min": ["min_count"],
            "row_count_between": ["min_count", "max_count"],
            "freshness_check": ["column", "max_age_days"],
        }[rule_type]
        missing_keys = [k for k in required if k not in rule]
        if missing_keys:
            base["message"] = f"Missing required keys: {', '.join(missing_keys)}"
            results.append(base)
            continue
        cols_to_check = rule.get("columns") or ([rule["column"]] if "column" in rule else [])
        missing_cols = [c for c in cols_to_check if c not in getattr(df, "columns", [])]
        if missing_cols:
            base["message"] = f"Missing required column(s): {', '.join(missing_cols)}"
            results.append(base)
            continue

        try:
            failed_count, total_count, threshold, msg = (_pandas_rule(df, rule, row_count) if resolved_engine == "pandas" else _spark_rule(df, rule, row_count))
        except ValueError as exc:
            base["message"] = str(exc)
            results.append(base)
            continue
        if sev_msg:
            msg = f"{msg}. {sev_msg}"
        results.append(_result_from_counts(rule, severity, failed_count, total_count, threshold, msg))

    blocking = any(r["status"] == "failed" and r["action"] == "block" for r in results)
    warning = any(r["status"] == "failed" and r["action"] == "warn" for r in results)
    status = "failed" if blocking else "warning" if warning else "passed"
    summary = {
        "total_rules": len(results),
        "passed_rules": sum(1 for r in results if r["status"] == "passed"),
        "failed_rules": sum(1 for r in results if r["status"] == "failed"),
        "skipped_rules": sum(1 for r in results if r["status"] == "skipped"),
    }
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "engine": resolved_engine,
        "status": status,
        "can_continue": not blocking,
        "results": _to_jsonable(results),
        "summary": _to_jsonable(summary),
        "generated_at": _now_iso(),
    }


def assert_quality_gate(result: dict, fail_on: str = "critical") -> None:
    """Assert quality gate.

    Run `assert_quality_gate`.

    Parameters
    ----------
    result : dict
        Parameter `result`.
    fail_on : str, optional
        Parameter `fail_on`.

    Returns
    -------
    result : None
        Return value from `assert_quality_gate`.

    Raises
    ------
    DataQualityError
        Raised when input validation or runtime checks fail.
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> assert_quality_gate(result, fail_on)
    """
    if fail_on != "critical":
        raise ValueError("Only fail_on='critical' is supported in MVP")
    if not result.get("can_continue", True):
        raise DataQualityError("Data quality gate failed due to critical rule failures.")


def build_quality_result_records(result: dict, *, run_id: str) -> list[dict]:
    """Build quality result records.

    Run `build_quality_result_records`.

    Parameters
    ----------
    result : dict
        Parameter `result`.
    run_id : str
        Parameter `run_id`.

    Returns
    -------
    result : list[dict]
        Return value from `build_quality_result_records`.

    Examples
    --------
    >>> build_quality_result_records(result, run_id)
    """
    rows = []
    for r in result.get("results", []):
        rows.append(
            {
                "run_id": run_id,
                "dataset_name": result.get("dataset_name"),
                "table_name": result.get("table_name"),
                "engine": result.get("engine"),
                "overall_status": result.get("status"),
                "can_continue": result.get("can_continue"),
                "rule_id": r.get("rule_id"),
                "rule_type": r.get("rule_type"),
                "column_name": r.get("column_name"),
                "columns": _to_jsonable(r.get("columns")),
                "severity": r.get("severity"),
                "status": r.get("status"),
                "action": r.get("action"),
                "failed_count": r.get("failed_count"),
                "total_count": r.get("total_count"),
                "failed_pct": r.get("failed_pct"),
                "threshold": _to_jsonable(r.get("threshold")),
                "message": r.get("message"),
                "reason": r.get("reason"),
                "generated_at": result.get("generated_at"),
            }
        )
    return _to_jsonable(rows)


# --- merged from dq.py ---


import importlib.util



def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_rule_id(rule: dict[str, Any]) -> str:
    return str(rule.get("rule_id") or rule.get("name") or "DQ_RULE")






def _fabric_ai_dependencies_available() -> bool:
    return importlib.util.find_spec("openai") is not None and importlib.util.find_spec("pydantic") is not None



def _extract_fabric_ai_response_payload(ai_response):
    import pandas as pd

    if isinstance(ai_response, (str, list)):
        return ai_response
    if isinstance(ai_response, dict):
        return ai_response.get("response") or ai_response.get("generated_response") or ai_response.get("text") or ai_response
    if isinstance(ai_response, pd.DataFrame):
        if ai_response.empty:
            return "[]"
        row = ai_response.iloc[0].to_dict()
        for key in ("response", "generated_response", "text"):
            val = row.get(key)
            if isinstance(val, (str, list, dict)):
                return val
        for val in row.values():
            if isinstance(val, str):
                return val
            if isinstance(val, list):
                return val
        return row
    return ai_response

def generate_dq_rule_candidates_with_fabric_ai(
    profile,
    contract=None,
    business_context=None,
    dataset_name=None,
    table_name=None,
    response_format=None,
) -> list[dict]:
    """Generate dq rule candidates with fabric ai.

    Run `generate_dq_rule_candidates_with_fabric_ai`.

    Parameters
    ----------
    profile : Any
        Parameter `profile`.
    contract : object, optional
        Parameter `contract`.
    business_context : object, optional
        Parameter `business_context`.
    dataset_name : object, optional
        Parameter `dataset_name`.
    table_name : object, optional
        Parameter `table_name`.
    response_format : object, optional
        Parameter `response_format`.

    Returns
    -------
    result : list[dict]
        Return value from `generate_dq_rule_candidates_with_fabric_ai`.

    Raises
    ------
    RuntimeError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> generate_dq_rule_candidates_with_fabric_ai(profile, contract)
    """
    import pandas as pd

    if not _fabric_ai_dependencies_available():
        raise RuntimeError(
            "Fabric AI candidate generation requires Microsoft Fabric AI functions plus openai/pydantic runtime dependencies. "
            "Install the fabric-ai extra or run %pip install openai pydantic in the Fabric notebook."
        )

    prompt = build_quality_rule_generation_prompt(
        profile=profile,
        contract=contract,
        business_context=business_context,
        table_name=table_name,
        dataset_name=dataset_name,
    )
    prompt_df = pd.DataFrame([{"prompt": prompt}])
    ai = getattr(prompt_df, "ai", None)
    if ai is None or not hasattr(ai, "generate_response"):
        raise RuntimeError(
            "Fabric AI candidate generation requires Microsoft Fabric AI functions plus openai/pydantic runtime dependencies. "
            "Install the fabric-ai extra or run %pip install openai pydantic in the Fabric notebook."
        )

    kwargs = {"prompt": prompt}
    if response_format is not None:
        kwargs["response_format"] = response_format
    ai_response = ai.generate_response(**kwargs)
    raw_response = _extract_fabric_ai_response_payload(ai_response)

    parsed = parse_ai_quality_rule_candidates(raw_response)
    out = []
    for c in parsed.get("candidates", []):
        rule = {
            "rule_id": c.get("rule_id") or c.get("name"),
            "table_name": table_name,
            "column": c.get("column"),
            "columns": c.get("columns"),
            "rule_type": c.get("rule_type"),
            "severity": c.get("severity", "warning"),
            "description": c.get("layman_rule") or c.get("reason"),
            "generated_by": "fabric_ai",
            "status": "candidate",
        }
        cfg = c.get("rule_config") or {}
        if isinstance(cfg, dict):
            rule.update(cfg)
        out.append(normalize_dq_rule(rule))
    return out
def generate_dq_rule_candidates(
    profile: dict,
    metadata: dict | None = None,
    business_context: str | dict | None = None,
    dataset_name: str | None = None,
    table_name: str | None = None,
) -> list[dict]:
    """Generate dq rule candidates.

    Run `generate_dq_rule_candidates`.

    Parameters
    ----------
    profile : dict
        Parameter `profile`.
    metadata : dict | None, optional
        Parameter `metadata`.
    business_context : str | dict | None, optional
        Parameter `business_context`.
    dataset_name : str | None, optional
        Parameter `dataset_name`.
    table_name : str | None, optional
        Parameter `table_name`.

    Returns
    -------
    result : list[dict]
        Return value from `generate_dq_rule_candidates`.

    Examples
    --------
    >>> generate_dq_rule_candidates(profile, metadata)
    """
    profile = profile or {}
    metadata = metadata or {}
    candidates: list[dict[str, Any]] = []
    for col in profile.get("columns", []):
        if not isinstance(col, dict):
            continue
        column = col.get("column_name") or col.get("column")
        if not column:
            continue
        null_count = col.get("null_count")
        row_count = profile.get("row_count")
        if isinstance(null_count, int) and isinstance(row_count, int) and row_count > 0 and null_count == 0:
            candidates.append({"rule_id": f"{column}_not_null", "column": column, "rule_type": "not_null", "severity": "warning", "description": f"{column} should not be null"})
        distinct_count = col.get("distinct_count")
        if isinstance(distinct_count, int) and isinstance(row_count, int) and row_count > 0 and distinct_count == row_count:
            candidates.append({"rule_id": f"{column}_unique", "column": column, "rule_type": "unique", "severity": "warning", "description": f"{column} should be unique"})

    if metadata.get("ai_response"):
        parsed = parse_ai_quality_rule_candidates(metadata["ai_response"])
        for candidate in parsed.get("candidates", []):
            rule = {"rule_id": candidate.get("rule_id") or candidate.get("name"), "column": candidate.get("column"), "columns": candidate.get("columns"), "rule_type": candidate.get("rule_type"), "severity": candidate.get("severity", "warning"), "description": candidate.get("layman_rule") or candidate.get("reason")}
            cfg = candidate.get("rule_config") or {}
            if isinstance(cfg, dict):
                rule.update(cfg)
            candidates.append(rule)

    out = []
    for c in candidates:
        n = normalize_dq_rule(c)
        n.setdefault("dataset_name", dataset_name or profile.get("dataset_name"))
        n.setdefault("table_name", table_name or profile.get("table_name"))
        n.setdefault("business_context", business_context)
        out.append(n)
    return out


def normalize_dq_rule(rule: dict) -> dict:
    """Normalize dq rule.

    Run `normalize_dq_rule`.

    Parameters
    ----------
    rule : dict
        Parameter `rule`.

    Returns
    -------
    result : dict
        Return value from `normalize_dq_rule`.

    Examples
    --------
    >>> normalize_dq_rule(rule)
    """
    r = dict(rule or {})
    if "rule_id" not in r:
        r["rule_id"] = r.get("id") or r.get("name") or "DQ_RULE"
    if "table_name" not in r and r.get("table"):
        r["table_name"] = r.get("table")
    if "column" not in r and r.get("field"):
        r["column"] = r.get("field")
    if "accepted_values" not in r:
        if r.get("allowed") is not None:
            r["accepted_values"] = r.get("allowed")
        elif r.get("allowed_values") is not None:
            r["accepted_values"] = r.get("allowed_values")
        elif r.get("values") is not None:
            r["accepted_values"] = r.get("values")
    if "min_value" not in r and "min" in r:
        r["min_value"] = r.get("min")
    if "max_value" not in r and "max" in r:
        r["max_value"] = r.get("max")

    alias = {
        "min_value": "range_check",
        "max_value": "range_check",
        "between": "range_check",
        "in_set": "accepted_values",
        "allowed_values": "accepted_values",
        "not_empty": "not_null",
    }
    rtype = str(r.get("rule_type") or "").strip().lower()
    if not rtype:
        if "min_value" in r or "max_value" in r:
            rtype = "range_check"
    r["rule_type"] = alias.get(rtype, rtype)

    r["severity"] = str(r.get("severity") or "warning").lower()
    r["status"] = str(r.get("status") or "candidate").lower()
    r["generated_by"] = r.get("generated_by") or "framework"
    if not r.get("description"):
        desc_col = r.get("column") or ",".join(r.get("columns") or []) or "dataset"
        r["description"] = f"{r.get('rule_type') or 'rule'} check for {desc_col}"
    return r


def normalize_dq_rules(rules: list[dict] | None) -> list[dict]:
    """Normalize dq rules.

    Run `normalize_dq_rules`.

    Parameters
    ----------
    rules : list[dict] | None
        Parameter `rules`.

    Returns
    -------
    result : list[dict]
        Return value from `normalize_dq_rules`.

    Examples
    --------
    >>> normalize_dq_rules(rules)
    """
    return [normalize_dq_rule(r) for r in (rules or [])]


def build_dq_rule_records(rules: list[dict], dataset_name: str, table_name: str, run_id: str | None = None, status: str = "candidate", generated_by: str = "framework") -> list[dict]:
    """Build dq rule records.

    Run `build_dq_rule_records`.

    Parameters
    ----------
    rules : list[dict]
        Parameter `rules`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    run_id : str | None, optional
        Parameter `run_id`.
    status : str, optional
        Parameter `status`.
    generated_by : str, optional
        Parameter `generated_by`.

    Returns
    -------
    result : list[dict]
        Return value from `build_dq_rule_records`.

    Examples
    --------
    >>> build_dq_rule_records(rules, dataset_name)
    """
    created_at = _now_iso()
    rows = []
    for rule in normalize_dq_rules(rules):
        stored_status = rule.get("status")
        if not stored_status or stored_status == "candidate":
            stored_status = status
        rule_for_json = dict(rule)
        rule_for_json["status"] = stored_status
        rows.append({
            "rule_id": _build_rule_id(rule_for_json), "dataset_name": dataset_name, "table_name": table_name,
            "source_table": rule_for_json.get("source_table") or table_name, "column": rule_for_json.get("column"), "rule_type": rule_for_json.get("rule_type"),
            "description": rule_for_json.get("description"), "severity": rule_for_json.get("severity", "warning"), "status": stored_status,
            "generated_by": rule_for_json.get("generated_by", generated_by), "approved_by": rule_for_json.get("approved_by"), "approved_at": rule_for_json.get("approved_at"),
            "run_id": run_id, "rule_json": json.dumps(rule_for_json, ensure_ascii=False), "created_at": created_at,
        })
    return rows


def store_dq_rules(spark, rules: list[dict], table_name: str, dataset_name: str | None = None, source_table: str | None = None, run_id: str | None = None, status: str = "candidate", generated_by: str = "framework", mode: str = "append") -> list[dict]:
    """Store dq rules.

    Run `store_dq_rules`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    rules : list[dict]
        Parameter `rules`.
    table_name : str
        Parameter `table_name`.
    dataset_name : str | None, optional
        Parameter `dataset_name`.
    source_table : str | None, optional
        Parameter `source_table`.
    run_id : str | None, optional
        Parameter `run_id`.
    status : str, optional
        Parameter `status`.
    generated_by : str, optional
        Parameter `generated_by`.
    mode : str, optional
        Parameter `mode`.

    Returns
    -------
    result : list[dict]
        Return value from `store_dq_rules`.

    Examples
    --------
    >>> store_dq_rules(spark, rules)
    """
    ds = dataset_name or "unknown"
    st = source_table or "unknown"
    records = build_dq_rule_records(rules, dataset_name=ds, table_name=st, run_id=run_id, status=status, generated_by=generated_by)
    if records:
        spark.createDataFrame(records).write.mode(mode).saveAsTable(table_name)
    return records


def load_dq_rules(spark, table_name: str, dataset_name: str | None = None, source_table: str | None = None, status: str | list[str] = "approved") -> list[dict]:
    """Load dq rules.

    Run `load_dq_rules`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    table_name : str
        Parameter `table_name`.
    dataset_name : str | None, optional
        Parameter `dataset_name`.
    source_table : str | None, optional
        Parameter `source_table`.
    status : str | list[str], optional
        Parameter `status`.

    Returns
    -------
    result : list[dict]
        Return value from `load_dq_rules`.

    Examples
    --------
    >>> load_dq_rules(spark, table_name)
    """
    rows = spark.table(table_name)
    if dataset_name is not None:
        rows = rows[rows["dataset_name"] == dataset_name] if hasattr(rows, "__getitem__") and "dataset_name" in rows.columns else rows
    if source_table is not None:
        for col in ("table_name", "source_table"):
            if hasattr(rows, "columns") and col in rows.columns:
                rows = rows[rows[col] == source_table]
                break
    statuses = [status] if isinstance(status, str) else list(status)
    if statuses and hasattr(rows, "columns") and "status" in rows.columns:
        rows = rows[rows["status"].isin(statuses)]
    records = rows.to_dict(orient="records") if hasattr(rows, "to_dict") else [r.asDict() for r in rows.collect()]

    rules = []
    for row in records:
        raw = row.get("rule_json")
        if raw:
            try:
                parsed = json.loads(raw) if isinstance(raw, str) else raw
                if isinstance(parsed, dict):
                    rules.append(normalize_dq_rule(parsed)); continue
            except Exception:
                pass
        rules.append(normalize_dq_rule(row))
    return rules


def run_dq_rules(df, rules: list[dict], dataset_name: str, table_name: str, engine: str = "spark", fail_on: str = "critical") -> dict:
    """Run dq rules.

    Run `run_dq_rules`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    rules : list[dict]
        Parameter `rules`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    engine : str, optional
        Parameter `engine`.
    fail_on : str, optional
        Parameter `fail_on`.

    Returns
    -------
    result : dict
        Return value from `run_dq_rules`.

    Examples
    --------
    >>> run_dq_rules(df, rules)
    """
    normalized = normalize_dq_rules(rules)
    result = run_quality_rules(df, normalized, dataset_name=dataset_name, table_name=table_name, engine=engine)
    supported = sorted(SUPPORTED_RULE_TYPES)
    for r in result.get("results", []):
        rule = next((x for x in normalized if x.get("rule_id") == r.get("rule_id")), None)
        if not rule:
            continue
        rtype = rule.get("rule_type")
        severity = str(rule.get("severity", "warning")).lower()
        if rtype not in SUPPORTED_RULE_TYPES:
            if severity == "critical":
                r.update({"status": "failed", "action": "block", "message": f"Unsupported critical rule_type '{rtype}'. Supported rule types: {supported}"})
                result["can_continue"] = False
                result["status"] = "failed"
            elif severity == "warning":
                r.update({"status": "skipped", "action": "warn", "message": f"Unsupported warning rule_type '{rtype}'. Supported rule types: {supported}"})
            else:
                r.update({"status": "skipped", "action": "allow", "message": f"Unsupported info rule_type '{rtype}'. Supported rule types: {supported}"})
    return result


def run_dq_workflow(spark, df, quality_contract, dataset_name: str, table_name: str, run_id: str | None = None, profile: dict | None = None, metadata: dict | None = None, business_context: str | dict | None = None, engine: str = "spark") -> dict:
    """Run dq workflow.

    Run `run_dq_workflow`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    df : Any
        Parameter `df`.
    quality_contract : Any
        Parameter `quality_contract`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    run_id : str | None, optional
        Parameter `run_id`.
    profile : dict | None, optional
        Parameter `profile`.
    metadata : dict | None, optional
        Parameter `metadata`.
    business_context : str | dict | None, optional
        Parameter `business_context`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `run_dq_workflow`.

    Examples
    --------
    >>> run_dq_workflow(spark, df)
    """
    qc = quality_contract
    explicit_rules = list(getattr(qc, "rules", None) or (qc.get("rules") if isinstance(qc, dict) else []) or [])
    loaded_rules: list[dict] = []
    generated_candidates: list[dict] = []
    stored_candidate_records: list[dict] = []

    use_store = bool(getattr(qc, "use_rule_store", False) if not isinstance(qc, dict) else qc.get("use_rule_store", False))
    rule_store_table = getattr(qc, "rule_store_table", None) if not isinstance(qc, dict) else qc.get("rule_store_table")
    rule_status = getattr(qc, "rule_status", "approved") if not isinstance(qc, dict) else qc.get("rule_status", "approved")
    generate_candidates = bool(getattr(qc, "generate_candidates", False) if not isinstance(qc, dict) else qc.get("generate_candidates", False))
    candidate_generation_method = getattr(qc, "candidate_generation_method", "profile") if not isinstance(qc, dict) else qc.get("candidate_generation_method", "profile")
    fail_on = getattr(qc, "fail_on", "critical") if not isinstance(qc, dict) else qc.get("fail_on", "critical")

    if use_store and rule_store_table:
        loaded_rules = load_dq_rules(spark, rule_store_table, dataset_name=dataset_name, source_table=table_name, status=rule_status)

    if generate_candidates:
        if str(candidate_generation_method).lower() == "fabric_ai":
            generated_candidates = generate_dq_rule_candidates_with_fabric_ai(
                profile=profile or {},
                contract=getattr(qc, "__dict__", qc),
                business_context=business_context,
                dataset_name=dataset_name,
                table_name=table_name,
            )
        else:
            generated_candidates = generate_dq_rule_candidates(profile or {}, metadata=metadata, business_context=business_context, dataset_name=dataset_name, table_name=table_name)
        if rule_store_table:
            stored_candidate_records = store_dq_rules(spark, generated_candidates, rule_store_table, dataset_name=dataset_name, source_table=table_name, run_id=run_id, status="candidate")

    combined = []
    seen = set()
    for r in [*explicit_rules, *loaded_rules]:
        nr = normalize_dq_rule(r)
        rid = nr.get("rule_id")
        if rid and rid in seen:
            continue
        if rid:
            seen.add(rid)
        combined.append(nr)

    quality_result = run_dq_rules(df, combined, dataset_name=dataset_name, table_name=table_name, engine=engine, fail_on=fail_on)
    gate_passed = True
    gate_error = None
    try:
        assert_quality_gate(quality_result, fail_on=fail_on)
    except Exception as exc:
        gate_passed = False
        gate_error = str(exc)

    return {
        "rules": combined,
        "generated_candidates": generated_candidates,
        "stored_candidate_records": stored_candidate_records,
        "loaded_rules": loaded_rules,
        "quality_result": quality_result,
        "gate_passed": gate_passed,
        "gate_error": gate_error,
        "rule_store_table": rule_store_table,
        "enforceable_rule_count": len(combined),
    }


# --- merged from contracts.py ---
"""Runtime contract validation helpers for pandas and Spark dataframes."""


from datetime import datetime, timedelta, timezone


from fabric_data_product_framework.runtime import detect_dataframe_engine, validate_engine

SEVERITY_TO_ACTION = {"info": "warn", "warning": "warn", "critical": "block"}


class ContractValidationError(Exception):
    """Contractvalidationerror.

    Public class used by the framework API for `ContractValidationError`.

    Examples
    --------
    >>> ContractValidationError(... )
    """


def _json_safe(value: Any) -> Any:
    if isinstance(value, (datetime, pd.Timestamp, timedelta)):
        return value.isoformat() if hasattr(value, "isoformat") else str(value)
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    return value


def _resolve_engine(df: Any, engine: str) -> str:
    normalized = validate_engine(engine)
    return detect_dataframe_engine(df) if normalized == "auto" else normalized


def _action_for(status: str, severity: str) -> str:
    if status in {"passed", "skipped"}:
        return "allow"
    return SEVERITY_TO_ACTION.get(severity, "block")


def _parse_freshness_timedelta(value: str | None) -> timedelta | None:
    if not value:
        return None
    m = re.match(r"^\s*(\d+)\s*(day|days|hour|hours)\s*$", str(value).strip().lower())
    if not m:
        return None
    qty, unit = int(m.group(1)), m.group(2)
    return timedelta(days=qty) if unit.startswith("day") else timedelta(hours=qty)


def validate_required_columns(df, expected_columns: list[str], *, dataset_name: str = "unknown", table_name: str = "unknown", check_name: str = "required_columns", severity: str = "critical", engine: str = "auto") -> dict:
    """Validate required columns.

    Run `validate_required_columns`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    expected_columns : list[str]
        Parameter `expected_columns`.
    dataset_name : str, optional
        Parameter `dataset_name`.
    table_name : str, optional
        Parameter `table_name`.
    check_name : str, optional
        Parameter `check_name`.
    severity : str, optional
        Parameter `severity`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `validate_required_columns`.

    Examples
    --------
    >>> validate_required_columns(df, expected_columns)
    """
    resolved = _resolve_engine(df, engine)
    actual_columns = list(df.columns) if resolved in {"pandas", "spark"} else []
    missing = [c for c in expected_columns if c not in actual_columns]
    extra = [c for c in actual_columns if c not in expected_columns]
    status = "failed" if missing else "passed"
    message = f"Missing required columns: {missing}" if missing else "All required columns are present"
    return {"dataset_name": dataset_name, "table_name": table_name, "check_name": check_name, "check_type": "required_columns", "severity": severity, "status": status, "action": _action_for(status, severity), "expected": expected_columns, "actual": actual_columns, "missing": missing, "extra": extra, "message": message}


def validate_grain(df, business_keys: list[str], *, dataset_name: str = "unknown", table_name: str = "unknown", severity: str = "critical", engine: str = "auto") -> dict:
    """Validate grain.

    Run `validate_grain`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    business_keys : list[str]
        Parameter `business_keys`.
    dataset_name : str, optional
        Parameter `dataset_name`.
    table_name : str, optional
        Parameter `table_name`.
    severity : str, optional
        Parameter `severity`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `validate_grain`.

    Examples
    --------
    >>> validate_grain(df, business_keys)
    """
    resolved = _resolve_engine(df, engine)
    missing = [k for k in business_keys if k not in getattr(df, "columns", [])]
    if missing:
        return {"dataset_name": dataset_name, "table_name": table_name, "check_name": "grain", "check_type": "grain", "severity": severity, "status": "failed", "action": _action_for("failed", severity), "business_keys": business_keys, "duplicate_key_count": None, "duplicate_row_count": None, "duplicate_count": None, "message": f"Missing business key columns: {missing}"}

    if resolved == "pandas":
        grouped = df.groupby(business_keys, dropna=False).size()
        duplicate_key_count = int((grouped > 1).sum())
        duplicate_row_count = int(grouped[grouped > 1].sum()) if duplicate_key_count else 0
    else:
        from pyspark.sql import functions as F

        dup_groups = df.groupBy(business_keys).count().filter(F.col("count") > 1)
        duplicate_key_count = int(dup_groups.count())
        duplicate_row_count = int(dup_groups.agg(F.sum("count").alias("dup_rows")).collect()[0]["dup_rows"] or 0)

    status = "failed" if duplicate_row_count > 0 else "passed"
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "check_name": "grain",
        "check_type": "grain",
        "severity": severity,
        "status": status,
        "action": _action_for(status, severity),
        "business_keys": business_keys,
        "duplicate_key_count": duplicate_key_count,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_count": duplicate_row_count,
        "message": "Business grain is unique" if status == "passed" else f"Found duplicate business keys: keys={duplicate_key_count}, rows={duplicate_row_count}",
    }


def validate_freshness(df, watermark_column: str, *, max_age_days: int | None = None, max_age_timedelta: timedelta | None = None, dataset_name: str = "unknown", table_name: str = "unknown", severity: str = "critical", engine: str = "auto") -> dict:
    """Validate freshness.

    Run `validate_freshness`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    watermark_column : str
        Parameter `watermark_column`.
    max_age_days : int | None, optional
        Parameter `max_age_days`.
    max_age_timedelta : timedelta | None, optional
        Parameter `max_age_timedelta`.
    dataset_name : str, optional
        Parameter `dataset_name`.
    table_name : str, optional
        Parameter `table_name`.
    severity : str, optional
        Parameter `severity`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `validate_freshness`.

    Examples
    --------
    >>> validate_freshness(df, watermark_column)
    """
    resolved = _resolve_engine(df, engine)
    threshold = max_age_timedelta if max_age_timedelta is not None else (timedelta(days=max_age_days) if max_age_days is not None else None)
    if threshold is None:
        return {"dataset_name": dataset_name, "table_name": table_name, "check_name": "freshness", "check_type": "freshness", "severity": severity, "status": "skipped", "action": "allow", "watermark_column": watermark_column, "max_watermark": None, "max_age_days": None, "max_age_timedelta": None, "message": "Freshness threshold not configured; check skipped"}
    if watermark_column not in getattr(df, "columns", []):
        return {"dataset_name": dataset_name, "table_name": table_name, "check_name": "freshness", "check_type": "freshness", "severity": severity, "status": "failed", "action": _action_for("failed", severity), "watermark_column": watermark_column, "max_watermark": None, "max_age_days": max_age_days, "max_age_timedelta": str(threshold), "message": f"Missing watermark column: {watermark_column}"}
    if resolved == "pandas":
        ts = pd.to_datetime(df[watermark_column], errors="coerce", utc=True).dropna()
        max_watermark = ts.max().to_pydatetime() if not ts.empty else None
    else:
        from pyspark.sql import functions as F

        max_watermark = df.select(F.max(F.col(watermark_column)).alias("max_ts")).collect()[0]["max_ts"]
        if max_watermark is not None and max_watermark.tzinfo is None:
            max_watermark = max_watermark.replace(tzinfo=timezone.utc)
    if max_watermark is None:
        status, msg = "failed", "No valid watermark values found"
    else:
        age = datetime.now(timezone.utc) - max_watermark
        status = "passed" if age <= threshold else "failed"
        msg = f"Latest watermark age {age} is within threshold {threshold}" if status == "passed" else f"Latest watermark age {age} exceeds threshold {threshold}"
    return {"dataset_name": dataset_name, "table_name": table_name, "check_name": "freshness", "check_type": "freshness", "severity": severity, "status": status, "action": _action_for(status, severity), "watermark_column": watermark_column, "max_watermark": _json_safe(max_watermark), "max_age_days": max_age_days, "max_age_timedelta": str(threshold), "message": msg}


def _combine_contract_checks(dataset_name: str, table_name: str, contract_type: str, checks: list[dict]) -> dict:
    statuses = [c.get("status") for c in checks]
    failed_blocking = [c for c in checks if c.get("status") == "failed" and c.get("action") == "block"]
    status = "failed" if failed_blocking else ("warning" if "failed" in statuses or "warning" in statuses else "passed")
    return {"dataset_name": dataset_name, "table_name": table_name, "contract_type": contract_type, "status": status, "can_continue": not failed_blocking, "checks": checks}


def validate_upstream_contract(df, contract: dict, *, dataset_name: str | None = None, table_name: str | None = None, engine: str = "auto") -> dict:
    """Validate upstream contract.

    Run `validate_upstream_contract`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    contract : dict
        Parameter `contract`.
    dataset_name : str | None, optional
        Parameter `dataset_name`.
    table_name : str | None, optional
        Parameter `table_name`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `validate_upstream_contract`.

    Examples
    --------
    >>> validate_upstream_contract(df, contract)
    """
    dataset_name = dataset_name or contract.get("dataset", {}).get("name", "unknown")
    table_name = table_name or contract.get("source", {}).get("table", "unknown")
    up = contract.get("contracts", {}).get("upstream", {})
    checks = [validate_required_columns(df, up.get("expected_columns", []), dataset_name=dataset_name, table_name=table_name, severity="critical", engine=engine)]
    freshness_td = _parse_freshness_timedelta(up.get("expected_freshness"))
    watermark_column = contract.get("refresh", {}).get("watermark_column")
    if watermark_column:
        checks.append(validate_freshness(df, watermark_column, max_age_timedelta=freshness_td, dataset_name=dataset_name, table_name=table_name, severity="warning" if freshness_td is None else "critical", engine=engine))
    return _combine_contract_checks(dataset_name, table_name, "upstream", checks)


def validate_downstream_contract(df, contract: dict, *, dataset_name: str | None = None, table_name: str | None = None, engine: str = "auto") -> dict:
    """Validate downstream contract.

    Run `validate_downstream_contract`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    contract : dict
        Parameter `contract`.
    dataset_name : str | None, optional
        Parameter `dataset_name`.
    table_name : str | None, optional
        Parameter `table_name`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `validate_downstream_contract`.

    Examples
    --------
    >>> validate_downstream_contract(df, contract)
    """
    dataset_name = dataset_name or contract.get("dataset", {}).get("name", "unknown")
    table_name = table_name or contract.get("target", {}).get("table", "unknown")
    down = contract.get("contracts", {}).get("downstream", {})
    checks = [validate_required_columns(df, down.get("guaranteed_columns", []), dataset_name=dataset_name, table_name=table_name, severity="critical", engine=engine), validate_grain(df, contract.get("keys", {}).get("business_keys", []), dataset_name=dataset_name, table_name=table_name, severity="critical", engine=engine)]
    return _combine_contract_checks(dataset_name, table_name, "downstream", checks)


def validate_runtime_contracts(*, source_df=None, output_df=None, contract: dict, engine: str = "auto") -> dict:
    """Validate runtime contracts.

    Run `validate_runtime_contracts`.

    Parameters
    ----------
    source_df : object, optional
        Parameter `source_df`.
    output_df : object, optional
        Parameter `output_df`.
    contract : dict
        Parameter `contract`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `validate_runtime_contracts`.

    Examples
    --------
    >>> validate_runtime_contracts(source_df, output_df)
    """
    results = []
    if source_df is not None:
        results.append(validate_upstream_contract(source_df, contract, engine=engine))
    if output_df is not None:
        results.append(validate_downstream_contract(output_df, contract, engine=engine))
    all_checks = [c for r in results for c in r.get("checks", [])]
    failed = sum(1 for c in all_checks if c.get("status") == "failed")
    warnings = sum(1 for c in all_checks if c.get("status") == "warning")
    passed = sum(1 for c in all_checks if c.get("status") in {"passed", "skipped"})
    blocking = sum(1 for c in all_checks if c.get("status") == "failed" and c.get("action") == "block")
    status = "failed" if any(not r.get("can_continue", True) for r in results) else ("warning" if warnings > 0 else "passed")
    return {"dataset_name": contract.get("dataset", {}).get("name", "unknown"), "status": status, "can_continue": blocking == 0, "results": results, "summary": {"passed_checks": passed, "warning_checks": warnings, "failed_checks": failed, "blocking_check_count": blocking}}


def assert_contracts_valid(result: dict) -> None:
    """Assert contracts valid.

    Run `assert_contracts_valid`.

    Parameters
    ----------
    result : dict
        Parameter `result`.

    Returns
    -------
    result : None
        Return value from `assert_contracts_valid`.

    Raises
    ------
    ContractValidationError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> assert_contracts_valid(result)
    """
    if not result.get("can_continue", False):
        raise ContractValidationError("Contract validation returned blocking failures")


def build_contract_validation_records(result: dict, *, run_id: str) -> list[dict]:
    """Build contract validation records.

    Run `build_contract_validation_records`.

    Parameters
    ----------
    result : dict
        Parameter `result`.
    run_id : str
        Parameter `run_id`.

    Returns
    -------
    result : list[dict]
        Return value from `build_contract_validation_records`.

    Examples
    --------
    >>> build_contract_validation_records(result, run_id)
    """
    records: list[dict] = []
    for section in result.get("results", []):
        for check in section.get("checks", []):
            records.append(_json_safe({"run_id": run_id, "dataset_name": result.get("dataset_name"), "contract_type": section.get("contract_type"), "table_name": section.get("table_name"), "overall_status": section.get("status"), "can_continue": section.get("can_continue"), "check_name": check.get("check_name"), "check_type": check.get("check_type"), "severity": check.get("severity"), "status": check.get("status"), "action": check.get("action"), "expected": check.get("expected"), "actual": check.get("actual"), "missing": check.get("missing"), "extra": check.get("extra"), "message": check.get("message")}))
    return records


# --- merged from data_contract.py ---


from dataclasses import asdict, dataclass, field
from pathlib import Path

from fabric_data_product_framework.config import load_dataset_contract
from fabric_data_product_framework.drift import (
    build_and_write_partition_snapshot,
    build_and_write_schema_snapshot,
    check_partition_drift,
    check_schema_drift,
    load_latest_partition_snapshot,
    load_latest_schema_snapshot,
    summarize_drift_results,
)
from fabric_data_product_framework.lineage import build_lineage_records
from fabric_data_product_framework.metadata import build_dataset_run_record, write_metadata_records
from fabric_data_product_framework.profiling import flatten_profile_for_metadata, profile_dataframe
from fabric_data_product_framework.governance import (
    build_governance_classification_records,
    classify_columns,
    summarize_governance_classifications,
    write_governance_classifications,
)
from fabric_data_product_framework.run_summary import build_run_summary, build_run_summary_record
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.technical_columns import add_audit_columns, add_hash_columns, default_technical_columns

_ALLOWED_REFRESH_MODES = {"full", "incremental", "snapshot", "append"}


@dataclass
class SourceContract:
    """Sourcecontract.

    Public class used by the framework API for `SourceContract`.

    Examples
    --------
    >>> SourceContract(... )
    """
    name: str | None = None
    type: str = "table"
    table: str | None = None
    path: str | None = None
    format: str = "delta"
    required_columns: list[str] = field(default_factory=list)
    business_keys: list[str] = field(default_factory=list)
    watermark_column: str | None = None
    partition_column: str | None = None
    read_options: dict[str, Any] = field(default_factory=dict)


@dataclass
class TargetContract:
    """Targetcontract.

    Public class used by the framework API for `TargetContract`.

    Examples
    --------
    >>> TargetContract(... )
    """
    table: str | None = None
    path: str | None = None
    format: str = "delta"
    mode: str = "append"
    partition_column: str | None = None
    required_columns: list[str] = field(default_factory=list)
    write_options: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityContract:
    """Qualitycontract.

    Public class used by the framework API for `QualityContract`.

    Examples
    --------
    >>> QualityContract(... )
    """
    rules: list[dict[str, Any]] = field(default_factory=list)
    rule_store_table: str | None = None
    use_rule_store: bool = False
    rule_status: str = "approved"
    generate_candidates: bool = False
    candidate_generation_method: str = "profile"
    fail_on: str = "critical"
    quarantine_enabled: bool = True
    quarantine_table: str | None = None


@dataclass
class DriftContract:
    """Driftcontract.

    Public class used by the framework API for `DriftContract`.

    Examples
    --------
    >>> DriftContract(... )
    """
    schema_enabled: bool = True
    data_enabled: bool = False
    schema_policy: dict[str, Any] = field(default_factory=dict)
    data_policy: dict[str, Any] = field(default_factory=dict)
    baseline_schema_table: str | None = None
    baseline_partition_table: str | None = None


@dataclass
class GovernanceContract:
    """Governancecontract.

    Public class used by the framework API for `GovernanceContract`.

    Examples
    --------
    >>> GovernanceContract(... )
    """
    classify_columns: bool = False
    classification_table: str | None = None
    require_human_approval: bool = True
    rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MetadataContract:
    """Metadatacontract.

    Public class used by the framework API for `MetadataContract`.

    Examples
    --------
    >>> MetadataContract(... )
    """
    schema: str = "fw_metadata"
    source_profile_table: str | None = None
    output_profile_table: str | None = None
    schema_snapshot_table: str | None = None
    partition_snapshot_table: str | None = None
    quality_result_table: str | None = None
    quarantine_table: str | None = None
    contract_validation_table: str | None = None
    lineage_table: str | None = None
    run_summary_table: str | None = None
    dataset_runs_table: str | None = None
    ai_context_table: str | None = None


@dataclass
class RuntimeContract:
    """Runtimecontract.

    Public class used by the framework API for `RuntimeContract`.

    Examples
    --------
    >>> RuntimeContract(... )
    """
    dataset_name: str = ""
    environment: str = "fabric"
    notebook_name: str | None = None
    run_id_prefix: str | None = None
    pipeline_name: str | None = None
    source_system: str | None = None


@dataclass
class DataProductContract:
    """Dataproductcontract.

    Public class used by the framework API for `DataProductContract`.

    Examples
    --------
    >>> DataProductContract(... )
    """
    dataset: dict[str, Any] = field(default_factory=dict)
    source: SourceContract = field(default_factory=SourceContract)
    target: TargetContract = field(default_factory=TargetContract)
    quality: QualityContract = field(default_factory=QualityContract)
    drift: DriftContract = field(default_factory=DriftContract)
    governance: GovernanceContract = field(default_factory=GovernanceContract)
    metadata: MetadataContract = field(default_factory=MetadataContract)
    runtime: RuntimeContract = field(default_factory=RuntimeContract)
    raw: dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Any:
        return _effective_contract_dict(self)[key]


def _dict(config: dict | None) -> dict:
    """Return a dictionary or an empty default for optional config fragments."""
    return config if isinstance(config, dict) else {}


def build_source_contract(config: dict) -> SourceContract:
    """Build source contract.

    Run `build_source_contract`.

    Parameters
    ----------
    config : dict
        Parameter `config`.

    Returns
    -------
    result : SourceContract
        Return value from `build_source_contract`.

    Examples
    --------
    >>> build_source_contract(config)
    """
    c = _dict(config)
    return SourceContract(
        name=c.get("name"),
        type=str(c.get("type") or "table"),
        table=c.get("table"),
        path=c.get("path"),
        format=str(c.get("format") or "delta"),
        required_columns=list(c.get("required_columns") or []),
        business_keys=list(c.get("business_keys") or []),
        watermark_column=c.get("watermark_column"),
        partition_column=c.get("partition_column"),
        read_options=dict(c.get("read_options") or {}),
    )


def build_target_contract(config: dict) -> TargetContract:
    """Build target contract.

    Run `build_target_contract`.

    Parameters
    ----------
    config : dict
        Parameter `config`.

    Returns
    -------
    result : TargetContract
        Return value from `build_target_contract`.

    Examples
    --------
    >>> build_target_contract(config)
    """
    c = _dict(config)
    return TargetContract(
        table=c.get("table"),
        path=c.get("path"),
        format=str(c.get("format") or "delta"),
        mode=str(c.get("mode") or "append"),
        partition_column=c.get("partition_column"),
        required_columns=list(c.get("required_columns") or []),
        write_options=dict(c.get("write_options") or {}),
    )


def build_quality_contract(config: dict) -> QualityContract:
    """Build quality contract.

    Run `build_quality_contract`.

    Parameters
    ----------
    config : dict
        Parameter `config`.

    Returns
    -------
    result : QualityContract
        Return value from `build_quality_contract`.

    Examples
    --------
    >>> build_quality_contract(config)
    """
    c = _dict(config)
    return QualityContract(
        rules=list(c.get("rules") or []),
        rule_store_table=c.get("rule_store_table"),
        use_rule_store=bool(c.get("use_rule_store", False)),
        rule_status=str(c.get("rule_status") or "approved"),
        generate_candidates=bool(c.get("generate_candidates", False)),
        candidate_generation_method=str(c.get("candidate_generation_method") or "profile"),
        fail_on=str(c.get("fail_on") or "critical"),
        quarantine_enabled=bool(c.get("quarantine_enabled", True)),
        quarantine_table=c.get("quarantine_table"),
    )


def build_drift_contract(config: dict) -> DriftContract:
    """Build drift contract.

    Run `build_drift_contract`.

    Parameters
    ----------
    config : dict
        Parameter `config`.

    Returns
    -------
    result : DriftContract
        Return value from `build_drift_contract`.

    Examples
    --------
    >>> build_drift_contract(config)
    """
    c = _dict(config)
    return DriftContract(
        schema_enabled=bool(c.get("schema_enabled", True)),
        data_enabled=bool(c.get("data_enabled", False)),
        schema_policy=dict(c.get("schema_policy") or {}),
        data_policy=dict(c.get("data_policy") or {}),
        baseline_schema_table=c.get("baseline_schema_table"),
        baseline_partition_table=c.get("baseline_partition_table"),
    )


def build_governance_contract(config: dict) -> GovernanceContract:
    """Build governance contract.

    Run `build_governance_contract`.

    Parameters
    ----------
    config : dict
        Parameter `config`.

    Returns
    -------
    result : GovernanceContract
        Return value from `build_governance_contract`.

    Examples
    --------
    >>> build_governance_contract(config)
    """
    c = _dict(config)
    return GovernanceContract(
        classify_columns=bool(c.get("classify_columns", False)),
        classification_table=c.get("classification_table"),
        require_human_approval=bool(c.get("require_human_approval", True)),
        rules=list(c.get("rules") or []),
    )


def build_metadata_contract(config: dict) -> MetadataContract:
    """Build metadata contract.

    Run `build_metadata_contract`.

    Parameters
    ----------
    config : dict
        Parameter `config`.

    Returns
    -------
    result : MetadataContract
        Return value from `build_metadata_contract`.

    Examples
    --------
    >>> build_metadata_contract(config)
    """
    c = _dict(config)
    return MetadataContract(
        schema=str(c.get("schema") or "fw_metadata"),
        source_profile_table=c.get("source_profile_table"),
        output_profile_table=c.get("output_profile_table"),
        schema_snapshot_table=c.get("schema_snapshot_table"),
        partition_snapshot_table=c.get("partition_snapshot_table"),
        quality_result_table=c.get("quality_result_table"),
        quarantine_table=c.get("quarantine_table"),
        contract_validation_table=c.get("contract_validation_table"),
        lineage_table=c.get("lineage_table"),
        run_summary_table=c.get("run_summary_table"),
        dataset_runs_table=c.get("dataset_runs_table"),
        ai_context_table=c.get("ai_context_table"),
    )


def build_runtime_contract(config: dict) -> RuntimeContract:
    """Build runtime contract.

    Run `build_runtime_contract`.

    Parameters
    ----------
    config : dict
        Parameter `config`.

    Returns
    -------
    result : RuntimeContract
        Return value from `build_runtime_contract`.

    Examples
    --------
    >>> build_runtime_contract(config)
    """
    c = _dict(config)
    return RuntimeContract(
        dataset_name=str(c.get("dataset_name") or ""),
        environment=str(c.get("environment") or "fabric"),
        notebook_name=c.get("notebook_name"),
        run_id_prefix=c.get("run_id_prefix"),
        pipeline_name=c.get("pipeline_name"),
        source_system=c.get("source_system"),
    )


def normalize_data_product_contract(contract: dict | DataProductContract) -> DataProductContract:
    """Normalize data product contract.

    Run `normalize_data_product_contract`.

    Parameters
    ----------
    contract : dict | DataProductContract
        Parameter `contract`.

    Returns
    -------
    result : DataProductContract
        Return value from `normalize_data_product_contract`.

    Examples
    --------
    >>> normalize_data_product_contract(contract)
    """
    if isinstance(contract, DataProductContract):
        return contract
    raw = dict(contract)
    dataset = dict(raw.get("dataset") or {})
    upstream = _dict(raw.get("upstream_contract"))
    downstream = _dict(raw.get("downstream_contract"))

    source_cfg = dict(raw.get("source") or {})
    source_cfg.setdefault("table", upstream.get("table_name"))
    source_cfg.setdefault("required_columns", upstream.get("required_columns", (raw.get("schema") or {}).get("required_source_columns", [])))
    source_cfg.setdefault("business_keys", upstream.get("business_keys", (raw.get("keys") or {}).get("business_keys", [])))
    source_cfg.setdefault("watermark_column", upstream.get("watermark_column", (raw.get("keys") or {}).get("watermark_column")))
    source_cfg.setdefault("partition_column", (raw.get("keys") or {}).get("partition_column"))

    target_cfg = dict(raw.get("target") or {})
    target_cfg.setdefault("table", downstream.get("table_name"))
    target_cfg.setdefault("required_columns", downstream.get("required_columns", (raw.get("schema") or {}).get("required_output_columns", [])))

    metadata_cfg = dict(raw.get("metadata") or {})
    metadata_cfg.setdefault("schema", raw.get("metadata_schema") or (raw.get("environment") or {}).get("metadata_schema") or "fw_metadata")

    quality_cfg = dict(raw.get("quality") or {})
    quality_cfg.setdefault("quarantine_table", metadata_cfg.get("quarantine_table"))

    drift_raw = dict(raw.get("drift") or {})
    drift_cfg = {
        "schema_enabled": drift_raw.get("schema_enabled", True),
        "data_enabled": drift_raw.get("data_enabled", False),
        "schema_policy": drift_raw.get("schema_policy", {}),
        "data_policy": drift_raw.get("data_policy", drift_raw.get("incremental_policy", {})),
        "baseline_schema_table": drift_raw.get("baseline_schema_table"),
        "baseline_partition_table": drift_raw.get("baseline_partition_table"),
    }

    runtime_cfg = dict(raw.get("runtime") or {})
    runtime_cfg.setdefault("dataset_name", dataset.get("name", ""))
    runtime_cfg.setdefault("environment", runtime_cfg.get("environment") or (raw.get("environment") or {}).get("name") or "fabric")

    return DataProductContract(
        dataset=dataset,
        source=build_source_contract(source_cfg),
        target=build_target_contract(target_cfg),
        quality=build_quality_contract(quality_cfg),
        drift=build_drift_contract(drift_cfg),
        governance=build_governance_contract(raw.get("governance") or {}),
        metadata=build_metadata_contract(metadata_cfg),
        runtime=build_runtime_contract(runtime_cfg),
        raw=raw,
    )


def data_product_contract_to_dict(contract: DataProductContract) -> dict:
    """Data product contract to dict.

    Run `data_product_contract_to_dict`.

    Parameters
    ----------
    contract : DataProductContract
        Parameter `contract`.

    Returns
    -------
    result : dict
        Return value from `data_product_contract_to_dict`.

    Examples
    --------
    >>> data_product_contract_to_dict(contract)
    """
    return asdict(contract)


def _effective_contract_dict(contract: dict | DataProductContract) -> dict:
    n = normalize_data_product_contract(contract)
    raw = dict(n.raw) if n.raw else {}
    effective = {
        "dataset": dict(n.dataset),
        "source": asdict(n.source),
        "target": asdict(n.target),
        "quality": asdict(n.quality),
        "drift": asdict(n.drift),
        "governance": asdict(n.governance),
        "metadata": asdict(n.metadata),
        "runtime": asdict(n.runtime),
        "refresh": dict(raw.get("refresh") or {}),
    }
    effective["environment"] = dict(raw.get("environment") or {"name": n.runtime.environment, "metadata_schema": n.metadata.schema})
    effective["keys"] = {
        "business_keys": list(n.source.business_keys),
        "watermark_column": n.source.watermark_column,
        "partition_column": n.source.partition_column,
    }
    effective["schema"] = {
        "required_source_columns": list(n.source.required_columns),
        "required_output_columns": list(n.target.required_columns),
    }
    return effective


def load_data_contract(path_or_dict: str | Path | dict) -> DataProductContract:
    """Load data contract.

    Run `load_data_contract`.

    Parameters
    ----------
    path_or_dict : str | Path | dict
        Parameter `path_or_dict`.

    Returns
    -------
    result : DataProductContract
        Return value from `load_data_contract`.

    Examples
    --------
    >>> load_data_contract(path_or_dict)
    """
    raw = dict(path_or_dict) if isinstance(path_or_dict, dict) else load_dataset_contract(path_or_dict)
    return normalize_data_product_contract(raw)


def _refresh_mode(contract: dict) -> str:
    return str((contract.get("refresh") or {}).get("mode") or "full").strip().lower()


def validate_data_contract_shape(contract: dict | DataProductContract) -> list[str]:
    """Validate data contract shape.

    Run `validate_data_contract_shape`.

    Parameters
    ----------
    contract : dict | DataProductContract
        Parameter `contract`.

    Returns
    -------
    result : list[str]
        Return value from `validate_data_contract_shape`.

    Examples
    --------
    >>> validate_data_contract_shape(contract)
    """
    n = normalize_data_product_contract(contract)
    raw = _effective_contract_dict(n)
    errors: list[str] = []
    if not n.dataset.get("name"):
        errors.append("Missing required key: dataset.name")
    if not n.source.table:
        errors.append("Missing required key: source.table")
    if not n.target.table:
        errors.append("Missing required key: target.table")
    required_metadata = ["source_profile_table", "output_profile_table", "schema_snapshot_table", "partition_snapshot_table", "quality_result_table", "quarantine_table", "contract_validation_table", "lineage_table", "run_summary_table", "dataset_runs_table"]
    md = asdict(n.metadata)
    for k in required_metadata:
        if not md.get(k):
            errors.append(f"Missing required key: metadata.{k}")

    mode = _refresh_mode(raw)
    if mode not in _ALLOWED_REFRESH_MODES:
        errors.append("Invalid refresh.mode. Expected one of: full, incremental, snapshot, append")
    if mode == "incremental":
        if not n.source.partition_column:
            errors.append("Missing required key for incremental mode: source.partition_column")
        if not n.source.business_keys:
            errors.append("Incremental mode requires non-empty source.business_keys")
    return errors


def build_runtime_context_from_contract(contract: dict | DataProductContract, overrides: dict | None = None) -> dict:
    """Build runtime context from contract.

    Run `build_runtime_context_from_contract`.

    Parameters
    ----------
    contract : dict | DataProductContract
        Parameter `contract`.
    overrides : dict | None, optional
        Parameter `overrides`.

    Returns
    -------
    result : dict
        Return value from `build_runtime_context_from_contract`.

    Examples
    --------
    >>> build_runtime_context_from_contract(contract, overrides)
    """
    n = normalize_data_product_contract(contract)
    context = build_runtime_context(dataset_name=n.dataset.get("name", ""), environment=n.runtime.environment, source_table=n.source.table or "", target_table=n.target.table or "", notebook_name=n.runtime.notebook_name, run_id=(overrides or {}).get("run_id"))
    if overrides:
        context.update(overrides)
    return context

# rest unchanged helpers

def _write_records_spark(spark, records: list[dict], table: str, mode: str = "append") -> None:
    if records:
        write_metadata_records(records, table, writer=lambda rows, t, mode="append", **_: spark.createDataFrame(rows).write.mode(mode).saveAsTable(t), mode=mode)


def _write_dataframe_to_table(spark, df, table: str, mode: str = "append") -> None:
    if hasattr(df, "write"):
        df.write.mode(mode).saveAsTable(table)
    else:
        spark.createDataFrame(df.to_dict(orient="records")).write.mode(mode).saveAsTable(table)


def _runtime_validation_contract(contract: dict | DataProductContract) -> dict:
    n = normalize_data_product_contract(contract)
    effective = _effective_contract_dict(n)
    effective["contracts"] = {"upstream": {"expected_columns": n.source.required_columns}, "downstream": {"guaranteed_columns": n.target.required_columns}}
    effective["refresh"] = effective.get("refresh") or {"watermark_column": n.source.watermark_column}
    return effective


def run_data_product(spark, contract: dict | DataProductContract, transform=None, source_df=None, write: bool | None = None, *, write_target: bool = True, write_metadata: bool = True) -> dict:
    """Run data product.

    Run `run_data_product`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    contract : dict | DataProductContract
        Parameter `contract`.
    transform : object, optional
        Parameter `transform`.
    source_df : object, optional
        Parameter `source_df`.
    write : bool | None, optional
        Parameter `write`.
    write_target : bool, optional
        Parameter `write_target`.
    write_metadata : bool, optional
        Parameter `write_metadata`.

    Returns
    -------
    result : dict
        Return value from `run_data_product`.

    Examples
    --------
    >>> run_data_product(spark, contract)
    """
    n = normalize_data_product_contract(contract)
    if write is False:
        write_target = False
        write_metadata = False
    elif write is True:
        write_target = True

    shape_errors = validate_data_contract_shape(n)
    if shape_errors:
        return {"status": "failed", "can_continue": False, "errors": shape_errors}

    ctx = build_runtime_context_from_contract(n)
    dataset_name, source_table, target_table, metadata = n.dataset["name"], n.source.table, n.target.table, n.metadata
    effective_contract = _effective_contract_dict(n)
    mode = _refresh_mode(effective_contract)
    src_df = source_df if source_df is not None else spark.table(source_table)
    md = asdict(metadata)
    if mode == "incremental" and n.source.partition_column and n.source.partition_column not in getattr(src_df, "columns", []):
        return {"status": "failed", "can_continue": False, "errors": [f"Incremental partition column missing in source dataframe: {n.source.partition_column}"], "runtime_context": ctx}

    source_profile = profile_dataframe(src_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(source_profile, source_table, ctx["run_id"], "source"), md["source_profile_table"])
    schema_drift_result = {"status": "disabled", "can_continue": True}
    schema_snapshot_write = None
    schema_baseline_table = n.drift.baseline_schema_table or md.get("schema_snapshot_table")
    if n.drift.schema_enabled:
        baseline = load_latest_schema_snapshot(spark, schema_baseline_table, dataset_name=dataset_name, table_name=source_table) if schema_baseline_table else None
        schema_drift_result = check_schema_drift(
            df=src_df,
            dataset_name=dataset_name,
            table_name=source_table,
            baseline_snapshot=baseline,
            policy=n.drift.schema_policy,
            engine="auto",
        )
        if write_metadata and md.get("schema_snapshot_table"):
            schema_snapshot_write = build_and_write_schema_snapshot(
                spark=spark, df=src_df, dataset_name=dataset_name, table_name=source_table, metadata_table=md["schema_snapshot_table"], run_id=ctx["run_id"], engine="auto"
            )

    out_df = transform(src_df, ctx, effective_contract) if transform else src_df
    out_df = add_audit_columns(out_df, run_id=ctx["run_id"], pipeline_name=dataset_name, environment=ctx["environment"], source_table=source_table, watermark_column=(n.source.watermark_column if n.source.watermark_column in getattr(out_df, "columns", []) else None))
    out_df = add_hash_columns(
        out_df,
        business_keys=n.source.business_keys,
        include_business_key_hash=bool(n.source.business_keys),
    )

    output_profile = profile_dataframe(out_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(output_profile, target_table, ctx["run_id"], "output", exclude_columns=default_technical_columns()), md["output_profile_table"])

    partition_column = n.drift.data_policy.get("partition_column") or n.source.partition_column
    business_keys = list(n.drift.data_policy.get("business_keys") or n.source.business_keys)
    watermark_column = n.drift.data_policy.get("watermark_column") or n.source.watermark_column
    data_drift_result = {"status": "disabled", "can_continue": True}
    partition_snapshot_write = None
    if n.drift.data_enabled:
        if not partition_column or not business_keys:
            data_drift_result = {"status": "skipped", "can_continue": True, "message": "Data drift skipped due to missing partition_column or business_keys configuration."}
        else:
            out_cols_raw = getattr(out_df, "columns", None)
            out_columns = set(list(out_cols_raw) if out_cols_raw is not None else [])
            missing_cols = [partition_column] + list(business_keys)
            if watermark_column:
                missing_cols.append(watermark_column)
            missing_cols = [c for c in missing_cols if c and c not in out_columns]
            if missing_cols:
                return {
                    "status": "failed",
                    "can_continue": False,
                    "errors": [f"Data drift configuration columns missing in output dataframe: {', '.join(sorted(set(missing_cols)))}"],
                    "runtime_context": ctx,
                }
            baseline_partition_table = n.drift.baseline_partition_table or md.get("partition_snapshot_table")
            partition_baseline = load_latest_partition_snapshot(spark, baseline_partition_table, dataset_name=dataset_name, table_name=target_table) if baseline_partition_table else None
            data_drift_result = check_partition_drift(
                df=out_df, dataset_name=dataset_name, table_name=target_table, partition_column=partition_column, business_keys=business_keys, watermark_column=watermark_column, baseline_snapshot=partition_baseline, policy=n.drift.data_policy, run_id=ctx["run_id"], engine="auto"
            )
            if write_metadata and md.get("partition_snapshot_table"):
                partition_snapshot_write = build_and_write_partition_snapshot(
                    spark=spark, df=out_df, dataset_name=dataset_name, table_name=target_table, metadata_table=md["partition_snapshot_table"], partition_column=partition_column, business_keys=business_keys, watermark_column=watermark_column, run_id=ctx["run_id"], engine="auto"
                )

    dq_workflow = run_dq_workflow(
        spark=spark,
        df=out_df,
        quality_contract=n.quality,
        dataset_name=dataset_name,
        table_name=target_table,
        run_id=ctx["run_id"],
        profile=output_profile,
        metadata=None,
        business_context=None,
        engine="auto",
    )
    rules = dq_workflow["rules"]
    quality_result = dq_workflow["quality_result"]
    if write_metadata:
        _write_records_spark(spark, build_quality_result_records(quality_result, run_id=ctx["run_id"]), md["quality_result_table"])

    enforceable_rules = bool(rules)
    quarantine = {"enabled": bool(n.quality.quarantine_enabled), "written": False}
    valid_df, quarantine_df = out_df, None
    quarantine_row_count = 0
    valid_row_count = output_profile.get("row_count")
    if n.quality.quarantine_enabled and enforceable_rules:
        valid_df, quarantine_df = split_valid_and_quarantine(out_df, rules=rules, engine="auto")
        valid_row_count = len(valid_df) if hasattr(valid_df, "__len__") else int(valid_df.count())
        quarantine_row_count = len(quarantine_df) if hasattr(quarantine_df, "__len__") else int(quarantine_df.count())
        quarantine["row_count"] = quarantine_row_count
        if write_target and write_metadata and md.get("quarantine_table") and quarantine_row_count > 0:
            _write_dataframe_to_table(spark, quarantine_df, md["quarantine_table"], mode="append")
            quarantine["written"] = True

    governance = {"classifications": [], "records": [], "summary": {}, "metadata_table": n.governance.classification_table, "written": False}
    if n.governance.classify_columns:
        classifications = classify_columns(
            profile=output_profile,
            business_context={"dataset_name": dataset_name, "table_name": target_table},
            rules=n.governance.rules,
            dataset_name=dataset_name,
            table_name=target_table,
            run_id=ctx["run_id"],
        )
        gov_records = build_governance_classification_records(classifications, dataset_name=dataset_name, table_name=target_table, run_id=ctx["run_id"])
        written = False
        if write_metadata and n.governance.classification_table:
            write_governance_classifications(spark, classifications=classifications, table_name=n.governance.classification_table, dataset_name=dataset_name, source_table=target_table, run_id=ctx["run_id"])
            written = True
        governance = {"classifications": classifications, "records": gov_records, "summary": summarize_governance_classifications(classifications), "metadata_table": n.governance.classification_table, "written": written}

    contract_result = validate_runtime_contracts(source_df=src_df, output_df=valid_df, contract=_runtime_validation_contract(n), engine="auto")
    if write_metadata:
        _write_records_spark(spark, build_contract_validation_records(contract_result, run_id=ctx["run_id"]), md["contract_validation_table"])

    lineage_rows = build_lineage_records(run_id=ctx["run_id"], dataset_name=dataset_name, source_tables=[source_table], target_table=target_table, transformation_steps=[])
    if write_metadata and md.get("lineage_table"):
        _write_records_spark(spark, lineage_rows, md["lineage_table"])

    run_summary = build_run_summary(runtime_context=ctx, contract=effective_contract, source_profile=source_profile, output_profile=output_profile, quality_result=quality_result, contract_validation_result=contract_result)
    if write_metadata:
        _write_records_spark(spark, [build_run_summary_record(run_summary)], md["run_summary_table"])

    drift_summary = summarize_drift_results(schema_drift_result=schema_drift_result, partition_drift_result=data_drift_result, profile_drift_result=None)
    can_continue = (
        bool(quality_result.get("can_continue", True))
        and bool(contract_result.get("can_continue", True))
        and bool(schema_drift_result.get("can_continue", True))
        and bool(data_drift_result.get("can_continue", True))
    )
    status = "passed" if can_continue else "failed"
    if write_target and can_continue:
        _write_dataframe_to_table(spark, valid_df, target_table, mode=n.target.mode)

    dataset_run = build_dataset_run_record(run_id=ctx["run_id"], dataset_name=dataset_name, environment=ctx["environment"], source_table=source_table, target_table=target_table, status=status, started_at_utc=ctx.get("started_at_utc"), row_count_source=source_profile.get("row_count"), row_count_output=output_profile.get("row_count"))
    if write_metadata:
        _write_records_spark(spark, [dataset_run], md["dataset_runs_table"])

    return {
        "status": status, "can_continue": can_continue, "runtime_context": ctx, "contract": effective_contract,
        "source_profile": source_profile, "output_profile": output_profile,
        "drift": {"schema": schema_drift_result, "data": data_drift_result, "profile": None, "summary": drift_summary, "schema_snapshot_write": schema_snapshot_write, "partition_snapshot_write": partition_snapshot_write},
        "dq_workflow": dq_workflow, "quality_result": quality_result, "quarantine": quarantine, "valid_row_count": valid_row_count, "quarantine_row_count": quarantine_row_count,
        "governance": governance, "contract_validation_result": contract_result, "lineage": lineage_rows, "run_summary": run_summary,
        "target_table": target_table, "written": bool(write_target and can_continue), "dataset_run_record": dataset_run,
        "lineage_records": lineage_rows, "dataset_run": dataset_run, "quarantine_written": quarantine.get("written", False),
    }


def assert_data_product_passed(result: dict) -> None:
    """Assert data product passed.

    Run `assert_data_product_passed`.

    Parameters
    ----------
    result : dict
        Parameter `result`.

    Returns
    -------
    result : None
        Return value from `assert_data_product_passed`.

    Raises
    ------
    RuntimeError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> assert_data_product_passed(result)
    """
    if result.get("status") != "passed":
        raise RuntimeError("Data product run failed contract/quality gates")



# --- merged from rule_compiler.py ---
"""Compile AI layman DQ candidates into executable framework quality rules."""




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

    Run `compile_layman_rule_to_quality_rule`.

    Parameters
    ----------
    candidate : Any
        Parameter `candidate`.

    Returns
    -------
    result : object
        Return value from `compile_layman_rule_to_quality_rule`.

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

    Run `compile_layman_rules_to_quality_rules`.

    Parameters
    ----------
    candidates : Any
        Parameter `candidates`.

    Returns
    -------
    result : object
        Return value from `compile_layman_rules_to_quality_rules`.

    Examples
    --------
    >>> compile_layman_rules_to_quality_rules(candidates)
    """
    records = [compile_layman_rule_to_quality_rule(c) for c in candidates]
    return {"compiled_rules": [r["quality_rule"] for r in records if r["status"] == "compiled"], "records": records, "summary": {"total": len(records), "compiled": sum(r["status"] == "compiled" for r in records), "skipped": sum(r["status"] == "skipped" for r in records)}}


def build_rule_registry_records(compiled_rules, run_id, dataset_name, table_name):
    """Build rule registry records.

    Run `build_rule_registry_records`.

    Parameters
    ----------
    compiled_rules : Any
        Parameter `compiled_rules`.
    run_id : Any
        Parameter `run_id`.
    dataset_name : Any
        Parameter `dataset_name`.
    table_name : Any
        Parameter `table_name`.

    Returns
    -------
    result : object
        Return value from `build_rule_registry_records`.

    Examples
    --------
    >>> build_rule_registry_records(compiled_rules, run_id)
    """
    return [{"run_id": run_id, "dataset_name": dataset_name, "table_name": table_name, "rule_id": r.get("rule_id"), "rule_type": r.get("rule_type"), "severity": r.get("severity"), "column": r.get("column"), "columns": r.get("columns"), "reason": r.get("reason"), "rule_json": r} for r in compiled_rules]



# --- merged from quarantine.py ---
"""Row-level helpers to annotate and split valid/quarantine records."""




ROW_LEVEL_SUPPORTED = {"not_null", "regex_check", "accepted_values", "range_check", "unique", "unique_combination"}
AGGREGATE_ONLY = {"row_count_min", "row_count_between", "freshness_check"}


def _severity_bucket(severity: str) -> str:
    return "dq_errors" if str(severity).lower() == "critical" else "dq_warnings"


def build_quarantine_rule_coverage_records(rules, run_id, dataset_name, table_name):
    """Build quarantine rule coverage records.

    Run `build_quarantine_rule_coverage_records`.

    Parameters
    ----------
    rules : Any
        Parameter `rules`.
    run_id : Any
        Parameter `run_id`.
    dataset_name : Any
        Parameter `dataset_name`.
    table_name : Any
        Parameter `table_name`.

    Returns
    -------
    result : object
        Return value from `build_quarantine_rule_coverage_records`.

    Examples
    --------
    >>> build_quarantine_rule_coverage_records(rules, run_id)
    """
    rows = []
    for i, rule in enumerate(rules):
        rt = rule.get("rule_type")
        if rt in ROW_LEVEL_SUPPORTED:
            status, message = "row_level_supported", "Rule evaluated at row level"
        elif rt in AGGREGATE_ONLY:
            status, message = "aggregate_only", "Rule is aggregate-level and not row-level executable"
        else:
            status, message = "unsupported", "Unsupported or unknown rule_type for quarantine row-level execution"
        rows.append({"run_id": run_id, "dataset_name": dataset_name, "table_name": table_name, "rule_id": rule.get("rule_id", f"DQ{i + 1:03d}"), "rule_type": rt, "coverage_status": status, "coverage_message": message})
    return rows


def add_dq_failure_columns(df, rules, engine="auto"):
    """Add dq failure columns.

    Run `add_dq_failure_columns`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    rules : Any
        Parameter `rules`.
    engine : object, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_dq_failure_columns`.

    Examples
    --------
    >>> add_dq_failure_columns(df, rules)
    """
    resolved = _resolve_engine(df, engine)
    return _add_spark(df, rules) if resolved == "spark" else _add_pandas(df, rules)


def split_valid_and_quarantine(df, rules, engine="auto"):
    """Split valid and quarantine.

    Run `split_valid_and_quarantine`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    rules : Any
        Parameter `rules`.
    engine : object, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `split_valid_and_quarantine`.

    Examples
    --------
    >>> split_valid_and_quarantine(df, rules)
    """
    enriched = add_dq_failure_columns(df, rules, engine=engine)
    if _resolve_engine(enriched, engine) == "spark":
        from pyspark.sql import functions as F

        return enriched.filter(F.size("dq_errors") == 0), enriched.filter(F.size("dq_errors") > 0)
    return enriched[~enriched["dq_errors"].map(bool)].copy(), enriched[enriched["dq_errors"].map(bool)].copy()


def build_quarantine_summary_records(quarantine_df, run_id, dataset_name, table_name, engine="auto"):
    """Build quarantine summary records.

    Run `build_quarantine_summary_records`.

    Parameters
    ----------
    quarantine_df : Any
        Parameter `quarantine_df`.
    run_id : Any
        Parameter `run_id`.
    dataset_name : Any
        Parameter `dataset_name`.
    table_name : Any
        Parameter `table_name`.
    engine : object, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `build_quarantine_summary_records`.

    Examples
    --------
    >>> build_quarantine_summary_records(quarantine_df, run_id)
    """
    resolved = _resolve_engine(quarantine_df, engine)
    q_count = quarantine_df.count() if resolved == "spark" else len(quarantine_df)
    return [{"run_id": run_id, "dataset_name": dataset_name, "table_name": table_name, "quarantine_row_count": int(q_count), "engine": resolved}]


def _add_pandas(df: pd.DataFrame, rules):
    out = df.copy()
    out["dq_errors"] = [[] for _ in range(len(out))]
    out["dq_warnings"] = [[] for _ in range(len(out))]

    for i, rule in enumerate(rules):
        rt = rule.get("rule_type")
        if rt not in ROW_LEVEL_SUPPORTED:
            continue
        msg = f"{rule.get('rule_id', f'DQ{i + 1:03d}')}: {rule.get('reason') or rt}"
        bucket = _severity_bucket(rule.get("severity", "critical"))
        mask = pd.Series(False, index=out.index)

        if rt == "not_null":
            mask = out[rule["column"]].isna()
        elif rt == "regex_check":
            s = out[rule["column"]].dropna().astype(str)
            mask.loc[s[~s.str.match(rule.get("pattern", ""), na=False)].index] = True
        elif rt == "accepted_values":
            mask = out[rule["column"]].notna() & ~out[rule["column"]].isin(rule.get("accepted_values", []))
        elif rt == "range_check":
            s = out[rule["column"]]
            if rule.get("min_value") is not None:
                mask |= s.notna() & (s < rule["min_value"])
            if rule.get("max_value") is not None:
                mask |= s.notna() & (s > rule["max_value"])
        elif rt == "unique":
            mask = out[rule["column"]].duplicated(keep=False) & out[rule["column"]].notna()
        elif rt == "unique_combination":
            cols = rule.get("columns", [])
            if cols:
                mask = out.duplicated(subset=cols, keep=False)

        for pos, failed in enumerate(mask.tolist()):
            if failed:
                out.iat[pos, out.columns.get_loc(bucket)].append(msg)
    return out


def _add_spark(df, rules):
    from pyspark.sql import functions as F

    out = df.withColumn("dq_errors", F.array().cast("array<string>")).withColumn("dq_warnings", F.array().cast("array<string>"))
    for i, rule in enumerate(rules):
        rt = rule.get("rule_type")
        if rt not in ROW_LEVEL_SUPPORTED:
            continue
        msg = f"{rule.get('rule_id', f'DQ{i + 1:03d}')}: {rule.get('reason') or rt}"
        bucket = _severity_bucket(rule.get("severity", "critical"))
        cond = None
        if rt == "not_null":
            cond = F.col(rule["column"]).isNull()
        elif rt == "regex_check":
            cond = F.col(rule["column"]).isNotNull() & ~F.col(rule["column"]).rlike(rule.get("pattern", ""))
        elif rt == "accepted_values":
            cond = F.col(rule["column"]).isNotNull() & ~F.col(rule["column"]).isin(rule.get("accepted_values", []))
        elif rt == "range_check":
            cond = F.lit(False)
            if rule.get("min_value") is not None:
                cond = cond | (F.col(rule["column"]) < F.lit(rule["min_value"]))
            if rule.get("max_value") is not None:
                cond = cond | (F.col(rule["column"]) > F.lit(rule["max_value"]))
            cond = F.col(rule["column"]).isNotNull() & cond
        elif rt == "unique":
            c = rule["column"]
            dup_keys = (
                df.groupBy(c)
                .count()
                .filter(F.col(c).isNotNull() & (F.col("count") > 1))
                .select(F.col(c).alias("__dup_key"))
                .withColumn("__dup_marker", F.lit(True))
            )
            joined = out.join(dup_keys, out[c] == F.col("__dup_key"), "left")
            out = joined.withColumn(bucket, F.when(F.col("__dup_marker") == True, F.array_union(F.col(bucket), F.array(F.lit(msg)))).otherwise(F.col(bucket))).drop("__dup_key", "__dup_marker")
            continue
        elif rt == "unique_combination":
            cols = rule.get("columns", [])
            if cols:
                dup_combo = (
                    df.groupBy(*cols)
                    .count()
                    .filter(F.col("count") > 1)
                    .select(*[F.col(c).alias(f"__dup_{c}") for c in cols])
                    .withColumn("__dup_marker", F.lit(True))
                )
                join_cond = [out[c] == F.col(f"__dup_{c}") for c in cols]
                joined = out.join(dup_combo, join_cond, "left")
                drop_cols = [f"__dup_{c}" for c in cols] + ["__dup_marker"]
                out = joined.withColumn(bucket, F.when(F.col("__dup_marker") == True, F.array_union(F.col(bucket), F.array(F.lit(msg)))).otherwise(F.col(bucket))).drop(*drop_cols)
                continue
        if cond is None:
            continue
        out = out.withColumn(bucket, F.when(cond, F.array_union(F.col(bucket), F.array(F.lit(msg)))).otherwise(F.col(bucket)))
    return out



# --- merged from ai_quality_rules.py ---
"""Provider-neutral helpers for AI-assisted data quality rule generation."""




SUPPORTED_CANDIDATE_FIELDS = {
    "rule_id", "table_name", "column", "columns", "layman_rule", "rule_type", "rule_config",
    "severity", "confidence", "reason", "evidence", "approval_status",
}


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return value


def build_quality_rule_prompt_context(profile, contract=None, business_context=None, table_name=None, dataset_name=None):
    """Build quality rule prompt context.

    Run `build_quality_rule_prompt_context`.

    Parameters
    ----------
    profile : Any
        Parameter `profile`.
    contract : object, optional
        Parameter `contract`.
    business_context : object, optional
        Parameter `business_context`.
    table_name : object, optional
        Parameter `table_name`.
    dataset_name : object, optional
        Parameter `dataset_name`.

    Returns
    -------
    result : object
        Return value from `build_quality_rule_prompt_context`.

    Examples
    --------
    >>> build_quality_rule_prompt_context(profile, contract)
    """
    profile = profile or {}
    return {
        "dataset_name": dataset_name or profile.get("dataset_name", "unknown"),
        "table_name": table_name or profile.get("table_name", "unknown"),
        "profile": _jsonable(profile),
        "contract": _jsonable(contract or {}),
        "business_context": _jsonable(business_context or {}),
        "supported_rule_types": sorted(SUPPORTED_RULE_TYPES),
        "candidate_fields": sorted(SUPPORTED_CANDIDATE_FIELDS),
    }


def build_quality_rule_generation_prompt(profile, contract=None, business_context=None, table_name=None, dataset_name=None):
    """Build quality rule generation prompt.

    Run `build_quality_rule_generation_prompt`.

    Parameters
    ----------
    profile : Any
        Parameter `profile`.
    contract : object, optional
        Parameter `contract`.
    business_context : object, optional
        Parameter `business_context`.
    table_name : object, optional
        Parameter `table_name`.
    dataset_name : object, optional
        Parameter `dataset_name`.

    Returns
    -------
    result : object
        Return value from `build_quality_rule_generation_prompt`.

    Examples
    --------
    >>> build_quality_rule_generation_prompt(profile, contract)
    """
    context = build_quality_rule_prompt_context(profile, contract, business_context, table_name, dataset_name)
    return (
        "You are generating conservative data quality rule candidates for Fabric data product workflows.\n"
        "Return JSON array only. Do not return markdown.\n"
        "Each array item must include human-readable 'layman_rule' and executable metadata fields: "
        "rule_id, table_name, column, columns, layman_rule, rule_type, rule_config, severity, confidence, reason, evidence, approval_status.\n"
        "Rules must be supported by profiling evidence only. Do not invent business rules.\n"
        "Use conservative suggestions, mark weak assumptions as low confidence.\n"
        "Do not set every column to not_null. Avoid accepted_values for high-cardinality columns. "
        "Avoid uniqueness unless distinct_count is close to row_count.\n"
        "Use severity='warning' by default unless business context clearly implies critical severity.\n"
        f"Supported rule types: {sorted(SUPPORTED_RULE_TYPES)}\n"
        f"Context JSON: {json.dumps(context, ensure_ascii=False)}"
    )


def _strip_json_fences(text: str) -> str:
    fenced = re.match(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", text, flags=re.DOTALL | re.IGNORECASE)
    return fenced.group(1) if fenced else text


def parse_ai_quality_rule_candidates(raw_response):
    """Parse ai quality rule candidates.

    Run `parse_ai_quality_rule_candidates`.

    Parameters
    ----------
    raw_response : Any
        Parameter `raw_response`.

    Returns
    -------
    result : object
        Return value from `parse_ai_quality_rule_candidates`.

    Examples
    --------
    >>> parse_ai_quality_rule_candidates(raw_response)
    """
    try:
        parsed = json.loads(_strip_json_fences(raw_response)) if isinstance(raw_response, str) else raw_response
    except Exception as exc:
        return {"ok": False, "candidates": [], "errors": [f"Invalid AI JSON response: {exc}"], "warnings": []}
    if not isinstance(parsed, list):
        return {"ok": False, "candidates": [], "errors": ["AI response must be a JSON array"], "warnings": []}

    errors: list[str] = []
    warnings: list[str] = []
    candidates = []
    for idx, item in enumerate(parsed):
        if not isinstance(item, dict):
            warnings.append(f"Skipped non-dict item at index {idx}")
            continue
        c = normalize_quality_rule_candidate(item)
        val = validate_ai_quality_rule_candidate(c)
        c["is_valid_candidate"] = val["is_valid"]
        c["validation_message"] = val["message"]
        c["can_compile"] = val["is_valid"]
        if not val["is_valid"]:
            warnings.append(val["message"])
        candidates.append(c)
    return {"ok": len(errors) == 0, "candidates": candidates, "errors": errors, "warnings": warnings}


def normalize_quality_rule_candidate(candidate):
    """Normalize quality rule candidate.

    Run `normalize_quality_rule_candidate`.

    Parameters
    ----------
    candidate : Any
        Parameter `candidate`.

    Returns
    -------
    result : object
        Return value from `normalize_quality_rule_candidate`.

    Examples
    --------
    >>> normalize_quality_rule_candidate(candidate)
    """
    out = {k: v for k, v in candidate.items() if k in SUPPORTED_CANDIDATE_FIELDS}
    out["rule_type"] = str(out.get("rule_type", "")).strip().lower()
    out["severity"] = str(out.get("severity", "warning")).strip().lower() or "warning"
    out["confidence"] = str(out.get("confidence", "medium")).strip().lower() or "medium"
    out["approval_status"] = str(out.get("approval_status", "candidate")).strip().lower() or "candidate"
    out["rule_config"] = out.get("rule_config") if isinstance(out.get("rule_config"), dict) else {}
    out["columns"] = out.get("columns") if isinstance(out.get("columns"), list) else ([] if out.get("columns") is None else [out.get("columns")])
    out.setdefault("layman_rule", out.get("reason") or "")
    out.setdefault("reason", out.get("layman_rule") or "")
    out.setdefault("evidence", "")
    return out


def validate_ai_quality_rule_candidate(candidate):
    """Validate ai quality rule candidate.

    Run `validate_ai_quality_rule_candidate`.

    Parameters
    ----------
    candidate : Any
        Parameter `candidate`.

    Returns
    -------
    result : object
        Return value from `validate_ai_quality_rule_candidate`.

    Examples
    --------
    >>> validate_ai_quality_rule_candidate(candidate)
    """
    rt = candidate.get("rule_type")
    if not rt:
        return {"is_valid": False, "message": "Missing rule_type"}
    if rt not in SUPPORTED_RULE_TYPES:
        return {"is_valid": False, "message": f"Unsupported rule_type: {rt}"}
    if rt in {"not_null", "unique", "accepted_values", "range_check", "regex_check", "freshness_check"} and not candidate.get("column"):
        return {"is_valid": False, "message": f"Missing column for rule_type: {rt}"}
    if rt == "unique_combination" and not candidate.get("columns"):
        return {"is_valid": False, "message": "Missing columns for unique_combination"}
    return {"is_valid": True, "message": "ok"}


def build_layman_rule_records(candidates, run_id, dataset_name, table_name):
    """Build layman rule records.

    Run `build_layman_rule_records`.

    Parameters
    ----------
    candidates : Any
        Parameter `candidates`.
    run_id : Any
        Parameter `run_id`.
    dataset_name : Any
        Parameter `dataset_name`.
    table_name : Any
        Parameter `table_name`.

    Returns
    -------
    result : object
        Return value from `build_layman_rule_records`.

    Examples
    --------
    >>> build_layman_rule_records(candidates, run_id)
    """
    rows = []
    for i, c in enumerate(candidates):
        can_compile = bool(c.get("can_compile")) if "can_compile" in c else validate_ai_quality_rule_candidate(c)["is_valid"]
        rows.append({
            "run_id": run_id,
            "dataset_name": dataset_name,
            "table_name": table_name,
            "rule_id": c.get("rule_id") or f"AI_DQ_{i + 1:03d}",
            "rule_type": c.get("rule_type"),
            "layman_rule": c.get("layman_rule"),
            "severity": c.get("severity", "warning"),
            "confidence": c.get("confidence", "medium"),
            "approval_status": c.get("approval_status", "candidate"),
            "is_valid_candidate": c.get("is_valid_candidate", can_compile),
            "validation_message": c.get("validation_message", "ok" if can_compile else "invalid candidate"),
            "can_compile": can_compile,
            "candidate_json": _jsonable(c),
        })
    return rows

