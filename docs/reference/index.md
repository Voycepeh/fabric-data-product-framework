# Callable Functions

Generated step-first catalogue of callable functions sourced from `fabricops_kit.__all__`.

## Notebook template quickstart

Use these notebook templates for an end-to-end lifecycle implementation:

- [`00_env_config.ipynb`](../../templates/notebooks/00_env_config.ipynb): shared runtime setup (Step 1, Step 2A, Step 2B).
- [`02_ex_agreement_topic.ipynb`](../../templates/notebooks/02_ex_agreement_topic.ipynb): exploration/profiling and AI-assisted advisory suggestions with human decisions (Step 3, Step 4, Step 5, Step 8, Step 9).
- [`03_pc_agreement_source_to_target.ipynb`](../../templates/notebooks/03_pc_agreement_source_to_target.ipynb): run-all-safe pipeline enforcement and controlled delivery (Step 1, Step 2B, Step 3, Step 6A-6D, Step 7, Step 10).

Clean split:
- `00_env_config` = shared setup.
- `02_ex` = exploration, profiling, AI suggestions, human decisions.
- `03_pc` = approved enforcement and output.

Step 8 and Step 9 AI functions belong in exploration notebooks. Pipeline notebooks should enforce approved rules and should not make AI decisions at runtime.

- `02_ex` drafts contract expectations from profiling evidence and AI-assisted suggestions.
- `03_pc` enforces approved contract expectations.
- FabricOps uses Open Data Contract principles in a Fabric-first way: metadata tables are the operational source of truth, and ODCS YAML is an optional exchange/export format.


## Modules

| Module |
|---|
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/docs_metadata/" title="Open docs_metadata module page" aria-label="Open docs_metadata module page">docs_metadata</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module page" aria-label="Open drift module page">drift</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module page" aria-label="Open governance module page">governance</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover/" title="Open handover module page" aria-label="Open handover module page">handover</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module page" aria-label="Open metadata module page">metadata</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module page" aria-label="Open profiling module page">profiling</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module page" aria-label="Open quality module page">quality</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/run_summary/" title="Open run_summary module page" aria-label="Open run_summary module page">run_summary</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module page" aria-label="Open runtime module page">runtime</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module page" aria-label="Open technical_columns module page">technical_columns</a> |

## Step 1: Governance context

This step captures the governance context: approved usage, owner, and data agreement. The agreement may live outside Fabric, such as in SharePoint documents. Functions in this step mainly link notebooks back to that agreement so the technical work stays tied to the approved business context.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`assert_notebook_name_valid`](./step-01-governance-context/assert_notebook_name_valid/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module page" aria-label="Open runtime module page">runtime</a> | Essential | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — |
| [`build_runtime_context`](./step-01-governance-context/build_runtime_context/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module page" aria-label="Open runtime module page">runtime</a> | Essential | Build a standard runtime context dictionary for Fabric notebooks. | — |
| [`configure_fabric_ai_functions`](./step-01-governance-context/configure_fabric_ai_functions/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Essential | Apply optional default Fabric AI Function configuration. | — |
| [`generate_run_id`](./step-01-governance-context/generate_run_id/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module page" aria-label="Open runtime module page">runtime</a> | Essential | Generate a notebook-safe run identifier. | — |
| [`validate_notebook_name`](./step-01-governance-context/validate_notebook_name/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module page" aria-label="Open runtime module page">runtime</a> | Essential | Validate notebook names against the framework workspace notebook model. | — |

## Step 2A: Create shared runtime config

This step creates the shared config that other notebooks depend on, including environment paths, workspace targets, AI availability, and standard naming rules. The goal is to define the project setup once so exploration and pipeline notebooks do not repeat hidden manual configuration.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`check_fabric_ai_functions_available`](./step-02a-shared-runtime-config/check_fabric_ai_functions_available/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Check whether Fabric AI Functions are available in the current runtime. | — |
| [`create_ai_prompt_config`](./step-02a-shared-runtime-config/create_ai_prompt_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Create the AI prompt-template configuration used by FabricOps. | — |
| [`create_framework_config`](./step-02a-shared-runtime-config/create_framework_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Create the top-level framework configuration object. | — |
| [`create_governance_config`](./step-02a-shared-runtime-config/create_governance_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Create governance-default configuration. | — |
| [`create_lineage_config`](./step-02a-shared-runtime-config/create_lineage_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Create lineage-default configuration. | — |
| [`create_notebook_runtime_config`](./step-02a-shared-runtime-config/create_notebook_runtime_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Create notebook naming-policy configuration for runtime guards. | — |
| [`create_path_config`](./step-02a-shared-runtime-config/create_path_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Create environment-to-target routing used by Fabric IO helpers. | — |
| [`create_quality_config`](./step-02a-shared-runtime-config/create_quality_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Create quality-default configuration. | — |
| [`get_path`](./step-02a-shared-runtime-config/get_path/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Resolve a configured Fabric path for an environment and target. | — |
| [`Housepath`](./step-02a-shared-runtime-config/Housepath/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Fabric lakehouse or warehouse connection details. | — |
| [`load_fabric_config`](./step-02a-shared-runtime-config/load_fabric_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Validate and return a framework config mapping. | — |
| [`validate_framework_config`](./step-02a-shared-runtime-config/validate_framework_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Validate and normalize framework config input. | — |

## Step 2B: Run notebook startup checks

This step runs the startup utility or smoke test at the beginning of every exploration and pipeline notebook. The goal is to confirm the notebook is running in the expected environment, follows naming rules, and has the required Fabric or AI capabilities before any data work begins.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`bootstrap_fabric_env`](./step-02b-notebook-startup-checks/bootstrap_fabric_env/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results. | [`_get_fabric_runtime_metadata`](./internal/config/_get_fabric_runtime_metadata.md) (internal) |
| [`run_config_smoke_tests`](./step-02b-notebook-startup-checks/run_config_smoke_tests/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module page" aria-label="Open config module page">config</a> | Essential | Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports. | [`_check_spark_session`](./internal/config/_check_spark_session.md) (internal), [`_get_fabric_runtime_metadata`](./internal/config/_get_fabric_runtime_metadata.md) (internal) |

## Step 3: Define source contract & ingestion pattern

This step defines the contract between the upstream source and this notebook. It captures what data is expected, including schema, data types, update frequency, update method, watermark column, and whether the source is append only, overwritten, or slowly changing. Functions in this step help the pipeline decide how to ingest, validate, snapshot, or incrementally process the source data.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`lakehouse_csv_read`](./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_excel_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_parquet_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](./internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_read`](./step-03-source-contract-ingestion-pattern/lakehouse_table_read/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`load_data_contract`](./step-03-source-contract-ingestion-pattern/load_data_contract/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module page" aria-label="Open quality module page">quality</a> | Essential | Load and normalize a data product contract from file path or dictionary. | — |
| [`warehouse_read`](./step-03-source-contract-ingestion-pattern/warehouse_read/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |

## Step 4: Ingest, profile & store source data

This step brings the source data into the framework, profiles it, and stores it for later use. Functions in this step focus on reading the data, capturing basic profiling results, and saving the raw or source-aligned version before business transformation begins.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`build_ai_quality_context`](./step-04-ingest-profile-store/build_ai_quality_context/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module page" aria-label="Open profiling module page">profiling</a> | Essential | Build deterministic AI-ready context from standard metadata profile rows. | — |
| [`build_schema_drift_records`](./step-04-ingest-profile-store/build_schema_drift_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module page" aria-label="Open metadata module page">metadata</a> | Essential | Convert schema drift results into metadata records for audit trails. | — |
| [`build_schema_snapshot_records`](./step-04-ingest-profile-store/build_schema_snapshot_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module page" aria-label="Open metadata module page">metadata</a> | Essential | Convert a schema snapshot into row-wise metadata records. | — |
| [`check_partition_drift`](./step-04-ingest-profile-store/check_partition_drift/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module page" aria-label="Open drift module page">drift</a> | Essential | Check partition-level drift using keys, partitions, and optional watermark baselines. | — |
| [`check_profile_drift`](./step-04-ingest-profile-store/check_profile_drift/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module page" aria-label="Open drift module page">drift</a> | Essential | Compare profile metrics against a baseline profile and drift thresholds. | — |
| [`check_schema_drift`](./step-04-ingest-profile-store/check_schema_drift/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module page" aria-label="Open drift module page">drift</a> | Essential | Compare a current dataframe schema against a baseline schema snapshot. | — |
| [`generate_metadata_profile`](./step-04-ingest-profile-store/generate_metadata_profile/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module page" aria-label="Open profiling module page">profiling</a> | Essential | Generate standard metadata profile rows for a Spark/Fabric DataFrame. | — |
| [`profile_dataframe`](./step-04-ingest-profile-store/profile_dataframe/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module page" aria-label="Open profiling module page">profiling</a> | Essential | Build a lightweight profile for pandas or Spark-like DataFrames. | — |
| [`profile_dataframe_to_metadata`](./step-04-ingest-profile-store/profile_dataframe_to_metadata/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module page" aria-label="Open profiling module page">profiling</a> | Essential | Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows. | — |
| [`profile_metadata_to_records`](./step-04-ingest-profile-store/profile_metadata_to_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module page" aria-label="Open profiling module page">profiling</a> | Essential | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — |
| [`summarize_drift_results`](./step-04-ingest-profile-store/summarize_drift_results/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module page" aria-label="Open drift module page">drift</a> | Essential | Summarize schema, partition, and profile drift outcomes into one decision. | — |

## Step 5: Explore data & explain transformation logic

This step is where the analyst studies the profiled source data and explains why transformation is needed. There may not be many helper functions here today, but future functions could support standard EDA, AI assisted analysis, and documentation of business assumptions before the logic becomes part of the repeatable pipeline.

No public callable currently mapped to this step.

No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.

## Step 6A: Write transformation logic

This step contains the main transformation logic that converts source-aligned data into the target output. Functions here support reusable pipeline code so the same logic can run consistently during development, testing, and scheduled refresh.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`run_data_product`](./step-06a-transformation-logic/run_data_product/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module page" aria-label="Open quality module page">quality</a> | Essential | Run the starter kit workflow end-to-end for a data product outcome. | [`_effective_contract_dict`](./internal/quality/_effective_contract_dict.md) (internal), [`_refresh_mode`](./internal/quality/_refresh_mode.md) (internal), [`_runtime_validation_contract`](./internal/quality/_runtime_validation_contract.md) (internal), [`_write_dataframe_to_table`](./internal/quality/_write_dataframe_to_table.md) (internal), [`_write_records_spark`](./internal/quality/_write_records_spark.md) (internal) |

## Step 6B: Apply runtime standards

This step applies standard runtime requirements such as technical columns, run IDs, timestamps, partition keys, and other repeatable conventions. Functions here make outputs easier to audit, troubleshoot, join back to pipeline runs, and operate at scale.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`add_audit_columns`](./step-06b-runtime-standards/add_audit_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module page" aria-label="Open technical_columns module page">technical_columns</a> | Essential | Add run tracking and audit columns for ingestion workflows. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_bucket_values_pandas`](./internal/technical_columns/_bucket_values_pandas.md) (internal), [`_get_fabric_runtime_context`](./internal/technical_columns/_get_fabric_runtime_context.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) |
| [`add_datetime_features`](./step-06b-runtime-standards/add_datetime_features/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module page" aria-label="Open technical_columns module page">technical_columns</a> | Essential | Add localized datetime feature columns derived from a UTC datetime column. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) |
| [`add_hash_columns`](./step-06b-runtime-standards/add_hash_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module page" aria-label="Open technical_columns module page">technical_columns</a> | Essential | Add business key and row-level SHA256 hash columns. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_hash_row`](./internal/technical_columns/_hash_row.md) (internal), [`_non_technical_columns`](./internal/technical_columns/_non_technical_columns.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) |
| [`default_technical_columns`](./step-06b-runtime-standards/default_technical_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module page" aria-label="Open technical_columns module page">technical_columns</a> | Essential | Return framework-generated and legacy technical column names to ignore. | — |

## Step 6C: Enforce pipeline controls

This step enforces the controls that decide whether the pipeline output should be trusted. Functions here support data quality rules, schema checks, classification checks, and other contract validations before data is released downstream.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`run_quality_rules`](./step-06c-pipeline-controls/run_quality_rules/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module page" aria-label="Open quality module page">quality</a> | Essential | Execute quality rules against a dataframe and return structured results. | [`_normalize_severity`](./internal/quality/_normalize_severity.md) (internal), [`_now_iso`](./internal/quality/_now_iso.md) (internal), [`_pandas_rule`](./internal/quality/_pandas_rule.md) (internal), [`_resolve_engine`](./internal/quality/_resolve_engine.md) (internal), [`_result_from_counts`](./internal/quality/_result_from_counts.md) (internal), [`_spark_rule`](./internal/quality/_spark_rule.md) (internal), [`_to_jsonable`](./internal/quality/_to_jsonable.md) (internal) |

## Step 6D: Write controlled outputs

This step writes the transformed output to the correct lakehouse, warehouse, or product layer. Functions here make the write pattern explicit, repeatable, and aligned to the intended environment instead of relying on ad hoc exports.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`lakehouse_table_write`](./step-06d-controlled-outputs/lakehouse_table_write/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`warehouse_write`](./step-06d-controlled-outputs/warehouse_write/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module page" aria-label="Open fabric_io module page">fabric_io</a> | Essential | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Step 7: Profile output & publish product contract

This step profiles the created output, stores its metadata, and creates the data contract for the next notebook, pipeline, or consumer. Functions here help record what was produced, write the evidence to metadata tables or catalogues, and make the output understandable and reusable downstream.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`build_dataset_run_record`](./step-07-output-profile-product-contract/build_dataset_run_record/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module page" aria-label="Open metadata module page">metadata</a> | Essential | Build a dataset-run metadata record for operational tracking. | — |
| [`build_quality_result_records`](./step-07-output-profile-product-contract/build_quality_result_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module page" aria-label="Open metadata module page">metadata</a> | Essential | Convert quality-rule execution output into metadata evidence records. | — |
| [`write_metadata_records`](./step-07-output-profile-product-contract/write_metadata_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module page" aria-label="Open metadata module page">metadata</a> | Essential | Write metadata records to a configured metadata sink. | — |
| [`write_multiple_metadata_outputs`](./step-07-output-profile-product-contract/write_multiple_metadata_outputs/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module page" aria-label="Open metadata module page">metadata</a> | Essential | Write multiple metadata payloads to their configured destinations. | — |

## Step 8: Suggest AI assisted data quality rules

This step uses AI in exploration notebooks to suggest possible data quality rules from profiling results, business context, and source knowledge. These AI functions are only advisory. The actual rule creation, approval, and enforcement must still be done by the human engineer in the pipeline notebook.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`build_dq_rule_candidate_prompt`](./step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Build the DQ-candidate prompt used in AI-assisted quality drafting. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_manual_dq_rule_prompt_package`](./step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Build copy/paste prompt package for manual DQ candidate generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) |
| [`generate_dq_rule_candidates_with_fabric_ai`](./step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Append AI-suggested DQ rule candidates to a profiling DataFrame. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) |

## Step 9: Suggest AI assisted column classification

This step uses AI in exploration notebooks to suggest column classifications such as PII, sensitivity level, and governance labels for the planned output. These AI functions are only advisory. The actual label assignment must be approved by governance or data stewards and enforced by the human engineer in the pipeline notebook.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`build_governance_candidate_prompt`](./step-09-ai-assisted-classification/build_governance_candidate_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Build the governance-candidate prompt for AI-assisted classification drafts. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_governance_classification_records`](./step-09-ai-assisted-classification/build_governance_classification_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module page" aria-label="Open governance module page">governance</a> | Optional | Build metadata-ready governance classification records from column suggestions. | — |
| [`build_manual_governance_prompt_package`](./step-09-ai-assisted-classification/build_manual_governance_prompt_package/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Build copy/paste prompt package for manual governance suggestion generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) |
| [`classify_column`](./step-09-ai-assisted-classification/classify_column/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module page" aria-label="Open governance module page">governance</a> | Optional | Classify one column using term matching, metadata cues, and business context. | [`_match_terms`](./internal/governance/_match_terms.md) (internal), [`_phrase_in_text`](./internal/governance/_phrase_in_text.md) (internal) |
| [`classify_columns`](./step-09-ai-assisted-classification/classify_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module page" aria-label="Open governance module page">governance</a> | Optional | Classify multiple columns and return normalized governance suggestions. | [`_column_name`](./internal/governance/_column_name.md) (internal), [`_normalize_columns`](./internal/governance/_normalize_columns.md) (internal) |
| [`generate_governance_candidates_with_fabric_ai`](./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Execute Fabric AI Functions to append governance suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`summarize_governance_classifications`](./step-09-ai-assisted-classification/summarize_governance_classifications/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module page" aria-label="Open governance module page">governance</a> | Optional | Summarize governance classification outputs into review-friendly counts. | — |
| [`write_governance_classifications`](./step-09-ai-assisted-classification/write_governance_classifications/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module page" aria-label="Open governance module page">governance</a> | Optional | Persist governance classifications to a metadata destination. | [`_spark_create_governance_metadata_dataframe`](./internal/governance/_spark_create_governance_metadata_dataframe.md) (internal) |

## Step 10: Generate lineage & handover documentation

This step creates the final documentation needed for review, handover, and future maintenance. Functions here support lineage, transformation summaries, and handover notes so another analyst or engineer can understand what was built, why it was built, and how to operate it.

| Function / class | Module | Importance | Purpose | Related helpers |
|---|---|---|---|---|
| [`build_handover_summary_prompt`](./step-10-lineage-handover-documentation/build_handover_summary_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Build the handover-summary prompt for AI-assisted run handoff drafting. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_lineage_from_notebook_code`](./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Scan, optionally enrich, and validate lineage from notebook source code. | — |
| [`build_lineage_handover_markdown`](./step-10-lineage-handover-documentation/build_lineage_handover_markdown/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Create a concise markdown handover summary from lineage execution results. | — |
| [`build_lineage_record_from_steps`](./step-10-lineage-handover-documentation/build_lineage_record_from_steps/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Create metadata-ready lineage records from validated lineage steps. | — |
| [`build_lineage_records`](./step-10-lineage-handover-documentation/build_lineage_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Build compact lineage records for downstream metadata sinks. | — |
| [`build_manual_handover_prompt_package`](./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Build copy/paste prompt package for manual handover summary generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) |
| [`build_run_summary`](./step-10-lineage-handover-documentation/build_run_summary/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/run_summary/" title="Open run_summary module page" aria-label="Open run_summary module page">run_summary</a> | Optional | Build a handover-friendly summary for one data product run. | — |
| [`enrich_lineage_steps_with_ai`](./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Optionally enrich deterministic lineage steps using an AI helper callable. | — |
| [`fallback_copilot_lineage_prompt`](./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Build a fallback Copilot prompt for manual lineage enrichment. | — |
| [`generate_handover_summary_with_fabric_ai`](./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Execute Fabric AI Functions to append handover summary suggestions. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`parse_manual_ai_json_response`](./step-10-lineage-handover-documentation/parse_manual_ai_json_response/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> | Optional | Parse manual AI JSON output into Python objects. | — |
| [`plot_lineage_steps`](./step-10-lineage-handover-documentation/plot_lineage_steps/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Render lineage steps as a directed graph figure. | — |
| [`render_run_summary_markdown`](./step-10-lineage-handover-documentation/render_run_summary_markdown/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/run_summary/" title="Open run_summary module page" aria-label="Open run_summary module page">run_summary</a> | Optional | Render a run summary dictionary into Markdown for handover notes. | [`_status_of`](./internal/run_summary/_status_of.md) (internal) |
| [`scan_notebook_cells`](./step-10-lineage-handover-documentation/scan_notebook_cells/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Scan multiple notebook cells and append cell references to lineage steps. | — |
| [`scan_notebook_lineage`](./step-10-lineage-handover-documentation/scan_notebook_lineage/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Extract deterministic lineage steps from notebook code using AST parsing. | [`_call_name`](./internal/lineage/_call_name.md) (internal), [`_flatten_chain`](./internal/lineage/_flatten_chain.md) (internal), [`_name`](./internal/lineage/_name.md) (internal), [`_resolve_write_target`](./internal/lineage/_resolve_write_target.md) (internal), [`_step`](./internal/lineage/_step.md) (internal) |
| [`validate_lineage_steps`](./step-10-lineage-handover-documentation/validate_lineage_steps/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module page" aria-label="Open lineage module page">lineage</a> | Optional | Validate lineage step structure and flag records requiring human review. | — |

## Other exported callables

These callables are exported by `fabricops_kit.__all__` but are not currently mapped to a lifecycle step. They are listed here so the public reference remains complete.

No unmapped exported callables.



Use these `.ipynb` templates by importing/copying them into Fabric and renaming the actual notebook to the required lifecycle naming convention. Notebook name validation reads the running notebook name from Fabric runtime context when available.


- Exploration notebooks can draft and approve contract records, then persist them via contract metadata helpers into the metadata target.
- Pipeline notebooks load latest approved contract records from the metadata target for required columns, keys, and quality-rule enforcement.
