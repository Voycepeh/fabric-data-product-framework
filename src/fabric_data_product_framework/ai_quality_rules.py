"""Provider-neutral helpers for AI-assisted data quality rule generation."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from .quality import SUPPORTED_RULE_TYPES

SUPPORTED_CANDIDATE_FIELDS = {
    "rule_id", "table_name", "column", "columns", "layman_rule", "rule_type", "rule_config",
    "severity", "confidence", "reason", "evidence", "approval_status",
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
    """Build a JSON-safe context object for AI-assisted DQ rule suggestion.

    Parameters
    ----------
    profile : dict
        Profiling payload (typically from ``profile_dataframe``) containing
        column-level evidence such as nulls, distinct counts, and sample values.
    contract : dict | None, optional
        Optional contract fragment used to ground candidate suggestions.
    business_context : str | dict | None, optional
        Optional plain-language context explaining business intent.
    table_name, dataset_name : str | None, optional
        Optional names persisted in the returned prompt context.

    Returns
    -------
    dict
        JSON-safe prompt context for AI candidate generation.

    Notes
    -----
    This helper prepares context only. Candidate rules still require human review
    and approval before compilation and production pipeline gating.
    """
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
    """Create the final AI prompt string for candidate DQ rule generation.

    Parameters
    ----------
    profile, contract, business_context, table_name, dataset_name
        Same inputs as :func:`build_quality_rule_prompt_context`.

    Returns
    -------
    str
        Prompt text that instructs AI to return a JSON array of conservative
        candidate rules compatible with the framework lifecycle.

    Notes
    -----
    The generated prompt enforces a review-first pattern. AI suggestions are not
    production checks until a human reviews and approves them.
    """
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
    """Parse and validate AI-generated DQ candidate JSON arrays.

    Returns normalized candidate records with per-candidate validation flags.
    """
    try:
        parsed = json.loads(_strip_json_fences(raw_response)) if isinstance(raw_response, str) else raw_response
    except Exception as exc:
        return {"ok": False, "candidates": [], "errors": [f"Invalid AI JSON response: {exc}"], "warnings": []}
    if not isinstance(parsed, list):
        return {"ok": False, "candidates": [], "errors": ["AI response must be a JSON array"], "warnings": []}

    errors: list[str] = []
    warnings: list[str] = []
    candidates = []
    for idx, item in enumerate(parsed):
        if not isinstance(item, dict):
            warnings.append(f"Skipped non-dict item at index {idx}")
            continue
        c = normalize_quality_rule_candidate(item)
        val = validate_ai_quality_rule_candidate(c)
        c["is_valid_candidate"] = val["is_valid"]
        c["validation_message"] = val["message"]
        c["can_compile"] = val["is_valid"]
        if not val["is_valid"]:
            warnings.append(val["message"])
        candidates.append(c)
    return {"ok": len(errors) == 0, "candidates": candidates, "errors": errors, "warnings": warnings}


def normalize_quality_rule_candidate(candidate):
    """Normalize one AI candidate to the framework review schema.

    Parameters
    ----------
    candidate : dict
        Raw candidate generated by AI or authored manually.

    Returns
    -------
    dict
        Candidate with normalized keys and defaults including ``rule_type``,
        ``severity``, ``confidence``, ``approval_status``, and ``rule_config``.
    """
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
    """Validate whether a candidate can be safely compiled to executable checks.

    Returns
    -------
    dict
        Validation result with ``is_valid`` and ``message`` fields.
    """
    rt = candidate.get("rule_type")
    if not rt:
        return {"is_valid": False, "message": "Missing rule_type"}
    if rt not in SUPPORTED_RULE_TYPES:
        return {"is_valid": False, "message": f"Unsupported rule_type: {rt}"}
    if rt in {"not_null", "unique", "accepted_values", "range_check", "regex_check", "freshness_check"} and not candidate.get("column"):
        return {"is_valid": False, "message": f"Missing column for rule_type: {rt}"}
    if rt == "unique_combination" and not candidate.get("columns"):
        return {"is_valid": False, "message": "Missing columns for unique_combination"}
    return {"is_valid": True, "message": "ok"}


def build_layman_rule_records(candidates, run_id, dataset_name, table_name):
    """Build metadata-table records for candidate review and steward approval.

    Parameters
    ----------
    candidates : list[dict]
        Candidate rule list, usually from AI suggestion or steward review.
    run_id, dataset_name, table_name : str
        Run and dataset context used for metadata persistence.

    Returns
    -------
    list[dict]
        Table-friendly records including candidate validity, review status, and
        JSON payload for approval workflows.
    """
    rows = []
    for i, c in enumerate(candidates):
        can_compile = bool(c.get("can_compile")) if "can_compile" in c else validate_ai_quality_rule_candidate(c)["is_valid"]
        rows.append({
            "run_id": run_id,
            "dataset_name": dataset_name,
            "table_name": table_name,
            "rule_id": c.get("rule_id") or f"AI_DQ_{i + 1:03d}",
            "rule_type": c.get("rule_type"),
            "layman_rule": c.get("layman_rule"),
            "severity": c.get("severity", "warning"),
            "confidence": c.get("confidence", "medium"),
            "approval_status": c.get("approval_status", "candidate"),
            "is_valid_candidate": c.get("is_valid_candidate", can_compile),
            "validation_message": c.get("validation_message", "ok" if can_compile else "invalid candidate"),
            "can_compile": can_compile,
            "candidate_json": _jsonable(c),
        })
    return rows
