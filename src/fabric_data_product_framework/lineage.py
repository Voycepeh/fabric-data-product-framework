"""Notebook lineage orchestration: deterministic scan, optional AI enrichment, validation, and rendering."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

from .lineage_ai_enrichment import enrich_lineage_steps_with_ai
from .notebook_lineage_scan import scan_notebook_lineage

_ALLOWED_TYPES = {"dataframe", "lakehouse_table", "warehouse_table", "file", "unknown"}
_ALLOWED_CONFIDENCE = {"high", "medium", "low"}


def validate_lineage_steps(lineage_steps: Any) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    review_required = False
    required = ["source", "target", "transformation", "reason", "source_type", "target_type", "confidence"]
    if not isinstance(lineage_steps, list):
        return {"is_valid": False, "errors": ["lineage_steps must be a list."], "warnings": [], "review_required": True}
    if not lineage_steps:
        return {"is_valid": False, "errors": ["lineage_steps cannot be empty."], "warnings": [], "review_required": True}
    for i, step in enumerate(lineage_steps, 1):
        if not isinstance(step, dict):
            errors.append(f"Step {i}: each lineage step must be a dict.")
            review_required = True
            continue
        for f in required:
            if f not in step:
                errors.append(f"Step {i}: missing required field '{f}'.")
        if step.get("source_type") == "unknown" or step.get("target_type") == "unknown":
            review_required = True; warnings.append(f"Step {i}: unknown type requires human review.")
        if step.get("confidence") == "low":
            review_required = True; warnings.append(f"Step {i}: low confidence requires human review.")
        if step.get("source_type") and step.get("source_type") not in _ALLOWED_TYPES:
            errors.append(f"Step {i}: invalid source_type")
        if step.get("target_type") and step.get("target_type") not in _ALLOWED_TYPES:
            errors.append(f"Step {i}: invalid target_type")
        if step.get("confidence") and step.get("confidence") not in _ALLOWED_CONFIDENCE:
            errors.append(f"Step {i}: invalid confidence")
    return {"is_valid": not errors, "errors": errors, "warnings": warnings, "review_required": review_required}


def build_lineage_record_from_steps(dataset_name: str, lineage_steps: list[dict], run_id: str | None = None, notebook_name: str | None = None, workspace_name: str | None = None, created_by: str | None = None) -> list[dict]:
    v = validate_lineage_steps(lineage_steps)
    if not v["is_valid"]:
        raise ValueError(f"Invalid lineage_steps: {v['errors']}")
    ts = datetime.now(timezone.utc).isoformat()
    return [{"dataset_name": dataset_name, "step_number": i, **s, "run_id": run_id, "notebook_name": notebook_name, "workspace_name": workspace_name, "created_by": created_by, "created_ts": ts} for i, s in enumerate(lineage_steps, 1)]


def build_lineage_from_notebook_code(code: str, use_ai: bool = True, ai_helper: Any | None = None) -> dict[str, Any]:
    steps = scan_notebook_lineage(code)
    enrichment = enrich_lineage_steps_with_ai(steps, ai_helper=ai_helper) if use_ai else {"steps": steps, "ai_used": False, "fallback_prompt": "", "notes": "AI disabled."}
    validation = validate_lineage_steps(enrichment["steps"]) if enrichment["steps"] else {"is_valid": False, "errors": ["No lineage detected."], "warnings": [], "review_required": True}
    return {"steps": enrichment["steps"], "validation": validation, "review_required": True if not validation["is_valid"] else (validation["review_required"] or not enrichment.get("ai_used", False)), "fallback_prompt": enrichment.get("fallback_prompt", ""), "ai_used": enrichment.get("ai_used", False), "notes": enrichment.get("notes", "")}


def plot_lineage_steps(lineage_steps_or_record, title: str | None = None):
    import matplotlib.pyplot as plt
    import networkx as nx
    rows = lineage_steps_or_record
    if rows and "step_number" in rows[0]:
        rows = [{k: v for k, v in r.items()} for r in rows]
    g = nx.DiGraph()
    for s in rows:
        g.add_edge(s.get("source", "unknown"), s.get("target", "unknown"), label=s.get("transformation", ""))
    fig, ax = plt.subplots(figsize=(10, 5))
    pos = nx.spring_layout(g, seed=42)
    nx.draw(g, pos, with_labels=True, node_color="#f2f2f2", ax=ax)
    nx.draw_networkx_edge_labels(g, pos, edge_labels={(u, v): d.get("label", "") for u, v, d in g.edges(data=True)}, font_size=7, ax=ax)
    ax.set_title(title or "Notebook lineage")
    return fig

# compatibility helper still used by quality.py

def build_lineage_records(*, dataset_name: str, run_id: str, source_tables: list[str], target_table: str, transformation_steps: list[dict]) -> list[dict]:
    return [{"run_id": run_id, "dataset_name": dataset_name, "source_tables": source_tables, "target_table": target_table, **s} for s in transformation_steps]

def build_lineage_record(*, dataset_name: str, run_id: str | None = None, lineage_steps: list[dict] | None = None, notebook_name: str | None = None, workspace_name: str | None = None, created_by: str | None = None) -> list[dict]:
    if lineage_steps is None:
        raise ValueError("lineage_steps is required.")
    return build_lineage_record_from_steps(dataset_name, lineage_steps, run_id, notebook_name, workspace_name, created_by)


def plot_lineage_networkx(lineage_steps_or_record, title=None):
    fig = plot_lineage_steps(lineage_steps_or_record, title=title)
    return None, fig, None
