"""Fabric runtime identity helpers."""

from __future__ import annotations

from typing import Any


_ID_ERROR = (
    "FabricOps could not fetch the current notebook identity from "
    "notebookutils.runtime.context. Run inside a Fabric notebook or pass "
    "notebook identity explicitly."
)


def _read_context_value(ctx: Any, keys: list[str]) -> str | None:
    for key in keys:
        value = None
        if isinstance(ctx, dict):
            value = ctx.get(key)
        else:
            value = getattr(ctx, key, None)
            if value is None:
                getter = getattr(ctx, "get", None)
                if callable(getter):
                    value = getter(key)
        if value is not None and str(value).strip() != "":
            return str(value)
    return None


def get_current_notebook_identity(strict: bool = True) -> dict:
    """Return Fabric notebook/workspace identity from ``notebookutils.runtime.context``."""
    error: str | None = None
    raw_context: dict[str, Any] = {}
    ctx: Any = None

    try:
        from notebookutils import runtime  # type: ignore

        ctx = runtime.context
        if callable(ctx):
            ctx = ctx()
        if isinstance(ctx, dict):
            raw_context = dict(ctx)
        else:
            as_dict = getattr(ctx, "asDict", None)
            if callable(as_dict):
                raw_context = dict(as_dict())
            else:
                attrs = getattr(ctx, "__dict__", None)
                if isinstance(attrs, dict):
                    raw_context = dict(attrs)
    except Exception:
        error = _ID_ERROR
        if strict:
            raise RuntimeError(_ID_ERROR) from None

    workspace_id = _read_context_value(ctx, ["workspaceId", "currentWorkspaceId", "tridentWorkspaceId"]) if ctx is not None else None
    workspace_name = _read_context_value(ctx, ["workspaceName", "currentWorkspaceName"]) if ctx is not None else None
    notebook_id = _read_context_value(ctx, ["notebookId", "currentNotebookId", "artifactId", "itemId"]) if ctx is not None else None
    notebook_name = _read_context_value(ctx, ["notebookName", "currentNotebookName", "artifactName", "itemName"]) if ctx is not None else None
    run_id = _read_context_value(ctx, ["runId", "activityRunId", "livyId", "sessionId"]) if ctx is not None else None

    if strict and (workspace_id is None or notebook_id is None):
        raise RuntimeError(_ID_ERROR)

    if not strict and (workspace_id is None or notebook_id is None):
        error = _ID_ERROR

    return {
        "workspace_id": workspace_id,
        "workspace_name": workspace_name,
        "notebook_id": notebook_id,
        "notebook_name": notebook_name,
        "run_id": run_id,
        "raw_context": raw_context,
        "error": error,
    }
