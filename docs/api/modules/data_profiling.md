# `data_profiling` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`profile_dataframe`](../../reference/step-04-ingest-profile-store/profile_dataframe.md) | function | Build canonical DQ-ready profiling rows from a Spark DataFrame. | [`_get_profiled_columns`](../../reference/internal/data_profiling/_get_profiled_columns.md) (internal), [`_is_min_max_supported_type`](../../reference/internal/data_profiling/_is_min_max_supported_type.md) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_get_profiled_columns`](../../reference/internal/data_profiling/_get_profiled_columns.md) | [`profile_dataframe`](../../reference/step-04-ingest-profile-store/profile_dataframe.md) |
| [`_is_min_max_supported_type`](../../reference/internal/data_profiling/_is_min_max_supported_type.md) | [`profile_dataframe`](../../reference/step-04-ingest-profile-store/profile_dataframe.md) |
