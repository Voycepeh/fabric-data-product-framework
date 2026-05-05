"""Metadata registry for generated public API documentation."""

from __future__ import annotations

from typing import NotRequired, TypedDict


class PublicSymbolDocMetadata(TypedDict):
    """Documentation metadata for a public symbol exported in ``__all__``."""

    symbol_name: str
    module: str
    kind: str
    workflow_step: int | None
    importance: NotRequired[str]
    purpose: NotRequired[str]
    summary_override: str | None


WORKFLOW_STEP_DOCS: list[dict[str, int | str]] = [
    {"number": 1, "slug": "step-01-governance-purpose-ownership", "title": "Define purpose, approved usage & governance ownership"},
    {"number": 2, "slug": "step-02-runtime-environment-path-rules", "title": "Configure runtime, environment & path rules"},
    {"number": 3, "slug": "step-03-source-contract-ingestion", "title": "Declare source contract & ingest source data"},
    {"number": 4, "slug": "step-04-source-validation-metadata", "title": "Validate source against contract & capture metadata"},
    {"number": 5, "slug": "step-05-exploration-rationale", "title": "Explore data & capture transformation / DQ rationale"},
    {"number": 6, "slug": "step-06-production-transformation-output", "title": "Build production transformation & write target output"},
    {"number": 7, "slug": "step-07-output-validation-target-metadata", "title": "Validate output & persist target metadata"},
    {"number": 8, "slug": "step-08-dq-rule-generation-review", "title": "Generate, review & configure DQ rules"},
    {"number": 9, "slug": "step-09-classification-sensitivity", "title": "Generate & review classification / sensitivity suggestions"},
    {"number": 10, "slug": "step-10-lineage-handover-documentation", "title": "Generate data lineage and handover documentation"},
]

PUBLIC_SYMBOL_DOCS: list[PublicSymbolDocMetadata] = [
    {"symbol_name": "Housepath", "module": "fabric_io", "kind": "class", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "create_path_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "create_notebook_runtime_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "create_ai_prompt_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "create_quality_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "create_governance_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "create_lineage_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "create_framework_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "validate_framework_config", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {
        "symbol_name": "run_config_smoke_tests",
        "module": "config",
        "kind": "function",
        "workflow_step": 2,
        "importance": "Essential",
        "purpose": "Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.",
        "summary_override": None,
    },
    {
        "symbol_name": "bootstrap_fabric_env",
        "module": "config",
        "kind": "function",
        "workflow_step": 2,
        "importance": "Essential",
        "purpose": "Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.",
        "summary_override": None,
    },
    {"symbol_name": "load_fabric_config", "module": "fabric_io", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "get_path", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "lakehouse_table_read", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "lakehouse_table_write", "module": "fabric_io", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "lakehouse_csv_read", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "lakehouse_parquet_read_as_spark", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "lakehouse_excel_read_as_spark", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "warehouse_read", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "warehouse_write", "module": "fabric_io", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "generate_run_id", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "build_runtime_context", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "validate_notebook_name", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "assert_notebook_name_valid", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "profile_dataframe", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "profile_dataframe_to_metadata", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "profile_metadata_to_records", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "generate_metadata_profile", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "build_ai_quality_context", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "run_quality_rules", "module": "quality", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "check_fabric_ai_functions_available", "module": "config", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "build_dq_rule_candidate_prompt", "module": "ai", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "build_governance_candidate_prompt", "module": "ai", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "build_handover_summary_prompt", "module": "ai", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "build_manual_dq_rule_prompt_package", "module": "ai", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "build_manual_governance_prompt_package", "module": "ai", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "build_manual_handover_prompt_package", "module": "ai", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "parse_manual_ai_json_response", "module": "ai", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "configure_fabric_ai_functions", "module": "ai", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "generate_dq_rule_candidates_with_fabric_ai", "module": "ai", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "generate_governance_candidates_with_fabric_ai", "module": "ai", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "generate_handover_summary_with_fabric_ai", "module": "ai", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "check_schema_drift", "module": "drift", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "check_partition_drift", "module": "drift", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "check_profile_drift", "module": "drift", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "summarize_drift_results", "module": "drift", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "classify_column", "module": "governance", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "classify_columns", "module": "governance", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "build_governance_classification_records", "module": "governance", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "write_governance_classifications", "module": "governance", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "summarize_governance_classifications", "module": "governance", "kind": "function", "workflow_step": 9, "summary_override": None},
    {"symbol_name": "build_lineage_records", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "scan_notebook_lineage", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "scan_notebook_cells", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "enrich_lineage_steps_with_ai", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "fallback_copilot_lineage_prompt", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "validate_lineage_steps", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "build_lineage_record_from_steps", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "build_lineage_from_notebook_code", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "build_lineage_handover_markdown", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "plot_lineage_steps", "module": "lineage", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "build_run_summary", "module": "run_summary", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "render_run_summary_markdown", "module": "run_summary", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "build_dataset_run_record", "module": "metadata", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "build_schema_snapshot_records", "module": "metadata", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "build_schema_drift_records", "module": "metadata", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "build_quality_result_records", "module": "metadata", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "write_metadata_records", "module": "metadata", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "write_multiple_metadata_outputs", "module": "metadata", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "load_data_contract", "module": "quality", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "run_data_product", "module": "quality", "kind": "function", "workflow_step": 6, "summary_override": "Run the starter kit workflow end-to-end for a data product outcome."},
    {"symbol_name": "default_technical_columns", "module": "technical_columns", "kind": "function", "workflow_step": 6, "summary_override": None},
    {"symbol_name": "add_datetime_features", "module": "technical_columns", "kind": "function", "workflow_step": 6, "summary_override": None},
    {"symbol_name": "add_audit_columns", "module": "technical_columns", "kind": "function", "workflow_step": 6, "summary_override": None},
    {"symbol_name": "add_hash_columns", "module": "technical_columns", "kind": "function", "workflow_step": 6, "summary_override": None},
]
