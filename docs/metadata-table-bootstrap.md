# Metadata table bootstrap for Fabric smoke test

This guide defines a minimal metadata table setup for the MVP smoke test.

## Table catalog

### `metadata.dataset_runs`
- **Purpose**: one run-level record per execution.
- **Record builder**: dataset run record builders from `metadata.py`.
- **Suggested columns**: `run_id`, `run_ts`, `dataset_name`, `environment`, `dry_run`, `profile_only`, `status`, `message`.

### `metadata.column_profiles`
- **Purpose**: column-level profiling output rows.
- **Record builder**: profile-to-metadata shaping helpers.
- **Suggested columns**: `run_id`, `table_name`, `column_name`, `data_type`, `row_count`, `null_count`, `distinct_count`, `profile_json`.

### `metadata.schema_snapshots`
- **Purpose**: persisted schema snapshots by run.
- **Record builder**: schema snapshot helper.
- **Suggested columns**: `run_id`, `table_name`, `snapshot_ts`, `schema_json`.

### `metadata.schema_drift_results`
- **Purpose**: schema drift decision output.
- **Record builder**: drift result builders.
- **Suggested columns**: `run_id`, `table_name`, `status`, `added_columns_json`, `removed_columns_json`, `changed_columns_json`, `message`.

### `metadata.incremental_safety_results`
- **Purpose**: incremental partition safety check results.
- **Record builder**: incremental safety result builders.
- **Suggested columns**: `run_id`, `table_name`, `partition_key`, `status`, `details_json`.

### `metadata.quality_results`
- **Purpose**: data quality rule outcomes.
- **Record builder**: quality result record builders.
- **Suggested columns**: `run_id`, `rule_id`, `severity`, `status`, `failed_count`, `details_json`.

### `metadata.contract_validation_results`
- **Purpose**: runtime contract validation outcomes.
- **Record builder**: contract validation result builders.
- **Suggested columns**: `run_id`, `table_name`, `status`, `missing_columns_json`, `unexpected_columns_json`, `message`.

### `metadata.lineage`
- **Purpose**: source-to-target lineage summary.
- **Record builder**: lineage recorder output.
- **Suggested columns**: `run_id`, `dataset_name`, `source_tables_json`, `target_table`, `lineage_json`, `captured_ts`.

### `metadata.run_summaries`
- **Purpose**: compact execution summary for handover and ops.
- **Record builder**: run summary builders.
- **Suggested columns**: `run_id`, `dataset_name`, `status`, `summary_json`, `captured_ts`.

## Notes on nested fields
For broad compatibility, store nested fields as JSON strings (`*_json`) before writing metadata rows.

## Spark SQL bootstrap example
```sql
CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS metadata.dataset_runs (
  run_id STRING,
  run_ts TIMESTAMP,
  dataset_name STRING,
  environment STRING,
  dry_run BOOLEAN,
  profile_only BOOLEAN,
  status STRING,
  message STRING
);
```

## PySpark bootstrap example
```python
spark.sql("CREATE SCHEMA IF NOT EXISTS metadata")

spark.sql("""
CREATE TABLE IF NOT EXISTS metadata.run_summaries (
  run_id STRING,
  dataset_name STRING,
  status STRING,
  summary_json STRING,
  captured_ts TIMESTAMP
)
""")
```

Repeat with similarly typed MVP columns for the remaining metadata tables above.
