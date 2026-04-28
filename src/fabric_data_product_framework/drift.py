"""Schema drift snapshot and comparison helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib


class SchemaDriftError(Exception):
    """Raised when schema drift contains blocking changes."""



def default_schema_drift_policy() -> dict:
    """Return the default schema drift policy."""
    return {
        "block_on_removed_column": True,
        "block_on_type_change": True,
        "warn_on_added_column": True,
        "require_approval_for_new_columns": True,
        "warn_on_nullable_change": True,
        "warn_on_ordinal_change": False,
    }



def _column_hash(column_name: str, ordinal_position: int, data_type: str, nullable: bool) -> str:
    payload = f"{column_name}|{ordinal_position}|{data_type}|{nullable}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()



def build_schema_snapshot(df, dataset_name: str = "unknown", table_name: str = "unknown") -> dict:
    """Build a JSON-serializable schema snapshot for a pandas DataFrame."""
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
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "columns": columns,
    }



def _resolve_change_behavior(is_warning: bool, is_blocking: bool) -> tuple[str, str]:
    if is_blocking:
        return "critical", "block"
    if is_warning:
        return "warning", "warn"
    return "info", "allow"



def compare_schema_snapshots(baseline_snapshot: dict, current_snapshot: dict, policy: dict | None = None) -> dict:
    """Compare two schema snapshots and return drift findings."""
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
        is_warning = bool(active_policy["warn_on_added_column"])
        is_blocking = bool(active_policy["require_approval_for_new_columns"])
        severity, action = _resolve_change_behavior(is_warning, is_blocking)
        add_change(
            "column_added",
            column_name,
            None,
            current_columns[column_name],
            severity,
            action,
            f"Column '{column_name}' was added.",
        )

    for column_name in sorted(set(baseline_columns) - set(current_columns)):
        is_blocking = bool(active_policy["block_on_removed_column"])
        severity, action = _resolve_change_behavior(True, is_blocking)
        add_change(
            "column_removed",
            column_name,
            baseline_columns[column_name],
            None,
            severity,
            action,
            f"Column '{column_name}' was removed.",
        )

    shared_columns = sorted(set(baseline_columns).intersection(current_columns))
    for column_name in shared_columns:
        base = baseline_columns[column_name]
        curr = current_columns[column_name]

        if base["data_type"] != curr["data_type"]:
            is_blocking = bool(active_policy["block_on_type_change"])
            severity, action = _resolve_change_behavior(True, is_blocking)
            add_change(
                "data_type_changed",
                column_name,
                base["data_type"],
                curr["data_type"],
                severity,
                action,
                f"Column '{column_name}' data type changed.",
            )

        if bool(base["nullable"]) != bool(curr["nullable"]):
            is_warning = bool(active_policy["warn_on_nullable_change"])
            severity, action = _resolve_change_behavior(is_warning, False)
            add_change(
                "nullable_changed",
                column_name,
                bool(base["nullable"]),
                bool(curr["nullable"]),
                severity,
                action,
                f"Column '{column_name}' nullability changed.",
            )

        if int(base["ordinal_position"]) != int(curr["ordinal_position"]):
            is_warning = bool(active_policy["warn_on_ordinal_change"])
            severity, action = _resolve_change_behavior(is_warning, False)
            add_change(
                "ordinal_changed",
                column_name,
                int(base["ordinal_position"]),
                int(curr["ordinal_position"]),
                severity,
                action,
                f"Column '{column_name}' ordinal position changed.",
            )

    blocking_change_count = sum(1 for change in changes if change["action"] == "block")
    warning_change_count = sum(1 for change in changes if change["action"] == "warn")

    if blocking_change_count > 0:
        status = "failed"
        can_continue = False
    elif warning_change_count > 0:
        status = "warning"
        can_continue = True
    else:
        status = "passed"
        can_continue = True

    return {
        "dataset_name": str(current_snapshot.get("dataset_name") or baseline_snapshot.get("dataset_name") or "unknown"),
        "table_name": str(current_snapshot.get("table_name") or baseline_snapshot.get("table_name") or "unknown"),
        "status": status,
        "can_continue": can_continue,
        "changes": changes,
        "summary": {
            "added_columns": sum(1 for change in changes if change["drift_type"] == "column_added"),
            "removed_columns": sum(1 for change in changes if change["drift_type"] == "column_removed"),
            "type_changed_columns": sum(1 for change in changes if change["drift_type"] == "data_type_changed"),
            "nullable_changed_columns": sum(1 for change in changes if change["drift_type"] == "nullable_changed"),
            "ordinal_changed_columns": sum(1 for change in changes if change["drift_type"] == "ordinal_changed"),
            "blocking_change_count": blocking_change_count,
            "warning_change_count": warning_change_count,
        },
    }



def assert_no_blocking_schema_drift(result: dict) -> None:
    """Raise SchemaDriftError when the comparison has blocking changes."""
    if not bool(result.get("can_continue", True)):
        raise SchemaDriftError("Blocking schema drift detected.")
