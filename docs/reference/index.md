# Callable Functions

Generated step-first catalogue of callable functions sourced from `fabricops_kit.__all__`.

## Modules

| Module |
|---|
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/docs_metadata/" title="Open docs_metadata module overview" aria-label="Open docs_metadata module overview">docs_metadata</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module overview" aria-label="Open drift module overview">drift</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module overview" aria-label="Open governance module overview">governance</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover/" title="Open handover module overview" aria-label="Open handover module overview">handover</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module overview" aria-label="Open metadata module overview">metadata</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module overview" aria-label="Open profiling module overview">profiling</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module overview" aria-label="Open quality module overview">quality</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/run_summary/" title="Open run_summary module overview" aria-label="Open run_summary module overview">run_summary</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module overview" aria-label="Open runtime module overview">runtime</a> |
| <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module overview" aria-label="Open technical_columns module overview">technical_columns</a> |

## Step 1: Package and runtime setup

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`assert_notebook_name_valid`](./step-01-purpose-setup/assert_notebook_name_valid/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module overview" aria-label="Open runtime module overview">runtime</a> | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — |
| [`build_runtime_context`](./step-01-purpose-setup/build_runtime_context/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module overview" aria-label="Open runtime module overview">runtime</a> | Build a standard runtime context dictionary for Fabric notebooks. | — |
| [`check_fabric_ai_functions_available`](./step-01-purpose-setup/check_fabric_ai_functions_available/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Check whether Fabric AI Functions can be imported in the current runtime. | — |
| [`configure_fabric_ai_functions`](./step-01-purpose-setup/configure_fabric_ai_functions/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Apply optional default Fabric AI Function configuration. | — |
| [`generate_run_id`](./step-01-purpose-setup/generate_run_id/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module overview" aria-label="Open runtime module overview">runtime</a> | Generate a notebook-safe run identifier. | — |
| [`validate_notebook_name`](./step-01-purpose-setup/validate_notebook_name/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime/" title="Open runtime module overview" aria-label="Open runtime module overview">runtime</a> | Validate notebook names against the framework workspace notebook model. | — |

## Step 2: Fabric config and paths

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`create_ai_prompt_config`](./step-02-runtime-configuration/create_ai_prompt_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Create AI prompt-template configuration. | — |
| [`create_framework_config`](./step-02-runtime-configuration/create_framework_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Create the top-level framework configuration object. | — |
| [`create_governance_config`](./step-02-runtime-configuration/create_governance_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Create governance-default configuration. | — |
| [`create_lineage_config`](./step-02-runtime-configuration/create_lineage_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Create lineage-default configuration. | — |
| [`create_notebook_runtime_config`](./step-02-runtime-configuration/create_notebook_runtime_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Create notebook runtime configuration. | — |
| [`create_path_config`](./step-02-runtime-configuration/create_path_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Create a validated :class:`PathConfig` object. | — |
| [`create_quality_config`](./step-02-runtime-configuration/create_quality_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Create quality-default configuration. | — |
| [`get_path`](./step-02-runtime-configuration/get_path/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Return the Fabric path object for an environment and target. | — |
| [`Housepath`](./step-02-runtime-configuration/Housepath/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Fabric lakehouse or warehouse connection details. | — |
| [`load_fabric_config`](./step-02-runtime-configuration/load_fabric_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Validate and return a framework config mapping. | — |
| [`validate_framework_config`](./step-02-runtime-configuration/validate_framework_config/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/config/" title="Open config module overview" aria-label="Open config module overview">config</a> | Validate and normalize framework config input. | — |

## Step 3: Pull source data

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`lakehouse_csv_read`](./step-03-source-declaration-paths/lakehouse_csv_read/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_excel_read_as_spark`](./step-03-source-declaration-paths/lakehouse_excel_read_as_spark/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_parquet_read_as_spark`](./step-03-source-declaration-paths/lakehouse_parquet_read_as_spark/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](./internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_read`](./step-03-source-declaration-paths/lakehouse_table_read/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |
| [`warehouse_read`](./step-03-source-declaration-paths/warehouse_read/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) |

## Step 4: Source profiling

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`build_ai_quality_context`](./step-04-source-ingestion-read-helpers/build_ai_quality_context/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module overview" aria-label="Open profiling module overview">profiling</a> | Build deterministic AI-ready context from standard metadata profile rows. | — |
| [`generate_metadata_profile`](./step-04-source-ingestion-read-helpers/generate_metadata_profile/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module overview" aria-label="Open profiling module overview">profiling</a> | Generate standard metadata profile rows for a Spark/Fabric DataFrame. | — |
| [`profile_dataframe`](./step-04-source-ingestion-read-helpers/profile_dataframe/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module overview" aria-label="Open profiling module overview">profiling</a> | Build a lightweight profile for pandas or Spark-like DataFrames. | — |
| [`profile_dataframe_to_metadata`](./step-04-source-ingestion-read-helpers/profile_dataframe_to_metadata/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module overview" aria-label="Open profiling module overview">profiling</a> | Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows. | — |
| [`profile_metadata_to_records`](./step-04-source-ingestion-read-helpers/profile_metadata_to_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/profiling/" title="Open profiling module overview" aria-label="Open profiling module overview">profiling</a> | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — |

## Step 5: AI assisted DQ rule drafting

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`build_dq_rule_candidate_prompt`](./step-05-source-profiling-metadata/build_dq_rule_candidate_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Build standardized prompt text for AI-assisted DQ candidate generation. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_manual_dq_rule_prompt_package`](./step-05-source-profiling-metadata/build_manual_dq_rule_prompt_package/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Build copy/paste prompt package for manual DQ candidate generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) |
| [`generate_dq_rule_candidates_with_fabric_ai`](./step-05-source-profiling-metadata/generate_dq_rule_candidates_with_fabric_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Execute Fabric AI Functions to append DQ candidate suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) |

## Step 6: Human review of rules and metadata

No public callable currently mapped to this step.

## Step 7: Compile and run DQ checks

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`load_data_contract`](./step-07-ai-rule-generation-review/load_data_contract/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module overview" aria-label="Open quality module overview">quality</a> | Load data contract. | — |
| [`run_quality_rules`](./step-07-ai-rule-generation-review/run_quality_rules/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module overview" aria-label="Open quality module overview">quality</a> | Run quality rules. | [`_normalize_severity`](./internal/quality/_normalize_severity.md) (internal), [`_now_iso`](./internal/quality/_now_iso.md) (internal), [`_pandas_rule`](./internal/quality/_pandas_rule.md) (internal), [`_resolve_engine`](./internal/quality/_resolve_engine.md) (internal), [`_result_from_counts`](./internal/quality/_result_from_counts.md) (internal), [`_spark_rule`](./internal/quality/_spark_rule.md) (internal), [`_to_jsonable`](./internal/quality/_to_jsonable.md) (internal) |

## Step 8: Schema/profile/data drift checks

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`check_partition_drift`](./step-08-quality-rule-execution/check_partition_drift/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module overview" aria-label="Open drift module overview">drift</a> | Check partition drift. | — |
| [`check_profile_drift`](./step-08-quality-rule-execution/check_profile_drift/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module overview" aria-label="Open drift module overview">drift</a> | Check profile drift. | — |
| [`check_schema_drift`](./step-08-quality-rule-execution/check_schema_drift/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module overview" aria-label="Open drift module overview">drift</a> | Check schema drift. | — |
| [`summarize_drift_results`](./step-08-quality-rule-execution/summarize_drift_results/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/drift/" title="Open drift module overview" aria-label="Open drift module overview">drift</a> | Summarize drift results. | — |

## Step 9: Core transformation

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`run_data_product`](./step-09-core-transformation-business-logic/run_data_product/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/quality/" title="Open quality module overview" aria-label="Open quality module overview">quality</a> | Run the starter kit workflow end-to-end for a data product outcome. | [`_effective_contract_dict`](./internal/quality/_effective_contract_dict.md) (internal), [`_refresh_mode`](./internal/quality/_refresh_mode.md) (internal), [`_runtime_validation_contract`](./internal/quality/_runtime_validation_contract.md) (internal), [`_write_dataframe_to_table`](./internal/quality/_write_dataframe_to_table.md) (internal), [`_write_records_spark`](./internal/quality/_write_records_spark.md) (internal) |

## Step 10: Standard technical columns

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`add_audit_columns`](./step-10-technical-columns-write-prep/add_audit_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module overview" aria-label="Open technical_columns module overview">technical_columns</a> | Add run tracking and audit columns for ingestion workflows. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_bucket_values_pandas`](./internal/technical_columns/_bucket_values_pandas.md) (internal), [`_get_fabric_runtime_context`](./internal/technical_columns/_get_fabric_runtime_context.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) |
| [`add_datetime_features`](./step-10-technical-columns-write-prep/add_datetime_features/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module overview" aria-label="Open technical_columns module overview">technical_columns</a> | Add localized datetime feature columns derived from a UTC datetime column. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) |
| [`add_hash_columns`](./step-10-technical-columns-write-prep/add_hash_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module overview" aria-label="Open technical_columns module overview">technical_columns</a> | Add business key and row-level SHA256 hash columns. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_hash_row`](./internal/technical_columns/_hash_row.md) (internal), [`_non_technical_columns`](./internal/technical_columns/_non_technical_columns.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) |
| [`default_technical_columns`](./step-10-technical-columns-write-prep/default_technical_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_columns/" title="Open technical_columns module overview" aria-label="Open technical_columns module overview">technical_columns</a> | Return framework-generated and legacy technical column names to ignore. | — |

## Step 11: Output write, output profiling, and metadata logging

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`build_dataset_run_record`](./step-11-output-write-metadata-logging/build_dataset_run_record/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module overview" aria-label="Open metadata module overview">metadata</a> | Build dataset run record. | — |
| [`build_quality_result_records`](./step-11-output-write-metadata-logging/build_quality_result_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module overview" aria-label="Open metadata module overview">metadata</a> | Build quality result records. | — |
| [`build_schema_drift_records`](./step-11-output-write-metadata-logging/build_schema_drift_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module overview" aria-label="Open metadata module overview">metadata</a> | Build schema drift records. | — |
| [`build_schema_snapshot_records`](./step-11-output-write-metadata-logging/build_schema_snapshot_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module overview" aria-label="Open metadata module overview">metadata</a> | Build schema snapshot records. | — |
| [`lakehouse_table_write`](./step-11-output-write-metadata-logging/lakehouse_table_write/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`warehouse_write`](./step-11-output-write-metadata-logging/warehouse_write/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_io/" title="Open fabric_io module overview" aria-label="Open fabric_io module overview">fabric_io</a> | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |
| [`write_metadata_records`](./step-11-output-write-metadata-logging/write_metadata_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module overview" aria-label="Open metadata module overview">metadata</a> | Write metadata records. | — |
| [`write_multiple_metadata_outputs`](./step-11-output-write-metadata-logging/write_multiple_metadata_outputs/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/metadata/" title="Open metadata module overview" aria-label="Open metadata module overview">metadata</a> | Write multiple metadata outputs. | — |

## Step 12: Governance classification and lineage

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`build_governance_candidate_prompt`](./step-12-governance-classification/build_governance_candidate_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Build standardized prompt text for AI-assisted governance suggestions. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_governance_classification_records`](./step-12-governance-classification/build_governance_classification_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module overview" aria-label="Open governance module overview">governance</a> | Build governance classification records. | — |
| [`build_lineage_from_notebook_code`](./step-12-governance-classification/build_lineage_from_notebook_code/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Scan, optionally enrich, and validate lineage from notebook source code. | — |
| [`build_lineage_handover_markdown`](./step-12-governance-classification/build_lineage_handover_markdown/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Create a concise markdown handover summary from lineage execution results. | — |
| [`build_lineage_record_from_steps`](./step-12-governance-classification/build_lineage_record_from_steps/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Create metadata-ready lineage records from validated lineage steps. | — |
| [`build_manual_governance_prompt_package`](./step-12-governance-classification/build_manual_governance_prompt_package/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Build copy/paste prompt package for manual governance suggestion generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) |
| [`classify_column`](./step-12-governance-classification/classify_column/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module overview" aria-label="Open governance module overview">governance</a> | Classify column. | [`_match_terms`](./internal/governance/_match_terms.md) (internal), [`_phrase_in_text`](./internal/governance/_phrase_in_text.md) (internal) |
| [`classify_columns`](./step-12-governance-classification/classify_columns/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module overview" aria-label="Open governance module overview">governance</a> | Classify columns. | [`_column_name`](./internal/governance/_column_name.md) (internal), [`_normalize_columns`](./internal/governance/_normalize_columns.md) (internal) |
| [`enrich_lineage_steps_with_ai`](./step-12-governance-classification/enrich_lineage_steps_with_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Optionally enrich deterministic lineage steps using an AI helper callable. | — |
| [`fallback_copilot_lineage_prompt`](./step-12-governance-classification/fallback_copilot_lineage_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Build a fallback Copilot prompt for manual lineage enrichment. | — |
| [`generate_governance_candidates_with_fabric_ai`](./step-12-governance-classification/generate_governance_candidates_with_fabric_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Execute Fabric AI Functions to append governance suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`plot_lineage_steps`](./step-12-governance-classification/plot_lineage_steps/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Render lineage steps as a directed graph figure. | — |
| [`scan_notebook_cells`](./step-12-governance-classification/scan_notebook_cells/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Scan multiple notebook cells and append cell references to lineage steps. | — |
| [`scan_notebook_lineage`](./step-12-governance-classification/scan_notebook_lineage/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Extract deterministic lineage steps from notebook code using AST parsing. | [`_call_name`](./internal/lineage/_call_name.md) (internal), [`_flatten_chain`](./internal/lineage/_flatten_chain.md) (internal), [`_name`](./internal/lineage/_name.md) (internal), [`_resolve_write_target`](./internal/lineage/_resolve_write_target.md) (internal), [`_step`](./internal/lineage/_step.md) (internal) |
| [`summarize_governance_classifications`](./step-12-governance-classification/summarize_governance_classifications/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module overview" aria-label="Open governance module overview">governance</a> | Summarize governance classifications. | — |
| [`validate_lineage_steps`](./step-12-governance-classification/validate_lineage_steps/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Validate lineage step structure and flag records requiring human review. | — |
| [`write_governance_classifications`](./step-12-governance-classification/write_governance_classifications/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/governance/" title="Open governance module overview" aria-label="Open governance module overview">governance</a> | Write governance classifications. | [`_spark_create_governance_metadata_dataframe`](./internal/governance/_spark_create_governance_metadata_dataframe.md) (internal) |

## Step 13: Run summary and handover package

| Function / class | Module | Purpose | Related helpers |
|---|---|---|---|
| [`build_handover_summary_prompt`](./step-13-lineage-summary-handover/build_handover_summary_prompt/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Build standardized prompt text for AI-assisted handover summary suggestions. | [`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_lineage_records`](./step-13-lineage-summary-handover/build_lineage_records/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/lineage/" title="Open lineage module overview" aria-label="Open lineage module overview">lineage</a> | Build compact lineage records for downstream metadata sinks. | — |
| [`build_manual_handover_prompt_package`](./step-13-lineage-summary-handover/build_manual_handover_prompt_package/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Build copy/paste prompt package for manual handover summary generation. | [`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal) |
| [`build_run_summary`](./step-13-lineage-summary-handover/build_run_summary/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/run_summary/" title="Open run_summary module overview" aria-label="Open run_summary module overview">run_summary</a> | Build run summary. | — |
| [`generate_handover_summary_with_fabric_ai`](./step-13-lineage-summary-handover/generate_handover_summary_with_fabric_ai/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Execute Fabric AI Functions to append handover summary suggestions. | [`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`parse_manual_ai_json_response`](./step-13-lineage-summary-handover/parse_manual_ai_json_response/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/ai/" title="Open ai module overview" aria-label="Open ai module overview">ai</a> | Parse manual AI JSON output into Python objects. | — |
| [`render_run_summary_markdown`](./step-13-lineage-summary-handover/render_run_summary_markdown/) | <a class="api-chip api-chip-module api-chip-link" href="../api/modules/run_summary/" title="Open run_summary module overview" aria-label="Open run_summary module overview">run_summary</a> | Render run summary markdown. | [`_status_of`](./internal/run_summary/_status_of.md) (internal) |

