"""Contract-ready drift checker wrappers over schema and incremental drift helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import json

from fabric_data_product_framework.drift import build_schema_snapshot, compare_schema_snapshots, default_schema_drift_policy
from fabric_data_product_framework.incremental import build_partition_snapshot, compare_partition_snapshots, default_incremental_safety_policy
from fabric_data_product_framework.profiling import to_jsonable


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_spark_collect(df):
    if df is None:
        return []
    if hasattr(df, "collect"):
        return df.collect()
    return []

def _is_missing_table_error(exc: Exception) -> bool:
    text = str(exc).lower()
    patterns = ["not found", "table or view not found", "no such table", "cannot resolve", "missing"]
    return any(p in text for p in patterns)


def _json_dumps(value) -> str:
    return json.dumps(to_jsonable(value), sort_keys=True)


def _write_metadata_rows(spark, metadata_table: str, records: list[dict], mode: str = "append") -> bool:
    if not records:
        return False
    metadata_df = spark.createDataFrame(records)
    metadata_df.write.mode(mode).saveAsTable(metadata_table)
    return True


def check_schema_drift(df, dataset_name: str, table_name: str, baseline_snapshot: dict | None = None, policy: dict | None = None, engine: str = "spark") -> dict:
    """Check schema drift.

    Execute `check_schema_drift`.

    Parameters
    ----------
    df : Any
        Value for `df`.
    dataset_name : str
        Value for `dataset_name`.
    table_name : str
        Value for `table_name`.
    baseline_snapshot : dict | None, optional
        Value for `baseline_snapshot`.
    policy : dict | None, optional
        Value for `policy`.
    engine : str, optional
        Value for `engine`.

    Returns
    -------
    result : dict
        Result returned by `check_schema_drift`.

    Examples
    --------
    >>> check_schema_drift(df, dataset_name)
    """
    current_snapshot = build_schema_snapshot(df, dataset_name=dataset_name, table_name=table_name, engine=engine)
    if baseline_snapshot is None:
        return {
            "dataset_name": dataset_name,
            "table_name": table_name,
            "status": "no_baseline",
            "can_continue": True,
            "current_snapshot": current_snapshot,
            "baseline_snapshot": None,
            "comparison": None,
            "message": "No baseline schema snapshot found; current snapshot captured as first observation.",
        }

    comparison = compare_schema_snapshots(baseline_snapshot, current_snapshot, policy=policy or default_schema_drift_policy())
    status = str(comparison.get("status", "passed"))
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "status": status,
        "can_continue": bool(comparison.get("can_continue", True)),
        "current_snapshot": current_snapshot,
        "baseline_snapshot": baseline_snapshot,
        "comparison": comparison,
        "message": "Schema drift check completed.",
    }


def build_and_write_schema_snapshot(spark, df, dataset_name: str, table_name: str, metadata_table: str, run_id: str | None = None, mode: str = "append", engine: str = "spark") -> dict:
    """Build and write schema snapshot.

    Execute `build_and_write_schema_snapshot`.

    Parameters
    ----------
    spark : Any
        Value for `spark`.
    df : Any
        Value for `df`.
    dataset_name : str
        Value for `dataset_name`.
    table_name : str
        Value for `table_name`.
    metadata_table : str
        Value for `metadata_table`.
    run_id : str | None, optional
        Value for `run_id`.
    mode : str, optional
        Value for `mode`.
    engine : str, optional
        Value for `engine`.

    Returns
    -------
    result : dict
        Result returned by `build_and_write_schema_snapshot`.

    Examples
    --------
    >>> build_and_write_schema_snapshot(spark, df)
    """
    snapshot = build_schema_snapshot(df, dataset_name=dataset_name, table_name=table_name, engine=engine)
    records = [
        {
            "run_id": run_id,
            "dataset_name": dataset_name,
            "table_name": table_name,
            "snapshot_type": "schema",
            "schema_snapshot_json": _json_dumps(snapshot),
            "created_at": _utc_now_iso(),
        }
    ]
    written = _write_metadata_rows(spark, metadata_table=metadata_table, records=records, mode=mode)
    return {"snapshot": snapshot, "records": records, "metadata_table": metadata_table, "written": written}


def load_latest_schema_snapshot(spark, metadata_table: str, dataset_name: str, table_name: str) -> dict | None:
    """Load latest schema snapshot.

    Execute `load_latest_schema_snapshot`.

    Parameters
    ----------
    spark : Any
        Value for `spark`.
    metadata_table : str
        Value for `metadata_table`.
    dataset_name : str
        Value for `dataset_name`.
    table_name : str
        Value for `table_name`.

    Returns
    -------
    result : dict | None
        Result returned by `load_latest_schema_snapshot`.

    Examples
    --------
    >>> load_latest_schema_snapshot(spark, metadata_table)
    """
    try:
        df = spark.table(metadata_table)
        if hasattr(df, "filter") and hasattr(df, "orderBy") and hasattr(df, "limit"):
            from pyspark.sql import functions as F

            df = (
                df.filter(
                    (F.col("dataset_name") == dataset_name)
                    & (F.col("table_name") == table_name)
                    & (F.col("snapshot_type") == "schema")
                )
                .orderBy(F.col("created_at").desc(), F.col("run_id").desc())
                .limit(1)
            )
            rows = _safe_spark_collect(df)
        else:
            rows = _safe_spark_collect(df)
    except Exception as exc:
        if _is_missing_table_error(exc):
            return None
        raise

    matched = [r.asDict() if hasattr(r, "asDict") else dict(r) for r in rows if (r["dataset_name"] == dataset_name and r["table_name"] == table_name and r.get("snapshot_type") == "schema")]
    if not matched:
        return None

    matched.sort(key=lambda x: (str(x.get("created_at", "")), str(x.get("run_id", ""))), reverse=True)
    raw = matched[0].get("schema_snapshot_json")
    if not raw:
        return None
    return json.loads(raw)


def check_partition_drift(df, dataset_name: str, table_name: str, partition_column: str, business_keys: list[str] | None = None, watermark_column: str | None = None, baseline_snapshot: list[dict] | dict | None = None, policy: dict | None = None, run_id: str | None = None, engine: str = "spark") -> dict:
    """Check partition drift.

    Execute `check_partition_drift`.

    Parameters
    ----------
    df : Any
        Value for `df`.
    dataset_name : str
        Value for `dataset_name`.
    table_name : str
        Value for `table_name`.
    partition_column : str
        Value for `partition_column`.
    business_keys : list[str] | None, optional
        Value for `business_keys`.
    watermark_column : str | None, optional
        Value for `watermark_column`.
    baseline_snapshot : list[dict] | dict | None, optional
        Value for `baseline_snapshot`.
    policy : dict | None, optional
        Value for `policy`.
    run_id : str | None, optional
        Value for `run_id`.
    engine : str, optional
        Value for `engine`.

    Returns
    -------
    result : dict
        Result returned by `check_partition_drift`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> check_partition_drift(df, dataset_name)
    """
    keys = business_keys or []
    if not keys:
        raise ValueError("business_keys must contain at least one column for partition drift checks.")
    current_snapshot = build_partition_snapshot(
        df,
        dataset_name=dataset_name,
        table_name=table_name,
        partition_column=partition_column,
        business_keys=keys,
        watermark_column=watermark_column,
        run_id=run_id,
        engine=engine,
    )
    if baseline_snapshot is None:
        return {
            "dataset_name": dataset_name,
            "table_name": table_name,
            "status": "no_baseline",
            "can_continue": True,
            "current_snapshot": current_snapshot,
            "baseline_snapshot": None,
            "comparison": None,
            "message": "No baseline partition snapshot found; current snapshot captured as first observation.",
        }

    baseline_rows = baseline_snapshot if isinstance(baseline_snapshot, list) else [baseline_snapshot]
    comparison = compare_partition_snapshots(baseline_rows, current_snapshot, policy=policy or default_incremental_safety_policy())
    status = str(comparison.get("status", "passed"))
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "status": status,
        "can_continue": bool(comparison.get("can_continue", True)),
        "current_snapshot": current_snapshot,
        "baseline_snapshot": baseline_rows,
        "comparison": comparison,
        "message": "Partition drift check completed.",
    }


def build_and_write_partition_snapshot(spark, df, dataset_name: str, table_name: str, metadata_table: str, partition_column: str, business_keys: list[str] | None = None, watermark_column: str | None = None, run_id: str | None = None, mode: str = "append", engine: str = "spark") -> dict:
    """Build and write partition snapshot.

    Execute `build_and_write_partition_snapshot`.

    Parameters
    ----------
    spark : Any
        Value for `spark`.
    df : Any
        Value for `df`.
    dataset_name : str
        Value for `dataset_name`.
    table_name : str
        Value for `table_name`.
    metadata_table : str
        Value for `metadata_table`.
    partition_column : str
        Value for `partition_column`.
    business_keys : list[str] | None, optional
        Value for `business_keys`.
    watermark_column : str | None, optional
        Value for `watermark_column`.
    run_id : str | None, optional
        Value for `run_id`.
    mode : str, optional
        Value for `mode`.
    engine : str, optional
        Value for `engine`.

    Returns
    -------
    result : dict
        Result returned by `build_and_write_partition_snapshot`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> build_and_write_partition_snapshot(spark, df)
    """
    keys = business_keys or []
    if not keys:
        raise ValueError("business_keys must contain at least one column for partition snapshots.")
    snapshot = build_partition_snapshot(
        df,
        dataset_name=dataset_name,
        table_name=table_name,
        partition_column=partition_column,
        business_keys=keys,
        watermark_column=watermark_column,
        run_id=run_id,
        engine=engine,
    )
    records = [
        {
            "run_id": run_id,
            "dataset_name": dataset_name,
            "table_name": table_name,
            "snapshot_type": "partition",
            "partition_column": partition_column,
            "business_keys_json": _json_dumps(keys),
            "watermark_column": watermark_column,
            "partition_snapshot_json": _json_dumps(snapshot),
            "created_at": _utc_now_iso(),
        }
    ]
    written = _write_metadata_rows(spark, metadata_table=metadata_table, records=records, mode=mode)
    return {"snapshot": snapshot, "records": records, "metadata_table": metadata_table, "written": written}


def load_latest_partition_snapshot(spark, metadata_table: str, dataset_name: str, table_name: str) -> list[dict] | dict | None:
    """Load latest partition snapshot.

    Execute `load_latest_partition_snapshot`.

    Parameters
    ----------
    spark : Any
        Value for `spark`.
    metadata_table : str
        Value for `metadata_table`.
    dataset_name : str
        Value for `dataset_name`.
    table_name : str
        Value for `table_name`.

    Returns
    -------
    result : list[dict] | dict | None
        Result returned by `load_latest_partition_snapshot`.

    Examples
    --------
    >>> load_latest_partition_snapshot(spark, metadata_table)
    """
    try:
        df = spark.table(metadata_table)
        if hasattr(df, "filter") and hasattr(df, "orderBy") and hasattr(df, "limit"):
            from pyspark.sql import functions as F

            df = (
                df.filter(
                    (F.col("dataset_name") == dataset_name)
                    & (F.col("table_name") == table_name)
                    & (F.col("snapshot_type") == "partition")
                )
                .orderBy(F.col("created_at").desc(), F.col("run_id").desc())
                .limit(1)
            )
            rows = _safe_spark_collect(df)
        else:
            rows = _safe_spark_collect(df)
    except Exception as exc:
        if _is_missing_table_error(exc):
            return None
        raise
    matched = [r.asDict() if hasattr(r, "asDict") else dict(r) for r in rows if (r["dataset_name"] == dataset_name and r["table_name"] == table_name and r.get("snapshot_type") == "partition")]
    if not matched:
        return None
    matched.sort(key=lambda x: (str(x.get("created_at", "")), str(x.get("run_id", ""))), reverse=True)
    raw = matched[0].get("partition_snapshot_json")
    if not raw:
        return None
    return json.loads(raw)


def check_profile_drift(current_profile: dict, baseline_profile: dict | None = None, policy: dict | None = None) -> dict:
    """Check profile drift.

    Execute `check_profile_drift`.

    Parameters
    ----------
    current_profile : dict
        Value for `current_profile`.
    baseline_profile : dict | None, optional
        Value for `baseline_profile`.
    policy : dict | None, optional
        Value for `policy`.

    Returns
    -------
    result : dict
        Result returned by `check_profile_drift`.

    Examples
    --------
    >>> check_profile_drift(current_profile, baseline_profile)
    """
    active = {
        "max_row_count_change_percent": 50,
        "max_null_percent_change_points": 20,
        "max_distinct_percent_change_points": 30,
        "fail_on_missing_column": True,
        **(policy or {}),
    }
    if baseline_profile is None:
        return {"status": "no_baseline", "can_continue": True, "checks": [], "message": "No baseline profile provided."}

    checks = []
    blocking = False
    b_row = float(baseline_profile.get("row_count") or 0)
    c_row = float(current_profile.get("row_count") or 0)
    row_delta_pct = 0.0 if b_row == 0 else abs(c_row - b_row) / b_row * 100.0
    row_ok = row_delta_pct <= float(active["max_row_count_change_percent"])
    checks.append({"check": "row_count_change_percent", "passed": row_ok, "value": row_delta_pct, "threshold": active["max_row_count_change_percent"]})
    blocking = blocking or (not row_ok)

    b_cols = {c.get("column_name"): c for c in baseline_profile.get("columns", [])}
    c_cols = {c.get("column_name"): c for c in current_profile.get("columns", [])}
    for col in sorted(set(b_cols) - set(c_cols)):
        passed = not bool(active["fail_on_missing_column"])
        checks.append({"check": "missing_column", "column": col, "passed": passed})
        blocking = blocking or (not passed)

    for col in sorted(set(b_cols).intersection(c_cols)):
        b = b_cols[col]
        c = c_cols[col]
        if "null_pct" in b and "null_pct" in c:
            delta = abs(float(c.get("null_pct") or 0) - float(b.get("null_pct") or 0))
            passed = delta <= float(active["max_null_percent_change_points"])
            checks.append({"check": "null_percent_change_points", "column": col, "passed": passed, "value": delta, "threshold": active["max_null_percent_change_points"]})
            blocking = blocking or (not passed)
        if "distinct_pct" in b and "distinct_pct" in c:
            delta = abs(float(c.get("distinct_pct") or 0) - float(b.get("distinct_pct") or 0))
            passed = delta <= float(active["max_distinct_percent_change_points"])
            checks.append({"check": "distinct_percent_change_points", "column": col, "passed": passed, "value": delta, "threshold": active["max_distinct_percent_change_points"]})
            blocking = blocking or (not passed)
        if b.get("min_value") != c.get("min_value"):
            checks.append({"check": "min_changed", "column": col, "passed": True, "baseline": b.get("min_value"), "current": c.get("min_value")})
        if b.get("max_value") != c.get("max_value"):
            checks.append({"check": "max_changed", "column": col, "passed": True, "baseline": b.get("max_value"), "current": c.get("max_value")})

    return {"status": "failed" if blocking else "passed", "can_continue": not blocking, "checks": checks, "message": "Profile drift check completed."}


def summarize_drift_results(schema_drift_result: dict | None = None, partition_drift_result: dict | None = None, profile_drift_result: dict | None = None) -> dict:
    """Summarize drift results.

    Execute `summarize_drift_results`.

    Parameters
    ----------
    schema_drift_result : dict | None, optional
        Value for `schema_drift_result`.
    partition_drift_result : dict | None, optional
        Value for `partition_drift_result`.
    profile_drift_result : dict | None, optional
        Value for `profile_drift_result`.

    Returns
    -------
    result : dict
        Result returned by `summarize_drift_results`.

    Examples
    --------
    >>> summarize_drift_results(schema_drift_result, partition_drift_result)
    """
    results = {"schema": schema_drift_result, "partition": partition_drift_result, "profile": profile_drift_result}
    statuses = {k: (v or {}).get("status") for k, v in results.items()}
    failed = [k for k, v in results.items() if v and (v.get("status") == "failed" or not v.get("can_continue", True))]
    warnings = [k for k, v in results.items() if v and v.get("status") in {"warning", "no_baseline"}]
    if failed:
        overall = "failed"
    elif warnings and all((v or {}).get("status") == "no_baseline" for v in results.values() if v):
        overall = "no_baseline"
    elif warnings:
        overall = "warning"
    else:
        overall = "passed"
    can_continue = len(failed) == 0
    return {
        "status": overall,
        "can_continue": can_continue,
        "schema_status": statuses["schema"],
        "partition_status": statuses["partition"],
        "profile_status": statuses["profile"],
        "blocking_checks": failed,
        "warnings": warnings,
    }
