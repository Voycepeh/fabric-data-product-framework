# Callable Reference

Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.

## Step 1: Package and runtime setup

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`assert_notebook_name_valid`](../api/modules/runtime.md#assert_notebook_name_valid) | `runtime` | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — | [module API](../api/modules/runtime.md#assert_notebook_name_valid) |
| [`build_runtime_context`](../api/modules/runtime.md#build_runtime_context) | `runtime` | Build a standard runtime context dictionary for Fabric notebooks. | — | [module API](../api/modules/runtime.md#build_runtime_context) |
| [`generate_run_id`](../api/modules/runtime.md#generate_run_id) | `runtime` | Generate a notebook-safe run identifier. | — | [module API](../api/modules/runtime.md#generate_run_id) |
| [`validate_notebook_name`](../api/modules/runtime.md#validate_notebook_name) | `runtime` | Validate a Fabric notebook name against required prefixes and format. | — | [module API](../api/modules/runtime.md#validate_notebook_name) |

## Step 2: Fabric config and paths

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`get_path`](../api/modules/fabric_io.md#get_path) | `fabric_io` | Return the Fabric path object for an environment and target. | — | [module API](../api/modules/fabric_io.md#get_path) |
| [`Housepath`](../api/modules/fabric_io.md#Housepath) | `fabric_io` | Fabric lakehouse or warehouse connection details. | — | [module API](../api/modules/fabric_io.md#Housepath) |
| [`load_fabric_config`](../api/modules/fabric_io.md#load_fabric_config) | `fabric_io` | Validate and return a Fabric config mapping. | — | [module API](../api/modules/fabric_io.md#load_fabric_config) |

## Step 3: Pull source data

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`lakehouse_csv_read`](../api/modules/fabric_io.md#lakehouse_csv_read) | `fabric_io` | Read a CSV file from a Fabric lakehouse Files path. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md#lakehouse_csv_read) |
| [`lakehouse_excel_read_as_spark`](../api/modules/fabric_io.md#lakehouse_excel_read_as_spark) | `fabric_io` | Read an Excel file from a Fabric lakehouse Files path. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md#lakehouse_excel_read_as_spark) |
| [`lakehouse_parquet_read_as_spark`](../api/modules/fabric_io.md#lakehouse_parquet_read_as_spark) | `fabric_io` | Read a Parquet file from a Fabric lakehouse Files path. | `_convert_single_parquet_ns_to_us` (internal), `_get_spark` (internal) | [module API](../api/modules/fabric_io.md#lakehouse_parquet_read_as_spark) |
| [`lakehouse_table_read`](../api/modules/fabric_io.md#lakehouse_table_read) | `fabric_io` | Read a Delta table from a Fabric lakehouse. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md#lakehouse_table_read) |
| [`warehouse_read`](../api/modules/fabric_io.md#warehouse_read) | `fabric_io` | Read a table from a Microsoft Fabric warehouse. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md#warehouse_read) |

## Step 4: Source profiling

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_ai_quality_context`](../api/modules/profiling.md#build_ai_quality_context) | `profiling` | Build deterministic AI-ready context from standard metadata profile rows. | — | [module API](../api/modules/profiling.md#build_ai_quality_context) |
| [`profile_dataframe`](../api/modules/profiling.md#profile_dataframe) | `profiling` | Build a lightweight profile for pandas or Spark-like DataFrames. | — | [module API](../api/modules/profiling.md#profile_dataframe) |
| [`profile_dataframe_to_metadata`](../api/modules/profiling.md#profile_dataframe_to_metadata) | `profiling` | Profile a Spark/Fabric DataFrame into ODI-compatible metadata rows. | — | [module API](../api/modules/profiling.md#profile_dataframe_to_metadata) |
| [`profile_metadata_to_records`](../api/modules/profiling.md#profile_metadata_to_records) | `profiling` | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — | [module API](../api/modules/profiling.md#profile_metadata_to_records) |

## Step 5: AI assisted DQ rule drafting

No public callable currently mapped to this step.

No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.

## Step 6: Human review of rules and metadata

No public callable currently mapped to this step.

## Step 7: Compile and run DQ checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`load_data_contract`](../api/modules/quality.md#load_data_contract) | `quality` | Load data contract. | — | [module API](../api/modules/quality.md#load_data_contract) |
| [`run_data_product`](../api/modules/quality.md#run_data_product) | `quality` | Run data product. | `_effective_contract_dict` (internal), `_refresh_mode` (internal), `_runtime_validation_contract` (internal), `_write_dataframe_to_table` (internal), `_write_records_spark` (internal) | [module API](../api/modules/quality.md#run_data_product) |
| [`run_quality_rules`](../api/modules/quality.md#run_quality_rules) | `quality` | Run quality rules. | `_normalize_severity` (internal), `_now_iso` (internal), `_pandas_rule` (internal), `_resolve_engine` (internal), `_result_from_counts` (internal), `_spark_rule` (internal), `_to_jsonable` (internal) | [module API](../api/modules/quality.md#run_quality_rules) |

## Step 8: Schema/profile/data drift checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`check_partition_drift`](../api/modules/drift.md#check_partition_drift) | `drift` | Check partition drift. | — | [module API](../api/modules/drift.md#check_partition_drift) |
| [`check_profile_drift`](../api/modules/drift.md#check_profile_drift) | `drift` | Check profile drift. | — | [module API](../api/modules/drift.md#check_profile_drift) |
| [`check_schema_drift`](../api/modules/drift.md#check_schema_drift) | `drift` | Check schema drift. | — | [module API](../api/modules/drift.md#check_schema_drift) |
| [`summarize_drift_results`](../api/modules/drift.md#summarize_drift_results) | `drift` | Summarize drift results. | — | [module API](../api/modules/drift.md#summarize_drift_results) |

## Step 9: Core transformation

No public callable currently mapped to this step.

## Step 10: Standard technical columns

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`add_audit_columns`](../api/modules/technical_columns.md#add_audit_columns) | `technical_columns` | Add run tracking and audit columns for ingestion workflows. | `_assert_columns_exist` (internal), `_bucket_values_pandas` (internal), `_get_fabric_runtime_context` (internal), `_resolve_engine` (internal) | [module API](../api/modules/technical_columns.md#add_audit_columns) |
| [`add_datetime_features`](../api/modules/technical_columns.md#add_datetime_features) | `technical_columns` | Add localized datetime feature columns derived from a UTC datetime column. | `_assert_columns_exist` (internal), `_resolve_engine` (internal) | [module API](../api/modules/technical_columns.md#add_datetime_features) |
| [`add_hash_columns`](../api/modules/technical_columns.md#add_hash_columns) | `technical_columns` | Add business key and row-level SHA256 hash columns. | `_assert_columns_exist` (internal), `_hash_row` (internal), `_non_technical_columns` (internal), `_resolve_engine` (internal) | [module API](../api/modules/technical_columns.md#add_hash_columns) |
| [`default_technical_columns`](../api/modules/technical_columns.md#default_technical_columns) | `technical_columns` | Return framework-generated and legacy technical column names to ignore. | — | [module API](../api/modules/technical_columns.md#default_technical_columns) |

## Step 11: Output write, output profiling, and metadata logging

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_dataset_run_record`](../api/modules/metadata.md#build_dataset_run_record) | `metadata` | Build dataset run record. | — | [module API](../api/modules/metadata.md#build_dataset_run_record) |
| [`build_quality_result_records`](../api/modules/quality.md#build_quality_result_records) | `quality` | Build quality result records. | `_to_jsonable` (internal) | [module API](../api/modules/quality.md#build_quality_result_records) |
| [`build_schema_drift_records`](../api/modules/metadata.md#build_schema_drift_records) | `metadata` | Build schema drift records. | — | [module API](../api/modules/metadata.md#build_schema_drift_records) |
| [`build_schema_snapshot_records`](../api/modules/metadata.md#build_schema_snapshot_records) | `metadata` | Build schema snapshot records. | — | [module API](../api/modules/metadata.md#build_schema_snapshot_records) |
| [`lakehouse_table_write`](../api/modules/fabric_io.md#lakehouse_table_write) | `fabric_io` | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — | [module API](../api/modules/fabric_io.md#lakehouse_table_write) |
| [`warehouse_write`](../api/modules/fabric_io.md#warehouse_write) | `fabric_io` | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [module API](../api/modules/fabric_io.md#warehouse_write) |
| [`write_metadata_records`](../api/modules/metadata.md#write_metadata_records) | `metadata` | Write metadata records. | — | [module API](../api/modules/metadata.md#write_metadata_records) |
| [`write_multiple_metadata_outputs`](../api/modules/metadata.md#write_multiple_metadata_outputs) | `metadata` | Write multiple metadata outputs. | — | [module API](../api/modules/metadata.md#write_multiple_metadata_outputs) |

## Step 12: Governance classification and lineage

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_governance_classification_records`](../api/modules/governance.md#build_governance_classification_records) | `governance` | Build governance classification records. | — | [module API](../api/modules/governance.md#build_governance_classification_records) |
| [`build_lineage_from_notebook_code`](../api/modules/lineage.md#build_lineage_from_notebook_code) | `lineage` | Scan, optionally enrich, and validate lineage from notebook source code. | — | [module API](../api/modules/lineage.md#build_lineage_from_notebook_code) |
| [`build_lineage_handover_markdown`](../api/modules/lineage.md#build_lineage_handover_markdown) | `lineage` | Create a concise markdown handover summary from lineage execution results. | — | [module API](../api/modules/lineage.md#build_lineage_handover_markdown) |
| [`build_lineage_record_from_steps`](../api/modules/lineage.md#build_lineage_record_from_steps) | `lineage` | Create metadata-ready lineage records from validated lineage steps. | — | [module API](../api/modules/lineage.md#build_lineage_record_from_steps) |
| [`classify_column`](../api/modules/governance.md#classify_column) | `governance` | Classify column. | `_match_terms` (internal), `_phrase_in_text` (internal) | [module API](../api/modules/governance.md#classify_column) |
| [`classify_columns`](../api/modules/governance.md#classify_columns) | `governance` | Classify columns. | `_column_name` (internal), `_normalize_columns` (internal) | [module API](../api/modules/governance.md#classify_columns) |
| [`enrich_lineage_steps_with_ai`](../api/modules/lineage.md#enrich_lineage_steps_with_ai) | `lineage` | Optionally enrich deterministic lineage steps using an AI helper callable. | — | [module API](../api/modules/lineage.md#enrich_lineage_steps_with_ai) |
| [`fallback_copilot_lineage_prompt`](../api/modules/lineage.md#fallback_copilot_lineage_prompt) | `lineage` | Build a fallback Copilot prompt for manual lineage enrichment. | — | [module API](../api/modules/lineage.md#fallback_copilot_lineage_prompt) |
| [`plot_lineage_steps`](../api/modules/lineage.md#plot_lineage_steps) | `lineage` | Render lineage steps as a directed graph figure. | — | [module API](../api/modules/lineage.md#plot_lineage_steps) |
| [`scan_notebook_cells`](../api/modules/lineage.md#scan_notebook_cells) | `lineage` | Scan multiple notebook cells and append cell references to lineage steps. | — | [module API](../api/modules/lineage.md#scan_notebook_cells) |
| [`scan_notebook_lineage`](../api/modules/lineage.md#scan_notebook_lineage) | `lineage` | Extract deterministic lineage steps from notebook code using AST parsing. | `_call_name` (internal), `_flatten_chain` (internal), `_name` (internal), `_resolve_write_target` (internal), `_step` (internal) | [module API](../api/modules/lineage.md#scan_notebook_lineage) |
| [`summarize_governance_classifications`](../api/modules/governance.md#summarize_governance_classifications) | `governance` | Summarize governance classifications. | — | [module API](../api/modules/governance.md#summarize_governance_classifications) |
| [`validate_lineage_steps`](../api/modules/lineage.md#validate_lineage_steps) | `lineage` | Validate lineage step structure and flag records requiring human review. | — | [module API](../api/modules/lineage.md#validate_lineage_steps) |
| [`write_governance_classifications`](../api/modules/governance.md#write_governance_classifications) | `governance` | Write governance classifications. | `_spark_create_governance_metadata_dataframe` (internal) | [module API](../api/modules/governance.md#write_governance_classifications) |

## Step 13: Run summary and handover package

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_lineage_records`](../api/modules/lineage.md#build_lineage_records) | `lineage` | Build compact lineage records for downstream metadata sinks. | — | [module API](../api/modules/lineage.md#build_lineage_records) |
| [`build_run_summary`](../api/modules/run_summary.md#build_run_summary) | `run_summary` | Build run summary. | — | [module API](../api/modules/run_summary.md#build_run_summary) |
| [`render_run_summary_markdown`](../api/modules/run_summary.md#render_run_summary_markdown) | `run_summary` | Render run summary markdown. | `_status_of` (internal) | [module API](../api/modules/run_summary.md#render_run_summary_markdown) |

