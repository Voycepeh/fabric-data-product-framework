"""Metadata-backed handover/data-contract assembly and export helpers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .ai import build_handover_summary_prompt


def _approved_rows(rows: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    approved = []
    for row in rows or []:
        status = str(row.get("approval_status") or row.get("status") or "").lower()
        if status in {"approved", "active", "published", ""}:
            approved.append(dict(row))
    return approved


def _latest_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        k = str(row.get(key) or "")
        if not k:
            continue
        existing = grouped.get(k)
        if not existing or str(row.get("updated_at") or row.get("approved_at") or "") > str(existing.get("updated_at") or existing.get("approved_at") or ""):
            grouped[k] = row
    return grouped


def generate_handover_contract(*, contracts: list[dict[str, Any]], contract_columns: list[dict[str, Any]], contract_rules: list[dict[str, Any]], quality_results: list[dict[str, Any]], lineage_records: list[dict[str, Any]], dataset_name: str | None = None, table_name: str | None = None, ai_narrative: str | None = None, include_prompt: bool = False) -> dict[str, Any]:
    """Assemble a deterministic handover/data-contract package from approved metadata evidence.

    Parameters
    ----------
    contracts : list[dict[str, Any]]
        Contract header rows from the metadata contract store.
    contract_columns : list[dict[str, Any]]
        Contract column rows from the metadata contract store.
    contract_rules : list[dict[str, Any]]
        Approved DQ or contract rule rows from the metadata contract store.
    quality_results : list[dict[str, Any]]
        Executed quality-result evidence rows for the selected contract scope.
    lineage_records : list[dict[str, Any]]
        Lineage evidence rows for the selected contract scope.
    dataset_name : str | None, default=None
        Optional dataset filter.
    table_name : str | None, default=None
        Optional table filter.
    ai_narrative : str | None, default=None
        Optional AI-generated narrative text; this function does not run approval or mutation logic.
    include_prompt : bool, default=False
        Include a prompt template that callers can use with existing AI helpers.

    Returns
    -------
    dict[str, Any]
        Assembled handover package with metadata evidence, deterministic summary, and optional AI narrative input.
    """
    contracts_approved = _approved_rows(contracts)
    columns_approved = _approved_rows(contract_columns)
    rules_approved = _approved_rows(contract_rules)

    if dataset_name:
        contracts_approved = [r for r in contracts_approved if str(r.get("dataset_name") or "") == dataset_name]
        columns_approved = [r for r in columns_approved if str(r.get("dataset_name") or "") == dataset_name]
        rules_approved = [r for r in rules_approved if str(r.get("dataset_name") or "") == dataset_name]
        quality_results = [r for r in quality_results if str(r.get("dataset_name") or "") == dataset_name]
        lineage_records = [r for r in lineage_records if str(r.get("dataset_name") or "") == dataset_name]
    if table_name:
        columns_approved = [r for r in columns_approved if str(r.get("table_name") or "") == table_name]
        rules_approved = [r for r in rules_approved if str(r.get("table_name") or "") == table_name]
        quality_results = [r for r in quality_results if str(r.get("table_name") or "") == table_name]

    latest_contract = list(_latest_by_key(contracts_approved, "contract_id").values())

    package = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "metadata_contract_store",
        "dataset_name": dataset_name or (latest_contract[0].get("dataset_name") if latest_contract else None),
        "table_name": table_name,
        "contracts": latest_contract,
        "contract_columns": columns_approved,
        "contract_rules": rules_approved,
        "quality_results": quality_results,
        "lineage_records": lineage_records,
        "summary": {
            "contract_count": len(latest_contract),
            "column_count": len(columns_approved),
            "rule_count": len(rules_approved),
            "quality_result_count": len(quality_results),
            "lineage_record_count": len(lineage_records),
        },
        "handover_narrative": ai_narrative or "",
        "governance_note": "AI content is narrative-only. Approval statuses and governance metadata are read-only inputs.",
    }
    if include_prompt:
        package["handover_summary_prompt"] = build_handover_summary_prompt()
    return package


def export_handover_contract(handover_contract: dict[str, Any], output_path: str, format: str = "yaml") -> str:
    """Export a handover package to reusable YAML or JSON.

    Parameters
    ----------
    handover_contract : dict[str, Any]
        Output of :func:`generate_handover_contract`.
    output_path : str
        Destination file path.
    format : str, default="yaml"
        Export format: ``yaml`` or ``json``.

    Returns
    -------
    str
        Output path written.

    Raises
    ------
    ValueError
        If ``format`` is unsupported.
    """
    selected = format.lower().strip()
    if selected == "json":
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(handover_contract, fh, indent=2, ensure_ascii=False, sort_keys=True)
        return output_path
    if selected == "yaml":
        try:
            import yaml  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise ValueError("YAML export requires PyYAML.") from exc
        with open(output_path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(handover_contract, fh, sort_keys=False, allow_unicode=True)
        return output_path
    raise ValueError("format must be 'yaml' or 'json'.")
