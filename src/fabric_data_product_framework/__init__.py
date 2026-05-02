"""Public notebook-friendly entrypoints for the Fabric Data Product Framework."""

from .contracts import load_data_contract, run_data_product
from .drift import check_partition_drift, check_profile_drift, check_schema_drift, summarize_drift_results
from .fabric_io import (
    Housepath,
    get_path,
    lakehouse_csv_read,
    lakehouse_excel_read_as_spark,
    lakehouse_parquet_read_as_spark,
    lakehouse_table_read,
    load_fabric_config,
    warehouse_read,
    warehouse_write,
)
from .governance import classify_columns, summarize_governance_classifications
from .lineage import LineageRecorder, build_lineage_records, build_transformation_summary_markdown, generate_mermaid_lineage
from .metadata import write_multiple_metadata_outputs
from .profiling import profile_dataframe, summarize_profile
from .quality import run_quality_rules
from .run_summary import build_run_summary, render_run_summary_markdown
from .runtime import assert_notebook_name_valid, build_runtime_context, generate_run_id, validate_notebook_name
from .technical_columns import add_audit_columns, add_datetime_features, add_hash_columns, default_technical_columns

__version__ = "0.1.0"

__all__ = [
    "Housepath",
    "load_fabric_config",
    "get_path",
    "lakehouse_table_read",
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
    "summarize_profile",
    "run_quality_rules",
    "check_schema_drift",
    "check_partition_drift",
    "check_profile_drift",
    "summarize_drift_results",
    "classify_columns",
    "summarize_governance_classifications",
    "LineageRecorder",
    "build_lineage_records",
    "generate_mermaid_lineage",
    "build_transformation_summary_markdown",
    "build_run_summary",
    "render_run_summary_markdown",
    "write_multiple_metadata_outputs",
    "load_data_contract",
    "run_data_product",
    "default_technical_columns",
    "add_datetime_features",
    "add_audit_columns",
    "add_hash_columns",
]
