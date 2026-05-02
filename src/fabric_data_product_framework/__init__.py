"""Public notebook-friendly entrypoints for the Fabric Data Product Framework."""

from .contracts import load_data_contract, run_data_product
from .drift import (
    check_partition_drift,
    check_profile_drift,
    check_schema_drift,
    summarize_drift_results,
)
from .fabric import load_fabric_config, read_table, write_table
from .governance import classify_columns, summarize_governance_classifications
from .lineage import (
    LineageRecorder,
    build_lineage_records,
    build_transformation_summary_markdown,
    generate_mermaid_lineage,
)
from .metadata import write_multiple_metadata_outputs
from .profiling import profile_dataframe, summarize_profile
from .quality import run_quality_rules
from .run_summary import build_run_summary, render_run_summary_markdown

__version__ = "0.1.0"

__all__ = [
    "load_fabric_config",
    "read_table",
    "write_table",
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
]
