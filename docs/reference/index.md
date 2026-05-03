# Callable Reference

Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.

## Step 1: Package and runtime setup

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`assert_notebook_name_valid`](../api/modules/runtime.md#assert-notebook-name-valid) | [`runtime`](../api/modules/runtime.md) | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — | [function API](../api/modules/runtime.md#assert-notebook-name-valid) |
| [`build_runtime_context`](../api/modules/runtime.md#build-runtime-context) | [`runtime`](../api/modules/runtime.md) | Build a standard runtime context dictionary for Fabric notebooks. | — | [function API](../api/modules/runtime.md#build-runtime-context) |
| [`generate_run_id`](../api/modules/runtime.md#generate-run-id) | [`runtime`](../api/modules/runtime.md) | Generate a notebook-safe run identifier. | — | [function API](../api/modules/runtime.md#generate-run-id) |
| [`validate_notebook_name`](../api/modules/runtime.md#validate-notebook-name) | [`runtime`](../api/modules/runtime.md) | Validate a Fabric notebook name against required prefixes and format. | — | [function API](../api/modules/runtime.md#validate-notebook-name) |

## Step 2: Fabric config and paths

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`get_path`](../api/modules/fabric_io.md#get-path) | [`fabric_io`](../api/modules/fabric_io.md) | Return the Fabric path object for an environment and target. | — | [function API](../api/modules/fabric_io.md#get-path) |
| [`Housepath`](../api/modules/fabric_io.md#housepath) | [`fabric_io`](../api/modules/fabric_io.md) | Fabric lakehouse or warehouse connection details. | — | [function API](../api/modules/fabric_io.md#housepath) |
| [`load_fabric_config`](../api/modules/fabric_io.md#load-fabric-config) | [`fabric_io`](../api/modules/fabric_io.md) | Validate and return a Fabric config mapping. | — | [function API](../api/modules/fabric_io.md#load-fabric-config) |

## Step 3: Pull source data

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`lakehouse_csv_read`](../api/modules/fabric_io.md#lakehouse-csv-read) | [`fabric_io`](../api/modules/fabric_io.md) | Read a CSV file from a Fabric lakehouse Files path. | `_get_spark` (internal) | [function API](../api/modules/fabric_io.md#lakehouse-csv-read) |
| [`lakehouse_excel_read_as_spark`](../api/modules/fabric_io.md#lakehouse-excel-read-as-spark) | [`fabric_io`](../api/modules/fabric_io.md) | Read an Excel file from a Fabric lakehouse Files path. | `_get_spark` (internal) | [function API](../api/modules/fabric_io.md#lakehouse-excel-read-as-spark) |
| [`lakehouse_parquet_read_as_spark`](../api/modules/fabric_io.md#lakehouse-parquet-read-as-spark) | [`fabric_io`](../api/modules/fabric_io.md) | Read a Parquet file from a Fabric lakehouse Files path. | `_convert_single_parquet_ns_to_us` (internal), `_get_spark` (internal) | [function API](../api/modules/fabric_io.md#lakehouse-parquet-read-as-spark) |
| [`lakehouse_table_read`](../api/modules/fabric_io.md#lakehouse-table-read) | [`fabric_io`](../api/modules/fabric_io.md) | Read a Delta table from a Fabric lakehouse. | `_get_spark` (internal) | [function API](../api/modules/fabric_io.md#lakehouse-table-read) |
| [`warehouse_read`](../api/modules/fabric_io.md#warehouse-read) | [`fabric_io`](../api/modules/fabric_io.md) | Read a table from a Microsoft Fabric warehouse. | `_get_spark` (internal) | [function API](../api/modules/fabric_io.md#warehouse-read) |

## Step 4: Source profiling

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_ai_quality_context`](../api/modules/profiling.md#build-ai-quality-context) | [`profiling`](../api/modules/profiling.md) | Build deterministic AI-ready context from standard metadata profile rows. | — | [function API](../api/modules/profiling.md#build-ai-quality-context) |
| [`profile_dataframe`](../api/modules/profiling.md#profile-dataframe) | [`profiling`](../api/modules/profiling.md) | Build a lightweight profile for pandas or Spark-like DataFrames. | — | [function API](../api/modules/profiling.md#profile-dataframe) |
| [`profile_dataframe_to_metadata`](../api/modules/profiling.md#profile-dataframe-to-metadata) | [`profiling`](../api/modules/profiling.md) | Profile a Spark/Fabric DataFrame into ODI-compatible metadata rows. | — | [function API](../api/modules/profiling.md#profile-dataframe-to-metadata) |
| [`profile_metadata_to_records`](../api/modules/profiling.md#profile-metadata-to-records) | [`profiling`](../api/modules/profiling.md) | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — | [function API](../api/modules/profiling.md#profile-metadata-to-records) |

## Step 5: AI assisted DQ rule drafting

No public callable currently mapped to this step.

No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.

## Step 6: Human review of rules and metadata

No public callable currently mapped to this step.

## Step 7: Compile and run DQ checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`load_data_contract`](../api/modules/quality.md#load-data-contract) | [`quality`](../api/modules/quality.md) | Load data contract. | — | [function API](../api/modules/quality.md#load-data-contract) |
| [`run_data_product`](../api/modules/quality.md#run-data-product) | [`quality`](../api/modules/quality.md) | Run data product. | `_effective_contract_dict` (internal), `_refresh_mode` (internal), `_runtime_validation_contract` (internal), `_write_dataframe_to_table` (internal), `_write_records_spark` (internal) | [function API](../api/modules/quality.md#run-data-product) |
| [`run_quality_rules`](../api/modules/quality.md#run-quality-rules) | [`quality`](../api/modules/quality.md) | Run quality rules. | `_normalize_severity` (internal), `_now_iso` (internal), `_pandas_rule` (internal), `_resolve_engine` (internal), `_result_from_counts` (internal), `_spark_rule` (internal), `_to_jsonable` (internal) | [function API](../api/modules/quality.md#run-quality-rules) |

## Step 8: Schema/profile/data drift checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`check_partition_drift`](../api/modules/drift.md#check-partition-drift) | [`drift`](../api/modules/drift.md) | Check partition drift. | — | [function API](../api/modules/drift.md#check-partition-drift) |
| [`check_profile_drift`](../api/modules/drift.md#check-profile-drift) | [`drift`](../api/modules/drift.md) | Check profile drift. | — | [function API](../api/modules/drift.md#check-profile-drift) |
| [`check_schema_drift`](../api/modules/drift.md#check-schema-drift) | [`drift`](../api/modules/drift.md) | Check schema drift. | — | [function API](../api/modules/drift.md#check-schema-drift) |
| [`summarize_drift_results`](../api/modules/drift.md#summarize-drift-results) | [`drift`](../api/modules/drift.md) | Summarize drift results. | — | [function API](../api/modules/drift.md#summarize-drift-results) |

## Step 9: Core transformation

No public callable currently mapped to this step.

## Step 10: Standard technical columns

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`add_audit_columns`](../api/modules/technical_columns.md#add-audit-columns) | [`technical_columns`](../api/modules/technical_columns.md) | Add run tracking and audit columns for ingestion workflows. | `_assert_columns_exist` (internal), `_bucket_values_pandas` (internal), `_get_fabric_runtime_context` (internal), `_resolve_engine` (internal) | [function API](../api/modules/technical_columns.md#add-audit-columns) |
| [`add_datetime_features`](../api/modules/technical_columns.md#add-datetime-features) | [`technical_columns`](../api/modules/technical_columns.md) | Add localized datetime feature columns derived from a UTC datetime column. | `_assert_columns_exist` (internal), `_resolve_engine` (internal) | [function API](../api/modules/technical_columns.md#add-datetime-features) |
| [`add_hash_columns`](../api/modules/technical_columns.md#add-hash-columns) | [`technical_columns`](../api/modules/technical_columns.md) | Add business key and row-level SHA256 hash columns. | `_assert_columns_exist` (internal), `_hash_row` (internal), `_non_technical_columns` (internal), `_resolve_engine` (internal) | [function API](../api/modules/technical_columns.md#add-hash-columns) |
| [`default_technical_columns`](../api/modules/technical_columns.md#default-technical-columns) | [`technical_columns`](../api/modules/technical_columns.md) | Return framework-generated and legacy technical column names to ignore. | — | [function API](../api/modules/technical_columns.md#default-technical-columns) |

## Step 11: Output write, output profiling, and metadata logging

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_dataset_run_record`](../api/modules/metadata.md#build-dataset-run-record) | [`metadata`](../api/modules/metadata.md) | Build dataset run record. | — | [function API](../api/modules/metadata.md#build-dataset-run-record) |
| [`build_quality_result_records`](../api/modules/metadata.md#build-quality-result-records) | [`metadata`](../api/modules/metadata.md) | Build quality result records. | — | [function API](../api/modules/metadata.md#build-quality-result-records) |
| [`build_schema_drift_records`](../api/modules/metadata.md#build-schema-drift-records) | [`metadata`](../api/modules/metadata.md) | Build schema drift records. | — | [function API](../api/modules/metadata.md#build-schema-drift-records) |
| [`build_schema_snapshot_records`](../api/modules/metadata.md#build-schema-snapshot-records) | [`metadata`](../api/modules/metadata.md) | Build schema snapshot records. | — | [function API](../api/modules/metadata.md#build-schema-snapshot-records) |
| [`lakehouse_table_write`](../api/modules/fabric_io.md#lakehouse-table-write) | [`fabric_io`](../api/modules/fabric_io.md) | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — | [function API](../api/modules/fabric_io.md#lakehouse-table-write) |
| [`warehouse_write`](../api/modules/fabric_io.md#warehouse-write) | [`fabric_io`](../api/modules/fabric_io.md) | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [function API](../api/modules/fabric_io.md#warehouse-write) |
| [`write_metadata_records`](../api/modules/metadata.md#write-metadata-records) | [`metadata`](../api/modules/metadata.md) | Write metadata records. | — | [function API](../api/modules/metadata.md#write-metadata-records) |
| [`write_multiple_metadata_outputs`](../api/modules/metadata.md#write-multiple-metadata-outputs) | [`metadata`](../api/modules/metadata.md) | Write multiple metadata outputs. | — | [function API](../api/modules/metadata.md#write-multiple-metadata-outputs) |

## Step 12: Governance classification and lineage

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_governance_classification_records`](../api/modules/governance.md#build-governance-classification-records) | [`governance`](../api/modules/governance.md) | Build governance classification records. | — | [function API](../api/modules/governance.md#build-governance-classification-records) |
| [`classify_column`](../api/modules/governance.md#classify-column) | [`governance`](../api/modules/governance.md) | Classify column. | `_match_terms` (internal), `_phrase_in_text` (internal) | [function API](../api/modules/governance.md#classify-column) |
| [`classify_columns`](../api/modules/governance.md#classify-columns) | [`governance`](../api/modules/governance.md) | Classify columns. | `_column_name` (internal), `_normalize_columns` (internal) | [function API](../api/modules/governance.md#classify-columns) |
| [`summarize_governance_classifications`](../api/modules/governance.md#summarize-governance-classifications) | [`governance`](../api/modules/governance.md) | Summarize governance classifications. | — | [function API](../api/modules/governance.md#summarize-governance-classifications) |
| [`write_governance_classifications`](../api/modules/governance.md#write-governance-classifications) | [`governance`](../api/modules/governance.md) | Write governance classifications. | `_spark_create_governance_metadata_dataframe` (internal) | [function API](../api/modules/governance.md#write-governance-classifications) |

## Step 13: Run summary and handover package

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_lineage_records`](../api/modules/lineage.md#build-lineage-records) | [`lineage`](../api/modules/lineage.md) | Build lineage records. | `_clean_list` (internal) | [function API](../api/modules/lineage.md#build-lineage-records) |
| [`build_run_summary`](../api/modules/run_summary.md#build-run-summary) | [`run_summary`](../api/modules/run_summary.md) | Build run summary. | — | [function API](../api/modules/run_summary.md#build-run-summary) |
| [`build_transformation_summary_markdown`](../api/modules/lineage.md#build-transformation-summary-markdown) | [`lineage`](../api/modules/lineage.md) | Build transformation summary markdown. | — | [function API](../api/modules/lineage.md#build-transformation-summary-markdown) |
| [`generate_mermaid_lineage`](../api/modules/lineage.md#generate-mermaid-lineage) | [`lineage`](../api/modules/lineage.md) | Generate mermaid lineage. | `_safe_node_id` (internal) | [function API](../api/modules/lineage.md#generate-mermaid-lineage) |
| [`LineageRecorder`](../api/modules/lineage.md#lineagerecorder) | [`lineage`](../api/modules/lineage.md) | Lineagerecorder. | — | [function API](../api/modules/lineage.md#lineagerecorder) |
| [`render_run_summary_markdown`](../api/modules/run_summary.md#render-run-summary-markdown) | [`run_summary`](../api/modules/run_summary.md) | Render run summary markdown. | `_status_of` (internal) | [function API](../api/modules/run_summary.md#render-run-summary-markdown) |

