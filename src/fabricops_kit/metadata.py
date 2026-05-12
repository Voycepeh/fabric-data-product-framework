from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from .fabric_input_output import lakehouse_table_write


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_action_by(action_by: str | None = None) -> str:
    if action_by:
        return str(action_by)
    try:
        import notebookutils.runtime as nb_runtime  # type: ignore

        context = getattr(nb_runtime, "context", None)
        if isinstance(context, dict):
            return context.get("userName") or context.get("userId") or "unknown"
        getter = getattr(context, "get", None)
        if callable(getter):
            return getter("userName") or getter("userId") or "unknown"
    except Exception:
        pass
    return "unknown"


def _key_part(value) -> str:
    return str(value or "").strip().lower()


def _sha256_key(*parts) -> str:
    normalized = "|".join(_key_part(p) for p in parts)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def build_metadata_table_key(environment_name, dataset_name, table_name) -> str:
    return _sha256_key(environment_name, dataset_name, table_name)


def build_metadata_column_key(environment_name, dataset_name, table_name, column_name) -> str:
    return _sha256_key(environment_name, dataset_name, table_name, column_name)


def build_dq_rule_key(environment_name, dataset_name, table_name, rule_id) -> str:
    return _sha256_key(environment_name, dataset_name, table_name, rule_id)


def _extract_columns_from_profile(profile_rows) -> list[str]:
    cols = []
    for row in profile_rows or []:
        c = row.get("column_name") or row.get("COLUMN_NAME")
        if c:
            cols.append(str(c))
    return sorted(set(cols))


def normalise_records_by_column(records) -> dict[str, dict]:
    out = {}
    for row in records or []:
        key = str(row.get("column_name") or row.get("COLUMN_NAME") or "")
        if key:
            out[key] = dict(row)
    return out


def column_context_rows_for_spark(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows or []:
        item = dict(row)
        if isinstance(item.get("approved_at"), datetime):
            item["approved_at"] = item["approved_at"].isoformat()
        if isinstance(item.get("ai_suggestion_json"), (dict, list)):
            item["ai_suggestion_json"] = json.dumps(item["ai_suggestion_json"], sort_keys=True)
        out.append(item)
    return out


def write_metadata_rows(spark, rows: list[dict], metadata_path, table_name: str, mode: str = "append"):
    """Write metadata rows to a lakehouse metadata table."""
    df = spark.createDataFrame(column_context_rows_for_spark(rows))
    lakehouse_table_write(df, metadata_path, table_name, mode=mode)
    return df


def write_column_business_context(spark, rows: list[dict], metadata_path, table_name: str = "METADATA_COLUMN_CONTEXT", mode: str = "append"):
    return write_metadata_rows(spark, rows, metadata_path, table_name, mode=mode)


def write_column_governance_context(spark, rows: list[dict], metadata_path, table_name: str = "METADATA_COLUMN_GOVERNANCE", mode: str = "append"):
    return write_metadata_rows(spark, rows, metadata_path, table_name, mode=mode)
