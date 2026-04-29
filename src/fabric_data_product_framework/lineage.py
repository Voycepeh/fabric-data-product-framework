"""Lightweight lineage and transformation summary helpers."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass


@dataclass
class TransformationStep:
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
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", (raw or "").strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return f"{prefix}_{cleaned or 'unknown'}"


class LineageRecorder:
    def __init__(
        self,
        dataset_name: str,
        run_id: str | None = None,
        source_tables: list[str] | None = None,
        target_table: str | None = None,
    ) -> None:
        self.dataset_name = dataset_name
        self.run_id = run_id
        self.source_tables = _clean_list(source_tables)
        self.target_table = target_table
        self._steps: list[TransformationStep] = []

    def add_step(
        self,
        *,
        step_id: str,
        step_name: str,
        input_name: str,
        output_name: str,
        description: str,
        reason: str,
        transformation_type: str = "custom",
        columns_used: list[str] | None = None,
        columns_created: list[str] | None = None,
        business_impact: str | None = None,
        notes: str | None = None,
    ) -> dict:
        step = TransformationStep(
            step_id=step_id,
            step_name=step_name,
            input_name=input_name,
            output_name=output_name,
            description=description,
            reason=reason,
            transformation_type=transformation_type,
            columns_used=_clean_list(columns_used),
            columns_created=_clean_list(columns_created),
            business_impact=business_impact,
            notes=notes,
        )
        self._steps.append(step)
        return asdict(step)

    def to_records(self) -> list[dict]:
        return [asdict(step) for step in self._steps]

    def build_summary(self) -> dict:
        steps = self.to_records()
        columns_used = _unique([c for step in steps for c in step.get("columns_used", [])])
        columns_created = _unique([c for step in steps for c in step.get("columns_created", [])])
        transformation_types = _unique([step.get("transformation_type", "custom") for step in steps])
        return {
            "dataset_name": self.dataset_name,
            "run_id": self.run_id,
            "source_tables": self.source_tables,
            "target_table": self.target_table,
            "step_count": len(steps),
            "steps": steps,
            "columns_used": columns_used,
            "columns_created": columns_created,
            "transformation_types": transformation_types,
            "summary_text": f"Recorded {len(steps)} transformation step(s) from {len(self.source_tables)} source table(s) to {self.target_table or 'target not set'}.",
        }


def build_lineage_records(
    *,
    dataset_name: str,
    run_id: str,
    source_tables: list[str],
    target_table: str,
    transformation_steps: list[dict],
) -> list[dict]:
    records = []
    for step in transformation_steps or []:
        records.append(
            {
                "run_id": run_id,
                "dataset_name": dataset_name,
                "source_tables": _clean_list(source_tables),
                "target_table": target_table,
                "step_id": step.get("step_id"),
                "step_name": step.get("step_name"),
                "input_name": step.get("input_name"),
                "output_name": step.get("output_name"),
                "transformation_type": step.get("transformation_type", "custom"),
                "columns_used": _clean_list(step.get("columns_used")),
                "columns_created": _clean_list(step.get("columns_created")),
                "description": step.get("description"),
                "reason": step.get("reason"),
                "business_impact": step.get("business_impact"),
                "notes": step.get("notes"),
            }
        )
    return records


def generate_mermaid_lineage(*, source_tables: list[str], target_table: str, transformation_steps: list[dict], graph_direction: str = "LR") -> str:
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
        first_step = step_nodes[0]
        for node in source_nodes:
            lines.append(f"    {node} --> {first_step}")
        for i in range(len(step_nodes) - 1):
            lines.append(f"    {step_nodes[i]} --> {step_nodes[i + 1]}")
        lines.append(f"    {step_nodes[-1]} --> {target_node}")
    else:
        for node in source_nodes:
            lines.append(f"    {node} --> {target_node}")
    return "\n".join(lines)


def build_transformation_summary_markdown(summary: dict, *, include_mermaid: bool = True) -> str:
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
            impact = step.get("business_impact") or "not_provided"
            lines.extend(
                [
                    f"- **{step.get('step_id', 'step')} — {step.get('step_name', 'Unnamed')}**",
                    f"  - Reason: {step.get('reason', 'not_provided')}",
                    f"  - Description: {step.get('description', 'not_provided')}",
                    f"  - Business impact: {impact}",
                ]
            )
    else:
        lines.append("- No transformation steps recorded.")
    if include_mermaid:
        mermaid = generate_mermaid_lineage(source_tables=summary.get("source_tables", []), target_table=summary.get("target_table") or "target", transformation_steps=steps)
        lines.extend(["", "### Lineage Diagram", "```mermaid", mermaid, "```"])
    return "\n".join(lines)


def build_lineage_prompt_context(
    *,
    dataset_name: str,
    source_tables: list[str],
    target_table: str,
    transformation_steps: list[dict],
    eda_notes: str | None = None,
) -> str:
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
    steps = transformation_steps or []
    if steps:
        for step in steps:
            lines.extend(
                [
                    f"- **{step.get('step_id', 'step')} — {step.get('step_name', 'Unnamed step')}**",
                    f"  - Reason: {step.get('reason', 'not_provided')}",
                    f"  - Columns used: {', '.join(_clean_list(step.get('columns_used')) or ['none'])}",
                    f"  - Columns created: {', '.join(_clean_list(step.get('columns_created')) or ['none'])}",
                ]
            )
    else:
        lines.append("- No transformation steps were recorded.")
    lines.extend(["", "## EDA Notes", eda_notes or "Not provided."])
    return "\n".join(lines)
