"""Notebook lineage helpers for deterministic parsing and metadata-ready evidence."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from typing import Any

_ALLOWED_TYPES = {"dataframe", "lakehouse_table", "warehouse_table", "file", "unknown"}
_ALLOWED_CONFIDENCE = {"high", "medium", "low"}
READ_HELPERS = {"read_lakehouse_table": "lakehouse_table", "read_warehouse_table": "warehouse_table", "read_lakehouse_csv": "file", "read_lakehouse_excel": "file", "read_lakehouse_parquet": "file"}
WRITE_HELPERS = {"write_lakehouse_table": "lakehouse_table", "write_warehouse_table": "warehouse_table"}


def _name(node: ast.AST) -> str | None:
    return node.id if isinstance(node, ast.Name) else None


def _call_name(call: ast.Call) -> str:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return "unknown"


def _flatten_chain(node: ast.AST) -> tuple[str | None, list[str]]:
    ops, cur = [], node
    while isinstance(cur, ast.Call) and isinstance(cur.func, ast.Attribute):
        ops.append(cur.func.attr)
        cur = cur.func.value
    return _name(cur), list(reversed(ops))


def _literal(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return node.id if isinstance(node, ast.Name) else None


def _resolve_write_target(cname: str, call: ast.Call) -> str:
    if cname == "write_lakehouse_table":
        return _literal(call.args[2]) if len(call.args) >= 3 else "unknown_lakehouse_table"
    if cname == "write_warehouse_table":
        if len(call.args) >= 5:
            return f"{_literal(call.args[3]) or 'schema'}.{_literal(call.args[4]) or 'table'}"
        return "unknown_warehouse_table"
    return "unknown_target"


def _step(source: str, target: str, transformation: str, source_type: str, target_type: str, confidence: str, lineno: int, ops: list[str], notes: str = "") -> dict[str, Any]:
    return {"source": source, "target": target, "transformation": transformation, "reason": "", "source_type": source_type, "target_type": target_type, "confidence": confidence, "notes": notes, "operation_types": ops, "code_refs": [f"line:{lineno}"]}


def _scan_notebook_lineage(code: str) -> list[dict[str, Any]]:
    """Extract deterministic lineage steps from notebook code using AST parsing.

    Parameters
    ----------
    code : str
        Python notebook source code to analyze.

    Returns
    -------
    list of dict of str to Any
        Ordered lineage step dictionaries inferred from read, transform, and write calls.
    """
    tree = ast.parse(code)
    steps: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets and isinstance(node.value, ast.Call):
            lhs = _name(node.targets[0])
            if not lhs:
                continue
            cname = _call_name(node.value)
            if cname in READ_HELPERS:
                steps.append(_step(cname, lhs, f"read via {cname}", READ_HELPERS[cname], "dataframe", "high", node.lineno, ["read"]))
                continue
            if cname in {"read_csv", "read_parquet", "read_excel"}:
                steps.append(_step(cname, lhs, f"read via pandas.{cname}", "file", "dataframe", "high", node.lineno, ["read"]))
                continue
            src, ops = _flatten_chain(node.value)
            if ops:
                steps.append(_step(src or "unknown", lhs, " -> ".join(ops), "dataframe" if src else "unknown", "dataframe", "high" if src else "medium", node.lineno, ops, "" if src else "base dataframe could not be inferred"))

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call, cname = node.value, _call_name(node.value)
            if cname in WRITE_HELPERS and call.args:
                src = _name(call.args[0]) or "unknown"
                steps.append(_step(src, _resolve_write_target(cname, call), f"write via {cname}", "dataframe" if src != "unknown" else "unknown", WRITE_HELPERS[cname], "high" if src != "unknown" else "medium", node.lineno, ["write"]))
    return steps


def _scan_notebook_cells(cells: list[str]) -> list[dict[str, Any]]:
    """Scan multiple notebook cells and append cell references to lineage steps.

    Parameters
    ----------
    cells : list of str
        Cell source strings in notebook execution order.

    Returns
    -------
    list of dict of str to Any
        Combined lineage steps with ``cell:<index>`` entries in ``code_refs``.
    """
    out: list[dict[str, Any]] = []
    for idx, cell in enumerate(cells):
        for step in _scan_notebook_lineage(cell):
            step["code_refs"].append(f"cell:{idx}")
            out.append(step)
    return out


def _fallback_copilot_lineage_prompt(lineage_steps: list[dict[str, Any]]) -> str:
    """Build a fallback Copilot prompt for manual lineage enrichment.

    Parameters
    ----------
    lineage_steps : list of dict of str to Any
        Deterministic lineage steps produced by the scanner.

    Returns
    -------
    str
        Prompt text instructing an AI helper to refine only reasoning fields.
    """
    return "Review these deterministic lineage steps and improve reasons/notes only; do not change structure. steps=" + str(lineage_steps)


def _enrich_lineage_steps_with_ai(lineage_steps: list[dict[str, Any]], ai_helper: Any | None = None) -> dict[str, Any]:
    """Optionally enrich deterministic lineage steps using an AI helper callable.

    Parameters
    ----------
    lineage_steps : list of dict of str to Any
        Deterministic lineage step dictionaries.
    ai_helper : Any or None, default=None
        Callable that accepts lineage steps and returns enriched steps.

    Returns
    -------
    dict of str to Any
        Enrichment payload containing steps, AI usage flag, fallback prompt, and notes.
    """
    if ai_helper is None:
        return {"steps": lineage_steps, "ai_used": False, "fallback_prompt": _fallback_copilot_lineage_prompt(lineage_steps), "notes": "AI helper unavailable; Copilot fallback prompt generated."}
    return {"steps": ai_helper(lineage_steps) or lineage_steps, "ai_used": True, "fallback_prompt": "", "notes": "AI enrichment applied."}


def _validate_lineage_steps(lineage_steps: Any) -> dict[str, Any]:
    """Validate lineage step structure and flag records requiring human review.

    Parameters
    ----------
    lineage_steps : Any
        Candidate lineage payload, expected to be a list of dictionaries.

    Returns
    -------
    dict of str to Any
        Validation result with ``is_valid``, ``errors``, ``warnings``, and ``review_required``.
    """
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
    return {"is_valid": not errors, "errors": errors, "warnings": warnings, "review_required": review_required}


def _build_lineage_record_from_steps(dataset_name: str, lineage_steps: list[dict], run_id: str | None = None, notebook_name: str | None = None, workspace_name: str | None = None, workspace_id: str | None = None, notebook_id: str | None = None, created_by: str | None = None) -> list[dict]:
    """Create metadata-ready lineage records from validated lineage steps.

    Parameters
    ----------
    dataset_name : str
        Dataset identifier associated with the lineage record set.
    lineage_steps : list of dict
        Validated lineage step dictionaries.
    run_id : str or None, default=None
        Optional run identifier for traceability.
    notebook_name : str or None, default=None
        Optional Fabric notebook name.
    workspace_name : str or None, default=None
        Optional workspace display name.
    created_by : str or None, default=None
        Optional creator identity string.

    Returns
    -------
    list of dict
        Lineage rows with step numbers and creation timestamp.

    Raises
    ------
    ValueError
        If lineage steps fail schema validation.
    """
    v = _validate_lineage_steps(lineage_steps)
    if not v["is_valid"]:
        raise ValueError(f"Invalid lineage_steps: {v['errors']}")
    ts = datetime.now(timezone.utc).isoformat()
    return [{"dataset_name": dataset_name, "step_number": i, **s, "run_id": run_id, "workspace_id": workspace_id, "workspace_name": workspace_name, "notebook_id": notebook_id, "notebook_name": notebook_name, "created_by": created_by, "created_ts": ts} for i, s in enumerate(lineage_steps, 1)]


def _build_lineage_records(dataset_name: str, lineage_steps: list[dict], run_id: str | None = None, notebook_name: str | None = None, workspace_name: str | None = None, workspace_id: str | None = None, notebook_id: str | None = None, created_by: str | None = None) -> list[dict]:
    """Build metadata-ready lineage rows from validated lineage steps.

    Parameters
    ----------
    dataset_name : str
        Dataset identifier associated with the lineage rows.
    lineage_steps : list of dict
        Validated lineage step dictionaries.
    run_id : str or None, default=None
        Optional run identifier.
    notebook_name : str or None, default=None
        Optional notebook name.
    workspace_name : str or None, default=None
        Optional workspace display name.
    created_by : str or None, default=None
        Optional creator identity.

    Returns
    -------
    list of dict
        Lineage rows suitable for metadata persistence.
    """
    return _build_lineage_record_from_steps(dataset_name, lineage_steps, run_id=run_id, notebook_name=notebook_name, workspace_name=workspace_name, workspace_id=workspace_id, notebook_id=notebook_id, created_by=created_by)


def build_lineage_records(*, dataset_name: str, run_id: str, source_tables: list[str], target_table: str, transformation_steps: list[dict]) -> list[dict]:
    """Build compact lineage records for downstream metadata sinks.

    Parameters
    ----------
    dataset_name : str
        Dataset identifier for all output rows.
    run_id : str
        Unique run identifier.
    source_tables : list of str
        Source table names captured for the run.
    target_table : str
        Target table name produced by the run.
    transformation_steps : list of dict
        Transformation step dictionaries to merge into each output row.

    Returns
    -------
    list of dict
        Row dictionaries suitable for metadata persistence.
    """
    return [{"run_id": run_id, "dataset_name": dataset_name, "source_tables": source_tables, "target_table": target_table, **s} for s in transformation_steps]


def plot_lineage_steps(lineage_steps_or_record, title: str | None = None):
    """Render lineage steps as a directed graph figure.

    Parameters
    ----------
    lineage_steps_or_record : iterable
        Lineage step dictionaries containing source, target, and transformation keys.
    title : str or None, default=None
        Optional chart title override.

    Returns
    -------
    matplotlib.figure.Figure
        Rendered lineage diagram figure.
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    g = nx.DiGraph()
    for s in lineage_steps_or_record:
        g.add_edge(s.get("source", "unknown"), s.get("target", "unknown"), label=s.get("transformation", ""))
    fig, ax = plt.subplots(figsize=(10, 5))
    pos = _build_top_down_lineage_layout(lineage_steps_or_record)
    nx.draw(g, pos, with_labels=True, node_color="#f2f2f2", ax=ax)
    nx.draw_networkx_edge_labels(g, pos, edge_labels={(u, v): d.get("label", "") for u, v, d in g.edges(data=True)}, font_size=7, ax=ax)
    ax.set_title(title or "Notebook lineage")
    return fig


def _build_top_down_lineage_layout(lineage_steps_or_record) -> dict[str, tuple[float, float]]:
    """Build a stable top-down layout for lineage graph plotting."""
    nodes: list[str] = []
    for step in lineage_steps_or_record:
        src = step.get("source", "unknown")
        tgt = step.get("target", "unknown")
        if src not in nodes:
            nodes.append(src)
        if tgt not in nodes:
            nodes.append(tgt)
    return {node: (0.0, float(-idx)) for idx, node in enumerate(nodes)}


def _build_lineage_summary_markdown(result: dict[str, Any]) -> str:
    """Create a concise markdown lineage summary from lineage execution results.

    Parameters
    ----------
    result : dict of str to Any
        Lineage result payload returned by ``build_lineage_from_notebook_code``.

    Returns
    -------
    str
        Markdown summary with step count, AI usage, and review requirement.
    """
    return f"## Lineage Summary\n- Steps: {len(result.get('steps', []))}\n- AI used: {result.get('ai_used')}\n- Review required: {result.get('review_required')}"


def build_lineage_handover_markdown(result: dict[str, Any]) -> str:
    """Backward-compatible alias for ``build_lineage_summary_markdown``."""
    return _build_lineage_summary_markdown(result)



def build_notebook_lineage(*, notebook_code: str | None = None, cells: list[str] | None = None, dataset_name: str = "unknown", table_name: str = "unknown", run_id: str | None = None, workspace_id: str | None = None, workspace_name: str | None = None, notebook_id: str | None = None, notebook_name: str | None = None, created_by: str | None = None) -> dict[str, Any]:
    """Build deterministic notebook lineage, validate it, and return metadata-ready records."""
    if notebook_code is None and cells is None:
        raise ValueError("Provide notebook_code or cells.")
    steps = _scan_notebook_lineage(notebook_code) if notebook_code is not None else _scan_notebook_cells(cells or [])
    validation = _validate_lineage_steps(steps) if steps else {"is_valid": False, "errors": ["No lineage detected."], "warnings": [], "review_required": True}
    records = []
    if validation["is_valid"]:
        records = _build_lineage_record_from_steps(
            dataset_name,
            steps,
            run_id=run_id,
            notebook_name=notebook_name,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            notebook_id=notebook_id,
            created_by=created_by,
        )
    result = {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "steps": steps,
        "validation": validation,
        "records": records,
        "review_required": True if not validation["is_valid"] else bool(validation.get("review_required", False)),
    }
    result["summary_markdown"] = _build_lineage_summary_markdown(result)
    return result


def build_lineage_from_notebook_code(code: str, use_ai: bool = True, ai_helper: Any | None = None) -> dict[str, Any]:
    """Backward-compatible alias to ``build_notebook_lineage``."""
    return build_notebook_lineage(notebook_code=code)


# Module-level compatibility aliases (not exported from package root)
scan_notebook_lineage = _scan_notebook_lineage
scan_notebook_cells = _scan_notebook_cells
validate_lineage_steps = _validate_lineage_steps
build_lineage_record_from_steps = _build_lineage_records
build_top_down_lineage_layout = _build_top_down_lineage_layout
build_lineage_summary_markdown = _build_lineage_summary_markdown
