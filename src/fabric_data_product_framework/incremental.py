"""Incremental partition safety snapshot and comparison helpers."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import hashlib
from typing import Any

from fabric_data_product_framework.engines import detect_dataframe_engine, validate_engine
from fabric_data_product_framework.profiling import to_jsonable


class IncrementalSafetyError(Exception):
    """Incrementalsafetyerror.

    Public class used by the framework API for `IncrementalSafetyError`.

    Examples
    --------
    >>> IncrementalSafetyError(... )
    """


def default_incremental_safety_policy() -> dict:
    """Default incremental safety policy.

    Execute `default_incremental_safety_policy`.

    Parameters
    ----------
    None
        This callable does not require user-provided parameters.

    Returns
    -------
    result : dict
        Result returned by `default_incremental_safety_policy`.

    Examples
    --------
    >>> default_incremental_safety_policy()
    """
    return {
        "block_on_historical_partition_change": True,
        "closed_partition_grace_days": 1,
        "allow_late_arriving_records": False,
        "lookback_partitions": 3,
        "allow_historical_changes": False,
        "require_approval_for_historical_changes": True,
        "approval_reference": None,
        "run_mode": "incremental",
    }


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _build_partition_hash(partition_value: Any, row_count: int, business_key_count: int, max_watermark: Any, min_watermark: Any, business_key_hash: str) -> str:
    payload = "|".join(
        [
            str(partition_value),
            str(row_count),
            str(business_key_count),
            str(max_watermark),
            str(min_watermark),
            str(business_key_hash),
        ]
    )
    return _hash(payload)


def _build_pandas_partition_snapshot(df, *, dataset_name: str, table_name: str, partition_column: str, business_keys: list[str], watermark_column: str | None, run_id: str | None) -> list[dict]:
    generated_at = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    grouped = df.groupby(partition_column, dropna=False)
    for partition_value, group in grouped:
        row_count = int(group.shape[0])
        key_rows = group[business_keys].astype(str).drop_duplicates().apply(lambda r: "||".join(r.values.tolist()), axis=1)
        sorted_key_rows = sorted(key_rows.tolist())
        business_key_hash = _hash("##".join(sorted_key_rows))
        business_key_count = int(len(sorted_key_rows))

        max_watermark = min_watermark = None
        if watermark_column:
            max_watermark = to_jsonable(group[watermark_column].max())
            min_watermark = to_jsonable(group[watermark_column].min())

        partition_hash = _build_partition_hash(partition_value, row_count, business_key_count, max_watermark, min_watermark, business_key_hash)
        rows.append(
            {
                "dataset_name": str(dataset_name),
                "table_name": str(table_name),
                "run_id": run_id,
                "engine": "pandas",
                "generated_at": generated_at,
                "partition_column": str(partition_column),
                "partition_value": to_jsonable(partition_value),
                "row_count": row_count,
                "business_key_count": business_key_count,
                "max_watermark": max_watermark,
                "min_watermark": min_watermark,
                "partition_hash": partition_hash,
                "business_key_hash": business_key_hash,
            }
        )

    return sorted(rows, key=lambda r: str(r["partition_value"]))


def _build_spark_partition_snapshot(df, *, dataset_name: str, table_name: str, partition_column: str, business_keys: list[str], watermark_column: str | None, run_id: str | None) -> list[dict]:
    from pyspark.sql import functions as F

    generated_at = datetime.now(timezone.utc).isoformat()
    key_cols = [F.coalesce(F.col(c).cast("string"), F.lit("")) for c in business_keys]
    with_key = df.withColumn("_business_key_row_hash", F.sha2(F.concat_ws("||", *key_cols), 256))
    agg_exprs = [
        F.count(F.lit(1)).alias("row_count"),
        F.countDistinct(*[F.col(c) for c in business_keys]).alias("business_key_count"),
        F.sha2(F.concat_ws("##", F.sort_array(F.collect_set(F.col("_business_key_row_hash")))), 256).alias("business_key_hash"),
    ]
    if watermark_column:
        agg_exprs.extend([F.max(F.col(watermark_column)).alias("max_watermark"), F.min(F.col(watermark_column)).alias("min_watermark")])
    else:
        agg_exprs.extend([F.lit(None).alias("max_watermark"), F.lit(None).alias("min_watermark")])

    snapshot_df = with_key.groupBy(F.col(partition_column)).agg(*agg_exprs)
    collected = snapshot_df.collect()
    rows = []
    for row in collected:
        part_val = row[partition_column]
        max_w = to_jsonable(row["max_watermark"])
        min_w = to_jsonable(row["min_watermark"])
        bkh = str(row["business_key_hash"])
        rows.append(
            {
                "dataset_name": str(dataset_name),
                "table_name": str(table_name),
                "run_id": run_id,
                "engine": "spark",
                "generated_at": generated_at,
                "partition_column": str(partition_column),
                "partition_value": to_jsonable(part_val),
                "row_count": int(row["row_count"]),
                "business_key_count": int(row["business_key_count"]),
                "max_watermark": max_w,
                "min_watermark": min_w,
                "partition_hash": _build_partition_hash(part_val, int(row["row_count"]), int(row["business_key_count"]), max_w, min_w, bkh),
                "business_key_hash": bkh,
            }
        )
    return sorted(rows, key=lambda r: str(r["partition_value"]))


def build_partition_snapshot(df, *, dataset_name: str = "unknown", table_name: str = "unknown", partition_column: str, business_keys: list[str], watermark_column: str | None = None, run_id: str | None = None, engine: str = "auto") -> list[dict]:
    """Build partition snapshot.

    Execute `build_partition_snapshot`.

    Parameters
    ----------
    df : Any
        Value for `df`.
    dataset_name : str, optional
        Value for `dataset_name`.
    table_name : str, optional
        Value for `table_name`.
    partition_column : str
        Value for `partition_column`.
    business_keys : list[str]
        Value for `business_keys`.
    watermark_column : str | None, optional
        Value for `watermark_column`.
    run_id : str | None, optional
        Value for `run_id`.
    engine : str, optional
        Value for `engine`.

    Returns
    -------
    result : list[dict]
        Result returned by `build_partition_snapshot`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> build_partition_snapshot(df, dataset_name)
    """
    selected_engine = validate_engine(engine)
    if selected_engine == "auto":
        selected_engine = detect_dataframe_engine(df)

    columns = set(getattr(df, "columns", []))
    if partition_column not in columns:
        raise ValueError(f"Missing partition column '{partition_column}'.")
    missing_keys = [c for c in business_keys if c not in columns]
    if missing_keys:
        raise ValueError(f"Missing business key columns: {missing_keys}")
    if watermark_column and watermark_column not in columns:
        raise ValueError(f"Missing watermark column '{watermark_column}'.")

    if selected_engine == "pandas":
        return _build_pandas_partition_snapshot(df, dataset_name=dataset_name, table_name=table_name, partition_column=partition_column, business_keys=business_keys, watermark_column=watermark_column, run_id=run_id)
    if selected_engine == "spark":
        return _build_spark_partition_snapshot(df, dataset_name=dataset_name, table_name=table_name, partition_column=partition_column, business_keys=business_keys, watermark_column=watermark_column, run_id=run_id)
    raise ValueError(f"Unsupported engine '{selected_engine}'.")


def _is_closed_partition(partition_value: Any, grace_days: int) -> bool:
    if grace_days == 0:
        return True
    try:
        parsed = datetime.fromisoformat(str(partition_value)).date()
    except ValueError:
        try:
            parsed = date.fromisoformat(str(partition_value))
        except ValueError:
            return True
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=grace_days)
    return parsed < cutoff


def compare_partition_snapshots(baseline_snapshots: list[dict], current_snapshots: list[dict], policy: dict | None = None) -> dict:
    """Compare partition snapshots.

    Execute `compare_partition_snapshots`.

    Parameters
    ----------
    baseline_snapshots : list[dict]
        Value for `baseline_snapshots`.
    current_snapshots : list[dict]
        Value for `current_snapshots`.
    policy : dict | None, optional
        Value for `policy`.

    Returns
    -------
    result : dict
        Result returned by `compare_partition_snapshots`.

    Examples
    --------
    >>> compare_partition_snapshots(baseline_snapshots, current_snapshots)
    """
    active_policy = {**default_incremental_safety_policy(), **(policy or {})}
    baseline = {str(s.get("partition_value")): s for s in baseline_snapshots}
    current = {str(s.get("partition_value")): s for s in current_snapshots}
    changes = []

    def add_change(drift_type: str, partition_value: str, previous_value, current_value, default_message: str) -> None:
        is_closed = _is_closed_partition(partition_value, int(active_policy["closed_partition_grace_days"]))
        run_mode = str(active_policy.get("run_mode", "incremental"))
        block_default = is_closed and bool(active_policy["block_on_historical_partition_change"])
        severity, action = ("warning", "warn") if not block_default else ("critical", "block")

        if run_mode == "backfill":
            severity, action = "warning", "warn"
        elif bool(active_policy.get("allow_historical_changes")):
            approval_required = bool(active_policy.get("require_approval_for_historical_changes"))
            approval_reference = active_policy.get("approval_reference")
            if (not approval_required) or approval_reference:
                severity, action = "warning", "warn"
            else:
                severity, action = "critical", "block"

        if drift_type == "partition_added":
            severity, action = "info", "allow"

        changes.append({"drift_type": drift_type, "partition_value": partition_value, "previous_value": to_jsonable(previous_value), "current_value": to_jsonable(current_value), "severity": severity, "action": action, "message": default_message})

    for part in sorted(set(current) - set(baseline)):
        add_change("partition_added", part, None, current[part], f"Partition '{part}' is new in the current snapshot.")
    for part in sorted(set(baseline) - set(current)):
        add_change("partition_removed", part, baseline[part], None, f"Partition '{part}' exists in baseline but is missing in current snapshot.")

    for part in sorted(set(baseline).intersection(current)):
        b, c = baseline[part], current[part]
        for field, drift_type in [("row_count", "row_count_changed"), ("business_key_count", "business_key_count_changed"), ("max_watermark", "max_watermark_changed"), ("min_watermark", "min_watermark_changed"), ("business_key_hash", "business_key_hash_changed"), ("partition_hash", "partition_hash_changed")]:
            if b.get(field) != c.get(field):
                add_change(drift_type, part, b.get(field), c.get(field), f"Partition '{part}' field '{field}' changed.")

    blocking = sum(1 for ch in changes if ch["action"] == "block")
    warning = sum(1 for ch in changes if ch["action"] == "warn")
    status = "failed" if blocking else "warning" if warning else "passed"
    return {"status": status, "can_continue": blocking == 0, "changes": changes, "summary": {"partition_count_baseline": len(baseline), "partition_count_current": len(current), "change_count": len(changes), "blocking_change_count": blocking, "warning_change_count": warning}, "policy": active_policy}


def assert_incremental_safe(result: dict) -> None:
    """Assert incremental safe.

    Execute `assert_incremental_safe`.

    Parameters
    ----------
    result : dict
        Value for `result`.

    Returns
    -------
    result : None
        Result returned by `assert_incremental_safe`.

    Raises
    ------
    IncrementalSafetyError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> assert_incremental_safe(result)
    """
    if not bool(result.get("can_continue", True)):
        raise IncrementalSafetyError("Blocking incremental partition safety changes detected.")


def build_incremental_safety_records(result: dict, *, run_id: str, dataset_name: str, table_name: str) -> list[dict]:
    """Build incremental safety records.

    Execute `build_incremental_safety_records`.

    Parameters
    ----------
    result : dict
        Value for `result`.
    run_id : str
        Value for `run_id`.
    dataset_name : str
        Value for `dataset_name`.
    table_name : str
        Value for `table_name`.

    Returns
    -------
    result : list[dict]
        Result returned by `build_incremental_safety_records`.

    Examples
    --------
    >>> build_incremental_safety_records(result, run_id)
    """
    changes = result.get("changes", []) or [
        {
            "drift_type": "none",
            "partition_value": None,
            "previous_value": None,
            "current_value": None,
            "severity": "info",
            "action": "allow",
            "message": "No incremental partition changes detected.",
        }
    ]
    rows = []
    for change in changes:
        rows.append(
            to_jsonable(
                {
                    "run_id": run_id,
                    "dataset_name": dataset_name,
                    "table_name": table_name,
                    "status": result.get("status", "passed"),
                    "can_continue": bool(result.get("can_continue", True)),
                    "drift_type": change.get("drift_type"),
                    "partition_value": change.get("partition_value"),
                    "previous_value": change.get("previous_value"),
                    "current_value": change.get("current_value"),
                    "severity": change.get("severity"),
                    "action": change.get("action"),
                    "message": change.get("message"),
                }
            )
        )
    return rows
