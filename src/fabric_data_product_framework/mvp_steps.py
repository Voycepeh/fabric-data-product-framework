"""Notebook-oriented MVP workflow step registry helpers."""

from __future__ import annotations

from typing import Any


MVP_STEPS: list[dict[str, str]] = [
    {"step": "configure runtime", "canonical_module": "runtime.py / fabric.py"},
    {"step": "read source", "canonical_module": "fabric.py"},
    {"step": "profile source", "canonical_module": "profiling.py"},
    {"step": "generate or compile quality rules", "canonical_module": "ai_quality_rules.py / rule_compiler.py"},
    {"step": "run quality checks", "canonical_module": "quality.py"},
    {"step": "check schema/data drift", "canonical_module": "drift.py / incremental.py"},
    {"step": "apply governance classification", "canonical_module": "governance.py"},
    {"step": "transform/write output", "canonical_module": "fabric.py"},
    {"step": "profile output", "canonical_module": "profiling.py"},
    {"step": "create lineage and handover summary", "canonical_module": "lineage.py / ai_lineage_summary.py"},
    {"step": "write run summary", "canonical_module": "run_summary.py / metadata.py"},
]


def get_mvp_step_registry() -> list[dict[str, str]]:
    """Return the canonical MVP notebook step sequence.

    Returns
    -------
    list[dict[str, str]]
        Ordered workflow entries, each with `step` and `canonical_module` keys.

    Notes
    -----
    Local Python compatible and Fabric notebook compatible.

    Examples
    --------
    >>> get_mvp_step_registry()[0]["step"]
    'configure runtime'
    """

    return [dict(step) for step in MVP_STEPS]


def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Validate whether expected MVP stage artifacts exist.

    Parameters
    ----------
    artifacts : dict[str, Any]
        Notebook artifact mapping keyed by stage names such as
        `source_profile`, `quality_result`, or `lineage_summary`.

    Returns
    -------
    dict[str, Any]
        Validation summary with missing/available keys and pass boolean.

    Notes
    -----
    Local Python compatible and Fabric notebook compatible.

    Examples
    --------
    >>> validate_mvp_artifacts({"source_profile": {}})["passed"]
    False
    """

    required = [
        "runtime_context",
        "source_profile",
        "quality_result",
        "drift_result",
        "governance_result",
        "lineage_summary",
        "run_summary",
    ]
    available = [k for k in required if artifacts.get(k) is not None]
    missing = [k for k in required if k not in available]
    return {"passed": not missing, "required": required, "available": available, "missing": missing}
