"""Provider-neutral helpers for AI-assisted data quality rule generation."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from .quality import SUPPORTED_RULE_TYPES

SUPPORTED_CANDIDATE_FIELDS = {
    "rule_id",
    "table_name",
    "column",
    "columns",
    "layman_rule",
    "rule_type",
    "rule_config",
    "severity",
    "confidence",
    "reason",
    "evidence",
    "approval_status",
}


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return value


def build_quality_rule_prompt_context(profile, contract=None, business_context=None, table_name=None, dataset_name=None):
    profile = profile or {}
    return {
        "dataset_name": dataset_name or profile.get("dataset_name", "unknown"),
        "table_name": table_name or profile.get("table_name", "unknown"),
        "profile": _jsonable(profile),
        "contract": _jsonable(contract or {}),
        "business_context": _jsonable(business_context or {}),
        "supported_rule_types": sorted(SUPPORTED_RULE_TYPES),
        "candidate_fields": sorted(SUPPORTED_CANDIDATE_FIELDS),
    }


def build_quality_rule_generation_prompt(profile, contract=None, business_context=None, table_name=None, dataset_name=None):
    context = build_quality_rule_prompt_context(profile, contract, business_context, table_name, dataset_name)
    return (
        "You are generating conservative data quality rule candidates for Fabric data product workflows.\n"
        "Return JSON array only. Do not return markdown.\n"
        "Each array item must include human-readable 'layman_rule' and executable metadata fields: "
        "rule_id, table_name, column, columns, layman_rule, rule_type, rule_config, severity, confidence, reason, evidence, approval_status.\n"
        "Rules must be supported by profiling evidence only. Do not invent business rules.\n"
        "Use conservative suggestions, mark weak assumptions as low confidence.\n"
        "Do not set every column to not_null. Avoid accepted_values for high-cardinality columns. "
        "Avoid uniqueness unless distinct_count is close to row_count.\n"
        "Use severity='warning' by default unless business context clearly implies critical severity.\n"
        f"Supported rule types: {sorted(SUPPORTED_RULE_TYPES)}\n"
        f"Context JSON: {json.dumps(context, ensure_ascii=False)}"
    )


def _strip_json_fences(text: str) -> str:
    fenced = re.match(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", text, flags=re.DOTALL | re.IGNORECASE)
    return fenced.group(1) if fenced else text


def parse_ai_quality_rule_candidates(raw_response):
    try:
        if isinstance(raw_response, str):
            parsed = json.loads(_strip_json_fences(raw_response))
        else:
            parsed = raw_response
        if not isinstance(parsed, list):
            return {"ok": False, "candidates": [], "errors": ["AI response must be a JSON array"]}
    except Exception as exc:
        return {"ok": False, "candidates": [], "errors": [f"Invalid AI JSON response: {exc}"]}

    normalized = [normalize_quality_rule_candidate(c) for c in parsed if isinstance(c, dict)]
    errors = []
    for c in normalized:
        validation = validate_ai_quality_rule_candidate(c)
        if not validation["is_valid"]:
            errors.append(validation["message"])
    clean = [c for c in normalized if validate_ai_quality_rule_candidate(c)["is_valid"]]
    return {"ok": len(errors) == 0, "candidates": clean, "errors": errors}


def normalize_quality_rule_candidate(candidate):
    out = {k: v for k, v in candidate.items() if k in SUPPORTED_CANDIDATE_FIELDS}
    out["rule_type"] = str(out.get("rule_type", "")).strip().lower()
    out["severity"] = str(out.get("severity", "warning")).strip().lower() or "warning"
    out["confidence"] = str(out.get("confidence", "medium")).strip().lower() or "medium"
    out["approval_status"] = str(out.get("approval_status", "candidate")).strip().lower() or "candidate"
    out["rule_config"] = out.get("rule_config") if isinstance(out.get("rule_config"), dict) else {}
    out["columns"] = out.get("columns") if isinstance(out.get("columns"), list) else ([] if out.get("columns") is None else [out.get("columns")])
    out.setdefault("layman_rule", out.get("reason") or "")
    out.setdefault("reason", out.get("layman_rule") or "")
    out.setdefault("evidence", "")
    return out


def validate_ai_quality_rule_candidate(candidate):
    rule_type = candidate.get("rule_type")
    if not rule_type:
        return {"is_valid": False, "message": "Missing rule_type"}
    if rule_type not in SUPPORTED_RULE_TYPES:
        return {"is_valid": False, "message": f"Unsupported rule_type: {rule_type}"}
    if rule_type in {"not_null", "unique", "accepted_values", "range_check", "regex_check", "freshness_check"} and not candidate.get("column"):
        return {"is_valid": False, "message": f"Missing column for rule_type: {rule_type}"}
    if rule_type == "unique_combination" and not candidate.get("columns"):
        return {"is_valid": False, "message": "Missing columns for unique_combination"}
    return {"is_valid": True, "message": "ok"}


def build_layman_rule_records(candidates, run_id, dataset_name, table_name):
    rows = []
    for i, c in enumerate(candidates):
        rows.append(
            {
                "run_id": run_id,
                "dataset_name": dataset_name,
                "table_name": table_name,
                "rule_id": c.get("rule_id") or f"AI_DQ_{i + 1:03d}",
                "rule_type": c.get("rule_type"),
                "layman_rule": c.get("layman_rule"),
                "severity": c.get("severity", "warning"),
                "confidence": c.get("confidence", "medium"),
                "approval_status": c.get("approval_status", "candidate"),
                "can_compile": validate_ai_quality_rule_candidate(c)["is_valid"],
                "candidate_json": _jsonable(c),
            }
        )
    return rows
