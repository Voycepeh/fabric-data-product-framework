"""Run summary builders for notebook handover and metadata logging."""

from __future__ import annotations

from datetime import datetime, timezone


SECTION_KEYS = ["source_profile", "output_profile", "schema_drift", "incremental_safety", "quality", "contracts", "lineage"]


def _status_of(section: dict | None) -> str:
    if not section:
        return "not_provided"
    return section.get("status", "not_provided")


def build_run_summary(*, runtime_context: dict, contract: dict | None = None, source_profile: dict | None = None, output_profile: dict | None = None, schema_drift_result: dict | None = None, incremental_safety_result: dict | None = None, quality_result: dict | None = None, contract_validation_result: dict | None = None, lineage_summary: dict | None = None, notes: list[str] | None = None) -> dict:
    """Build a compact handover summary from pipeline run evidence.

    Parameters
    ----------
    runtime_context : dict
        Run context containing identifiers and environment details.
    contract : dict, optional
        Dataset contract used for purpose and dataset metadata.
    source_profile, output_profile, schema_drift_result, incremental_safety_result, quality_result, contract_validation_result, lineage_summary : dict, optional
        Optional section payloads included in the consolidated summary.
    notes : list of str, optional
        Additional handover notes.

    Returns
    -------
    dict
        Structured run summary with overall status, continuation signal,
        section payloads, and action items.
    """
    sections = {"purpose": (contract or {}).get("dataset", {}).get("purpose"), "source_profile": source_profile, "output_profile": output_profile, "schema_drift": schema_drift_result, "incremental_safety": incremental_safety_result, "quality": quality_result, "contracts": contract_validation_result, "lineage": lineage_summary, "notes": notes or []}
    not_provided_sections = [k for k in SECTION_KEYS if sections.get(k) is None]
    considered = [sections[k] for k in SECTION_KEYS if sections.get(k)]
    failed = any((v.get("can_continue") is False) or v.get("status") == "failed" for v in considered)
    warning = any(v.get("status") == "warning" for v in considered)
    overall = "failed" if failed else ("warning" if warning else "passed")
    action_items = []
    if failed:
        action_items.append("Investigate blocking checks before continuing.")
    if warning:
        action_items.append("Review warning checks and monitor downstream impact.")
    if not_provided_sections:
        action_items.append(f"Optional sections not provided: {', '.join(not_provided_sections)}.")
    return {"run_id": runtime_context.get("run_id"), "dataset_name": runtime_context.get("dataset_name") or (contract or {}).get("dataset", {}).get("name"), "environment": runtime_context.get("environment"), "source_table": runtime_context.get("source_table"), "target_table": runtime_context.get("target_table"), "started_at_utc": runtime_context.get("started_at_utc"), "generated_at_utc": datetime.now(timezone.utc).isoformat(), "overall_status": overall, "can_continue": not failed, "sections": sections, "not_provided_sections": not_provided_sections, "action_items": action_items}


def render_run_summary_markdown(summary: dict) -> str:
    """Render a pipeline run summary as handover-ready Markdown.

    Parameters
    ----------
    summary : dict
        Summary object produced by :func:`build_run_summary`.

    Returns
    -------
    str
        Markdown text suitable for handover or release notes.
    """
    s = summary.get("sections", {})
    lines = [f"# Run Summary — {summary.get('dataset_name', 'unknown')}", f"- Run ID: `{summary.get('run_id', 'unknown')}`", f"- Environment: `{summary.get('environment', 'unknown')}`", f"- Overall status: **{summary.get('overall_status', 'unknown')}**", "", "## Run Context", f"- Source table: `{summary.get('source_table', 'unknown')}`", f"- Target table: `{summary.get('target_table', 'unknown')}`", f"- Started at (UTC): `{summary.get('started_at_utc', 'unknown')}`", "", "## Dataset Purpose", f"{s.get('purpose') or 'Not provided.'}", "", "## Section Status", f"- Schema drift: **{_status_of(s.get('schema_drift'))}**", f"- Incremental safety: **{_status_of(s.get('incremental_safety'))}**", f"- Quality: **{_status_of(s.get('quality'))}**", f"- Contracts: **{_status_of(s.get('contracts'))}**"]
    lines.extend(["", "## Not Provided Sections"])
    lines.extend([f"- {n}" for n in summary.get("not_provided_sections", [])] or ["- None"])
    src_count = (s.get("source_profile") or {}).get("row_count")
    out_count = (s.get("output_profile") or {}).get("row_count")
    lines.extend(["", f"- Source row count: `{src_count}`", f"- Output row count: `{out_count}`", "", "## Action Items"])
    lines.extend([f"- {item}" for item in summary.get("action_items", [])] or ["- None"])
    lines.extend(["", "## Notes"])
    lines.extend([f"- {n}" for n in (s.get("notes") or [])] or ["- None"])
    return "\n".join(lines)


def build_run_summary_record(summary: dict) -> dict:
    """Execute the `build_run_summary_record` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        summary : Any
            Input parameter `summary`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> build_run_summary_record(...)
        """
    sections = summary.get("sections", {})
    return {"run_id": summary.get("run_id"), "dataset_name": summary.get("dataset_name"), "environment": summary.get("environment"), "source_table": summary.get("source_table"), "target_table": summary.get("target_table"), "overall_status": summary.get("overall_status"), "can_continue": summary.get("can_continue"), "generated_at_utc": summary.get("generated_at_utc"), "source_row_count": (sections.get("source_profile") or {}).get("row_count"), "output_row_count": (sections.get("output_profile") or {}).get("row_count"), "schema_drift_status": _status_of(sections.get("schema_drift")), "incremental_safety_status": _status_of(sections.get("incremental_safety")), "quality_status": _status_of(sections.get("quality")), "contract_status": _status_of(sections.get("contracts")), "action_item_count": len(summary.get("action_items", [])), "summary_markdown": render_run_summary_markdown(summary)}
