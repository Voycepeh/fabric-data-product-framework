# Callable Functions

Generated step-first catalogue of callable functions sourced from `fabricops_kit.__all__`.

## Modules

| Module | Link |
|---|---|
| `ai` | [Open module overview](../api/modules/ai/) |
| `config` | [Open module overview](../api/modules/config/) |
| `docs_metadata` | [Open module overview](../api/modules/docs_metadata/) |
| `drift` | [Open module overview](../api/modules/drift/) |
| `fabric_io` | [Open module overview](../api/modules/fabric_io/) |
| `governance` | [Open module overview](../api/modules/governance/) |
| `handover` | [Open module overview](../api/modules/handover/) |
| `lineage` | [Open module overview](../api/modules/lineage/) |
| `metadata` | [Open module overview](../api/modules/metadata/) |
| `profiling` | [Open module overview](../api/modules/profiling/) |
| `quality` | [Open module overview](../api/modules/quality/) |
| `run_summary` | [Open module overview](../api/modules/run_summary/) |
| `runtime` | [Open module overview](../api/modules/runtime/) |
| `technical_columns` | [Open module overview](../api/modules/technical_columns/) |

## Step 1: Define purpose, approved usage & governance ownership

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`assert_notebook_name_valid`](./step-01-governance-purpose-ownership/assert_notebook_name_valid/) | `runtime` | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — | [module overview](../api/modules/runtime/) |
| [`build_runtime_context`](./step-01-governance-purpose-ownership/build_runtime_context/) | `runtime` | Build a standard runtime context dictionary for Fabric notebooks. | — | [module overview](../api/modules/runtime/) |
| [`check_fabric_ai_functions_available`](./step-01-governance-purpose-ownership/check_fabric_ai_functions_available/) | `ai` | Check whether Fabric AI Functions can be imported in the current runtime. | — | [module overview](../api/modules/ai/) |
| [`configure_fabric_ai_functions`](./step-01-governance-purpose-ownership/configure_fabric_ai_functions/) | `ai` | Apply optional default Fabric AI Function configuration. | — | [module overview](../api/modules/ai/) |
| [`generate_run_id`](./step-01-governance-purpose-ownership/generate_run_id/) | `runtime` | Generate a notebook-safe run identifier. | — | [module overview](../api/modules/runtime/) |
| [`validate_notebook_name`](./step-01-governance-purpose-ownership/validate_notebook_name/) | `runtime` | Validate notebook names against the framework workspace notebook model. | — | [module overview](../api/modules/runtime/) |

## Step 2: Configure runtime, environment & path rules

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`create_ai_prompt_config`](./step-02-runtime-environment-path-rules/create_ai_prompt_config/) | `config` | Create AI prompt-template configuration. | — | [module overview](../api/modules/config/) |
| [`create_framework_config`](./step-02-runtime-environment-path-rules/create_framework_config/) | `config` | Create the top-level framework configuration object. | — | [module overview](../api/modules/config/) |
| [`create_governance_config`](./step-02-runtime-environment-path-rules/create_governance_config/) | `config` | Create governance-default configuration. | — | [module overview](../api/modules/config/) |
| [`create_lineage_config`](./step-02-runtime-environment-path-rules/create_lineage_config/) | `config` | Create lineage-default configuration. | — | [module overview](../api/modules/config/) |
| [`create_notebook_runtime_config`](./step-02-runtime-environment-path-rules/create_notebook_runtime_config/) | `config` | Create notebook runtime configuration. | — | [module overview](../api/modules/config/) |
| [`create_path_config`](./step-02-runtime-environment-path-rules/create_path_config/) | `config` | Create a validated :class:`PathConfig` object. | — | [module overview](../api/modules/config/) |
| [`create_quality_config`](./step-02-runtime-environment-path-rules/create_quality_config/) | `config` | Create quality-default configuration. | — | [module overview](../api/modules/config/) |
| [`get_path`](./step-02-runtime-environment-path-rules/get_path/) | `fabric_io` | Return the Fabric path object for an environment and target. | — | [module overview](../api/modules/fabric_io/) |
| [`Housepath`](./step-02-runtime-environment-path-rules/Housepath/) | `fabric_io` | Fabric lakehouse or warehouse connection details. | — | [module overview](../api/modules/fabric_io/) |
| [`load_fabric_config`](./step-02-runtime-environment-path-rules/load_fabric_config/) | `fabric_io` | Validate and return a framework config mapping. | — | [module overview](../api/modules/fabric_io/) |
| [`validate_framework_config`](./step-02-runtime-environment-path-rules/validate_framework_config/) | `config` | Validate and normalize framework config input. | — | [module overview](../api/modules/config/) |

## Step 3: Declare source contract & ingest source data

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`lakehouse_csv_read`](./step-03-source-contract-ingestion/lakehouse_csv_read/) | `fabric_io` | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io/) |
| [`lakehouse_excel_read_as_spark`](./step-03-source-contract-ingestion/lakehouse_excel_read_as_spark/) | `fabric_io` | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io/) |
| [`lakehouse_parquet_read_as_spark`](./step-03-source-contract-ingestion/lakehouse_parquet_read_as_spark/) | `fabric_io` | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](./internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io/) |
| [`lakehouse_table_read`](./step-03-source-contract-ingestion/lakehouse_table_read/) | `fabric_io` | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io/) |
| [`load_data_contract`](./step-03-source-contract-ingestion/load_data_contract/) | `quality` | Load data contract. | — | [module overview](../api/modules/quality/) |
| [`warehouse_read`](./step-03-source-contract-ingestion/warehouse_read/) | `fabric_io` | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io/) |

## Step 4: Validate source against contract & capture metadata

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_ai_quality_context`](./step-04-source-validation-metadata/build_ai_quality_context/) | `profiling` | Build deterministic AI-ready context from standard metadata profile rows. | — | [module overview](../api/modules/profiling/) |
| [`build_schema_drift_records`](./step-04-source-validation-metadata/build_schema_drift_records/) | `metadata` | Build schema drift records. | — | [module overview](../api/modules/metadata/) |
| [`build_schema_snapshot_records`](./step-04-source-validation-metadata/build_schema_snapshot_records/) | `metadata` | Build schema snapshot records. | — | [module overview](../api/modules/metadata/) |
| [`check_partition_drift`](./step-04-source-validation-metadata/check_partition_drift/) | `drift` | Check partition drift. | — | [module overview](../api/modules/drift/) |
| [`check_profile_drift`](./step-04-source-validation-metadata/check_profile_drift/) | `drift` | Check profile drift. | — | [module overview](../api/modules/drift/) |
| [`check_schema_drift`](./step-04-source-validation-metadata/check_schema_drift/) | `drift` | Check schema drift. | — | [module overview](../api/modules/drift/) |
| [`generate_metadata_profile`](./step-04-source-validation-metadata/generate_metadata_profile/) | `profiling` | Generate standard metadata profile rows for a Spark/Fabric DataFrame. | — | [module overview](../api/modules/profiling/) |
| [`profile_dataframe`](./step-04-source-validation-metadata/profile_dataframe/) | `profiling` | Build a lightweight profile for pandas or Spark-like DataFrames. | — | [module overview](../api/modules/profiling/) |
| [`profile_dataframe_to_metadata`](./step-04-source-validation-metadata/profile_dataframe_to_metadata/) | `profiling` | Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows. | — | [module overview](../api/modules/profiling/) |
| [`profile_metadata_to_records`](./step-04-source-validation-metadata/profile_metadata_to_records/) | `profiling` | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — | [module overview](../api/modules/profiling/) |
| [`summarize_drift_results`](./step-04-source-validation-metadata/summarize_drift_results/) | `drift` | Summarize drift results. | — | [module overview](../api/modules/drift/) |

## Step 5: Explore data & capture transformation / DQ rationale

No public callable currently mapped to this step.

No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.

## Step 6: Build production transformation & write target output

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`add_audit_columns`](./step-06-production-transformation-output/add_audit_columns/) | `technical_columns` | Add run tracking and audit columns for ingestion workflows. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_bucket_values_pandas`](./internal/technical_columns/_bucket_values_pandas.md) (internal), [`_get_fabric_runtime_context`](./internal/technical_columns/_get_fabric_runtime_context.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) | [module overview](../api/modules/technical_columns/) |
| [`add_datetime_features`](./step-06-production-transformation-output/add_datetime_features/) | `technical_columns` | Add localized datetime feature columns derived from a UTC datetime column. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) | [module overview](../api/modules/technical_columns/) |
| [`add_hash_columns`](./step-06-production-transformation-output/add_hash_columns/) | `technical_columns` | Add business key and row-level SHA256 hash columns. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_hash_row`](./internal/technical_columns/_hash_row.md) (internal), [`_non_technical_columns`](./internal/technical_columns/_non_technical_columns.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) | [module overview](../api/modules/technical_columns/) |
| [`default_technical_columns`](./step-06-production-transformation-output/default_technical_columns/) | `technical_columns` | Return framework-generated and legacy technical column names to ignore. | — | [module overview](../api/modules/technical_columns/) |
| [`run_data_product`](./step-06-production-transformation-output/run_data_product/) | `quality` | Run the starter kit workflow end-to-end for a data product outcome. | [`_effective_contract_dict`](./internal/quality/_effective_contract_dict.md) (internal), [`_refresh_mode`](./internal/quality/_refresh_mode.md) (internal), [`_runtime_validation_contract`](./internal/quality/_runtime_validation_contract.md) (internal), [`_write_dataframe_to_table`](./internal/quality/_write_dataframe_to_table.md) (internal), [`_write_records_spark`](./internal/quality/_write_records_spark.md) (internal) | [module overview](../api/modules/quality/) |

## Step 7: Validate output & persist target metadata

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_dataset_run_record`](./step-07-output-validation-target-metadata/build_dataset_run_record/) | `metadata` | Build dataset run record. | — | [module overview](../api/modules/metadata/) |
| [`build_quality_result_records`](./step-07-output-validation-target-metadata/build_quality_result_records/) | `metadata` | Build quality result records. | — | [module overview](../api/modules/metadata/) |
| [`lakehouse_table_write`](./step-07-output-validation-target-metadata/lakehouse_table_write/) | `fabric_io` | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — | [module overview](../api/modules/fabric_io/) |
| [`warehouse_write`](./step-07-output-validation-target-metadata/warehouse_write/) | `fabric_io` | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [module overview](../api/modules/fabric_io/) |
| [`write_metadata_records`](./step-07-output-validation-target-metadata/write_metadata_records/) | `metadata` | Write metadata records. | — | [module overview](../api/modules/metadata/) |
| [`write_multiple_metadata_outputs`](./step-07-output-validation-target-metadata/write_multiple_metadata_outputs/) | `metadata` | Write multiple metadata outputs. | — | [module overview](../api/modules/metadata/) |

## Step 8: Generate, review & configure DQ rules

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_dq_rule_candidate_prompt`](./step-08-dq-rule-generation-review/build_dq_rule_candidate_prompt/) | `ai` | Build standardized prompt text for AI-assisted DQ candidate generation. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) | [module overview](../api/modules/ai/) |
| [`build_manual_dq_rule_prompt_package`](./step-08-dq-rule-generation-review/build_manual_dq_rule_prompt_package/) | `ai` | Build copy/paste prompt package for manual DQ candidate generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) | [module overview](../api/modules/ai/) |
| [`generate_dq_rule_candidates_with_fabric_ai`](./step-08-dq-rule-generation-review/generate_dq_rule_candidates_with_fabric_ai/) | `ai` | Execute Fabric AI Functions to append DQ candidate suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) | [module overview](../api/modules/ai/) |
| [`run_quality_rules`](./step-08-dq-rule-generation-review/run_quality_rules/) | `quality` | Run quality rules. | [`_normalize_severity`](./internal/quality/_normalize_severity.md) (internal), [`_now_iso`](./internal/quality/_now_iso.md) (internal), [`_pandas_rule`](./internal/quality/_pandas_rule.md) (internal), [`_resolve_engine`](./internal/quality/_resolve_engine.md) (internal), [`_result_from_counts`](./internal/quality/_result_from_counts.md) (internal), [`_spark_rule`](./internal/quality/_spark_rule.md) (internal), [`_to_jsonable`](./internal/quality/_to_jsonable.md) (internal) | [module overview](../api/modules/quality/) |

## Step 9: Generate & review classification / sensitivity suggestions

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_governance_candidate_prompt`](./step-09-classification-sensitivity/build_governance_candidate_prompt/) | `ai` | Build standardized prompt text for AI-assisted governance suggestions. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) | [module overview](../api/modules/ai/) |
| [`build_governance_classification_records`](./step-09-classification-sensitivity/build_governance_classification_records/) | `governance` | Build governance classification records. | — | [module overview](../api/modules/governance/) |
| [`build_manual_governance_prompt_package`](./step-09-classification-sensitivity/build_manual_governance_prompt_package/) | `ai` | Build copy/paste prompt package for manual governance suggestion generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) | [module overview](../api/modules/ai/) |
| [`classify_column`](./step-09-classification-sensitivity/classify_column/) | `governance` | Classify column. | [`_match_terms`](./internal/governance/_match_terms.md) (internal), [`_phrase_in_text`](./internal/governance/_phrase_in_text.md) (internal) | [module overview](../api/modules/governance/) |
| [`classify_columns`](./step-09-classification-sensitivity/classify_columns/) | `governance` | Classify columns. | [`_column_name`](./internal/governance/_column_name.md) (internal), [`_normalize_columns`](./internal/governance/_normalize_columns.md) (internal) | [module overview](../api/modules/governance/) |
| [`generate_governance_candidates_with_fabric_ai`](./step-09-classification-sensitivity/generate_governance_candidates_with_fabric_ai/) | `ai` | Execute Fabric AI Functions to append governance suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) | [module overview](../api/modules/ai/) |
| [`summarize_governance_classifications`](./step-09-classification-sensitivity/summarize_governance_classifications/) | `governance` | Summarize governance classifications. | — | [module overview](../api/modules/governance/) |
| [`write_governance_classifications`](./step-09-classification-sensitivity/write_governance_classifications/) | `governance` | Write governance classifications. | [`_spark_create_governance_metadata_dataframe`](./internal/governance/_spark_create_governance_metadata_dataframe.md) (internal) | [module overview](../api/modules/governance/) |

## Step 10: Generate data lineage and handover documentation

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_handover_summary_prompt`](./step-10-lineage-handover-documentation/build_handover_summary_prompt/) | `ai` | Build standardized prompt text for AI-assisted handover summary suggestions. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) | [module overview](../api/modules/ai/) |
| [`build_lineage_from_notebook_code`](./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/) | `lineage` | Scan, optionally enrich, and validate lineage from notebook source code. | — | [module overview](../api/modules/lineage/) |
| [`build_lineage_handover_markdown`](./step-10-lineage-handover-documentation/build_lineage_handover_markdown/) | `lineage` | Create a concise markdown handover summary from lineage execution results. | — | [module overview](../api/modules/lineage/) |
| [`build_lineage_record_from_steps`](./step-10-lineage-handover-documentation/build_lineage_record_from_steps/) | `lineage` | Create metadata-ready lineage records from validated lineage steps. | — | [module overview](../api/modules/lineage/) |
| [`build_lineage_records`](./step-10-lineage-handover-documentation/build_lineage_records/) | `lineage` | Build compact lineage records for downstream metadata sinks. | — | [module overview](../api/modules/lineage/) |
| [`build_manual_handover_prompt_package`](./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/) | `ai` | Build copy/paste prompt package for manual handover summary generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) | [module overview](../api/modules/ai/) |
| [`build_run_summary`](./step-10-lineage-handover-documentation/build_run_summary/) | `run_summary` | Build run summary. | — | [module overview](../api/modules/run_summary/) |
| [`enrich_lineage_steps_with_ai`](./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/) | `lineage` | Optionally enrich deterministic lineage steps using an AI helper callable. | — | [module overview](../api/modules/lineage/) |
| [`fallback_copilot_lineage_prompt`](./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/) | `lineage` | Build a fallback Copilot prompt for manual lineage enrichment. | — | [module overview](../api/modules/lineage/) |
| [`generate_handover_summary_with_fabric_ai`](./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/) | `ai` | Execute Fabric AI Functions to append handover summary suggestions. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) | [module overview](../api/modules/ai/) |
| [`parse_manual_ai_json_response`](./step-10-lineage-handover-documentation/parse_manual_ai_json_response/) | `ai` | Parse manual AI JSON output into Python objects. | — | [module overview](../api/modules/ai/) |
| [`plot_lineage_steps`](./step-10-lineage-handover-documentation/plot_lineage_steps/) | `lineage` | Render lineage steps as a directed graph figure. | — | [module overview](../api/modules/lineage/) |
| [`render_run_summary_markdown`](./step-10-lineage-handover-documentation/render_run_summary_markdown/) | `run_summary` | Render run summary markdown. | [`_status_of`](./internal/run_summary/_status_of.md) (internal) | [module overview](../api/modules/run_summary/) |
| [`scan_notebook_cells`](./step-10-lineage-handover-documentation/scan_notebook_cells/) | `lineage` | Scan multiple notebook cells and append cell references to lineage steps. | — | [module overview](../api/modules/lineage/) |
| [`scan_notebook_lineage`](./step-10-lineage-handover-documentation/scan_notebook_lineage/) | `lineage` | Extract deterministic lineage steps from notebook code using AST parsing. | [`_call_name`](./internal/lineage/_call_name.md) (internal), [`_flatten_chain`](./internal/lineage/_flatten_chain.md) (internal), [`_name`](./internal/lineage/_name.md) (internal), [`_resolve_write_target`](./internal/lineage/_resolve_write_target.md) (internal), [`_step`](./internal/lineage/_step.md) (internal) | [module overview](../api/modules/lineage/) |
| [`validate_lineage_steps`](./step-10-lineage-handover-documentation/validate_lineage_steps/) | `lineage` | Validate lineage step structure and flag records requiring human review. | — | [module overview](../api/modules/lineage/) |

