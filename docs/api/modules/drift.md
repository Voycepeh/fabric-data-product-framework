# `drift` module

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `check_partition_drift` | function | Check partition drift. | — |
| `check_profile_drift` | function | Check profile drift. | — |
| `check_schema_drift` | function | Check schema drift. | — |
| `summarize_drift_results` | function | Summarize drift results. | — |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_build_pandas_partition_snapshot` | — |
| `_build_pandas_schema_snapshot` | — |
| `_build_partition_hash` | — |
| `_build_spark_partition_snapshot` | — |
| `_build_spark_schema_snapshot` | — |
| `_column_hash` | — |
| `_hash` | — |
| `_is_closed_partition` | — |
| `_is_missing_table_error` | — |
| `_json_dumps` | — |
| `_resolve_change_behavior` | — |
| `_safe_spark_collect` | — |
| `_utc_now_iso` | — |
| `_write_metadata_rows` | — |

## Full module API

::: fabric_data_product_framework.drift
