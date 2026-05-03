# Callable Reference

Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.

## Step 1: Package and runtime setup

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`assert_notebook_name_valid`](../api/modules/runtime.md#assert-notebook-name-valid) | [`runtime`](../api/modules/runtime.md) | Raise :class:`NotebookNamingError` when a notebook name is invalid. | [`NotebookNamingError`](../api/modules/runtime.md#notebooknamingerror) | [API anchor](../api/modules/runtime.md#assert-notebook-name-valid) · [Module](../api/modules/runtime.md) |
| [`build_runtime_context`](../api/modules/runtime.md#build-runtime-context) | [`runtime`](../api/modules/runtime.md) | Build a standard runtime context dictionary for Fabric notebooks. | [`get_current_timestamp_utc`](../api/modules/runtime.md#get-current-timestamp-utc) | [API anchor](../api/modules/runtime.md#build-runtime-context) · [Module](../api/modules/runtime.md) |
| [`generate_run_id`](../api/modules/runtime.md#generate-run-id) | [`runtime`](../api/modules/runtime.md) | Generate a notebook-safe run identifier. | [`normalize_name`](../api/modules/runtime.md#normalize-name) | [API anchor](../api/modules/runtime.md#generate-run-id) · [Module](../api/modules/runtime.md) |
| [`validate_notebook_name`](../api/modules/runtime.md#validate-notebook-name) | [`runtime`](../api/modules/runtime.md) | Validate a Fabric notebook name against required prefixes and format. | [`normalize_name`](../api/modules/runtime.md#normalize-name) | [API anchor](../api/modules/runtime.md#validate-notebook-name) · [Module](../api/modules/runtime.md) |

## Step 2: Fabric config and paths

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`get_path`](../api/modules/fabric_io.md#get-path) | [`fabric_io`](../api/modules/fabric_io.md) | Return the Fabric path object for an environment and target. | — | [API anchor](../api/modules/fabric_io.md#get-path) · [Module](../api/modules/fabric_io.md) |
| [`Housepath`](../api/modules/fabric_io.md#housepath) | [`fabric_io`](../api/modules/fabric_io.md) | Fabric lakehouse or warehouse connection details. | — | [API anchor](../api/modules/fabric_io.md#housepath) · [Module](../api/modules/fabric_io.md) |
| [`load_fabric_config`](../api/modules/fabric_io.md#load-fabric-config) | [`fabric_io`](../api/modules/fabric_io.md) | Validate and return a Fabric config mapping. | — | [API anchor](../api/modules/fabric_io.md#load-fabric-config) · [Module](../api/modules/fabric_io.md) |

## Step 3: Pull source data

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`lakehouse_csv_read`](../api/modules/fabric_io.md#lakehouse-csv-read) | [`fabric_io`](../api/modules/fabric_io.md) | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](../api/modules/fabric_io.md#get-spark) | [API anchor](../api/modules/fabric_io.md#lakehouse-csv-read) · [Module](../api/modules/fabric_io.md) |
| [`lakehouse_excel_read_as_spark`](../api/modules/fabric_io.md#lakehouse-excel-read-as-spark) | [`fabric_io`](../api/modules/fabric_io.md) | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](../api/modules/fabric_io.md#get-spark) | [API anchor](../api/modules/fabric_io.md#lakehouse-excel-read-as-spark) · [Module](../api/modules/fabric_io.md) |
| [`lakehouse_parquet_read_as_spark`](../api/modules/fabric_io.md#lakehouse-parquet-read-as-spark) | [`fabric_io`](../api/modules/fabric_io.md) | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](../api/modules/fabric_io.md#convert-single-parquet-ns-to-us), [`_get_spark`](../api/modules/fabric_io.md#get-spark) | [API anchor](../api/modules/fabric_io.md#lakehouse-parquet-read-as-spark) · [Module](../api/modules/fabric_io.md) |
| [`lakehouse_table_read`](../api/modules/fabric_io.md#lakehouse-table-read) | [`fabric_io`](../api/modules/fabric_io.md) | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](../api/modules/fabric_io.md#get-spark) | [API anchor](../api/modules/fabric_io.md#lakehouse-table-read) · [Module](../api/modules/fabric_io.md) |
| [`warehouse_read`](../api/modules/fabric_io.md#warehouse-read) | [`fabric_io`](../api/modules/fabric_io.md) | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](../api/modules/fabric_io.md#get-spark) | [API anchor](../api/modules/fabric_io.md#warehouse-read) · [Module](../api/modules/fabric_io.md) |

## Step 4: Source profiling

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`profile_dataframe`](../api/modules/profiling.md#profile-dataframe) | [`profiling`](../api/modules/profiling.md) | Build a lightweight profile for pandas or Spark-like DataFrames. | [`ColumnProfile`](../api/modules/profiling.md#columnprofile), [`DataFrameProfile`](../api/modules/profiling.md#dataframeprofile), [`profile_dataframe_to_metadata`](../api/modules/profiling.md#profile-dataframe-to-metadata), [`profile_metadata_to_records`](../api/modules/profiling.md#profile-metadata-to-records), [`to_jsonable`](../api/modules/profiling.md#to-jsonable) | [API anchor](../api/modules/profiling.md#profile-dataframe) · [Module](../api/modules/profiling.md) |
| [`summarize_profile`](../api/modules/profiling.md#summarize-profile) | [`profiling`](../api/modules/profiling.md) | Deprecated legacy API. | — | [API anchor](../api/modules/profiling.md#summarize-profile) · [Module](../api/modules/profiling.md) |

## Step 5: AI assisted DQ rule drafting

No public callable currently mapped to this step.

No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.

## Step 6: Human review of rules and metadata

No public callable currently mapped to this step.

## Step 7: Compile and run DQ checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`load_data_contract`](../api/modules/quality.md#load-data-contract) | [`quality`](../api/modules/quality.md) | Load data contract. | [`normalize_data_product_contract`](../api/modules/quality.md#normalize-data-product-contract) | [API anchor](../api/modules/quality.md#load-data-contract) · [Module](../api/modules/quality.md) |
| [`run_data_product`](../api/modules/quality.md#run-data-product) | [`quality`](../api/modules/quality.md) | Run data product. | [`_effective_contract_dict`](../api/modules/quality.md#effective-contract-dict), [`_refresh_mode`](../api/modules/quality.md#refresh-mode), [`_runtime_validation_contract`](../api/modules/quality.md#runtime-validation-contract), [`_write_dataframe_to_table`](../api/modules/quality.md#write-dataframe-to-table), [`_write_records_spark`](../api/modules/quality.md#write-records-spark), [`build_contract_validation_records`](../api/modules/quality.md#build-contract-validation-records), [`build_quality_result_records`](../api/modules/quality.md#build-quality-result-records), [`build_runtime_context_from_contract`](../api/modules/quality.md#build-runtime-context-from-contract), [`normalize_data_product_contract`](../api/modules/quality.md#normalize-data-product-contract), [`run_dq_workflow`](../api/modules/quality.md#run-dq-workflow), [`split_valid_and_quarantine`](../api/modules/quality.md#split-valid-and-quarantine), [`validate_data_contract_shape`](../api/modules/quality.md#validate-data-contract-shape), [`validate_runtime_contracts`](../api/modules/quality.md#validate-runtime-contracts) | [API anchor](../api/modules/quality.md#run-data-product) · [Module](../api/modules/quality.md) |
| [`run_quality_rules`](../api/modules/quality.md#run-quality-rules) | [`quality`](../api/modules/quality.md) | Run quality rules. | [`_normalize_severity`](../api/modules/quality.md#normalize-severity), [`_now_iso`](../api/modules/quality.md#now-iso), [`_pandas_rule`](../api/modules/quality.md#pandas-rule), [`_resolve_engine`](../api/modules/quality.md#resolve-engine), [`_result_from_counts`](../api/modules/quality.md#result-from-counts), [`_spark_rule`](../api/modules/quality.md#spark-rule), [`_to_jsonable`](../api/modules/quality.md#to-jsonable) | [API anchor](../api/modules/quality.md#run-quality-rules) · [Module](../api/modules/quality.md) |

## Step 8: Schema/profile/data drift checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`check_partition_drift`](../api/modules/drift.md#check-partition-drift) | [`drift`](../api/modules/drift.md) | Check partition drift. | [`build_partition_snapshot`](../api/modules/drift.md#build-partition-snapshot), [`compare_partition_snapshots`](../api/modules/drift.md#compare-partition-snapshots), [`default_incremental_safety_policy`](../api/modules/drift.md#default-incremental-safety-policy) | [API anchor](../api/modules/drift.md#check-partition-drift) · [Module](../api/modules/drift.md) |
| [`check_profile_drift`](../api/modules/drift.md#check-profile-drift) | [`drift`](../api/modules/drift.md) | Check profile drift. | — | [API anchor](../api/modules/drift.md#check-profile-drift) · [Module](../api/modules/drift.md) |
| [`check_schema_drift`](../api/modules/drift.md#check-schema-drift) | [`drift`](../api/modules/drift.md) | Check schema drift. | [`build_schema_snapshot`](../api/modules/drift.md#build-schema-snapshot), [`compare_schema_snapshots`](../api/modules/drift.md#compare-schema-snapshots), [`default_schema_drift_policy`](../api/modules/drift.md#default-schema-drift-policy) | [API anchor](../api/modules/drift.md#check-schema-drift) · [Module](../api/modules/drift.md) |
| [`summarize_drift_results`](../api/modules/drift.md#summarize-drift-results) | [`drift`](../api/modules/drift.md) | Summarize drift results. | — | [API anchor](../api/modules/drift.md#summarize-drift-results) · [Module](../api/modules/drift.md) |

## Step 9: Core transformation

No public callable currently mapped to this step.

## Step 10: Standard technical columns

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`add_audit_columns`](../api/modules/technical_columns.md#add-audit-columns) | [`technical_columns`](../api/modules/technical_columns.md) | Add run tracking and audit columns for ingestion workflows. | [`_assert_columns_exist`](../api/modules/technical_columns.md#assert-columns-exist), [`_bucket_values_pandas`](../api/modules/technical_columns.md#bucket-values-pandas), [`_get_fabric_runtime_context`](../api/modules/technical_columns.md#get-fabric-runtime-context), [`_resolve_engine`](../api/modules/technical_columns.md#resolve-engine) | [API anchor](../api/modules/technical_columns.md#add-audit-columns) · [Module](../api/modules/technical_columns.md) |
| [`add_datetime_features`](../api/modules/technical_columns.md#add-datetime-features) | [`technical_columns`](../api/modules/technical_columns.md) | Add localized datetime feature columns derived from a UTC datetime column. | [`_assert_columns_exist`](../api/modules/technical_columns.md#assert-columns-exist), [`_resolve_engine`](../api/modules/technical_columns.md#resolve-engine) | [API anchor](../api/modules/technical_columns.md#add-datetime-features) · [Module](../api/modules/technical_columns.md) |
| [`add_hash_columns`](../api/modules/technical_columns.md#add-hash-columns) | [`technical_columns`](../api/modules/technical_columns.md) | Add business key and row-level SHA256 hash columns. | [`_assert_columns_exist`](../api/modules/technical_columns.md#assert-columns-exist), [`_hash_row`](../api/modules/technical_columns.md#hash-row), [`_non_technical_columns`](../api/modules/technical_columns.md#non-technical-columns), [`_resolve_engine`](../api/modules/technical_columns.md#resolve-engine) | [API anchor](../api/modules/technical_columns.md#add-hash-columns) · [Module](../api/modules/technical_columns.md) |
| [`default_technical_columns`](../api/modules/technical_columns.md#default-technical-columns) | [`technical_columns`](../api/modules/technical_columns.md) | Return framework-generated and legacy technical column names to ignore. | — | [API anchor](../api/modules/technical_columns.md#default-technical-columns) · [Module](../api/modules/technical_columns.md) |

## Step 11: Output write, output profiling, and metadata logging

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`lakehouse_table_write`](../api/modules/fabric_io.md#lakehouse-table-write) | [`fabric_io`](../api/modules/fabric_io.md) | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — | [API anchor](../api/modules/fabric_io.md#lakehouse-table-write) · [Module](../api/modules/fabric_io.md) |
| [`warehouse_write`](../api/modules/fabric_io.md#warehouse-write) | [`fabric_io`](../api/modules/fabric_io.md) | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [API anchor](../api/modules/fabric_io.md#warehouse-write) · [Module](../api/modules/fabric_io.md) |
| [`write_multiple_metadata_outputs`](../api/modules/metadata.md#write-multiple-metadata-outputs) | [`metadata`](../api/modules/metadata.md) | Write multiple metadata outputs. | [`write_metadata_records`](../api/modules/metadata.md#write-metadata-records) | [API anchor](../api/modules/metadata.md#write-multiple-metadata-outputs) · [Module](../api/modules/metadata.md) |

## Step 12: Governance classification and lineage

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`classify_columns`](../api/modules/governance.md#classify-columns) | [`governance`](../api/modules/governance.md) | Classify columns. | [`_column_name`](../api/modules/governance.md#column-name), [`_normalize_columns`](../api/modules/governance.md#normalize-columns), [`classify_column`](../api/modules/governance.md#classify-column) | [API anchor](../api/modules/governance.md#classify-columns) · [Module](../api/modules/governance.md) |
| [`summarize_governance_classifications`](../api/modules/governance.md#summarize-governance-classifications) | [`governance`](../api/modules/governance.md) | Summarize governance classifications. | — | [API anchor](../api/modules/governance.md#summarize-governance-classifications) · [Module](../api/modules/governance.md) |

## Step 13: Run summary and handover package

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| [`build_lineage_records`](../api/modules/lineage.md#build-lineage-records) | [`lineage`](../api/modules/lineage.md) | Build lineage records. | [`_clean_list`](../api/modules/lineage.md#clean-list) | [API anchor](../api/modules/lineage.md#build-lineage-records) · [Module](../api/modules/lineage.md) |
| [`build_run_summary`](../api/modules/run_summary.md#build-run-summary) | [`run_summary`](../api/modules/run_summary.md) | Build run summary. | — | [API anchor](../api/modules/run_summary.md#build-run-summary) · [Module](../api/modules/run_summary.md) |
| [`build_transformation_summary_markdown`](../api/modules/lineage.md#build-transformation-summary-markdown) | [`lineage`](../api/modules/lineage.md) | Build transformation summary markdown. | — | [API anchor](../api/modules/lineage.md#build-transformation-summary-markdown) · [Module](../api/modules/lineage.md) |
| [`generate_mermaid_lineage`](../api/modules/lineage.md#generate-mermaid-lineage) | [`lineage`](../api/modules/lineage.md) | Generate mermaid lineage. | [`_safe_node_id`](../api/modules/lineage.md#safe-node-id) | [API anchor](../api/modules/lineage.md#generate-mermaid-lineage) · [Module](../api/modules/lineage.md) |
| [`LineageRecorder`](../api/modules/lineage.md#lineagerecorder) | [`lineage`](../api/modules/lineage.md) | Lineagerecorder. | — | [API anchor](../api/modules/lineage.md#lineagerecorder) · [Module](../api/modules/lineage.md) |
| [`render_run_summary_markdown`](../api/modules/run_summary.md#render-run-summary-markdown) | [`run_summary`](../api/modules/run_summary.md) | Render run summary markdown. | [`_status_of`](../api/modules/run_summary.md#status-of) | [API anchor](../api/modules/run_summary.md#render-run-summary-markdown) · [Module](../api/modules/run_summary.md) |

