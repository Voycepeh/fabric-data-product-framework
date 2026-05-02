"""Canonical 13-step MVP lifecycle registry and artifact validation helpers."""

from __future__ import annotations

from typing import Any


MVP_STEP_REGISTRY: list[dict[str, Any]] = [
    {
        "step_number": 1,
        "step_name": "Package and runtime setup",
        "owner_type": "framework",
        "canonical_modules": ["runtime.py", "fabric_io.py"],
        "expected_artifacts": ["runtime_context"],
        "description": "Initialize the notebook runtime and verify the framework package and execution context.",
    },
    {
        "step_number": 2,
        "step_name": "Fabric config and paths",
        "owner_type": "human",
        "canonical_modules": ["fabric_io.py", "config.py"],
        "expected_artifacts": ["fabric_config", "path_context"],
        "description": "Set project-specific Fabric configuration, source/target paths, and run identifiers.",
    },
    {
        "step_number": 3,
        "step_name": "Pull source data",
        "owner_type": "framework",
        "canonical_modules": ["fabric_io.py"],
        "expected_artifacts": ["source_dataframe"],
        "description": "Read source data from Fabric lakehouse, warehouse, or file path into the pipeline runtime.",
    },
    {"step_number": 4, "step_name": "Source profiling", "owner_type": "framework", "canonical_modules": ["profiling.py"], "expected_artifacts": ["source_profile"], "description": "Profile source structure and quality signals to establish baseline metadata."},
    {
        "step_number": 5,
        "step_name": "AI assisted DQ rule drafting",
        "owner_type": "ai_assisted",
        "canonical_modules": ["ai_quality_rules.py", "rule_compiler.py"],
        "expected_artifacts": ["draft_dq_rules"],
        "description": "Use AI support to draft candidate data quality rules from profiling outputs and business context.",
    },
    {
        "step_number": 6,
        "step_name": "Human review of rules and metadata",
        "owner_type": "human",
        "canonical_modules": ["rule_compiler.py", "metadata.py"],
        "expected_artifacts": ["approved_dq_rules", "approved_metadata_notes"],
        "description": "Review and approve drafted rules and key metadata assumptions before enforcement.",
    },
    {
        "step_number": 7,
        "step_name": "Compile and run DQ checks",
        "owner_type": "framework",
        "canonical_modules": ["quality.py", "rule_compiler.py"],
        "expected_artifacts": ["compiled_dq_rules", "dq_results"],
        "description": "Compile approved rules and execute data quality checks against the source dataframe.",
    },
    {
        "step_number": 8,
        "step_name": "Schema/profile/data drift checks",
        "owner_type": "framework",
        "canonical_modules": ["drift.py", "incremental.py"],
        "expected_artifacts": ["drift_results"],
        "description": "Compare current run metrics with baseline snapshots and flag schema/profile/data drift.",
    },
    {
        "step_number": 9,
        "step_name": "Core transformation",
        "owner_type": "mixed",
        "canonical_modules": ["fabric_io.py", "contracts.py"],
        "expected_artifacts": ["transformed_dataframe"],
        "description": "Apply business transformation logic using project code with framework-compatible conventions.",
    },
    {
        "step_number": 10,
        "step_name": "Standard technical columns",
        "owner_type": "framework",
        "canonical_modules": ["fabric_io.py", "technical_columns.py"],
        "expected_artifacts": ["output_with_technical_columns"],
        "description": "Apply required operational metadata columns to the transformed output dataframe.",
    },
    {
        "step_number": 11,
        "step_name": "Write output and profile output",
        "owner_type": "framework",
        "canonical_modules": ["fabric_io.py", "profiling.py", "metadata.py"],
        "expected_artifacts": ["target_write_result", "output_profile"],
        "description": "Write output data to target and capture output profiling metadata for traceability.",
    },
    {
        "step_number": 12,
        "step_name": "Governance classification and lineage",
        "owner_type": "mixed",
        "canonical_modules": ["governance.py", "lineage.py", "ai_lineage_summary.py"],
        "expected_artifacts": ["governance_labels", "lineage_records"],
        "description": "Classify governance tags and record lineage with human approval for AI-assisted suggestions.",
    },
    {
        "step_number": 13,
        "step_name": "Run summary and handover package",
        "owner_type": "framework",
        "canonical_modules": ["run_summary.py", "metadata.py"],
        "expected_artifacts": ["run_summary", "handover_package"],
        "description": "Publish run summary and handover artifacts for operational continuity and review.",
    },
]


_OWNER_TYPES = {"human", "ai_assisted", "framework", "mixed"}


def get_mvp_step_registry() -> list[dict[str, Any]]:
    """Return the canonical 13-step MVP lifecycle registry."""

    return [dict(step) for step in MVP_STEP_REGISTRY]


def get_mvp_step_names() -> list[str]:
    """Return ordered MVP step names."""

    return [step["step_name"] for step in MVP_STEP_REGISTRY]


def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Validate provided artifacts against the canonical MVP registry."""

    expected = sorted({name for step in MVP_STEP_REGISTRY for name in step["expected_artifacts"]})
    available = sorted([name for name in expected if artifacts.get(name) is not None])
    missing = [name for name in expected if name not in available]

    step_errors = []
    for step in MVP_STEP_REGISTRY:
        owner_type = step.get("owner_type")
        if owner_type not in _OWNER_TYPES:
            step_errors.append({"step_number": step["step_number"], "error": f"invalid owner_type: {owner_type}"})

    return {
        "valid": not missing and not step_errors,
        "expected_artifacts": expected,
        "available_artifacts": available,
        "missing_artifacts": missing,
        "step_errors": step_errors,
    }
