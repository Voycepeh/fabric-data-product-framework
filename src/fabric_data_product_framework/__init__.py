"""Public notebook-friendly entrypoints for the Fabric Data Product Framework."""

from .drift import check_partition_drift, check_profile_drift, check_schema_drift, summarize_drift_results
from .fabric_io import (
    Housepath,
    get_path,
    lakehouse_csv_read,
    lakehouse_excel_read_as_spark,
    lakehouse_parquet_read_as_spark,
    lakehouse_table_read,
    lakehouse_table_write,
    load_fabric_config,
    warehouse_read,
    warehouse_write,
)
from .lineage import (
    build_lineage_from_notebook_code,
    build_lineage_handover_markdown,
    build_lineage_record_from_steps,
    build_lineage_records,
    enrich_lineage_steps_with_ai,
    fallback_copilot_lineage_prompt,
    plot_lineage_steps,
    scan_notebook_cells,
    scan_notebook_lineage,
    validate_lineage_steps,
)
from .governance import (
    build_governance_classification_records,
    classify_column,
    classify_columns,
    summarize_governance_classifications,
    write_governance_classifications,
)
from .metadata import (
    build_dataset_run_record,
    build_quality_result_records,
    build_schema_drift_records,
    build_schema_snapshot_records,
    write_metadata_records,
    write_multiple_metadata_outputs,
)
from .profiling import (
    build_ai_quality_context,
    profile_dataframe,
    profile_dataframe_to_metadata,
    profile_metadata_to_records,
)
from .quality import load_data_contract, run_data_product, run_quality_rules
from .run_summary import build_run_summary, render_run_summary_markdown
from .runtime import assert_notebook_name_valid, build_runtime_context, generate_run_id, validate_notebook_name
from .technical_columns import add_audit_columns, add_datetime_features, add_hash_columns, default_technical_columns

__version__ = "0.1.0"

__all__ = [
    "Housepath",
    "load_fabric_config",
    "get_path",
    "lakehouse_table_read",
    "lakehouse_table_write",
    "lakehouse_csv_read",
    "lakehouse_parquet_read_as_spark",
    "lakehouse_excel_read_as_spark",
    "warehouse_read",
    "warehouse_write",
    "generate_run_id",
    "build_runtime_context",
    "validate_notebook_name",
    "assert_notebook_name_valid",
    "profile_dataframe",
    "profile_dataframe_to_metadata",
    "profile_metadata_to_records",
    "build_ai_quality_context",
    "run_quality_rules",
    "check_schema_drift",
    "check_partition_drift",
    "check_profile_drift",
    "summarize_drift_results",
    "classify_column",
    "classify_columns",
    "build_governance_classification_records",
    "write_governance_classifications",
    "summarize_governance_classifications",
    "build_lineage_records",
    "scan_notebook_lineage",
    "scan_notebook_cells",
    "enrich_lineage_steps_with_ai",
    "fallback_copilot_lineage_prompt",
    "validate_lineage_steps",
    "build_lineage_record_from_steps",
    "build_lineage_from_notebook_code",
    "build_lineage_handover_markdown",
    "plot_lineage_steps",
    "build_run_summary",
    "render_run_summary_markdown",
    "build_dataset_run_record",
    "build_schema_snapshot_records",
    "build_schema_drift_records",
    "build_quality_result_records",
    "write_metadata_records",
    "write_multiple_metadata_outputs",
    "load_data_contract",
    "run_data_product",
    "default_technical_columns",
    "add_datetime_features",
    "add_audit_columns",
    "add_hash_columns",
]
