"""Lightweight data quality rule execution for pandas and Spark."""

from __future__ import annotations

from datetime import datetime, timezone
import math
import re
from typing import Any

import pandas as pd


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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> DataQualityError(...)
    """
    """Raised when data quality gate fails."""


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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    df : Any
    Description of `df`.
    rules : Any
    Description of `rules`.
    dataset_name : Any
    Description of `dataset_name`.
    table_name : Any
    Description of `table_name`.
    engine : Any
    Description of `engine`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> run_quality_rules(...)
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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    result : Any
    Description of `result`.
    fail_on : Any
    Description of `fail_on`.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> assert_quality_gate(...)
    """
    if fail_on != "critical":
        raise ValueError("Only fail_on='critical' is supported in MVP")
    if not result.get("can_continue", True):
        raise DataQualityError("Data quality gate failed due to critical rule failures.")


def build_quality_result_records(result: dict, *, run_id: str) -> list[dict]:
    """Build quality result records.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    result : Any
    Description of `result`.
    run_id : Any
    Description of `run_id`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_quality_result_records(...)
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
