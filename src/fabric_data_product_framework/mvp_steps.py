"""Canonical MVP workflow registry for the Fabric data product framework."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

MVP_STEPS = [
    {"step_id": 1, "name": "Define data product", "actor": "Human led", "description": "Define purpose, grain, usage, and context.", "required_inputs": ["data product purpose", "expected grain", "approved usage"], "output_artifacts": ["data_product_context"], "fabric_test_hint": "Record context cell output or metadata row."},
    {"step_id": 2, "name": "Setup config and environment", "actor": "Framework led", "description": "Build runtime config and execution context.", "required_inputs": ["environment", "source/target placeholders"], "output_artifacts": ["runtime_config"], "fabric_test_hint": "Validate runtime context and notebook naming checks."},
    {"step_id": 3, "name": "Declare source and ingest data", "actor": "Framework led", "description": "Declare source table and read data.", "required_inputs": ["source declaration", "adapter reader"], "output_artifacts": ["source_declaration"], "fabric_test_hint": "Read synthetic source table in DRY_RUN mode."},
    {"step_id": 4, "name": "Profile source and capture metadata", "actor": "Framework led", "description": "Profile source and persist profile metadata.", "required_inputs": ["source dataframe"], "output_artifacts": ["source_profile"], "fabric_test_hint": "Persist source profile metadata rows."},
    {"step_id": 5, "name": "Explore data", "actor": "Human led", "description": "Review exploratory summaries and caveats.", "required_inputs": ["source_profile"], "output_artifacts": ["exploration_notes"], "fabric_test_hint": "Capture exploration markdown note cell."},
    {"step_id": 6, "name": "Explain transformation logic", "actor": "Human led", "description": "Document business rationale for transformations.", "required_inputs": ["business context", "exploration_notes"], "output_artifacts": ["transformation_rationale"], "fabric_test_hint": "Save rationale text/record."},
    {"step_id": 7, "name": "Build transformation pipeline", "actor": "Framework led", "description": "Run transformation and write output table.", "required_inputs": ["transformation logic", "runtime_config"], "output_artifacts": ["output_table"], "fabric_test_hint": "Write synthetic curated table or DRY_RUN equivalent."},
    {"step_id": 8, "name": "AI generate DQ rules from metadata, profile, and context", "actor": "AI assisted", "description": "Generate candidate rules using metadata evidence.", "required_inputs": ["source_profile", "column metadata", "data product context"], "output_artifacts": ["dq_candidate_rules"], "fabric_test_hint": "Generate candidates or stub candidate payload in dry run."},
    {"step_id": 9, "name": "Human review DQ rules", "actor": "Human led", "description": "Approve/edit/reject candidate DQ rules.", "required_inputs": ["dq_candidate_rules"], "output_artifacts": ["approved_dq_rules"], "fabric_test_hint": "Freeze approved rules artifact and run DQ gate."},
    {"step_id": 10, "name": "AI suggest sensitivity labels", "actor": "AI assisted", "description": "Suggest sensitivity labels from profile and context.", "required_inputs": ["source_profile", "column metadata", "approved usage"], "output_artifacts": ["sensitivity_suggestions"], "fabric_test_hint": "Generate or stub sensitivity suggestions in dry run."},
    {"step_id": 11, "name": "Human review and governance gate", "actor": "Human led", "description": "Approve governance labels and gate publication.", "required_inputs": ["sensitivity_suggestions"], "output_artifacts": ["approved_governance_labels"], "fabric_test_hint": "Record governance review artifact and gate decision."},
    {"step_id": 12, "name": "AI generated lineage and transformation summary", "actor": "AI assisted", "description": "Draft lineage and transformation summary.", "required_inputs": ["transformation_rationale", "source_profile", "output_table"], "output_artifacts": ["lineage_record"], "fabric_test_hint": "Generate lineage summary markdown/records."},
    {"step_id": 13, "name": "Handover framework pack", "actor": "Framework led", "description": "Assemble handover artifacts for transfer.", "required_inputs": ["approved_dq_rules", "approved_governance_labels", "lineage_record", "source_profile"], "output_artifacts": ["handover_pack"], "fabric_test_hint": "Export or assemble handover package with caveats and run summary."},
]

REQUIRED_HANDOVER_PACK_KEYS = ["profile", "dq", "governance", "lineage", "run_summary", "caveats"]


def get_mvp_step_registry() -> list[dict[str, Any]]:
    """Get mvp step registry.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> get_mvp_step_registry(...)
    """
    return deepcopy(MVP_STEPS)


def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Validate mvp artifacts.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    artifacts : Any
    Description of `artifacts`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> validate_mvp_artifacts(...)
    """
    expected_top_level = sorted({a for s in MVP_STEPS for a in s["output_artifacts"]})
    missing_top_level = [name for name in expected_top_level if name not in artifacts]
    invalid_fields: list[dict[str, str]] = []

    if "approved_dq_rules" in artifacts and not isinstance(artifacts["approved_dq_rules"], list):
        invalid_fields.append({"field": "approved_dq_rules", "issue": "must be a list"})

    if "approved_governance_labels" in artifacts and not isinstance(artifacts["approved_governance_labels"], list):
        invalid_fields.append({"field": "approved_governance_labels", "issue": "must be a list"})

    if "lineage_record" in artifacts and not isinstance(artifacts["lineage_record"], (dict, list)):
        invalid_fields.append({"field": "lineage_record", "issue": "must be a dict or list"})

    missing_handover_keys: list[str] = []
    if "handover_pack" in artifacts:
        if not isinstance(artifacts["handover_pack"], dict):
            invalid_fields.append({"field": "handover_pack", "issue": "must be a dict"})
        else:
            missing_handover_keys = [k for k in REQUIRED_HANDOVER_PACK_KEYS if k not in artifacts["handover_pack"]]

    valid = not missing_top_level and not invalid_fields and not missing_handover_keys
    return {
        "valid": valid,
        "is_valid": valid,
        "expected_top_level_artifacts": expected_top_level,
        "missing_top_level_artifacts": missing_top_level,
        "invalid_fields": invalid_fields,
        "required_handover_pack_keys": REQUIRED_HANDOVER_PACK_KEYS,
        "missing_handover_pack_keys": missing_handover_keys,
    }
