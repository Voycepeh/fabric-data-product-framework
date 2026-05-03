# `drift` module

## Module contents

- Public callables: 4
- Related internal helpers: 6
- Other internal objects: 25
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`_build_pandas_partition_snapshot`](#build-pandas-partition-snapshot) | Internal | Function | — | — | [Jump](#build-pandas-partition-snapshot) |
| [`_build_pandas_schema_snapshot`](#build-pandas-schema-snapshot) | Internal | Function | — | — | [Jump](#build-pandas-schema-snapshot) |
| [`_build_partition_hash`](#build-partition-hash) | Internal | Function | — | — | [Jump](#build-partition-hash) |
| [`_build_spark_partition_snapshot`](#build-spark-partition-snapshot) | Internal | Function | — | — | [Jump](#build-spark-partition-snapshot) |
| [`_build_spark_schema_snapshot`](#build-spark-schema-snapshot) | Internal | Function | — | — | [Jump](#build-spark-schema-snapshot) |
| [`_column_hash`](#column-hash) | Internal | Function | — | — | [Jump](#column-hash) |
| [`_hash`](#hash) | Internal | Function | — | — | [Jump](#hash) |
| [`_is_closed_partition`](#is-closed-partition) | Internal | Function | — | — | [Jump](#is-closed-partition) |
| [`_is_missing_table_error`](#is-missing-table-error) | Internal | Function | — | — | [Jump](#is-missing-table-error) |
| [`_json_dumps`](#json-dumps) | Internal | Function | — | — | [Jump](#json-dumps) |
| [`_resolve_change_behavior`](#resolve-change-behavior) | Internal | Function | — | — | [Jump](#resolve-change-behavior) |
| [`_safe_spark_collect`](#safe-spark-collect) | Internal | Function | — | — | [Jump](#safe-spark-collect) |
| [`_utc_now_iso`](#utc-now-iso) | Internal | Function | — | — | [Jump](#utc-now-iso) |
| [`_write_metadata_rows`](#write-metadata-rows) | Internal | Function | — | — | [Jump](#write-metadata-rows) |
| [`assert_incremental_safe`](#assert-incremental-safe) | Internal | Function | Assert incremental safe. | — | [Jump](#assert-incremental-safe) |
| [`assert_no_blocking_schema_drift`](#assert-no-blocking-schema-drift) | Internal | Function | Assert no blocking schema drift. | — | [Jump](#assert-no-blocking-schema-drift) |
| [`build_and_write_partition_snapshot`](#build-and-write-partition-snapshot) | Internal | Function | Build and write partition snapshot. | — | [Jump](#build-and-write-partition-snapshot) |
| [`build_and_write_schema_snapshot`](#build-and-write-schema-snapshot) | Internal | Function | Build and write schema snapshot. | — | [Jump](#build-and-write-schema-snapshot) |
| [`build_incremental_safety_records`](#build-incremental-safety-records) | Internal | Function | Build incremental safety records. | — | [Jump](#build-incremental-safety-records) |
| [`build_partition_snapshot`](#build-partition-snapshot) | Internal helper | Function | Build partition snapshot. | [`check_partition_drift`](#check-partition-drift) | [Jump](#build-partition-snapshot) |
| [`build_schema_snapshot`](#build-schema-snapshot) | Internal helper | Function | Build schema snapshot. | [`check_schema_drift`](#check-schema-drift) | [Jump](#build-schema-snapshot) |
| [`check_partition_drift`](#check-partition-drift) | Public | Function | Check partition drift. | — | [Jump](#check-partition-drift) |
| [`check_profile_drift`](#check-profile-drift) | Public | Function | Check profile drift. | — | [Jump](#check-profile-drift) |
| [`check_schema_drift`](#check-schema-drift) | Public | Function | Check schema drift. | — | [Jump](#check-schema-drift) |
| [`compare_partition_snapshots`](#compare-partition-snapshots) | Internal helper | Function | Compare partition snapshots. | [`check_partition_drift`](#check-partition-drift) | [Jump](#compare-partition-snapshots) |
| [`compare_schema_snapshots`](#compare-schema-snapshots) | Internal helper | Function | Compare schema snapshots. | [`check_schema_drift`](#check-schema-drift) | [Jump](#compare-schema-snapshots) |
| [`default_incremental_safety_policy`](#default-incremental-safety-policy) | Internal helper | Function | Default incremental safety policy. | [`check_partition_drift`](#check-partition-drift) | [Jump](#default-incremental-safety-policy) |
| [`default_schema_drift_policy`](#default-schema-drift-policy) | Internal helper | Function | Default schema drift policy. | [`check_schema_drift`](#check-schema-drift) | [Jump](#default-schema-drift-policy) |
| [`detect_dataframe_engine`](#detect-dataframe-engine) | Internal | Function | Detect dataframe engine. | — | [Jump](#detect-dataframe-engine) |
| [`IncrementalSafetyError`](#incrementalsafetyerror) | Internal | Class | Incrementalsafetyerror. | — | [Jump](#incrementalsafetyerror) |
| [`load_latest_partition_snapshot`](#load-latest-partition-snapshot) | Internal | Function | Load latest partition snapshot. | — | [Jump](#load-latest-partition-snapshot) |
| [`load_latest_schema_snapshot`](#load-latest-schema-snapshot) | Internal | Function | Load latest schema snapshot. | — | [Jump](#load-latest-schema-snapshot) |
| [`SchemaDriftError`](#schemadrifterror) | Internal | Class | Schemadrifterror. | — | [Jump](#schemadrifterror) |
| [`summarize_drift_results`](#summarize-drift-results) | Public | Function | Summarize drift results. | — | [Jump](#summarize-drift-results) |
| [`UnsupportedDataFrameEngineError`](#unsupporteddataframeengineerror) | Internal | Class | Unsupporteddataframeengineerror. | — | [Jump](#unsupporteddataframeengineerror) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`check_partition_drift`](#check-partition-drift) | Function | Check partition drift. | [`build_partition_snapshot`](#build-partition-snapshot), [`compare_partition_snapshots`](#compare-partition-snapshots), [`default_incremental_safety_policy`](#default-incremental-safety-policy) |
| [`check_profile_drift`](#check-profile-drift) | Function | Check profile drift. | — |
| [`check_schema_drift`](#check-schema-drift) | Function | Check schema drift. | [`build_schema_snapshot`](#build-schema-snapshot), [`compare_schema_snapshots`](#compare-schema-snapshots), [`default_schema_drift_policy`](#default-schema-drift-policy) |
| [`summarize_drift_results`](#summarize-drift-results) | Function | Summarize drift results. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`build_partition_snapshot`](#build-partition-snapshot) | [`check_partition_drift`](#check-partition-drift) |
| [`build_schema_snapshot`](#build-schema-snapshot) | [`check_schema_drift`](#check-schema-drift) |
| [`compare_partition_snapshots`](#compare-partition-snapshots) | [`check_partition_drift`](#check-partition-drift) |
| [`compare_schema_snapshots`](#compare-schema-snapshots) | [`check_schema_drift`](#check-schema-drift) |
| [`default_incremental_safety_policy`](#default-incremental-safety-policy) | [`check_partition_drift`](#check-partition-drift) |
| [`default_schema_drift_policy`](#default-schema-drift-policy) | [`check_schema_drift`](#check-schema-drift) |

## Full module API

::: fabric_data_product_framework.drift
