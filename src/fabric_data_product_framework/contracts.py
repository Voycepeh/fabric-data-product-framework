"""Runtime contract validation helpers for pandas and Spark dataframes."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
from typing import Any

import pandas as pd

from fabric_data_product_framework.engines import detect_dataframe_engine, validate_engine

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
