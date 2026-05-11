"""Notebook lineage utilities: deterministic scan, optional AI enrichment, validation, records, and plotting."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from typing import Any

_ALLOWED_TYPES = {"dataframe", "lakehouse_table", "warehouse_table", "file", "unknown"}
_ALLOWED_CONFIDENCE = {"high", "medium", "low"}
READ_HELPERS = {"lakehouse_table_read": "lakehouse_table", "warehouse_read": "warehouse_table", "lakehouse_csv_read": "file", "lakehouse_excel_read_as_spark": "file", "lakehouse_parquet_read_as_spark": "file"}
WRITE_HELPERS = {"lakehouse_table_write": "lakehouse_table", "warehouse_write": "warehouse_table"}


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
    if cname == "lakehouse_table_write":
        return _literal(call.args[2]) if len(call.args) >= 3 else "unknown_lakehouse_table"
    if cname == "warehouse_write":
        if len(call.args) >= 5:
            return f"{_literal(call.args[3]) or 'schema'}.{_literal(call.args[4]) or 'table'}"
        return "unknown_warehouse_table"
    return "unknown_target"


def _step(source: str, target: str, transformation: str, source_type: str, target_type: str, confidence: str, lineno: int, ops: list[str], notes: str = "") -> dict[str, Any]:
    return {"source": source, "target": target, "transformation": transformation, "reason": "", "source_type": source_type, "target_type": target_type, "confidence": confidence, "notes": notes, "operation_types": ops, "code_refs": [f"line:{lineno}"]}


def scan_notebook_lineage(code: str) -> list[dict[str, Any]]:
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


def scan_notebook_cells(cells: list[str]) -> list[dict[str, Any]]:
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
        for step in scan_notebook_lineage(cell):
            step["code_refs"].append(f"cell:{idx}")
            out.append(step)
    return out


def fallback_copilot_lineage_prompt(lineage_steps: list[dict[str, Any]]) -> str:
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


def enrich_lineage_steps_with_ai(lineage_steps: list[dict[str, Any]], ai_helper: Any | None = None) -> dict[str, Any]:
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
        return {"steps": lineage_steps, "ai_used": False, "fallback_prompt": fallback_copilot_lineage_prompt(lineage_steps), "notes": "AI helper unavailable; Copilot fallback prompt generated."}
    return {"steps": ai_helper(lineage_steps) or lineage_steps, "ai_used": True, "fallback_prompt": "", "notes": "AI enrichment applied."}


def validate_lineage_steps(lineage_steps: Any) -> dict[str, Any]:
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


def build_lineage_record_from_steps(dataset_name: str, lineage_steps: list[dict], run_id: str | None = None, notebook_name: str | None = None, workspace_name: str | None = None, created_by: str | None = None) -> list[dict]:
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
    v = validate_lineage_steps(lineage_steps)
    if not v["is_valid"]:
        raise ValueError(f"Invalid lineage_steps: {v['errors']}")
    ts = datetime.now(timezone.utc).isoformat()
    return [{"dataset_name": dataset_name, "step_number": i, **s, "run_id": run_id, "notebook_name": notebook_name, "workspace_name": workspace_name, "created_by": created_by, "created_ts": ts} for i, s in enumerate(lineage_steps, 1)]


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


def build_lineage_from_notebook_code(code: str, use_ai: bool = True, ai_helper: Any | None = None) -> dict[str, Any]:
    """Scan, optionally enrich, and validate lineage from notebook source code.

    Parameters
    ----------
    code : str
        Notebook source code to parse.
    use_ai : bool, default=True
        Whether to invoke AI enrichment when a helper is provided.
    ai_helper : Any or None, default=None
        Optional callable used to enrich deterministic lineage steps.

    Returns
    -------
    dict of str to Any
        End-to-end lineage result with steps, validation, review status, and notes.
    """
    steps = scan_notebook_lineage(code)
    enrichment = enrich_lineage_steps_with_ai(steps, ai_helper=ai_helper) if use_ai else {"steps": steps, "ai_used": False, "fallback_prompt": "", "notes": "AI disabled."}
    validation = validate_lineage_steps(enrichment["steps"]) if enrichment["steps"] else {"is_valid": False, "errors": ["No lineage detected."], "warnings": [], "review_required": True}
    return {"steps": enrichment["steps"], "validation": validation, "review_required": True if not validation["is_valid"] else (validation["review_required"] or not enrichment.get("ai_used", False)), "fallback_prompt": enrichment.get("fallback_prompt", ""), "ai_used": enrichment.get("ai_used", False), "notes": enrichment.get("notes", "")}


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
    pos = nx.spring_layout(g, seed=42)
    nx.draw(g, pos, with_labels=True, node_color="#f2f2f2", ax=ax)
    nx.draw_networkx_edge_labels(g, pos, edge_labels={(u, v): d.get("label", "") for u, v, d in g.edges(data=True)}, font_size=7, ax=ax)
    ax.set_title(title or "Notebook lineage")
    return fig


def build_lineage_handover_markdown(result: dict[str, Any]) -> str:
    """Create a concise markdown handover summary from lineage execution results.

    Parameters
    ----------
    result : dict of str to Any
        Lineage result payload returned by ``build_lineage_from_notebook_code``.

    Returns
    -------
    str
        Markdown summary with step count, AI usage, and review requirement.
    """
    return f"## Lineage Handover\n- Steps: {len(result.get('steps', []))}\n- AI used: {result.get('ai_used')}\n- Review required: {result.get('review_required')}"
