"""Canonical MVP workflow step registry for Fabric data products."""

from __future__ import annotations

from typing import Any

MVP_STEPS: list[dict[str, Any]] = [
    {"step_id": 1, "name": "Define data product", "actor": "Human led", "description": "Define the data product purpose, usage, grain, and scope.", "required_inputs": ["business_purpose", "expected_grain", "approved_usage"], "output_artifacts": ["data_product_context"], "fabric_test_hint": "Notebook section 1 captures purpose and approved usage notes."},
    {"step_id": 2, "name": "Setup config and environment", "actor": "Framework led", "description": "Build runtime config, path helpers, and environment guards.", "required_inputs": ["environment", "workspace", "lakehouse"], "output_artifacts": ["runtime_config"], "fabric_test_hint": "Runtime context and config cells execute with DRY_RUN support."},
    {"step_id": 3, "name": "Declare source and ingest data", "actor": "Framework led", "description": "Declare source expectations and read source data.", "required_inputs": ["source_table", "refresh_pattern"], "output_artifacts": ["source_declaration"], "fabric_test_hint": "Synthetic source table is read successfully in Fabric."},
    {"step_id": 4, "name": "Profile source and capture metadata", "actor": "Framework led", "description": "Generate source profile and metadata rows.", "required_inputs": ["source_dataframe"], "output_artifacts": ["source_profile"], "fabric_test_hint": "Source profile records are written or printed."},
    {"step_id": 5, "name": "Explore data", "actor": "Human led", "description": "Perform exploratory checks and capture assumptions.", "required_inputs": ["source_profile"], "output_artifacts": ["exploration_notes"], "fabric_test_hint": "EDA notes section is completed or marked TODO."},
    {"step_id": 6, "name": "Explain transformation logic", "actor": "Human led", "description": "Document why transformations exist.", "required_inputs": ["business_rules"], "output_artifacts": ["transformation_rationale"], "fabric_test_hint": "Transformation rationale markdown or dictionary is produced."},
    {"step_id": 7, "name": "Build transformation pipeline", "actor": "Framework led", "description": "Apply transformations and write output table.", "required_inputs": ["source_dataframe", "transformation_rationale"], "output_artifacts": ["output_table"], "fabric_test_hint": "Transformed output table is created in DRY_RUN or write mode."},
    {"step_id": 8, "name": "AI generate DQ rules from metadata, profile, and context", "actor": "AI assisted", "description": "Generate candidate DQ rules with AI from saved evidence.", "required_inputs": ["source_profile", "column_metadata", "data_product_context"], "output_artifacts": ["dq_candidate_rules"], "fabric_test_hint": "DQ candidates are generated or stubbed for dry run."},
    {"step_id": 9, "name": "Human review DQ rules", "actor": "Human led", "description": "Approve, reject, or edit candidate DQ rules.", "required_inputs": ["dq_candidate_rules"], "output_artifacts": ["approved_dq_rules"], "fabric_test_hint": "Approved DQ rule record is stored or printed."},
    {"step_id": 10, "name": "AI suggest sensitivity labels", "actor": "AI assisted", "description": "Suggest sensitivity labels from profile and context.", "required_inputs": ["source_profile", "data_product_context"], "output_artifacts": ["sensitivity_suggestions"], "fabric_test_hint": "Sensitivity suggestions are generated or stubbed for dry run."},
    {"step_id": 11, "name": "Human review and governance gate", "actor": "Human led", "description": "Approve governance labels and gate production use.", "required_inputs": ["sensitivity_suggestions", "approved_dq_rules"], "output_artifacts": ["approved_governance_labels"], "fabric_test_hint": "Governance review artifact is captured."},
    {"step_id": 12, "name": "AI generated lineage and transformation summary", "actor": "AI assisted", "description": "Generate lineage and transformation summary draft for review.", "required_inputs": ["transformation_rationale", "source_profile"], "output_artifacts": ["lineage_record"], "fabric_test_hint": "Lineage record and summary are produced."},
    {"step_id": 13, "name": "Handover framework pack", "actor": "Framework led", "description": "Assemble handover package with approved artifacts and caveats.", "required_inputs": ["approved_dq_rules", "approved_governance_labels", "lineage_record"], "output_artifacts": ["handover_pack"], "fabric_test_hint": "Handover pack includes profile, DQ, governance, lineage, and run summary placeholders."},
]


def get_mvp_step_registry() -> list[dict[str, Any]]:
    return [dict(step) for step in MVP_STEPS]


def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    expected = [a for step in MVP_STEPS for a in step["output_artifacts"]]
    missing = [artifact for artifact in expected if artifact not in artifacts]
    return {"is_valid": len(missing) == 0, "missing_artifacts": missing, "expected_artifacts": expected}
