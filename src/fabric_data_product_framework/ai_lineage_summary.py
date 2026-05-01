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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    lineage_summary : Any
    Description of `lineage_summary`.
    code_snippets : Any
    Description of `code_snippets`.
    runtime_metrics : Any
    Description of `runtime_metrics`.
    business_context : Any
    Description of `business_context`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_transformation_summary_prompt_context(...)
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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    lineage_summary : Any
    Description of `lineage_summary`.
    code_snippets : Any
    Description of `code_snippets`.
    runtime_metrics : Any
    Description of `runtime_metrics`.
    business_context : Any
    Description of `business_context`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_transformation_summary_generation_prompt(...)
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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    candidate : Any
    Description of `candidate`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> normalize_transformation_summary_candidate(...)
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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    raw_response : Any
    Description of `raw_response`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> parse_ai_transformation_summaries(...)
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

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    candidates : Any
    Description of `candidates`.
    run_id : Any
    Description of `run_id`.
    dataset_name : Any
    Description of `dataset_name`.
    table_name : Any
    Description of `table_name`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_transformation_summary_records(...)
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
