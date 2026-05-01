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
    """Build transformation summary prompt context.

    Use this callable to support the framework workflow step implemented by `build_transformation_summary_prompt_context`.

    Parameters
    ----------
    lineage_summary : Any
        Input value for `lineage_summary`.
    code_snippets : Any, optional
        Input value for `code_snippets`.
    runtime_metrics : Any, optional
        Input value for `runtime_metrics`.
    business_context : Any, optional
        Input value for `business_context`.

    Returns
    -------
    result : Any
        Output produced by `build_transformation_summary_prompt_context`.

    Examples
    --------
    >>> build_transformation_summary_prompt_context(lineage_summary, code_snippets)
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

    Use this callable to support the framework workflow step implemented by `build_transformation_summary_generation_prompt`.

    Parameters
    ----------
    lineage_summary : Any
        Input value for `lineage_summary`.
    code_snippets : Any, optional
        Input value for `code_snippets`.
    runtime_metrics : Any, optional
        Input value for `runtime_metrics`.
    business_context : Any, optional
        Input value for `business_context`.

    Returns
    -------
    result : Any
        Output produced by `build_transformation_summary_generation_prompt`.

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
    """Normalize transformation summary candidate.

    Use this callable to support the framework workflow step implemented by `normalize_transformation_summary_candidate`.

    Parameters
    ----------
    candidate : Any
        Input value for `candidate`.

    Returns
    -------
    result : Any
        Output produced by `normalize_transformation_summary_candidate`.

    Examples
    --------
    >>> normalize_transformation_summary_candidate(candidate)
    """
    known = {k: candidate.get(k) for k in REQUIRED_FIELDS if k in candidate}
    metadata = {k: v for k, v in candidate.items() if k not in REQUIRED_FIELDS}
    known["approval_status"] = str(known.get("approval_status", "candidate")).lower() or "candidate"
    known["confidence"] = str(known.get("confidence", "medium")).lower() or "medium"
    known["evidence"] = known.get("evidence") if isinstance(known.get("evidence"), list) else ([] if known.get("evidence") is None else [known.get("evidence")])
    known["metadata"] = metadata
    return known


def parse_ai_transformation_summaries(raw_response):
    """Parse ai transformation summaries.

    Use this callable to support the framework workflow step implemented by `parse_ai_transformation_summaries`.

    Parameters
    ----------
    raw_response : Any
        Input value for `raw_response`.

    Returns
    -------
    result : Any
        Output produced by `parse_ai_transformation_summaries`.

    Examples
    --------
    >>> parse_ai_transformation_summaries(raw_response)
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

    Use this callable to support the framework workflow step implemented by `build_transformation_summary_records`.

    Parameters
    ----------
    candidates : Any
        Input value for `candidates`.
    run_id : Any
        Input value for `run_id`.
    dataset_name : Any
        Input value for `dataset_name`.
    table_name : Any
        Input value for `table_name`.

    Returns
    -------
    result : Any
        Output produced by `build_transformation_summary_records`.

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
