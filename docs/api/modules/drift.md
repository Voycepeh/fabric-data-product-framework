# `drift` module

Public callables: 4  
Related internal helpers: 6  
Other internal objects: 25  
Deprecated objects: 0

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [IncrementalSafetyError](#incrementalsafetyerror) | Internal | Class | Incrementalsafetyerror. | — | [API](#incrementalsafetyerror) |
| [SchemaDriftError](#schemadrifterror) | Internal | Class | Schemadrifterror. | — | [API](#schemadrifterror) |
| [UnsupportedDataFrameEngineError](#unsupporteddataframeengineerror) | Internal | Class | Unsupporteddataframeengineerror. | — | [API](#unsupporteddataframeengineerror) |
| [_build_pandas_partition_snapshot](#-build-pandas-partition-snapshot) | Internal | Function | — | — | [API](#-build-pandas-partition-snapshot) |
| [_build_pandas_schema_snapshot](#-build-pandas-schema-snapshot) | Internal | Function | — | — | [API](#-build-pandas-schema-snapshot) |
| [_build_partition_hash](#-build-partition-hash) | Internal | Function | — | — | [API](#-build-partition-hash) |
| [_build_spark_partition_snapshot](#-build-spark-partition-snapshot) | Internal | Function | — | — | [API](#-build-spark-partition-snapshot) |
| [_build_spark_schema_snapshot](#-build-spark-schema-snapshot) | Internal | Function | — | — | [API](#-build-spark-schema-snapshot) |
| [_column_hash](#-column-hash) | Internal | Function | — | — | [API](#-column-hash) |
| [_hash](#-hash) | Internal | Function | — | — | [API](#-hash) |
| [_is_closed_partition](#-is-closed-partition) | Internal | Function | — | — | [API](#-is-closed-partition) |
| [_is_missing_table_error](#-is-missing-table-error) | Internal | Function | — | — | [API](#-is-missing-table-error) |
| [_json_dumps](#-json-dumps) | Internal | Function | — | — | [API](#-json-dumps) |
| [_resolve_change_behavior](#-resolve-change-behavior) | Internal | Function | — | — | [API](#-resolve-change-behavior) |
| [_safe_spark_collect](#-safe-spark-collect) | Internal | Function | — | — | [API](#-safe-spark-collect) |
| [_utc_now_iso](#-utc-now-iso) | Internal | Function | — | — | [API](#-utc-now-iso) |
| [_write_metadata_rows](#-write-metadata-rows) | Internal | Function | — | — | [API](#-write-metadata-rows) |
| [assert_incremental_safe](#assert-incremental-safe) | Internal | Function | Assert incremental safe. | — | [API](#assert-incremental-safe) |
| [assert_no_blocking_schema_drift](#assert-no-blocking-schema-drift) | Internal | Function | Assert no blocking schema drift. | — | [API](#assert-no-blocking-schema-drift) |
| [build_and_write_partition_snapshot](#build-and-write-partition-snapshot) | Internal | Function | Build and write partition snapshot. | — | [API](#build-and-write-partition-snapshot) |
| [build_and_write_schema_snapshot](#build-and-write-schema-snapshot) | Internal | Function | Build and write schema snapshot. | — | [API](#build-and-write-schema-snapshot) |
| [build_incremental_safety_records](#build-incremental-safety-records) | Internal | Function | Build incremental safety records. | — | [API](#build-incremental-safety-records) |
| [build_partition_snapshot](#build-partition-snapshot) | Internal helper | Function | Build partition snapshot. | `check_partition_drift` | [API](#build-partition-snapshot) |
| [build_schema_snapshot](#build-schema-snapshot) | Internal helper | Function | Build schema snapshot. | `check_schema_drift` | [API](#build-schema-snapshot) |
| [check_partition_drift](#check-partition-drift) | Public | Function | Check partition drift. | — | [API](#check-partition-drift) |
| [check_profile_drift](#check-profile-drift) | Public | Function | Check profile drift. | — | [API](#check-profile-drift) |
| [check_schema_drift](#check-schema-drift) | Public | Function | Check schema drift. | — | [API](#check-schema-drift) |
| [compare_partition_snapshots](#compare-partition-snapshots) | Internal helper | Function | Compare partition snapshots. | `check_partition_drift` | [API](#compare-partition-snapshots) |
| [compare_schema_snapshots](#compare-schema-snapshots) | Internal helper | Function | Compare schema snapshots. | `check_schema_drift` | [API](#compare-schema-snapshots) |
| [default_incremental_safety_policy](#default-incremental-safety-policy) | Internal helper | Function | Default incremental safety policy. | `check_partition_drift` | [API](#default-incremental-safety-policy) |
| [default_schema_drift_policy](#default-schema-drift-policy) | Internal helper | Function | Default schema drift policy. | `check_schema_drift` | [API](#default-schema-drift-policy) |
| [detect_dataframe_engine](#detect-dataframe-engine) | Internal | Function | Detect dataframe engine. | — | [API](#detect-dataframe-engine) |
| [load_latest_partition_snapshot](#load-latest-partition-snapshot) | Internal | Function | Load latest partition snapshot. | — | [API](#load-latest-partition-snapshot) |
| [load_latest_schema_snapshot](#load-latest-schema-snapshot) | Internal | Function | Load latest schema snapshot. | — | [API](#load-latest-schema-snapshot) |
| [summarize_drift_results](#summarize-drift-results) | Public | Function | Summarize drift results. | — | [API](#summarize-drift-results) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `check_partition_drift` | Function | Check partition drift. | — |
| `check_profile_drift` | Function | Check profile drift. | — |
| `check_schema_drift` | Function | Check schema drift. | — |
| `summarize_drift_results` | Function | Summarize drift results. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `build_partition_snapshot` | `check_partition_drift` |
| `build_schema_snapshot` | `check_schema_drift` |
| `compare_partition_snapshots` | `check_partition_drift` |
| `compare_schema_snapshots` | `check_schema_drift` |
| `default_incremental_safety_policy` | `check_partition_drift` |
| `default_schema_drift_policy` | `check_schema_drift` |

## Full module API

::: fabric_data_product_framework.drift
