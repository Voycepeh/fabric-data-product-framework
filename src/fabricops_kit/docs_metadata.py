"""Metadata registry for generated public API documentation."""

from __future__ import annotations

from typing import NotRequired, TypedDict


class PublicSymbolDocMetadata(TypedDict):
    """Documentation metadata for a public symbol exported in ``__all__``."""

    symbol_name: str
    module: str
    kind: str
    workflow_step: int | str | None
    role: str
    purpose: NotRequired[str]
    summary_override: str | None






class ModuleDocMetadata(TypedDict):
    """Documentation metadata that drives module navigation and overview generation."""

    module_name: str
    visibility: str
    module_summary: str
    sidebar_group: str
    sidebar_include: bool


MODULE_DOCS_METADATA: list[ModuleDocMetadata] = [
    {"module_name": "environment_config", "visibility": "public", "module_summary": "Runtime and path bootstrap helpers for shared notebook setup.", "sidebar_group": "Modules", "sidebar_include": True},
    {"module_name": "fabric_input_output", "visibility": "public", "module_summary": "Lakehouse and warehouse read/write helpers.", "sidebar_group": "Modules", "sidebar_include": True},
    {"module_name": "data_profiling", "visibility": "public", "module_summary": "Source/output profiling and metadata conversion helpers.", "sidebar_group": "Modules", "sidebar_include": True},
    {"module_name": "data_contracts", "visibility": "public", "module_summary": "Data contract normalization, validation, and persistence helpers.", "sidebar_group": "Modules", "sidebar_include": True},
    {"module_name": "data_quality", "visibility": "public", "module_summary": "Deterministic DQ rule validation and enforcement helpers.", "sidebar_group": "Modules", "sidebar_include": True},
    {"module_name": "data_governance", "visibility": "public", "module_summary": "Governance classification helpers and metadata builders.", "sidebar_group": "Modules", "sidebar_include": True},
    {"module_name": "data_lineage", "visibility": "public", "module_summary": "Lineage extraction and handover documentation helpers.", "sidebar_group": "Modules", "sidebar_include": True},
        {"module_name": "data_drift", "visibility": "internal", "module_summary": "Schema/profile/partition drift checks supporting notebook validation.", "sidebar_group": "Advanced", "sidebar_include": False},
        {"module_name": "handover_documentation", "visibility": "internal", "module_summary": "Run summary and handover markdown helpers.", "sidebar_group": "Advanced", "sidebar_include": False},
    {"module_name": "technical_audit_columns", "visibility": "internal", "module_summary": "Technical/audit enrichment helpers for pipeline outputs.", "sidebar_group": "Advanced", "sidebar_include": False},
    {"module_name": "notebook_review", "visibility": "internal", "module_summary": "Human-in-the-loop DQ review helpers.", "sidebar_group": "Advanced", "sidebar_include": False},
    {"module_name": "ai", "visibility": "internal", "module_summary": "AI-assisted helper utilities and prompt builders.", "sidebar_group": "Advanced", "sidebar_include": False},
]

class TemplateFlowSegmentMetadata(TypedDict):
    """Segment metadata for starter template guidance on the reference landing page."""

    title: str
    symbols: list[str]
    text: NotRequired[str]


class TemplateFlowDocMetadata(TypedDict):
    """Starter template metadata used to render the template-first function reference."""

    notebook_key: str
    notebook_label: str
    template_path: str
    segment_intro: str
    segments: list[TemplateFlowSegmentMetadata]


TEMPLATE_FLOW_DOCS: list[TemplateFlowDocMetadata] = [
    {
        "notebook_key": "00_env_config",
        "notebook_label": "`00_env_config`",
        "template_path": "templates/notebooks/00_env_config.ipynb",
        "segment_intro": "Shared environment bootstrap and validation before exploration or pipeline notebooks run.",
        "segments": [
            {
                "title": "Segment 1: Explain the shared environment role",
                "text": "Describe what this shared config notebook sets up and what downstream exploration or pipeline notebooks depend on.",
                "symbols": [],
            },
            {
                "title": "Segment 2: Define environment targets and notebook policy",
                "symbols": [
                    "Housepath",
                    "load_fabric_config",
                    "get_path",
                ],
            },
            {
                "title": "Segment 3: Set AI, quality, governance, and lineage defaults",
                "symbols": [
                ],
            },
            {
                "title": "Segment 4: Assemble and validate framework config",
                "symbols": [
                    "load_fabric_config",
                ],
            },
            {
                "title": "Segment 5: Run startup checks and show resolved paths",
                "symbols": [
                    "setup_fabricops_notebook",
                    "get_path",
                ],
            },
        ],
    },
    {
        "notebook_key": "02_ex",
        "notebook_label": "`02_ex_<agreement>_<topic>`",
        "template_path": "templates/notebooks/02_ex_agreement_topic.ipynb",
        "segment_intro": "Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.",
        "segments": [
            {
                "title": "Segment 1: Load shared config and runtime",
                "symbols": [
                    "setup_fabricops_notebook",
                    "load_fabric_config",
                    "get_path",
                ],
            },
            {
                "title": "Segment 2: Profile source and capture evidence",
                "symbols": [
                    "seed_minimal_sample_source_table",
                    "lakehouse_table_read",
                    "warehouse_read",
                    
                    
                ],
            },
            {
                "title": "Segment 3: AI-assisted drafting (advisory only)",
                "symbols": [
                    "draft_dq_rules",
                    "review_dq_rules",
                    "write_dq_rules",
                ],
            },
            {
                "title": "Segment 4: Human approval and contract write",
                "symbols": [
                    "normalize_contract_dict",
                    "validate_contract_dict",
                    "write_contract_to_lakehouse",
                ],
            },
            {
                "title": "Optional lineage notes",
                "symbols": ["build_lineage_from_notebook_code"],
            },
        ],
    },
    {
        "notebook_key": "03_pc",
        "notebook_label": "`03_pc_<agreement>_<pipeline>`",
        "template_path": "templates/notebooks/03_pc_agreement_source_to_target.ipynb",
        "segment_intro": "Pipeline-contract notebook flow for deterministic enforcement and controlled publishing.",
        "segments": [
            {
                "title": "Segment 1: Load shared config and runtime context",
                "symbols": [
                    "setup_fabricops_notebook",
                    "load_fabric_config",
                    "get_path",
                ],
            },
            {
                "title": "Segment 2: Load approved contract and source data",
                "symbols": [
                    "load_latest_approved_contract",
                    "lakehouse_table_read",
                    "warehouse_read",
                ],
            },
            {
                "title": "Segment 3: Validate columns, transform, and compile rules",
                "symbols": [
                    "extract_required_columns",
                    "get_executable_quality_rules",
                    "validate_dq_rules",
                ],
            },
            {
                "title": "Segment 4: Run DQ, split outputs, and publish",
                "symbols": [
                    "enforce_dq_rules",
                    "assert_dq_passed",
                    "lakehouse_table_write",
                    "warehouse_write",
                ],
            },
            {
                "title": "Optional metadata / lineage / handover evidence",
                "symbols": [
                    
                    
                    
                    "build_lineage_records",
                ],
            },
        ],
    },
]
WORKFLOW_STEP_DOCS: list[dict[str, int | str]] = [
    {"number": 1, "slug": "step-01-governance-context", "title": "Governance context", "subtext": "This step captures the governance context: approved usage, owner, and data agreement. The agreement may live outside Fabric, such as in SharePoint documents. Functions in this step mainly link notebooks back to that agreement so the technical work stays tied to the approved business context."},
    {"number": "2A", "slug": "step-02a-shared-runtime-config", "title": "Create shared runtime config", "subtext": "This step creates the shared config that other notebooks depend on, including environment paths, workspace targets, AI availability, and standard naming rules. The goal is to define the project setup once so exploration and pipeline notebooks do not repeat hidden manual configuration."},
    {"number": "2B", "slug": "step-02b-notebook-startup-checks", "title": "Run notebook startup checks", "subtext": "This step runs the startup utility or smoke test at the beginning of every exploration and pipeline notebook. The goal is to confirm the notebook is running in the expected environment, follows naming rules, and has the required Fabric or AI capabilities before any data work begins."},
    {"number": 3, "slug": "step-03-source-contract-ingestion-pattern", "title": "Define source contract & ingestion pattern", "subtext": "This step defines the contract between the upstream source and this notebook. It captures what data is expected, including schema, data types, update frequency, update method, watermark column, and whether the source is append only, overwritten, or slowly changing. Functions in this step help the pipeline decide how to ingest, validate, snapshot, or incrementally process the source data."},
    {"number": 4, "slug": "step-04-ingest-profile-store", "title": "Ingest, profile & store source data", "subtext": "This step brings the source data into the framework, profiles it, and stores it for later use. Functions in this step focus on reading the data, capturing basic profiling results, and saving the raw or source-aligned version before business transformation begins."},
    {"number": 5, "slug": "step-05-explore-transform-logic", "title": "Explore data & explain transformation logic", "subtext": "This step is where the analyst studies the profiled source data and explains why transformation is needed. There may not be many helper functions here today, but future functions could support standard EDA, AI assisted analysis, and documentation of business assumptions before the logic becomes part of the repeatable pipeline."},
    {"number": "6A", "slug": "step-06a-transformation-logic", "title": "Write transformation logic", "subtext": "This step contains the main transformation logic that converts source-aligned data into the target output. Functions here support reusable pipeline code so the same logic can run consistently during development, testing, and scheduled refresh."},
    {"number": "6B", "slug": "step-06b-runtime-standards", "title": "Apply runtime standards", "subtext": "This step applies standard runtime requirements such as technical columns, run IDs, timestamps, partition keys, and other repeatable conventions. Functions here make outputs easier to audit, troubleshoot, join back to pipeline runs, and operate at scale."},
    {"number": "6C", "slug": "step-06c-pipeline-controls", "title": "Enforce pipeline controls", "subtext": "This step enforces the controls that decide whether the pipeline output should be trusted. Functions here support data quality rules, schema checks, classification checks, and other contract validations before data is released downstream."},
    {"number": "6D", "slug": "step-06d-controlled-outputs", "title": "Write controlled outputs", "subtext": "This step writes the transformed output to the correct lakehouse, warehouse, or product layer. Functions here make the write pattern explicit, repeatable, and aligned to the intended environment instead of relying on ad hoc exports."},
    {"number": 7, "slug": "step-07-output-profile-product-contract", "title": "Profile output & publish product contract", "subtext": "This step profiles the created output, stores its metadata, and creates the data contract for the next notebook, pipeline, or consumer. Functions here help record what was produced, write the evidence to metadata tables or catalogues, and make the output understandable and reusable downstream."},
    {"number": 8, "slug": "step-08-ai-assisted-dq-suggestions", "title": "Suggest AI assisted data quality rules", "subtext": "This step uses AI in exploration notebooks to suggest possible data quality rules from profiling results, business context, and source knowledge. These AI functions are only advisory. The actual rule creation, approval, and enforcement must still be done by the human engineer in the pipeline notebook."},
    {"number": 9, "slug": "step-09-ai-assisted-classification", "title": "Suggest AI assisted column classification", "subtext": "This step uses AI in exploration notebooks to suggest column classifications such as PII, sensitivity level, and governance labels for the planned output. These AI functions are only advisory. The actual label assignment must be approved by governance or data stewards and enforced by the human engineer in the pipeline notebook."},
    {"number": 10, "slug": "step-10-lineage-handover-documentation", "title": "Generate lineage & handover documentation", "subtext": "This step creates the final documentation needed for review, handover, and future maintenance. Functions here support lineage, transformation summaries, and handover notes so another analyst or engineer can understand what was built, why it was built, and how to operate it."},
]

PUBLIC_SYMBOL_DOCS: list[PublicSymbolDocMetadata] = [
    {"symbol_name": "Housepath", "module": "fabric_input_output", "kind": "class", "workflow_step": "2A", "role": "essential", "summary_override": None},
            {"symbol_name": "load_fabric_config", "module": "config", "kind": "function", "workflow_step": "2A", "role": "essential", "summary_override": None},
    {"symbol_name": "setup_fabricops_notebook", "module": "config", "kind": "function", "workflow_step": "2B", "role": "essential", "summary_override": None},
    {"symbol_name": "DQEnforcementResult", "module": "data_quality", "kind": "class", "workflow_step": "6C", "role": "optional", "summary_override": None},
    {"symbol_name": "get_path", "module": "config", "kind": "function", "workflow_step": "2A", "role": "essential", "summary_override": None},
    {"symbol_name": "lakehouse_table_read", "module": "fabric_input_output", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": None},
    {"symbol_name": "lakehouse_table_write", "module": "fabric_input_output", "kind": "function", "workflow_step": "6D", "role": "essential", "summary_override": None},
    {"symbol_name": "lakehouse_csv_read", "module": "fabric_input_output", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": None},
    {"symbol_name": "lakehouse_parquet_read_as_spark", "module": "fabric_input_output", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": None},
    {"symbol_name": "lakehouse_excel_read_as_spark", "module": "fabric_input_output", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": None},
    {"symbol_name": "warehouse_read", "module": "fabric_input_output", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": None},
    {"symbol_name": "warehouse_write", "module": "fabric_input_output", "kind": "function", "workflow_step": "6D", "role": "essential", "summary_override": None},
    {"symbol_name": "seed_minimal_sample_source_table", "module": "fabric_input_output", "kind": "function", "workflow_step": 4, "role": "optional", "summary_override": "Create and persist deterministic demo rows into a sample source table."},
    
                    {"symbol_name": "profile_dataframe", "module": "data_profiling", "kind": "function", "workflow_step": 4, "role": "optional", "summary_override": None},
    {"symbol_name": "build_ai_quality_context", "module": "data_profiling", "kind": "function", "workflow_step": 4, "role": "essential", "summary_override": None},
    {"symbol_name": "validate_dq_rules", "module": "data_quality", "kind": "function", "workflow_step": "6C", "role": "optional", "summary_override": None},
    {"symbol_name": "assert_dq_passed", "module": "data_quality", "kind": "function", "workflow_step": "6D", "role": "essential", "summary_override": None},
    {"symbol_name": "draft_dq_rules", "module": "data_quality", "kind": "function", "workflow_step": 8, "role": "essential", "summary_override": None},
    {"symbol_name": "write_dq_rules", "module": "data_quality", "kind": "function", "workflow_step": 8, "role": "essential", "summary_override": None},
    {"symbol_name": "enforce_dq_rules", "module": "data_quality", "kind": "function", "workflow_step": "6C", "role": "essential", "summary_override": "Run notebook-facing DQ rules and return a Spark DataFrame result."},
    {"symbol_name": "review_dq_rules", "module": "data_quality", "kind": "function", "workflow_step": 8, "role": "essential", "summary_override": None},
    {"symbol_name": "review_dq_rule_deactivations", "module": "notebook_review", "kind": "function", "workflow_step": 8, "role": "optional", "summary_override": None},
        {"symbol_name": "build_governance_candidate_prompt", "module": "ai", "kind": "function", "workflow_step": 9, "role": "optional", "summary_override": None},
    {"symbol_name": "build_handover_summary_prompt", "module": "ai", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "build_manual_governance_prompt_package", "module": "ai", "kind": "function", "workflow_step": 9, "role": "optional", "summary_override": None},
    {"symbol_name": "build_manual_handover_prompt_package", "module": "ai", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "parse_manual_ai_json_response", "module": "ai", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "generate_governance_candidates_with_fabric_ai", "module": "ai", "kind": "function", "workflow_step": 9, "role": "optional", "summary_override": None},
    {"symbol_name": "generate_handover_summary_with_fabric_ai", "module": "ai", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "check_schema_drift", "module": "drift", "kind": "function", "workflow_step": 4, "role": "essential", "summary_override": None},
    {"symbol_name": "check_partition_drift", "module": "drift", "kind": "function", "workflow_step": 4, "role": "essential", "summary_override": None},
    {"symbol_name": "check_profile_drift", "module": "drift", "kind": "function", "workflow_step": 4, "role": "essential", "summary_override": None},
    {"symbol_name": "summarize_drift_results", "module": "drift", "kind": "function", "workflow_step": 4, "role": "essential", "summary_override": None},
    {"symbol_name": "classify_column", "module": "data_governance", "kind": "function", "workflow_step": 9, "role": "optional", "summary_override": None},
    {"symbol_name": "classify_columns", "module": "data_governance", "kind": "function", "workflow_step": 9, "role": "essential", "summary_override": None},
    {"symbol_name": "build_governance_classification_records", "module": "data_governance", "kind": "function", "workflow_step": 9, "role": "essential", "summary_override": None},
    {"symbol_name": "write_governance_classifications", "module": "data_governance", "kind": "function", "workflow_step": 9, "role": "essential", "summary_override": None},
    {"symbol_name": "summarize_governance_classifications", "module": "data_governance", "kind": "function", "workflow_step": 9, "role": "essential", "summary_override": None},
    {"symbol_name": "build_lineage_records", "module": "data_lineage", "kind": "function", "workflow_step": 10, "role": "essential", "summary_override": None},
    {"symbol_name": "scan_notebook_lineage", "module": "data_lineage", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "scan_notebook_cells", "module": "data_lineage", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "validate_lineage_steps", "module": "data_lineage", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "build_lineage_from_notebook_code", "module": "data_lineage", "kind": "function", "workflow_step": 10, "role": "essential", "summary_override": None},
    {"symbol_name": "build_lineage_handover_markdown", "module": "data_lineage", "kind": "function", "workflow_step": 10, "role": "essential", "summary_override": None},
    {"symbol_name": "plot_lineage_steps", "module": "data_lineage", "kind": "function", "workflow_step": 10, "role": "optional", "summary_override": None},
    {"symbol_name": "build_run_summary", "module": "run_summary", "kind": "function", "workflow_step": 10, "role": "essential", "summary_override": None},
    {"symbol_name": "render_run_summary_markdown", "module": "run_summary", "kind": "function", "workflow_step": 10, "role": "essential", "summary_override": None},
    {"symbol_name": "normalize_contract_dict", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": None},
    {"symbol_name": "validate_contract_dict", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": None},
    {"symbol_name": "write_contract_to_lakehouse", "module": "data_contracts", "kind": "function", "workflow_step": 7, "role": "essential", "summary_override": "Validate and persist contract records into Fabric metadata tables."},
    {"symbol_name": "load_contract_from_lakehouse", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": "Load one contract by ID/version from Fabric metadata storage."},
    {"symbol_name": "load_latest_approved_contract", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": "Load the latest approved contract for a dataset/object pair."},
    {"symbol_name": "extract_required_columns", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": "Extract required column names from a normalized contract."},
    {"symbol_name": "extract_optional_columns", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": "Extract optional column names from a normalized contract."},
    {"symbol_name": "extract_business_keys", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": "Extract business-key column names from a normalized contract."},
    {"symbol_name": "extract_classifications", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": "Extract column classification mappings from a normalized contract."},
    {"symbol_name": "extract_quality_rules", "module": "data_contracts", "kind": "function", "workflow_step": 3, "role": "essential", "summary_override": "Extract raw quality-rule definitions from a normalized contract."},
    {"symbol_name": "get_executable_quality_rules", "module": "data_contracts", "kind": "function", "workflow_step": "6C", "role": "essential", "summary_override": "Return normalized quality rules ready for pipeline enforcement."},
    {"symbol_name": "standardize_output_columns", "module": "technical_columns", "kind": "function", "workflow_step": "6B", "role": "essential", "summary_override": None},
    {"symbol_name": "build_contract_summary", "module": "data_contracts", "kind": "function", "workflow_step": 7, "role": "essential", "summary_override": "Build a concise contract summary for reviews and handover."},
]
