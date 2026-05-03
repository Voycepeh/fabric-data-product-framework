"""Metadata registry for generated public API documentation."""

from __future__ import annotations

from typing import TypedDict


class PublicSymbolDocMetadata(TypedDict):
    """Documentation metadata for a public symbol exported in ``__all__``."""

    symbol_name: str
    module: str
    kind: str
    workflow_step: int
    summary_override: str | None


PUBLIC_SYMBOL_DOCS: list[PublicSymbolDocMetadata] = [
    {"symbol_name": "Housepath", "module": "fabric_io", "kind": "class", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "load_fabric_config", "module": "fabric_io", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "get_path", "module": "fabric_io", "kind": "function", "workflow_step": 2, "summary_override": None},
    {"symbol_name": "lakehouse_table_read", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "lakehouse_table_write", "module": "fabric_io", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "lakehouse_csv_read", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "lakehouse_parquet_read_as_spark", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "lakehouse_excel_read_as_spark", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "warehouse_read", "module": "fabric_io", "kind": "function", "workflow_step": 3, "summary_override": None},
    {"symbol_name": "warehouse_write", "module": "fabric_io", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "generate_run_id", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "build_runtime_context", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "validate_notebook_name", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "assert_notebook_name_valid", "module": "runtime", "kind": "function", "workflow_step": 1, "summary_override": None},
    {"symbol_name": "profile_dataframe", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "profile_dataframe_to_metadata", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "profile_metadata_to_records", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "build_ai_quality_context", "module": "profiling", "kind": "function", "workflow_step": 4, "summary_override": None},
    {"symbol_name": "run_quality_rules", "module": "quality", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "check_schema_drift", "module": "drift", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "check_partition_drift", "module": "drift", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "check_profile_drift", "module": "drift", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "summarize_drift_results", "module": "drift", "kind": "function", "workflow_step": 8, "summary_override": None},
    {"symbol_name": "classify_column", "module": "governance", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "classify_columns", "module": "governance", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "build_governance_classification_records", "module": "governance", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "write_governance_classifications", "module": "governance", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "summarize_governance_classifications", "module": "governance", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "build_lineage_records", "module": "lineage", "kind": "function", "workflow_step": 13, "summary_override": None},
    {"symbol_name": "scan_notebook_lineage", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "scan_notebook_cells", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "enrich_lineage_steps_with_ai", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "fallback_copilot_lineage_prompt", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "validate_lineage_steps", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "build_lineage_record_from_steps", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "build_lineage_from_notebook_code", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "build_lineage_handover_markdown", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "plot_lineage_steps", "module": "lineage", "kind": "function", "workflow_step": 12, "summary_override": None},
    {"symbol_name": "build_run_summary", "module": "run_summary", "kind": "function", "workflow_step": 13, "summary_override": None},
    {"symbol_name": "render_run_summary_markdown", "module": "run_summary", "kind": "function", "workflow_step": 13, "summary_override": None},
    {"symbol_name": "build_dataset_run_record", "module": "metadata", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "build_schema_snapshot_records", "module": "metadata", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "build_schema_drift_records", "module": "metadata", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "build_quality_result_records", "module": "metadata", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "write_metadata_records", "module": "metadata", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "write_multiple_metadata_outputs", "module": "metadata", "kind": "function", "workflow_step": 11, "summary_override": None},
    {"symbol_name": "load_data_contract", "module": "quality", "kind": "function", "workflow_step": 7, "summary_override": None},
    {"symbol_name": "run_data_product", "module": "quality", "kind": "function", "workflow_step": 9, "summary_override": "Run the framework pipeline end-to-end for a data product."},
    {"symbol_name": "default_technical_columns", "module": "technical_columns", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "add_datetime_features", "module": "technical_columns", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "add_audit_columns", "module": "technical_columns", "kind": "function", "workflow_step": 10, "summary_override": None},
    {"symbol_name": "add_hash_columns", "module": "technical_columns", "kind": "function", "workflow_step": 10, "summary_override": None},
]
