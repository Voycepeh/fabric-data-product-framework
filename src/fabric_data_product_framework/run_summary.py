"""Run summary builders for notebook handover and metadata logging."""

from __future__ import annotations

from datetime import datetime, timezone


def _status_of(section: dict | None) -> str:
    if not section:
        return "not_provided"
    return section.get("status", "not_provided")


def build_run_summary(*, runtime_context: dict, contract: dict | None = None, source_profile: dict | None = None, output_profile: dict | None = None, schema_drift_result: dict | None = None, incremental_safety_result: dict | None = None, quality_result: dict | None = None, contract_validation_result: dict | None = None, lineage_summary: dict | None = None, notes: list[str] | None = None) -> dict:
    sections = {
        "purpose": (contract or {}).get("dataset", {}).get("purpose"),
        "source_profile": source_profile,
        "output_profile": output_profile,
        "schema_drift": schema_drift_result,
        "incremental_safety": incremental_safety_result,
        "quality": quality_result,
        "contracts": contract_validation_result,
        "lineage": lineage_summary,
        "notes": notes or [],
    }
    considered = [v for k, v in sections.items() if k not in {"purpose", "notes"} and v]
    failed = any((v.get("can_continue") is False) or v.get("status") == "failed" for v in considered)
    warning = any(v.get("status") == "warning" for v in considered)
    overall = "failed" if failed else ("warning" if warning else "passed")
    can_continue = not failed
    action_items = []
    if failed:
        action_items.append("Investigate blocking checks before continuing.")
    if warning:
        action_items.append("Review warning checks and monitor downstream impact.")
    return {
        "run_id": runtime_context.get("run_id"),
        "dataset_name": runtime_context.get("dataset_name") or (contract or {}).get("dataset", {}).get("name"),
        "environment": runtime_context.get("environment"),
        "source_table": runtime_context.get("source_table"),
        "target_table": runtime_context.get("target_table"),
        "started_at_utc": runtime_context.get("started_at_utc"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall,
        "can_continue": can_continue,
        "sections": sections,
        "action_items": action_items,
    }


def render_run_summary_markdown(summary: dict) -> str:
    s = summary.get("sections", {})
    lines = [
        f"# Run Summary — {summary.get('dataset_name', 'unknown')}",
        f"- Run ID: `{summary.get('run_id', 'unknown')}`",
        f"- Environment: `{summary.get('environment', 'unknown')}`",
        f"- Overall status: **{summary.get('overall_status', 'unknown')}**",
        "",
        "## Run Context",
        f"- Source table: `{summary.get('source_table', 'unknown')}`",
        f"- Target table: `{summary.get('target_table', 'unknown')}`",
        f"- Started at (UTC): `{summary.get('started_at_utc', 'unknown')}`",
        "",
        "## Dataset Purpose",
        f"{s.get('purpose') or 'Not provided.'}",
        "",
        "## Section Status",
        f"- Schema drift: **{_status_of(s.get('schema_drift'))}**",
        f"- Incremental safety: **{_status_of(s.get('incremental_safety'))}**",
        f"- Quality: **{_status_of(s.get('quality'))}**",
        f"- Contracts: **{_status_of(s.get('contracts'))}**",
    ]
    src_count = (s.get("source_profile") or {}).get("row_count")
    out_count = (s.get("output_profile") or {}).get("row_count")
    lines.extend([f"- Source row count: `{src_count}`", f"- Output row count: `{out_count}`", "", "## Action Items"])
    action_items = summary.get("action_items", [])
    lines.extend([f"- {item}" for item in action_items] or ["- None"])
    notes = s.get("notes") or []
    lines.extend(["", "## Notes"])
    lines.extend([f"- {n}" for n in notes] or ["- None"])
    return "\n".join(lines)


def build_run_summary_record(summary: dict) -> dict:
    sections = summary.get("sections", {})
    record = {
        "run_id": summary.get("run_id"),
        "dataset_name": summary.get("dataset_name"),
        "environment": summary.get("environment"),
        "source_table": summary.get("source_table"),
        "target_table": summary.get("target_table"),
        "overall_status": summary.get("overall_status"),
        "can_continue": summary.get("can_continue"),
        "generated_at_utc": summary.get("generated_at_utc"),
        "source_row_count": (sections.get("source_profile") or {}).get("row_count"),
        "output_row_count": (sections.get("output_profile") or {}).get("row_count"),
        "schema_drift_status": _status_of(sections.get("schema_drift")),
        "incremental_safety_status": _status_of(sections.get("incremental_safety")),
        "quality_status": _status_of(sections.get("quality")),
        "contract_status": _status_of(sections.get("contracts")),
        "action_item_count": len(summary.get("action_items", [])),
        "summary_markdown": render_run_summary_markdown(summary),
    }
    return record
