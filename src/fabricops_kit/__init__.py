"""Public notebook-friendly entrypoints for the FabricOps Starter Kit."""

from .drift import check_partition_drift, check_profile_drift, check_schema_drift, summarize_drift_results
from .config import (
    get_path,
    load_fabric_config,
    setup_fabricops_notebook,
)
from .fabric_input_output import (
    Housepath,
    lakehouse_csv_read,
    lakehouse_excel_read_as_spark,
    lakehouse_parquet_read_as_spark,
    lakehouse_table_read,
    lakehouse_table_write,
    warehouse_read,
    warehouse_write,
    seed_minimal_sample_source_table,
)
from .data_lineage import (
    build_lineage_from_notebook_code,
    build_lineage_handover_markdown,
    build_lineage_records,
    plot_lineage_steps,
    scan_notebook_cells,
    scan_notebook_lineage,
    validate_lineage_steps,
)
from .data_governance import (
    build_governance_classification_records,
    classify_column,
    classify_columns,
    summarize_governance_classifications,
    write_governance_classifications,
)

from .data_profiling import (
    profile_dataframe,
)
from .ai import (
    build_governance_candidate_prompt,
    build_handover_summary_prompt,
    build_manual_governance_prompt_package,
    build_manual_handover_prompt_package,
    generate_governance_candidates_with_fabric_ai,
    generate_handover_summary_with_fabric_ai,
    parse_manual_ai_json_response,
)
from .data_quality import (
    DQEnforcementResult,
    draft_dq_rules,
    write_dq_rules,
    enforce_dq_rules,
    validate_dq_rules,
    assert_dq_passed,
)
from .notebook_review import review_dq_rules, review_dq_rule_deactivations
from .run_summary import build_run_summary, render_run_summary_markdown
from .technical_columns import standardize_output_columns

__version__ = "0.1.0"

__all__ = [
    "review_dq_rule_deactivations",
    "DQEnforcementResult",
    "review_dq_rules",
    "draft_dq_rules",
    "write_dq_rules",
    "enforce_dq_rules",
    "Housepath",
    "load_fabric_config",
    "get_path",
    "setup_fabricops_notebook",
    "lakehouse_table_read",
    "lakehouse_table_write",
    "lakehouse_csv_read",
    "lakehouse_parquet_read_as_spark",
    "lakehouse_excel_read_as_spark",
    "warehouse_read",
    "warehouse_write",
    "seed_minimal_sample_source_table",
    "profile_dataframe",
    "assert_dq_passed",
    "validate_dq_rules",
    "parse_manual_ai_json_response",
    "build_manual_handover_prompt_package",
    "build_manual_governance_prompt_package",
    "build_handover_summary_prompt",
    "build_governance_candidate_prompt",
    "generate_governance_candidates_with_fabric_ai",
    "generate_handover_summary_with_fabric_ai",
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
    "validate_lineage_steps",
    "build_lineage_from_notebook_code",
    "build_lineage_handover_markdown",
    "plot_lineage_steps",
    "build_run_summary",
    "render_run_summary_markdown",
    "standardize_output_columns",
]
