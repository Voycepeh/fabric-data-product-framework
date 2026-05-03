# Callable Reference

Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.

## Step 1: Package and runtime setup

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`assert_notebook_name_valid`](./step-01-purpose-setup/assert_notebook_name_valid.md) | `runtime` | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — | [module overview](../api/modules/runtime.md) |
| [`build_runtime_context`](./step-01-purpose-setup/build_runtime_context.md) | `runtime` | Build a standard runtime context dictionary for Fabric notebooks. | — | [module overview](../api/modules/runtime.md) |
| [`generate_run_id`](./step-01-purpose-setup/generate_run_id.md) | `runtime` | Generate a notebook-safe run identifier. | — | [module overview](../api/modules/runtime.md) |
| [`validate_notebook_name`](./step-01-purpose-setup/validate_notebook_name.md) | `runtime` | Validate a Fabric notebook name against required prefixes and format. | — | [module overview](../api/modules/runtime.md) |

## Step 2: Fabric config and paths

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`get_path`](./step-02-runtime-configuration/get_path.md) | `fabric_io` | Return the Fabric path object for an environment and target. | — | [module overview](../api/modules/fabric_io.md) |
| [`Housepath`](./step-02-runtime-configuration/Housepath.md) | `fabric_io` | Fabric lakehouse or warehouse connection details. | — | [module overview](../api/modules/fabric_io.md) |
| [`load_fabric_config`](./step-02-runtime-configuration/load_fabric_config.md) | `fabric_io` | Validate and return a Fabric config mapping. | — | [module overview](../api/modules/fabric_io.md) |

## Step 3: Pull source data

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`lakehouse_csv_read`](./step-03-source-declaration-paths/lakehouse_csv_read.md) | `fabric_io` | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io.md) |
| [`lakehouse_excel_read_as_spark`](./step-03-source-declaration-paths/lakehouse_excel_read_as_spark.md) | `fabric_io` | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io.md) |
| [`lakehouse_parquet_read_as_spark`](./step-03-source-declaration-paths/lakehouse_parquet_read_as_spark.md) | `fabric_io` | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](./internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io.md) |
| [`lakehouse_table_read`](./step-03-source-declaration-paths/lakehouse_table_read.md) | `fabric_io` | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io.md) |
| [`warehouse_read`](./step-03-source-declaration-paths/warehouse_read.md) | `fabric_io` | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal) | [module overview](../api/modules/fabric_io.md) |

## Step 4: Source profiling

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_ai_quality_context`](./step-04-source-ingestion-read-helpers/build_ai_quality_context.md) | `profiling` | Build deterministic AI-ready context from standard metadata profile rows. | — | [module overview](../api/modules/profiling.md) |
| [`profile_dataframe`](./step-04-source-ingestion-read-helpers/profile_dataframe.md) | `profiling` | Build a lightweight profile for pandas or Spark-like DataFrames. | — | [module overview](../api/modules/profiling.md) |
| [`profile_dataframe_to_metadata`](./step-04-source-ingestion-read-helpers/profile_dataframe_to_metadata.md) | `profiling` | Profile a Spark/Fabric DataFrame into ODI-compatible metadata rows. | — | [module overview](../api/modules/profiling.md) |
| [`profile_metadata_to_records`](./step-04-source-ingestion-read-helpers/profile_metadata_to_records.md) | `profiling` | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — | [module overview](../api/modules/profiling.md) |

## Step 5: AI assisted DQ rule drafting

No public callable currently mapped to this step.

No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.

## Step 6: Human review of rules and metadata

No public callable currently mapped to this step.

## Step 7: Compile and run DQ checks

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`load_data_contract`](./step-07-ai-rule-generation-review/load_data_contract.md) | `quality` | Load data contract. | — | [module overview](../api/modules/quality.md) |
| [`run_quality_rules`](./step-07-ai-rule-generation-review/run_quality_rules.md) | `quality` | Run quality rules. | [`_normalize_severity`](./internal/quality/_normalize_severity.md) (internal), [`_now_iso`](./internal/quality/_now_iso.md) (internal), [`_pandas_rule`](./internal/quality/_pandas_rule.md) (internal), [`_resolve_engine`](./internal/quality/_resolve_engine.md) (internal), [`_result_from_counts`](./internal/quality/_result_from_counts.md) (internal), [`_spark_rule`](./internal/quality/_spark_rule.md) (internal), [`_to_jsonable`](./internal/quality/_to_jsonable.md) (internal) | [module overview](../api/modules/quality.md) |

## Step 8: Schema/profile/data drift checks

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`check_partition_drift`](./step-08-quality-rule-execution/check_partition_drift.md) | `drift` | Check partition drift. | — | [module overview](../api/modules/drift.md) |
| [`check_profile_drift`](./step-08-quality-rule-execution/check_profile_drift.md) | `drift` | Check profile drift. | — | [module overview](../api/modules/drift.md) |
| [`check_schema_drift`](./step-08-quality-rule-execution/check_schema_drift.md) | `drift` | Check schema drift. | — | [module overview](../api/modules/drift.md) |
| [`summarize_drift_results`](./step-08-quality-rule-execution/summarize_drift_results.md) | `drift` | Summarize drift results. | — | [module overview](../api/modules/drift.md) |

## Step 9: Core transformation

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`run_data_product`](./step-09-core-transformation-business-logic/run_data_product.md) | `quality` | Run the framework pipeline end-to-end for a data product. | [`_effective_contract_dict`](./internal/quality/_effective_contract_dict.md) (internal), [`_refresh_mode`](./internal/quality/_refresh_mode.md) (internal), [`_runtime_validation_contract`](./internal/quality/_runtime_validation_contract.md) (internal), [`_write_dataframe_to_table`](./internal/quality/_write_dataframe_to_table.md) (internal), [`_write_records_spark`](./internal/quality/_write_records_spark.md) (internal) | [module overview](../api/modules/quality.md) |

## Step 10: Standard technical columns

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`add_audit_columns`](./step-10-technical-columns-write-prep/add_audit_columns.md) | `technical_columns` | Add run tracking and audit columns for ingestion workflows. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_bucket_values_pandas`](./internal/technical_columns/_bucket_values_pandas.md) (internal), [`_get_fabric_runtime_context`](./internal/technical_columns/_get_fabric_runtime_context.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) | [module overview](../api/modules/technical_columns.md) |
| [`add_datetime_features`](./step-10-technical-columns-write-prep/add_datetime_features.md) | `technical_columns` | Add localized datetime feature columns derived from a UTC datetime column. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) | [module overview](../api/modules/technical_columns.md) |
| [`add_hash_columns`](./step-10-technical-columns-write-prep/add_hash_columns.md) | `technical_columns` | Add business key and row-level SHA256 hash columns. | [`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_hash_row`](./internal/technical_columns/_hash_row.md) (internal), [`_non_technical_columns`](./internal/technical_columns/_non_technical_columns.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal) | [module overview](../api/modules/technical_columns.md) |
| [`default_technical_columns`](./step-10-technical-columns-write-prep/default_technical_columns.md) | `technical_columns` | Return framework-generated and legacy technical column names to ignore. | — | [module overview](../api/modules/technical_columns.md) |

## Step 11: Output write, output profiling, and metadata logging

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_dataset_run_record`](./step-11-output-write-metadata-logging/build_dataset_run_record.md) | `metadata` | Build dataset run record. | — | [module overview](../api/modules/metadata.md) |
| [`build_quality_result_records`](./step-11-output-write-metadata-logging/build_quality_result_records.md) | `metadata` | Build quality result records. | — | [module overview](../api/modules/metadata.md) |
| [`build_schema_drift_records`](./step-11-output-write-metadata-logging/build_schema_drift_records.md) | `metadata` | Build schema drift records. | — | [module overview](../api/modules/metadata.md) |
| [`build_schema_snapshot_records`](./step-11-output-write-metadata-logging/build_schema_snapshot_records.md) | `metadata` | Build schema snapshot records. | — | [module overview](../api/modules/metadata.md) |
| [`lakehouse_table_write`](./step-11-output-write-metadata-logging/lakehouse_table_write.md) | `fabric_io` | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — | [module overview](../api/modules/fabric_io.md) |
| [`warehouse_write`](./step-11-output-write-metadata-logging/warehouse_write.md) | `fabric_io` | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [module overview](../api/modules/fabric_io.md) |
| [`write_metadata_records`](./step-11-output-write-metadata-logging/write_metadata_records.md) | `metadata` | Write metadata records. | — | [module overview](../api/modules/metadata.md) |
| [`write_multiple_metadata_outputs`](./step-11-output-write-metadata-logging/write_multiple_metadata_outputs.md) | `metadata` | Write multiple metadata outputs. | — | [module overview](../api/modules/metadata.md) |

## Step 12: Governance classification and lineage

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_governance_classification_records`](./step-12-governance-classification/build_governance_classification_records.md) | `governance` | Build governance classification records. | — | [module overview](../api/modules/governance.md) |
| [`build_lineage_from_notebook_code`](./step-12-governance-classification/build_lineage_from_notebook_code.md) | `lineage` | Scan, optionally enrich, and validate lineage from notebook source code. | — | [module overview](../api/modules/lineage.md) |
| [`build_lineage_handover_markdown`](./step-12-governance-classification/build_lineage_handover_markdown.md) | `lineage` | Create a concise markdown handover summary from lineage execution results. | — | [module overview](../api/modules/lineage.md) |
| [`build_lineage_record_from_steps`](./step-12-governance-classification/build_lineage_record_from_steps.md) | `lineage` | Create metadata-ready lineage records from validated lineage steps. | — | [module overview](../api/modules/lineage.md) |
| [`classify_column`](./step-12-governance-classification/classify_column.md) | `governance` | Classify column. | [`_match_terms`](./internal/governance/_match_terms.md) (internal), [`_phrase_in_text`](./internal/governance/_phrase_in_text.md) (internal) | [module overview](../api/modules/governance.md) |
| [`classify_columns`](./step-12-governance-classification/classify_columns.md) | `governance` | Classify columns. | [`_column_name`](./internal/governance/_column_name.md) (internal), [`_normalize_columns`](./internal/governance/_normalize_columns.md) (internal) | [module overview](../api/modules/governance.md) |
| [`enrich_lineage_steps_with_ai`](./step-12-governance-classification/enrich_lineage_steps_with_ai.md) | `lineage` | Optionally enrich deterministic lineage steps using an AI helper callable. | — | [module overview](../api/modules/lineage.md) |
| [`fallback_copilot_lineage_prompt`](./step-12-governance-classification/fallback_copilot_lineage_prompt.md) | `lineage` | Build a fallback Copilot prompt for manual lineage enrichment. | — | [module overview](../api/modules/lineage.md) |
| [`plot_lineage_steps`](./step-12-governance-classification/plot_lineage_steps.md) | `lineage` | Render lineage steps as a directed graph figure. | — | [module overview](../api/modules/lineage.md) |
| [`scan_notebook_cells`](./step-12-governance-classification/scan_notebook_cells.md) | `lineage` | Scan multiple notebook cells and append cell references to lineage steps. | — | [module overview](../api/modules/lineage.md) |
| [`scan_notebook_lineage`](./step-12-governance-classification/scan_notebook_lineage.md) | `lineage` | Extract deterministic lineage steps from notebook code using AST parsing. | [`_call_name`](./internal/lineage/_call_name.md) (internal), [`_flatten_chain`](./internal/lineage/_flatten_chain.md) (internal), [`_name`](./internal/lineage/_name.md) (internal), [`_resolve_write_target`](./internal/lineage/_resolve_write_target.md) (internal), [`_step`](./internal/lineage/_step.md) (internal) | [module overview](../api/modules/lineage.md) |
| [`summarize_governance_classifications`](./step-12-governance-classification/summarize_governance_classifications.md) | `governance` | Summarize governance classifications. | — | [module overview](../api/modules/governance.md) |
| [`validate_lineage_steps`](./step-12-governance-classification/validate_lineage_steps.md) | `lineage` | Validate lineage step structure and flag records requiring human review. | — | [module overview](../api/modules/lineage.md) |
| [`write_governance_classifications`](./step-12-governance-classification/write_governance_classifications.md) | `governance` | Write governance classifications. | [`_spark_create_governance_metadata_dataframe`](./internal/governance/_spark_create_governance_metadata_dataframe.md) (internal) | [module overview](../api/modules/governance.md) |

## Step 13: Run summary and handover package

| Function / class | Module | Purpose | Related helpers | Module page |
|---|---|---|---|---|
| [`build_lineage_records`](./step-13-lineage-summary-handover/build_lineage_records.md) | `lineage` | Build compact lineage records for downstream metadata sinks. | — | [module overview](../api/modules/lineage.md) |
| [`build_run_summary`](./step-13-lineage-summary-handover/build_run_summary.md) | `run_summary` | Build run summary. | — | [module overview](../api/modules/run_summary.md) |
| [`render_run_summary_markdown`](./step-13-lineage-summary-handover/render_run_summary_markdown.md) | `run_summary` | Render run summary markdown. | [`_status_of`](./internal/run_summary/_status_of.md) (internal) | [module overview](../api/modules/run_summary.md) |

