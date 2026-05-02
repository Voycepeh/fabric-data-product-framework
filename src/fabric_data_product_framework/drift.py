"""Schema drift snapshot and comparison helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib


class SchemaDriftError(Exception):
    """Schemadrifterror.

    Public class used by the framework API for `SchemaDriftError`.

    Examples
    --------
    >>> SchemaDriftError(... )
    """


class UnsupportedDataFrameEngineError(Exception):
    """Unsupporteddataframeengineerror.

    Public class used by the framework API for `UnsupportedDataFrameEngineError`.

    Examples
    --------
    >>> UnsupportedDataFrameEngineError(... )
    """


VALID_ENGINES = {"auto", "pandas", "spark"}


def default_schema_drift_policy() -> dict:
    """Default schema drift policy.

    Run `default_schema_drift_policy`.

    Parameters
    ----------
    None
        This callable does not require user-provided parameters.

    Returns
    -------
    result : dict
        Return value from `default_schema_drift_policy`.

    Examples
    --------
    >>> default_schema_drift_policy()
    """
    return {
        "block_on_removed_column": True,
        "block_on_type_change": True,
        "warn_on_added_column": True,
        "require_approval_for_new_columns": True,
        "warn_on_nullable_change": True,
        "warn_on_ordinal_change": False,
    }


def detect_dataframe_engine(df) -> str:
    """Detect dataframe engine.

    Run `detect_dataframe_engine`.

    Parameters
    ----------
    df : Any
        Parameter `df`.

    Returns
    -------
    result : str
        Return value from `detect_dataframe_engine`.

    Raises
    ------
    UnsupportedDataFrameEngineError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> detect_dataframe_engine(df)
    """
    module_name = type(df).__module__
    if module_name.startswith("pandas") and hasattr(df, "dtypes") and hasattr(df, "columns"):
        return "pandas"

    has_spark_shape = hasattr(df, "schema") and hasattr(df, "columns") and hasattr(getattr(df, "schema"), "fields")
    if module_name.startswith("pyspark.sql") or has_spark_shape:
        return "spark"

    raise UnsupportedDataFrameEngineError(
        f"Unsupported dataframe engine for type '{type(df).__name__}' from module '{module_name}'."
    )


def _column_hash(column_name: str, ordinal_position: int, data_type: str, nullable: bool) -> str:
    payload = f"{column_name}|{ordinal_position}|{data_type}|{nullable}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_pandas_schema_snapshot(df, dataset_name: str, table_name: str) -> dict:
    columns = []
    for index, column_name in enumerate(df.columns):
        data_type = str(df[column_name].dtype)
        nullable = bool(df[column_name].isna().any())
        ordinal_position = int(index)
        columns.append(
            {
                "column_name": str(column_name),
                "ordinal_position": ordinal_position,
                "data_type": data_type,
                "nullable": nullable,
                "column_hash": _column_hash(str(column_name), ordinal_position, data_type, nullable),
            }
        )

    return {
        "dataset_name": str(dataset_name),
        "table_name": str(table_name),
        "engine": "pandas",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "columns": columns,
    }


def _build_spark_schema_snapshot(df, dataset_name: str, table_name: str) -> dict:
    columns = []
    for index, field in enumerate(df.schema.fields):
        column_name = str(field.name)
        data_type = str(field.dataType)
        nullable = bool(field.nullable)
        ordinal_position = int(index)
        columns.append(
            {
                "column_name": column_name,
                "ordinal_position": ordinal_position,
                "data_type": data_type,
                "nullable": nullable,
                "column_hash": _column_hash(column_name, ordinal_position, data_type, nullable),
            }
        )

    return {
        "dataset_name": str(dataset_name),
        "table_name": str(table_name),
        "engine": "spark",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "columns": columns,
    }


def build_schema_snapshot(df, dataset_name: str = "unknown", table_name: str = "unknown", engine: str = "auto") -> dict:
    """Build schema snapshot.

    Run `build_schema_snapshot`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    dataset_name : str, optional
        Parameter `dataset_name`.
    table_name : str, optional
        Parameter `table_name`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `build_schema_snapshot`.

    Raises
    ------
    UnsupportedDataFrameEngineError
        Raised when input validation or runtime checks fail.
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> build_schema_snapshot(df, dataset_name)
    """
    if engine not in VALID_ENGINES:
        raise ValueError(f"Unsupported engine '{engine}'. Expected one of: {sorted(VALID_ENGINES)}")

    resolved_engine = detect_dataframe_engine(df) if engine == "auto" else engine

    if resolved_engine == "pandas":
        return _build_pandas_schema_snapshot(df, dataset_name=dataset_name, table_name=table_name)
    if resolved_engine == "spark":
        return _build_spark_schema_snapshot(df, dataset_name=dataset_name, table_name=table_name)

    raise UnsupportedDataFrameEngineError(f"Unable to build snapshot for engine '{resolved_engine}'.")


def _resolve_change_behavior(is_warning: bool, is_blocking: bool) -> tuple[str, str]:
    if is_blocking:
        return "critical", "block"
    if is_warning:
        return "warning", "warn"
    return "info", "allow"


def compare_schema_snapshots(baseline_snapshot: dict, current_snapshot: dict, policy: dict | None = None) -> dict:
    """Compare schema snapshots.

    Run `compare_schema_snapshots`.

    Parameters
    ----------
    baseline_snapshot : dict
        Parameter `baseline_snapshot`.
    current_snapshot : dict
        Parameter `current_snapshot`.
    policy : dict | None, optional
        Parameter `policy`.

    Returns
    -------
    result : dict
        Return value from `compare_schema_snapshots`.

    Examples
    --------
    >>> compare_schema_snapshots(baseline_snapshot, current_snapshot)
    """
    active_policy = {**default_schema_drift_policy(), **(policy or {})}

    baseline_columns = {col["column_name"]: col for col in baseline_snapshot.get("columns", [])}
    current_columns = {col["column_name"]: col for col in current_snapshot.get("columns", [])}
    changes: list[dict] = []

    def add_change(drift_type: str, column_name: str, previous_value, current_value, severity: str, action: str, message: str) -> None:
        changes.append(
            {
                "drift_type": drift_type,
                "column_name": str(column_name),
                "previous_value": previous_value,
                "current_value": current_value,
                "severity": severity,
                "action": action,
                "message": message,
            }
        )

    for column_name in sorted(set(current_columns) - set(baseline_columns)):
        severity, action = _resolve_change_behavior(
            bool(active_policy["warn_on_added_column"]), bool(active_policy["require_approval_for_new_columns"])
        )
        add_change("column_added", column_name, None, current_columns[column_name], severity, action, f"Column '{column_name}' was added.")

    for column_name in sorted(set(baseline_columns) - set(current_columns)):
        severity, action = _resolve_change_behavior(True, bool(active_policy["block_on_removed_column"]))
        add_change("column_removed", column_name, baseline_columns[column_name], None, severity, action, f"Column '{column_name}' was removed.")

    for column_name in sorted(set(baseline_columns).intersection(current_columns)):
        base = baseline_columns[column_name]
        curr = current_columns[column_name]

        if base["data_type"] != curr["data_type"]:
            severity, action = _resolve_change_behavior(True, bool(active_policy["block_on_type_change"]))
            add_change("data_type_changed", column_name, base["data_type"], curr["data_type"], severity, action, f"Column '{column_name}' data type changed.")

        if bool(base["nullable"]) != bool(curr["nullable"]):
            severity, action = _resolve_change_behavior(bool(active_policy["warn_on_nullable_change"]), False)
            add_change("nullable_changed", column_name, bool(base["nullable"]), bool(curr["nullable"]), severity, action, f"Column '{column_name}' nullability changed.")

        if int(base["ordinal_position"]) != int(curr["ordinal_position"]):
            severity, action = _resolve_change_behavior(bool(active_policy["warn_on_ordinal_change"]), False)
            add_change("ordinal_changed", column_name, int(base["ordinal_position"]), int(curr["ordinal_position"]), severity, action, f"Column '{column_name}' ordinal position changed.")

    blocking_change_count = sum(1 for change in changes if change["action"] == "block")
    warning_change_count = sum(1 for change in changes if change["action"] == "warn")

    status = "failed" if blocking_change_count > 0 else "warning" if warning_change_count > 0 else "passed"
    can_continue = blocking_change_count == 0

    return {
        "dataset_name": str(current_snapshot.get("dataset_name") or baseline_snapshot.get("dataset_name") or "unknown"),
        "table_name": str(current_snapshot.get("table_name") or baseline_snapshot.get("table_name") or "unknown"),
        "baseline_engine": str(baseline_snapshot.get("engine", "unknown")),
        "current_engine": str(current_snapshot.get("engine", "unknown")),
        "status": status,
        "can_continue": can_continue,
        "changes": changes,
        "summary": {
            "added_columns": sum(1 for c in changes if c["drift_type"] == "column_added"),
            "removed_columns": sum(1 for c in changes if c["drift_type"] == "column_removed"),
            "type_changed_columns": sum(1 for c in changes if c["drift_type"] == "data_type_changed"),
            "nullable_changed_columns": sum(1 for c in changes if c["drift_type"] == "nullable_changed"),
            "ordinal_changed_columns": sum(1 for c in changes if c["drift_type"] == "ordinal_changed"),
            "blocking_change_count": blocking_change_count,
            "warning_change_count": warning_change_count,
        },
    }


def assert_no_blocking_schema_drift(result: dict) -> None:
    """Assert no blocking schema drift.

    Run `assert_no_blocking_schema_drift`.

    Parameters
    ----------
    result : dict
        Parameter `result`.

    Returns
    -------
    result : None
        Return value from `assert_no_blocking_schema_drift`.

    Raises
    ------
    SchemaDriftError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> assert_no_blocking_schema_drift(result)
    """
    if not bool(result.get("can_continue", True)):
        raise SchemaDriftError("Blocking schema drift detected.")


# --- merged from drift_checkers.py ---


from datetime import datetime, timezone
import json

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

    Run `check_schema_drift`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    baseline_snapshot : dict | None, optional
        Parameter `baseline_snapshot`.
    policy : dict | None, optional
        Parameter `policy`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `check_schema_drift`.

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

    Run `build_and_write_schema_snapshot`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    df : Any
        Parameter `df`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    metadata_table : str
        Parameter `metadata_table`.
    run_id : str | None, optional
        Parameter `run_id`.
    mode : str, optional
        Parameter `mode`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `build_and_write_schema_snapshot`.

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

    Run `load_latest_schema_snapshot`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    metadata_table : str
        Parameter `metadata_table`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.

    Returns
    -------
    result : dict | None
        Return value from `load_latest_schema_snapshot`.

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

    Run `check_partition_drift`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    partition_column : str
        Parameter `partition_column`.
    business_keys : list[str] | None, optional
        Parameter `business_keys`.
    watermark_column : str | None, optional
        Parameter `watermark_column`.
    baseline_snapshot : list[dict] | dict | None, optional
        Parameter `baseline_snapshot`.
    policy : dict | None, optional
        Parameter `policy`.
    run_id : str | None, optional
        Parameter `run_id`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `check_partition_drift`.

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

    Run `build_and_write_partition_snapshot`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    df : Any
        Parameter `df`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    metadata_table : str
        Parameter `metadata_table`.
    partition_column : str
        Parameter `partition_column`.
    business_keys : list[str] | None, optional
        Parameter `business_keys`.
    watermark_column : str | None, optional
        Parameter `watermark_column`.
    run_id : str | None, optional
        Parameter `run_id`.
    mode : str, optional
        Parameter `mode`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict
        Return value from `build_and_write_partition_snapshot`.

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

    Run `load_latest_partition_snapshot`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    metadata_table : str
        Parameter `metadata_table`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.

    Returns
    -------
    result : list[dict] | dict | None
        Return value from `load_latest_partition_snapshot`.

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

    Run `check_profile_drift`.

    Parameters
    ----------
    current_profile : dict
        Parameter `current_profile`.
    baseline_profile : dict | None, optional
        Parameter `baseline_profile`.
    policy : dict | None, optional
        Parameter `policy`.

    Returns
    -------
    result : dict
        Return value from `check_profile_drift`.

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

    Run `summarize_drift_results`.

    Parameters
    ----------
    schema_drift_result : dict | None, optional
        Parameter `schema_drift_result`.
    partition_drift_result : dict | None, optional
        Parameter `partition_drift_result`.
    profile_drift_result : dict | None, optional
        Parameter `profile_drift_result`.

    Returns
    -------
    result : dict
        Return value from `summarize_drift_results`.

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
