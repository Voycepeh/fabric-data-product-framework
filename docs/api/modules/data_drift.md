# `data_drift` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`check_partition_drift`](../../reference/check_partition_drift/) | function | Check partition-level drift using keys, partitions, and optional watermark baselines. | — |
| [`check_profile_drift`](../../reference/check_profile_drift/) | function | Compare profile metrics against a baseline profile and drift thresholds. | — |
| [`check_schema_drift`](../../reference/check_schema_drift/) | function | Compare a current dataframe schema against a baseline schema snapshot. | — |
| [`summarize_drift_results`](../../reference/summarize_drift_results/) | function | Summarize schema, partition, and profile drift outcomes into one decision. | — |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_build_pandas_partition_snapshot`](../../reference/internal/drift/_build_pandas_partition_snapshot.md) | — |
| [`_build_pandas_schema_snapshot`](../../reference/internal/drift/_build_pandas_schema_snapshot.md) | — |
| [`_build_partition_hash`](../../reference/internal/drift/_build_partition_hash.md) | — |
| [`_build_spark_partition_snapshot`](../../reference/internal/drift/_build_spark_partition_snapshot.md) | — |
| [`_build_spark_schema_snapshot`](../../reference/internal/drift/_build_spark_schema_snapshot.md) | — |
| [`_column_hash`](../../reference/internal/drift/_column_hash.md) | — |
| [`_hash`](../../reference/internal/drift/_hash.md) | — |
| [`_is_closed_partition`](../../reference/internal/drift/_is_closed_partition.md) | — |
| [`_is_missing_table_error`](../../reference/internal/drift/_is_missing_table_error.md) | — |
| [`_json_dumps`](../../reference/internal/drift/_json_dumps.md) | — |
| [`_resolve_change_behavior`](../../reference/internal/drift/_resolve_change_behavior.md) | — |
| [`_safe_spark_collect`](../../reference/internal/drift/_safe_spark_collect.md) | — |
| [`_utc_now_iso`](../../reference/internal/drift/_utc_now_iso.md) | — |
| [`_write_metadata_rows`](../../reference/internal/drift/_write_metadata_rows.md) | — |
