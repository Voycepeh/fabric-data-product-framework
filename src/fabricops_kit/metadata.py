from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any
from .fabric_input_output import write_lakehouse_table

EVIDENCE_SOURCE_PROFILE = "source_profile"
EVIDENCE_OUTPUT_PROFILE = "output_profile"
EVIDENCE_DRIFT_RESULT = "drift_result"
EVIDENCE_LINEAGE = "lineage"
EVIDENCE_BUSINESS_CONTEXT = "business_context"
EVIDENCE_GOVERNANCE_CONTEXT = "governance_context"


def default_evidence_types() -> dict[str, str]:
    """Return canonical evidence type names used across metadata records."""
    return {
        "source_profile": EVIDENCE_SOURCE_PROFILE,
        "output_profile": EVIDENCE_OUTPUT_PROFILE,
        "drift_result": EVIDENCE_DRIFT_RESULT,
        "lineage": EVIDENCE_LINEAGE,
        "business_context": EVIDENCE_BUSINESS_CONTEXT,
        "governance_context": EVIDENCE_GOVERNANCE_CONTEXT,
    }


def build_evidence_row(*, dataset_name: str, table_name: str, run_id: str | None, evidence_type: str, payload_json: str, workspace_id: str | None = None, workspace_name: str | None = None, notebook_id: str | None = None, notebook_name: str | None = None, created_at: str | None = None) -> dict:
    """Build a lightweight metadata-ready evidence row."""
    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "run_id": run_id,
        "workspace_id": workspace_id,
        "workspace_name": workspace_name,
        "notebook_id": notebook_id,
        "notebook_name": notebook_name,
        "evidence_type": evidence_type,
        "payload_json": payload_json,
        "created_at": created_at or _now_utc_iso(),
    }


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
    write_lakehouse_table(df, metadata_path, table_name, mode=mode)
    return df


def write_column_business_context(spark, rows: list[dict], metadata_path, table_name: str = "METADATA_COLUMN_CONTEXT", mode: str = "append"):
    return write_metadata_rows(spark, rows, metadata_path, table_name, mode=mode)


def write_column_governance_context(spark, rows: list[dict], metadata_path, table_name: str = "METADATA_COLUMN_GOVERNANCE", mode: str = "append"):
    return write_metadata_rows(spark, rows, metadata_path, table_name, mode=mode)


def _runtime_context() -> dict[str, Any]:
    try:
        import notebookutils.runtime as nb_runtime  # type: ignore

        context = getattr(nb_runtime, "context", None)
        if isinstance(context, dict):
            return context
        getter = getattr(context, "get", None)
        keys = ["workspaceId", "workspaceName", "notebookId", "notebookName", "userName", "userId"]
        if callable(getter):
            return {k: getter(k) for k in keys}
    except Exception:
        pass
    return {}


def register_current_notebook(spark, metadata_path, agreement_id, notebook_type, environment_name=None, dataset_name=None, table_name=None, topic=None, pipeline_name=None, metadata_table="METADATA_NOTEBOOK_REGISTRY"):
    ctx = _runtime_context()
    notebook_name = ctx.get("notebookName") or "unknown_notebook"
    inferred_type = notebook_type or str(notebook_name).split("_", 1)[0]
    workspace_id = ctx.get("workspaceId")
    notebook_id = ctx.get("notebookId")
    row = {
        "agreement_id": agreement_id,
        "environment_name": environment_name,
        "dataset_name": dataset_name,
        "table_name": table_name,
        "topic": topic,
        "pipeline_name": pipeline_name,
        "notebook_type": inferred_type,
        "workspace_id": workspace_id,
        "workspace_name": ctx.get("workspaceName"),
        "notebook_id": notebook_id,
        "notebook_name": notebook_name,
        "notebook_url": f"https://app.fabric.microsoft.com/groups/{workspace_id}/notebooks/{notebook_id}" if workspace_id and notebook_id else None,
        "user_name": ctx.get("userName"),
        "user_id": ctx.get("userId"),
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    write_metadata_rows(spark, [row], metadata_path=metadata_path, table_name=metadata_table, mode="append")
    return row


def load_notebook_registry(spark, agreement_id, metadata_table="METADATA_NOTEBOOK_REGISTRY", notebook_type=None, environment_name=None, missing_ok: bool = True) -> list[dict[str, Any]]:
    try:
        rows = _coerce_row_dicts(spark.table(metadata_table))
    except Exception:
        if missing_ok:
            return []
        raise
    out = []
    for row in rows:
        if str(row.get("agreement_id") or "") != str(agreement_id):
            continue
        if notebook_type and str(row.get("notebook_type") or "") != str(notebook_type):
            continue
        if environment_name and str(row.get("environment_name") or "") != str(environment_name):
            continue
        out.append(row)
    return out
