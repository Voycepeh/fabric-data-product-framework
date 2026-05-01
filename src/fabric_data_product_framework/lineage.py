"""Lightweight lineage and transformation summary helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from dataclasses import asdict, dataclass

_ALLOWED_TYPES = {"dataframe", "lakehouse_table", "warehouse_table", "file", "unknown"}
_ALLOWED_CONFIDENCE = {"high", "medium", "low"}


@dataclass
class TransformationStep:
    """Transformationstep.

    Public class used by the framework API for `TransformationStep`.

    Examples
    --------
    >>> TransformationStep(... )
    """
    step_id: str
    step_name: str
    input_name: str
    output_name: str
    description: str
    reason: str
    transformation_type: str = "custom"
    columns_used: list[str] | None = None
    columns_created: list[str] | None = None
    business_impact: str | None = None
    notes: str | None = None


def _clean_list(values: list[str] | None) -> list[str]:
    """Normalize optional string lists by dropping blank values."""
    return [str(v) for v in (values or []) if str(v).strip()]


def _unique(values: list[str]) -> list[str]:
    seen = set()
    ordered = []
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def _safe_node_id(raw: str, prefix: str = "node") -> str:
    """Create Mermaid/graph-safe node identifiers from free-text names."""
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", (raw or "").strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return f"{prefix}_{cleaned or 'unknown'}"




class LineageRecorder:
    """Lineagerecorder.

    Public class used by the framework API for `LineageRecorder`.

    Examples
    --------
    >>> LineageRecorder(... )
    """
    def __init__(self, dataset_name: str, run_id: str | None = None, source_tables: list[str] | None = None, target_table: str | None = None) -> None:
        self.dataset_name = dataset_name
        self.run_id = run_id
        self.source_tables = _clean_list(source_tables)
        self.target_table = target_table
        self._steps: list[TransformationStep] = []

    def add_step(self, *, step_id: str, step_name: str, input_name: str, output_name: str, description: str, reason: str, transformation_type: str = "custom", columns_used: list[str] | None = None, columns_created: list[str] | None = None, business_impact: str | None = None, notes: str | None = None) -> dict:
        """Add step.

        Use this callable to support the framework workflow step implemented by `add_step`.

        Parameters
        ----------
        step_id : str
            Input value for `step_id`.
        step_name : str
            Input value for `step_name`.
        input_name : str
            Input value for `input_name`.
        output_name : str
            Input value for `output_name`.
        description : str
            Input value for `description`.
        reason : str
            Input value for `reason`.
        transformation_type : str, optional
            Input value for `transformation_type`.
        columns_used : list[str] | None, optional
            Input value for `columns_used`.
        columns_created : list[str] | None, optional
            Input value for `columns_created`.
        business_impact : str | None, optional
            Input value for `business_impact`.
        notes : str | None, optional
            Input value for `notes`.

        Returns
        -------
        result : dict
            Output produced by `add_step`.

        Examples
        --------
        >>> add_step(step_id, step_name)
        """
        step = TransformationStep(step_id=step_id, step_name=step_name, input_name=input_name, output_name=output_name, description=description, reason=reason, transformation_type=transformation_type, columns_used=_clean_list(columns_used), columns_created=_clean_list(columns_created), business_impact=business_impact, notes=notes)
        self._steps.append(step)
        return asdict(step)

    def to_records(self) -> list[dict]:
        """To records.

        Use this callable to support the framework workflow step implemented by `to_records`.

        Parameters
        ----------
        None
            This callable does not require user-provided parameters.

        Returns
        -------
        result : list[dict]
            Output produced by `to_records`.

        Examples
        --------
        >>> to_records()
        """
        return [asdict(step) for step in self._steps]

    def build_summary(self) -> dict:
        """Build summary.

        Use this callable to support the framework workflow step implemented by `build_summary`.

        Parameters
        ----------
        None
            This callable does not require user-provided parameters.

        Returns
        -------
        result : dict
            Output produced by `build_summary`.

        Examples
        --------
        >>> build_summary()
        """
        steps = self.to_records()
        return {"dataset_name": self.dataset_name, "run_id": self.run_id, "source_tables": self.source_tables, "target_table": self.target_table, "step_count": len(steps), "steps": steps, "columns_used": _unique([c for s in steps for c in s.get("columns_used", [])]), "columns_created": _unique([c for s in steps for c in s.get("columns_created", [])]), "transformation_types": _unique([s.get("transformation_type", "custom") for s in steps]), "summary_text": f"Recorded {len(steps)} transformation step(s) from {len(self.source_tables)} source table(s) to {self.target_table or 'target not set'}."}


def generate_mermaid_lineage(*, source_tables: list[str], target_table: str, transformation_steps: list[dict], graph_direction: str = "LR") -> str:
    """Generate mermaid lineage.

    Use this callable to support the framework workflow step implemented by `generate_mermaid_lineage`.

    Parameters
    ----------
    source_tables : list[str]
        Input value for `source_tables`.
    target_table : str
        Input value for `target_table`.
    transformation_steps : list[dict]
        Input value for `transformation_steps`.
    graph_direction : str, optional
        Input value for `graph_direction`.

    Returns
    -------
    result : str
        Output produced by `generate_mermaid_lineage`.

    Examples
    --------
    >>> generate_mermaid_lineage(source_tables, target_table)
    """
    direction = graph_direction if graph_direction in {"LR", "TD", "RL", "BT"} else "LR"
    lines = [f"flowchart {direction}"]
    steps = transformation_steps or []
    step_nodes = []
    for step in steps:
        sid = step.get("step_id", "step")
        name = step.get("step_name", "Unnamed step")
        node_id = _safe_node_id(f"step_{sid}", prefix="step")
        label = f"{sid}: {name}".replace('"', "'")
        step_nodes.append(node_id)
        lines.append(f'    {node_id}["{label}"]')
    source_nodes = []
    for idx, table in enumerate(source_tables or [], start=1):
        node = _safe_node_id(f"source_{idx}_{table}", prefix="source")
        source_nodes.append(node)
        lines.append(f'    {node}["{str(table).replace(chr(34), chr(39))}"]')
    target_node = _safe_node_id(target_table or "target", prefix="target")
    lines.append(f'    {target_node}["{(target_table or "target").replace(chr(34), chr(39))}"]')
    if step_nodes:
        for node in source_nodes:
            lines.append(f"    {node} --> {step_nodes[0]}")
        for i in range(len(step_nodes)-1):
            lines.append(f"    {step_nodes[i]} --> {step_nodes[i+1]}")
        lines.append(f"    {step_nodes[-1]} --> {target_node}")
    else:
        for node in source_nodes:
            lines.append(f"    {node} --> {target_node}")
    return "\n".join(lines)


def build_transformation_summary_markdown(summary: dict, *, include_mermaid: bool = True) -> str:
    """Build transformation summary markdown.

    Use this callable to support the framework workflow step implemented by `build_transformation_summary_markdown`.

    Parameters
    ----------
    summary : dict
        Input value for `summary`.
    include_mermaid : bool, optional
        Input value for `include_mermaid`.

    Returns
    -------
    result : str
        Output produced by `build_transformation_summary_markdown`.

    Examples
    --------
    >>> build_transformation_summary_markdown(summary, include_mermaid)
    """
    steps = summary.get("steps", []) or []
    lines = [
        f"## Transformation Summary — {summary.get('dataset_name', 'unknown')}",
        f"- Run ID: `{summary.get('run_id') or 'not_provided'}`",
        f"- Source tables: `{', '.join(summary.get('source_tables', []) or ['not_provided'])}`",
        f"- Target table: `{summary.get('target_table') or 'not_provided'}`",
        f"- Step count: `{summary.get('step_count', len(steps))}`",
        f"- Columns used: `{', '.join(summary.get('columns_used', []) or ['none'])}`",
        f"- Columns created: `{', '.join(summary.get('columns_created', []) or ['none'])}`",
        "",
        "### Steps",
    ]
    if steps:
        for step in steps:
            lines.extend([
                f"- **{step.get('step_id', 'step')} — {step.get('step_name', 'Unnamed')}**",
                f"  - Reason: {step.get('reason', 'not_provided')}",
                f"  - Description: {step.get('description', 'not_provided')}",
                f"  - Business impact: {step.get('business_impact') or 'not_provided'}",
            ])
    else:
        lines.append("- No transformation steps recorded.")
    if include_mermaid:
        mermaid = generate_mermaid_lineage(source_tables=summary.get("source_tables", []), target_table=summary.get("target_table") or "target", transformation_steps=steps)
        lines.extend(["", "### Lineage Diagram", "```mermaid", mermaid, "```"])
    return "\n".join(lines)


def build_lineage_prompt_context(*, dataset_name: str, source_tables: list[str], target_table: str, transformation_steps: list[dict], eda_notes: str | None = None) -> str:
    """Build lineage prompt context.

    Use this callable to support the framework workflow step implemented by `build_lineage_prompt_context`.

    Parameters
    ----------
    dataset_name : str
        Input value for `dataset_name`.
    source_tables : list[str]
        Input value for `source_tables`.
    target_table : str
        Input value for `target_table`.
    transformation_steps : list[dict]
        Input value for `transformation_steps`.
    eda_notes : str | None, optional
        Input value for `eda_notes`.

    Returns
    -------
    result : str
        Output produced by `build_lineage_prompt_context`.

    Examples
    --------
    >>> build_lineage_prompt_context(dataset_name, source_tables)
    """
    lines = [
        "Use this context to draft or review a lineage explanation.",
        "Do not invent transformations not listed here.",
        "",
        f"- Dataset: `{dataset_name}`",
        f"- Source tables: `{', '.join(_clean_list(source_tables) or ['not_provided'])}`",
        f"- Target table: `{target_table}`",
        "",
        "## Transformation Steps",
    ]
    if transformation_steps:
        for step in transformation_steps:
            lines.extend([
                f"- **{step.get('step_id', 'step')} — {step.get('step_name', 'Unnamed step')}**",
                f"  - Reason: {step.get('reason', 'not_provided')}",
                f"  - Columns used: {', '.join(_clean_list(step.get('columns_used')) or ['none'])}",
                f"  - Columns created: {', '.join(_clean_list(step.get('columns_created')) or ['none'])}",
            ])
    else:
        lines.append("- No transformation steps were recorded.")
    lines.extend(["", "## EDA Notes", eda_notes or "Not provided."])
    return "\n".join(lines)
def get_fabric_copilot_lineage_prompt() -> str:
    """Get fabric copilot lineage prompt.

    Use this callable to support the framework workflow step implemented by `get_fabric_copilot_lineage_prompt`.

    Parameters
    ----------
    None
        This callable does not require user-provided parameters.

    Returns
    -------
    result : str
        Output produced by `get_fabric_copilot_lineage_prompt`.

    Examples
    --------
    >>> get_fabric_copilot_lineage_prompt()
    """
    return """You are assisting with notebook-level lineage inside a Microsoft Fabric notebook.\nscan the entire current Fabric notebook before answering: inspect markdown, comments, section headers, EDA notes, and Python code cells.\nInspect Spark and Pandas DataFrame assignments and transformations including reads, writes, joins, filters, select/selectExpr, withColumn, groupBy, aggregations, unions, drops, renames, window functions, lakehouse reads, warehouse reads, file reads, table writes, and final outputs.\nIdentify only meaningful lineage steps. Ignore temporary diagnostics unless they affect final output. Infer the business/analytical reason from notebook context when possible.\nReturn ONLY valid Python code that defines lineage_steps = [...] using this exact schema and field names:\n\nlineage_steps = [\n    {\n        \"source\": \"<source dataframe/table/file>\",\n        \"target\": \"<target dataframe/table/file>\",\n        \"transformation\": \"<short technical summary>\",\n        \"reason\": \"<business or analytical reason>\",\n        \"source_type\": \"<dataframe|lakehouse_table|warehouse_table|file|unknown>\",\n        \"target_type\": \"<dataframe|lakehouse_table|warehouse_table|file|unknown>\",\n        \"confidence\": \"<high|medium|low>\",\n        \"notes\": \"<optional review note>\"\n    }\n]\n\nUse \"Needs human review\" if the reason cannot be inferred confidently.\nDo not invent business context. For Fabric notebook rendering, use matplotlib + networkx and avoid Mermaid.\nThis output must be reviewed by a human before approval and storage.\n"""


def validate_lineage_steps(lineage_steps) -> dict:
    """Validate lineage steps.

    Use this callable to support the framework workflow step implemented by `validate_lineage_steps`.

    Parameters
    ----------
    lineage_steps : Any
        Input value for `lineage_steps`.

    Returns
    -------
    result : dict
        Output produced by `validate_lineage_steps`.

    Examples
    --------
    >>> validate_lineage_steps(lineage_steps)
    """
    errors: list[str] = []
    warnings: list[str] = []
    review_required = False
    required_fields = ["source", "target", "transformation", "reason", "source_type", "target_type", "confidence"]

    if not isinstance(lineage_steps, list):
        return {"is_valid": False, "errors": ["lineage_steps must be a list."], "warnings": [], "review_required": True}
    if len(lineage_steps) == 0:
        return {
            "is_valid": False,
            "errors": ["lineage_steps cannot be empty. Paste Copilot generated lineage_steps first."],
            "warnings": [],
            "review_required": True,
        }

    for idx, step in enumerate(lineage_steps, start=1):
        if not isinstance(step, dict):
            errors.append(f"Step {idx}: each lineage step must be a dict.")
            continue
        for field in required_fields:
            if field not in step:
                errors.append(f"Step {idx}: missing required field '{field}'.")

        source = str(step.get("source", "")).strip()
        target = str(step.get("target", "")).strip()
        transformation = str(step.get("transformation", "")).strip()
        reason = str(step.get("reason", "")).strip()
        source_type = str(step.get("source_type", "")).strip()
        target_type = str(step.get("target_type", "")).strip()
        confidence = str(step.get("confidence", "")).strip().lower()

        if not source:
            errors.append(f"Step {idx}: source cannot be empty.")
        if not target:
            errors.append(f"Step {idx}: target cannot be empty.")
        if not transformation:
            errors.append(f"Step {idx}: transformation cannot be empty.")
        if not reason:
            errors.append(f"Step {idx}: reason cannot be empty.")

        if source_type and source_type not in _ALLOWED_TYPES:
            errors.append(f"Step {idx}: source_type must be one of {sorted(_ALLOWED_TYPES)}.")
        if target_type and target_type not in _ALLOWED_TYPES:
            errors.append(f"Step {idx}: target_type must be one of {sorted(_ALLOWED_TYPES)}.")
        if confidence and confidence not in _ALLOWED_CONFIDENCE:
            errors.append(f"Step {idx}: confidence must be one of {sorted(_ALLOWED_CONFIDENCE)}.")

        if confidence == "low":
            review_required = True
            warnings.append(f"Step {idx}: low confidence requires human review.")
        if reason == "Needs human review":
            review_required = True
            warnings.append(f"Step {idx}: reason requires human review.")
        if source_type == "unknown" or target_type == "unknown":
            review_required = True
            warnings.append(f"Step {idx}: unknown type requires human review.")

    return {"is_valid": len(errors) == 0, "errors": errors, "warnings": warnings, "review_required": review_required}


def build_lineage_record_from_steps(dataset_name, lineage_steps, run_id=None, notebook_name=None, workspace_name=None, created_by=None) -> list[dict]:
    """Build lineage record from steps.

    Use this callable to support the framework workflow step implemented by `build_lineage_record_from_steps`.

    Parameters
    ----------
    dataset_name : Any
        Input value for `dataset_name`.
    lineage_steps : Any
        Input value for `lineage_steps`.
    run_id : Any, optional
        Input value for `run_id`.
    notebook_name : Any, optional
        Input value for `notebook_name`.
    workspace_name : Any, optional
        Input value for `workspace_name`.
    created_by : Any, optional
        Input value for `created_by`.

    Returns
    -------
    result : list[dict]
        Output produced by `build_lineage_record_from_steps`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> build_lineage_record_from_steps(dataset_name, lineage_steps)
    """
    validation = validate_lineage_steps(lineage_steps)
    if not validation["is_valid"]:
        raise ValueError(f"Invalid lineage_steps: {validation['errors']}")
    created_ts = datetime.now(timezone.utc).isoformat()
    rows = []
    for idx, step in enumerate(lineage_steps, start=1):
        rows.append({
            "dataset_name": dataset_name,
            "step_number": idx,
            "source": step.get("source"),
            "target": step.get("target"),
            "transformation": step.get("transformation"),
            "reason": step.get("reason"),
            "source_type": step.get("source_type"),
            "target_type": step.get("target_type"),
            "confidence": step.get("confidence"),
            "notes": step.get("notes", ""),
            "run_id": run_id,
            "notebook_name": notebook_name,
            "workspace_name": workspace_name,
            "created_by": created_by,
            "created_ts": created_ts,
        })
    return rows


def build_lineage_records(*, dataset_name: str, run_id: str, source_tables: list[str], target_table: str, transformation_steps: list[dict]) -> list[dict]:
    """Build lineage records.

    Use this callable to support the framework workflow step implemented by `build_lineage_records`.

    Parameters
    ----------
    dataset_name : str
        Input value for `dataset_name`.
    run_id : str
        Input value for `run_id`.
    source_tables : list[str]
        Input value for `source_tables`.
    target_table : str
        Input value for `target_table`.
    transformation_steps : list[dict]
        Input value for `transformation_steps`.

    Returns
    -------
    result : list[dict]
        Output produced by `build_lineage_records`.

    Examples
    --------
    >>> build_lineage_records(dataset_name, run_id)
    """
    return [{"run_id": run_id, "dataset_name": dataset_name, "source_tables": _clean_list(source_tables), "target_table": target_table, "step_id": step.get("step_id"), "step_name": step.get("step_name"), "input_name": step.get("input_name"), "output_name": step.get("output_name"), "transformation_type": step.get("transformation_type", "custom"), "columns_used": _clean_list(step.get("columns_used")), "columns_created": _clean_list(step.get("columns_created")), "description": step.get("description"), "reason": step.get("reason"), "business_impact": step.get("business_impact"), "notes": step.get("notes")} for step in (transformation_steps or [])]


def build_lineage_record(*, dataset_name: str, run_id: str | None = None, lineage_steps: list[dict] | None = None, notebook_name: str | None = None, workspace_name: str | None = None, created_by: str | None = None) -> list[dict]:
    """Build lineage record.

    Use this callable to support the framework workflow step implemented by `build_lineage_record`.

    Parameters
    ----------
    dataset_name : str
        Input value for `dataset_name`.
    run_id : str | None, optional
        Input value for `run_id`.
    lineage_steps : list[dict] | None, optional
        Input value for `lineage_steps`.
    notebook_name : str | None, optional
        Input value for `notebook_name`.
    workspace_name : str | None, optional
        Input value for `workspace_name`.
    created_by : str | None, optional
        Input value for `created_by`.

    Returns
    -------
    result : list[dict]
        Output produced by `build_lineage_record`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> build_lineage_record(dataset_name, run_id)
    """
    if lineage_steps is None:
        raise ValueError("lineage_steps is required. Use get_fabric_copilot_lineage_prompt() to generate notebook lineage steps via Fabric Copilot.")
    return build_lineage_record_from_steps(dataset_name, lineage_steps, run_id, notebook_name, workspace_name, created_by)


def plot_lineage_networkx(lineage_steps_or_record, title=None):
    """Plot lineage networkx.

    Use this callable to support the framework workflow step implemented by `plot_lineage_networkx`.

    Parameters
    ----------
    lineage_steps_or_record : Any
        Input value for `lineage_steps_or_record`.
    title : Any, optional
        Input value for `title`.

    Returns
    -------
    result : Any
        Output produced by `plot_lineage_networkx`.

    Raises
    ------
    ImportError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> plot_lineage_networkx(lineage_steps_or_record, title)
    """
    try:
        import matplotlib.pyplot as plt
    except Exception as ex:
        raise ImportError("matplotlib is required for plot_lineage_networkx. Install matplotlib.") from ex
    try:
        import networkx as nx
    except Exception as ex:
        raise ImportError("networkx is required for plot_lineage_networkx. Install networkx.") from ex

    steps = lineage_steps_or_record or []
    if steps and "step_number" in steps[0]:
        normalized = steps
    else:
        normalized = build_lineage_record_from_steps("lineage", steps)

    g = nx.DiGraph()
    for row in normalized:
        src = row.get("source")
        tgt = row.get("target")
        tfm = (row.get("transformation") or "")[:36]
        g.add_node(src)
        g.add_node(tgt)
        g.add_edge(src, tgt, transformation=tfm, confidence=row.get("confidence", "medium"))

    layers: dict[str, int] = {}
    for u, v in g.edges():
        layers[v] = max(layers.get(v, 0), layers.get(u, 0) + 1)
        layers.setdefault(u, layers.get(u, 0))
    x_slots: dict[int, int] = {}
    pos = {}
    for node in g.nodes():
        y = -layers.get(node, 0)
        x = x_slots.get(layers.get(node, 0), 0)
        x_slots[layers.get(node, 0)] = x + 1
        pos[node] = (x, y)

    fig, ax = plt.subplots(figsize=(12, 6))
    edge_colors = ["#d62728" if g.edges[e].get("confidence") == "low" else "#4c78a8" for e in g.edges()]
    nx.draw_networkx_nodes(g, pos, node_size=1800, node_color="#f2f2f2", ax=ax)
    nx.draw_networkx_labels(g, pos, font_size=9, ax=ax)
    nx.draw_networkx_edges(g, pos, edge_color=edge_colors, arrows=True, arrowstyle="-|>", ax=ax)
    edge_labels = {(u, v): g.edges[(u, v)].get("transformation", "") for u, v in g.edges()}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=7, ax=ax)
    ax.set_title(title or "Notebook lineage")
    ax.axis("off")
    plt.tight_layout()
    return g, fig, ax
