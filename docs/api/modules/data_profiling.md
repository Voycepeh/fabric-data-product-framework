# `data_profiling` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`profile_dataframe`](../../reference/step-04-ingest-profile-store/profile_dataframe.md) | function | Build canonical DQ-ready profiling rows from a Spark DataFrame. | [`_profile_dataframe_to_metadata`](../../reference/internal/data_profiling/_profile_dataframe_to_metadata.md) (internal) |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_ai_quality_context`](../../reference/step-04-ingest-profile-store/build_ai_quality_context.md) | function | Build deterministic AI-ready context from standard metadata profile rows. | [`_profile_metadata_to_records`](../../reference/internal/data_profiling/_profile_metadata_to_records.md) (internal) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_generate_metadata_profile`](../../reference/internal/data_profiling/_generate_metadata_profile.md) | — |
| [`_profile_dataframe_to_metadata`](../../reference/internal/data_profiling/_profile_dataframe_to_metadata.md) | [`profile_dataframe`](../../reference/step-04-ingest-profile-store/profile_dataframe.md) |
| [`_profile_metadata_to_records`](../../reference/internal/data_profiling/_profile_metadata_to_records.md) | [`build_ai_quality_context`](../../reference/step-04-ingest-profile-store/build_ai_quality_context.md) |
