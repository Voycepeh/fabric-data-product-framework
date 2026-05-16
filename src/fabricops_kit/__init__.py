"""Public notebook-friendly entrypoints for the FabricOps Starter Kit."""

from .config import load_config, setup_notebook
from .fabric_input_output import (
    FabricStore,
    read_lakehouse_csv,
    read_lakehouse_excel,
    read_lakehouse_parquet,
    read_lakehouse_table,
    read_warehouse_table,
    write_lakehouse_table,
    write_warehouse_table,
)
from .data_profiling import profile_dataframe
from .business_context import (
    draft_business_context,
    extract_column_business_context_suggestions,
    get_reviewed_business_context_rows,
    prepare_business_context_profile_input,
    review_business_context,
    write_business_context,
)
from .data_quality import (
    assert_dq_passed,
    draft_dq_rules,
    enforce_dq,
    get_dq_review_results,
    load_dq_rules,
    review_dq_rule_deactivations,
    review_dq_rules,
    validate_dq_rules,
    write_dq_rules,
)
from .data_governance import (
    draft_governance,
    extract_governance_suggestions,
    load_governance,
    prepare_governance_input,
    review_governance,
    write_governance,
)
from .drift import check_partition_drift, check_profile_drift, check_schema_drift, summarize_drift_results
from .data_lineage import build_lineage_handover_markdown, build_lineage_records
from .handover import build_handover, render_handover_markdown
from .data_agreement import get_selected_agreement, load_agreements, select_agreement
from .metadata import load_notebook_registry, register_current_notebook, write_metadata_rows
from .technical_columns import standardize_columns

__version__ = "0.1.0"

__all__ = [
    "load_config","setup_notebook","load_agreements","select_agreement","get_selected_agreement","register_current_notebook","load_notebook_registry",
    "write_metadata_rows",
    "read_lakehouse_table","write_lakehouse_table","read_warehouse_table","write_warehouse_table","profile_dataframe",
    "draft_business_context","review_business_context","write_business_context",
    "prepare_business_context_profile_input","extract_column_business_context_suggestions","get_reviewed_business_context_rows",
    "draft_dq_rules","review_dq_rules","get_dq_review_results","write_dq_rules","load_dq_rules","enforce_dq","assert_dq_passed",
    "draft_governance","review_governance","write_governance","load_governance","prepare_governance_input","extract_governance_suggestions","standardize_columns","build_lineage_records","build_lineage_handover_markdown","build_handover","render_handover_markdown",
    "read_lakehouse_csv","read_lakehouse_parquet","read_lakehouse_excel","validate_dq_rules","review_dq_rule_deactivations","check_schema_drift","check_partition_drift","check_profile_drift","summarize_drift_results",
    "FabricStore",
]
