"""Provider-neutral helpers for AI-assisted transformation summarisation."""

from __future__ import annotations

import json
import re
from typing import Any

REQUIRED_FIELDS = {
    "step_id",
    "step_name",
    "input_name",
    "output_name",
    "transformation_type",
    "technical_summary",
    "business_summary",
    "business_impact",
    "risk_or_caveat",
    "confidence",
    "evidence",
    "approval_status",
}


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


def build_transformation_summary_prompt_context(lineage_summary, code_snippets=None, runtime_metrics=None, business_context=None):
    """Build the AI prompt context payload for transformation summaries.

    Parameters
    ----------
    lineage_summary : dict
        Lineage summary payload describing transformation steps and data flow.
    code_snippets : list[str] or list[dict], optional
        Optional source snippets or extracted transformation code fragments used
        as evidence for the summary.
    runtime_metrics : dict, optional
        Optional runtime statistics such as row counts, durations, or resource
        usage that help ground the generated text.
    business_context : dict, optional
        Optional business explanation or stakeholder notes that should shape the
        non-technical summary.

    Returns
    -------
    dict
        Context dictionary with keys ``lineage_summary``, ``code_snippets``,
        ``runtime_metrics``, ``business_context``, and ``instructions``.
    """
    return {
        "lineage_summary": _jsonable(lineage_summary or {}),
        "code_snippets": _jsonable(code_snippets or []),
        "runtime_metrics": _jsonable(runtime_metrics or {}),
        "business_context": _jsonable(business_context or {}),
        "instructions": {
            "required_fields": sorted(REQUIRED_FIELDS),
            "format": "json_array",
        },
    }


def build_transformation_summary_generation_prompt(lineage_summary, code_snippets=None, runtime_metrics=None, business_context=None):
    """Build transformation summary generation prompt.

    Execute `build_transformation_summary_generation_prompt`.

    Parameters
    ----------
    lineage_summary : Any
        Value for `lineage_summary`.
    code_snippets : Any, optional
        Value for `code_snippets`.
    runtime_metrics : Any, optional
        Value for `runtime_metrics`.
    business_context : Any, optional
        Value for `business_context`.

    Returns
    -------
    result : Any
        Result returned by `build_transformation_summary_generation_prompt`.

    Examples
    --------
    >>> build_transformation_summary_generation_prompt(lineage_summary, code_snippets)
    """
    context = build_transformation_summary_prompt_context(lineage_summary, code_snippets, runtime_metrics, business_context)
    return (
        "Generate transformation summaries as JSON array only (no markdown). "
        "Create one object per transformation step. "
        "Each object must include: step_id, step_name, input_name, output_name, transformation_type, "
        "technical_summary, business_summary, business_impact, risk_or_caveat, confidence, evidence, approval_status. "
        "Do not invent transformations not present in evidence. Mark uncertainty clearly and set confidence accordingly. "
        f"Context: {json.dumps(context, ensure_ascii=False)}"
    )


def _strip_fences(text: str) -> str:
    m = re.match(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", text, flags=re.IGNORECASE | re.DOTALL)
    return m.group(1) if m else text


def normalize_transformation_summary_candidate(candidate):
    """Normalize one AI-generated transformation summary object.

    Parameters
    ----------
    candidate : dict
        Mapping parsed from an AI response for a single transformation step.

    Returns
    -------
    dict
        Normalized summary record where required fields are preserved, default
        values are set for ``approval_status`` and ``confidence``, evidence is
        coerced to a list, and unknown fields are moved under ``metadata``.
    """
    known = {k: candidate.get(k) for k in REQUIRED_FIELDS if k in candidate}
    metadata = {k: v for k, v in candidate.items() if k not in REQUIRED_FIELDS}
    known["approval_status"] = str(known.get("approval_status", "candidate")).lower() or "candidate"
    known["confidence"] = str(known.get("confidence", "medium")).lower() or "medium"
    known["evidence"] = known.get("evidence") if isinstance(known.get("evidence"), list) else ([] if known.get("evidence") is None else [known.get("evidence")])
    known["metadata"] = metadata
    return known


def parse_ai_transformation_summaries(raw_response):
    """Parse and validate AI output for transformation summaries.

    Parameters
    ----------
    raw_response : str or list[dict] or dict
        JSON string (optionally fenced with ```json ... ```), or an already
        parsed payload returned by an AI client.

    Returns
    -------
    dict
        Validation payload with keys:
        ``ok`` (bool), ``candidates`` (list[dict]), and ``errors`` (list[str]).
        Candidate objects are normalized before field validation.
    """
    try:
        payload = json.loads(_strip_fences(raw_response)) if isinstance(raw_response, str) else raw_response
    except Exception as exc:
        return {"ok": False, "candidates": [], "errors": [f"Invalid AI JSON response: {exc}"]}
    if not isinstance(payload, list):
        return {"ok": False, "candidates": [], "errors": ["AI response must be a JSON array"]}

    normalized = [normalize_transformation_summary_candidate(c) for c in payload if isinstance(c, dict)]
    errors = []
    valid = []
    for c in normalized:
        missing = [k for k in REQUIRED_FIELDS if k not in c or c.get(k) in (None, "")]
        if missing:
            errors.append(f"Missing required fields for step {c.get('step_id', 'unknown')}: {', '.join(sorted(missing))}")
        else:
            valid.append(c)
    return {"ok": len(errors) == 0, "candidates": valid, "errors": errors}


def build_transformation_summary_records(candidates, run_id, dataset_name, table_name):
    """Build transformation summary records.

    Execute `build_transformation_summary_records`.

    Parameters
    ----------
    candidates : Any
        Value for `candidates`.
    run_id : Any
        Value for `run_id`.
    dataset_name : Any
        Value for `dataset_name`.
    table_name : Any
        Value for `table_name`.

    Returns
    -------
    result : Any
        Result returned by `build_transformation_summary_records`.

    Examples
    --------
    >>> build_transformation_summary_records(candidates, run_id)
    """
    return [
        {
            "run_id": run_id,
            "dataset_name": dataset_name,
            "table_name": table_name,
            "step_id": c.get("step_id"),
            "step_name": c.get("step_name"),
            "input_name": c.get("input_name"),
            "output_name": c.get("output_name"),
            "transformation_type": c.get("transformation_type"),
            "technical_summary": c.get("technical_summary"),
            "business_summary": c.get("business_summary"),
            "business_impact": c.get("business_impact"),
            "risk_or_caveat": c.get("risk_or_caveat"),
            "confidence": c.get("confidence", "medium"),
            "evidence": c.get("evidence", []),
            "approval_status": c.get("approval_status", "candidate"),
            "metadata": c.get("metadata", {}),
        }
        for c in candidates
    ]
