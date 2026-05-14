from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

from .metadata import write_metadata_rows

_SELECTED_AGREEMENT: dict[str, Any] | None = None


def _coerce_row_dicts(rows: Any) -> list[dict[str, Any]]:
    if rows is None:
        return []
    if hasattr(rows, "collect"):
        rows = rows.collect()
    out = []
    for row in rows:
        if hasattr(row, "asDict"):
            out.append(row.asDict(recursive=True))
        else:
            out.append(dict(row))
    return out


def _latest_distinct_agreements(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        agreement_id = str(row.get("agreement_id") or "").strip()
        if not agreement_id:
            continue
        cur = latest.get(agreement_id)
        row_ts = str(row.get("updated_at") or row.get("approved_at") or "")
        cur_ts = str((cur or {}).get("updated_at") or (cur or {}).get("approved_at") or "")
        if cur is None or row_ts >= cur_ts:
            latest[agreement_id] = row
    return list(latest.values())


def load_agreements(spark, metadata_table: str = "METADATA_DATA_AGREEMENT", missing_ok: bool = False) -> list[dict[str, Any]]:
    """Load latest distinct agreement rows for widget selection."""
    try:
        rows = _coerce_row_dicts(spark.table(metadata_table))
    except Exception:
        if missing_ok:
            return []
        raise RuntimeError("No agreements found. Run 01_data_sharing_agreement first.")
    picked = []
    for row in _latest_distinct_agreements(rows):
        picked.append(
            {
                "agreement_id": row.get("agreement_id"),
                "agreement_name": row.get("agreement_name") or row.get("agreement_id"),
                "approved_usage": row.get("approved_usage", ""),
                "business_context": row.get("business_context", ""),
                "ownership": row.get("ownership", ""),
                "updated_at": row.get("updated_at"),
                "approved_at": row.get("approved_at"),
            }
        )
    return picked


def _agreement_option_label(row: dict[str, Any]) -> str:
    return f"{row.get('agreement_name') or row.get('agreement_id') or 'unknown'} | {row.get('agreement_id') or 'unknown'} | {row.get('approved_usage') or ''}"


def select_agreement(agreement_rows_or_df) -> None:
    """Render a widget dropdown and store selected agreement row in module state."""
    import ipywidgets as widgets
    from IPython.display import display

    global _SELECTED_AGREEMENT
    rows = _coerce_row_dicts(agreement_rows_or_df)
    if not rows:
        raise ValueError("No agreements found. Save a data agreement in notebook 01 first.")
    options = [(_agreement_option_label(r), r) for r in rows]
    dropdown = widgets.Dropdown(options=options, description="Agreement", layout=widgets.Layout(width="1000px"))

    def _on_change(change):
        if change.get("name") == "value" and change.get("new") is not None:
            _SELECTED_AGREEMENT = dict(change["new"])
            globals()["_SELECTED_AGREEMENT"] = _SELECTED_AGREEMENT

    dropdown.observe(_on_change)
    _SELECTED_AGREEMENT = dict(options[0][1])
    display(dropdown)


def get_selected_agreement() -> dict[str, Any]:
    """Return selected agreement from widget flow."""
    if not _SELECTED_AGREEMENT:
        raise RuntimeError("No agreement selected. Run select_agreement(...) and pick an agreement first.")
    return dict(_SELECTED_AGREEMENT)


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
