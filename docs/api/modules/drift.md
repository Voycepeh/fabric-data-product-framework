# `drift` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`check_partition_drift`](../../reference/step-08-quality-rule-execution/check_partition_drift.md) | function | Check partition drift. | — |
| [`check_profile_drift`](../../reference/step-08-quality-rule-execution/check_profile_drift.md) | function | Check profile drift. | — |
| [`check_schema_drift`](../../reference/step-08-quality-rule-execution/check_schema_drift.md) | function | Check schema drift. | — |
| [`summarize_drift_results`](../../reference/step-08-quality-rule-execution/summarize_drift_results.md) | function | Summarize drift results. | — |

## Internal helpers

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
