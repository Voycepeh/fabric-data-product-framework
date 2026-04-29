"""Schema drift snapshot and comparison helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib


class SchemaDriftError(Exception):
    """Raised when schema drift contains blocking changes."""


class UnsupportedDataFrameEngineError(Exception):
    """Raised when schema snapshotting cannot identify a supported dataframe engine."""


VALID_ENGINES = {"auto", "pandas", "spark"}


def default_schema_drift_policy() -> dict:
    return {
        "block_on_removed_column": True,
        "block_on_type_change": True,
        "warn_on_added_column": True,
        "require_approval_for_new_columns": True,
        "warn_on_nullable_change": True,
        "warn_on_ordinal_change": False,
    }


def detect_dataframe_engine(df) -> str:
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
    if not bool(result.get("can_continue", True)):
        raise SchemaDriftError("Blocking schema drift detected.")
