"""Runtime contract validation helpers for pandas and Spark dataframes."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
from typing import Any

import pandas as pd

from fabric_data_product_framework.engines import detect_dataframe_engine, validate_engine

SEVERITY_TO_ACTION = {"info": "warn", "warning": "warn", "critical": "block"}


class ContractValidationError(Exception):
    """Raised when runtime contract validation has blocking failures."""


def _json_safe(value: Any) -> Any:
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.isoformat()
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


def validate_required_columns(df, expected_columns: list[str], *, dataset_name: str = "unknown", table_name: str = "unknown", check_name: str = "required_columns", severity: str = "critical", engine: str = "auto") -> dict:
    resolved = _resolve_engine(df, engine)
    actual_columns = list(df.columns) if resolved in {"pandas", "spark"} else []
    missing = [c for c in expected_columns if c not in actual_columns]
    extra = [c for c in actual_columns if c not in expected_columns]
    status = "failed" if missing else "passed"
    message = f"Missing required columns: {missing}" if missing else "All required columns are present"
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "check_name": check_name,
        "check_type": "required_columns",
        "severity": severity,
        "status": status,
        "action": _action_for(status, severity),
        "expected": expected_columns,
        "actual": actual_columns,
        "missing": missing,
        "extra": extra,
        "message": message,
    }


def validate_grain(df, business_keys: list[str], *, dataset_name: str = "unknown", table_name: str = "unknown", severity: str = "critical", engine: str = "auto") -> dict:
    resolved = _resolve_engine(df, engine)
    missing = [k for k in business_keys if k not in getattr(df, "columns", [])]
    if missing:
        return {
            "dataset_name": dataset_name,
            "table_name": table_name,
            "check_name": "grain",
            "check_type": "grain",
            "severity": severity,
            "status": "failed",
            "action": _action_for("failed", severity),
            "business_keys": business_keys,
            "duplicate_count": None,
            "message": f"Missing business key columns: {missing}",
        }
    if resolved == "pandas":
        duplicate_count = int(df.duplicated(subset=business_keys, keep=False).sum())
    else:
        from pyspark.sql import functions as F

        duplicate_count = int(df.groupBy(business_keys).count().filter(F.col("count") > 1).count())
    status = "failed" if duplicate_count > 0 else "passed"
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "check_name": "grain",
        "check_type": "grain",
        "severity": severity,
        "status": status,
        "action": _action_for(status, severity),
        "business_keys": business_keys,
        "duplicate_count": duplicate_count,
        "message": "Business grain is unique" if status == "passed" else f"Found duplicate business keys: {duplicate_count}",
    }


def validate_freshness(df, watermark_column: str, *, max_age_days: int | None = None, dataset_name: str = "unknown", table_name: str = "unknown", severity: str = "critical", engine: str = "auto") -> dict:
    resolved = _resolve_engine(df, engine)
    if max_age_days is None:
        return {
            "dataset_name": dataset_name, "table_name": table_name, "check_name": "freshness", "check_type": "freshness", "severity": severity,
            "status": "skipped", "action": "allow", "watermark_column": watermark_column, "max_watermark": None, "max_age_days": None,
            "message": "Freshness threshold not configured; check skipped",
        }
    if watermark_column not in getattr(df, "columns", []):
        return {
            "dataset_name": dataset_name, "table_name": table_name, "check_name": "freshness", "check_type": "freshness", "severity": severity,
            "status": "failed", "action": _action_for("failed", severity), "watermark_column": watermark_column, "max_watermark": None, "max_age_days": max_age_days,
            "message": f"Missing watermark column: {watermark_column}",
        }
    if resolved == "pandas":
        ts = pd.to_datetime(df[watermark_column], errors="coerce", utc=True).dropna()
        max_watermark = ts.max().to_pydatetime() if not ts.empty else None
    else:
        from pyspark.sql import functions as F

        max_watermark = df.select(F.max(F.col(watermark_column)).alias("max_ts")).collect()[0]["max_ts"]
        if max_watermark is not None and max_watermark.tzinfo is None:
            max_watermark = max_watermark.replace(tzinfo=timezone.utc)
    if max_watermark is None:
        status = "failed"
        msg = "No valid watermark values found"
    else:
        age = datetime.now(timezone.utc) - max_watermark
        status = "passed" if age <= timedelta(days=max_age_days) else "failed"
        msg = f"Latest watermark is within {max_age_days} day(s)" if status == "passed" else f"Latest watermark exceeds {max_age_days} day(s)"
    return {
        "dataset_name": dataset_name, "table_name": table_name, "check_name": "freshness", "check_type": "freshness", "severity": severity,
        "status": status, "action": _action_for(status, severity), "watermark_column": watermark_column,
        "max_watermark": _json_safe(max_watermark), "max_age_days": max_age_days, "message": msg,
    }


def _parse_freshness_days(value: str | None) -> int | None:
    if not value:
        return None
    m = re.match(r"^\s*(\d+)\s*(day|days|hour|hours)\s*$", str(value).strip().lower())
    if not m:
        return None
    qty, unit = int(m.group(1)), m.group(2)
    return qty if unit.startswith("day") else max(1, qty // 24)


def _combine_contract_checks(dataset_name: str, table_name: str, contract_type: str, checks: list[dict]) -> dict:
    statuses = [c.get("status") for c in checks]
    failed_blocking = [c for c in checks if c.get("status") == "failed" and c.get("action") == "block"]
    status = "failed" if failed_blocking else ("warning" if "failed" in statuses or "warning" in statuses else "passed")
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "contract_type": contract_type,
        "status": status,
        "can_continue": not failed_blocking,
        "checks": checks,
    }


def validate_upstream_contract(df, contract: dict, *, dataset_name: str | None = None, table_name: str | None = None, engine: str = "auto") -> dict:
    dataset_name = dataset_name or contract.get("dataset", {}).get("name", "unknown")
    table_name = table_name or contract.get("source", {}).get("table", "unknown")
    up = contract.get("contracts", {}).get("upstream", {})
    checks = [validate_required_columns(df, up.get("expected_columns", []), dataset_name=dataset_name, table_name=table_name, severity="critical", engine=engine)]
    max_age_days = _parse_freshness_days(up.get("expected_freshness"))
    watermark_column = contract.get("refresh", {}).get("watermark_column")
    if watermark_column:
        checks.append(validate_freshness(df, watermark_column, max_age_days=max_age_days, dataset_name=dataset_name, table_name=table_name, severity="warning" if max_age_days is None else "critical", engine=engine))
    return _combine_contract_checks(dataset_name, table_name, "upstream", checks)


def validate_downstream_contract(df, contract: dict, *, dataset_name: str | None = None, table_name: str | None = None, engine: str = "auto") -> dict:
    dataset_name = dataset_name or contract.get("dataset", {}).get("name", "unknown")
    table_name = table_name or contract.get("target", {}).get("table", "unknown")
    down = contract.get("contracts", {}).get("downstream", {})
    checks = [
        validate_required_columns(df, down.get("guaranteed_columns", []), dataset_name=dataset_name, table_name=table_name, severity="critical", engine=engine),
        validate_grain(df, contract.get("keys", {}).get("business_keys", []), dataset_name=dataset_name, table_name=table_name, severity="critical", engine=engine),
    ]
    return _combine_contract_checks(dataset_name, table_name, "downstream", checks)


def validate_runtime_contracts(*, source_df=None, output_df=None, contract: dict, engine: str = "auto") -> dict:
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
    return {
        "dataset_name": contract.get("dataset", {}).get("name", "unknown"),
        "status": status,
        "can_continue": blocking == 0,
        "results": results,
        "summary": {"passed_checks": passed, "warning_checks": warnings, "failed_checks": failed, "blocking_check_count": blocking},
    }


def assert_contracts_valid(result: dict) -> None:
    if not result.get("can_continue", False):
        raise ContractValidationError("Contract validation returned blocking failures")


def build_contract_validation_records(result: dict, *, run_id: str) -> list[dict]:
    records: list[dict] = []
    for section in result.get("results", []):
        for check in section.get("checks", []):
            records.append(_json_safe({
                "run_id": run_id,
                "dataset_name": result.get("dataset_name"),
                "contract_type": section.get("contract_type"),
                "table_name": section.get("table_name"),
                "overall_status": section.get("status"),
                "can_continue": section.get("can_continue"),
                "check_name": check.get("check_name"),
                "check_type": check.get("check_type"),
                "severity": check.get("severity"),
                "status": check.get("status"),
                "action": check.get("action"),
                "expected": check.get("expected"),
                "actual": check.get("actual"),
                "missing": check.get("missing"),
                "extra": check.get("extra"),
                "message": check.get("message"),
            }))
    return records
