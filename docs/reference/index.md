# Callable Reference

Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.

## Step 1: Package and runtime setup

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `assert_notebook_name_valid` | `runtime` | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — | [module API](../api/modules/runtime.md) |
| `build_runtime_context` | `runtime` | Build a standard runtime context dictionary for Fabric notebooks. | — | [module API](../api/modules/runtime.md) |
| `generate_run_id` | `runtime` | Generate a notebook-safe run identifier. | — | [module API](../api/modules/runtime.md) |
| `get_path` | `fabric_io` | Return the Fabric path object for an environment and target. | — | [module API](../api/modules/fabric_io.md) |
| `Housepath` | `fabric_io` | Fabric lakehouse or warehouse connection details. | — | [module API](../api/modules/fabric_io.md) |
| `lakehouse_csv_read` | `fabric_io` | Read a CSV file from a Fabric lakehouse Files path. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md) |
| `lakehouse_excel_read_as_spark` | `fabric_io` | Read an Excel file from a Fabric lakehouse Files path. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md) |
| `lakehouse_parquet_read_as_spark` | `fabric_io` | Read a Parquet file from a Fabric lakehouse Files path. | `_convert_single_parquet_ns_to_us` (internal), `_get_spark` (internal) | [module API](../api/modules/fabric_io.md) |
| `lakehouse_table_read` | `fabric_io` | Read a Delta table from a Fabric lakehouse. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md) |
| `load_fabric_config` | `fabric_io` | Validate and return a Fabric config mapping. | — | [module API](../api/modules/fabric_io.md) |
| `validate_notebook_name` | `runtime` | Validate a Fabric notebook name against required prefixes and format. | — | [module API](../api/modules/runtime.md) |
| `warehouse_read` | `fabric_io` | Read a table from a Microsoft Fabric warehouse. | `_get_spark` (internal) | [module API](../api/modules/fabric_io.md) |
| `warehouse_write` | `fabric_io` | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [module API](../api/modules/fabric_io.md) |

## Step 2: Fabric config and paths

No public callable currently mapped to this step.

## Step 3: Pull source data

No public callable currently mapped to this step.

## Step 4: Source profiling

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `profile_dataframe` | `profiling` | Build a lightweight profile for pandas or Spark-like DataFrames. | — | [module API](../api/modules/profiling.md) |
| `summarize_profile` | `profiling` | Deprecated legacy API. | — | [module API](../api/modules/profiling.md) |

## Step 5: AI assisted DQ rule drafting

No public callable currently mapped to this step.

## Step 6: Human review of rules and metadata

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `write_multiple_metadata_outputs` | `metadata` | Write multiple metadata outputs. | — | [module API](../api/modules/metadata.md) |

## Step 7: Compile and run DQ checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `load_data_contract` | `quality` | Load data contract. | — | [module API](../api/modules/quality.md) |
| `run_data_product` | `quality` | Run data product. | `_effective_contract_dict` (internal), `_refresh_mode` (internal), `_runtime_validation_contract` (internal), `_write_dataframe_to_table` (internal), `_write_records_spark` (internal) | [module API](../api/modules/quality.md) |
| `run_quality_rules` | `quality` | Run quality rules. | `_normalize_severity` (internal), `_now_iso` (internal), `_pandas_rule` (internal), `_resolve_engine` (internal), `_result_from_counts` (internal), `_spark_rule` (internal), `_to_jsonable` (internal) | [module API](../api/modules/quality.md) |

## Step 8: Schema/profile/data drift checks

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `check_partition_drift` | `drift` | Check partition drift. | — | [module API](../api/modules/drift.md) |
| `check_profile_drift` | `drift` | Check profile drift. | — | [module API](../api/modules/drift.md) |
| `check_schema_drift` | `drift` | Check schema drift. | — | [module API](../api/modules/drift.md) |
| `summarize_drift_results` | `drift` | Summarize drift results. | — | [module API](../api/modules/drift.md) |

## Step 9: Core transformation

No public callable currently mapped to this step.

## Step 10: Standard technical columns

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `add_audit_columns` | `technical_columns` | Add run tracking and audit columns for ingestion workflows. | `_assert_columns_exist` (internal), `_bucket_values_pandas` (internal), `_get_fabric_runtime_context` (internal), `_resolve_engine` (internal) | [module API](../api/modules/technical_columns.md) |
| `add_datetime_features` | `technical_columns` | Add localized datetime feature columns derived from a UTC datetime column. | `_assert_columns_exist` (internal), `_resolve_engine` (internal) | [module API](../api/modules/technical_columns.md) |
| `add_hash_columns` | `technical_columns` | Add business key and row-level SHA256 hash columns. | `_assert_columns_exist` (internal), `_hash_row` (internal), `_non_technical_columns` (internal), `_resolve_engine` (internal) | [module API](../api/modules/technical_columns.md) |
| `default_technical_columns` | `technical_columns` | Return framework-generated and legacy technical column names to ignore. | — | [module API](../api/modules/technical_columns.md) |

## Step 11: Write output and profile output

No public callable currently mapped to this step.

## Step 12: Governance classification and lineage

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `build_lineage_records` | `lineage` | Build lineage records. | `_clean_list` (internal) | [module API](../api/modules/lineage.md) |
| `build_transformation_summary_markdown` | `lineage` | Build transformation summary markdown. | — | [module API](../api/modules/lineage.md) |
| `classify_columns` | `governance` | Classify columns. | `_column_name` (internal), `_normalize_columns` (internal) | [module API](../api/modules/governance.md) |
| `generate_mermaid_lineage` | `lineage` | Generate mermaid lineage. | `_safe_node_id` (internal) | [module API](../api/modules/lineage.md) |
| `LineageRecorder` | `lineage` | Lineagerecorder. | — | [module API](../api/modules/lineage.md) |
| `summarize_governance_classifications` | `governance` | Summarize governance classifications. | — | [module API](../api/modules/governance.md) |

## Step 13: Run summary and handover package

| Function / class | Module | Purpose | Related helpers | API link |
|---|---|---|---|---|
| `build_run_summary` | `run_summary` | Build run summary. | — | [module API](../api/modules/run_summary.md) |
| `render_run_summary_markdown` | `run_summary` | Render run summary markdown. | `_status_of` (internal) | [module API](../api/modules/run_summary.md) |

