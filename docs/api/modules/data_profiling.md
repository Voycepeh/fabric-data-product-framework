# `data_profiling` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_ai_quality_context`](../../reference/step-04-ingest-profile-store/build_ai_quality_context.md) | function | Build deterministic AI-ready context from standard metadata profile rows. | — |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`profile_dataframe`](../../reference/step-04-ingest-profile-store/profile_dataframe.md) | function | Build a lightweight profile from a PySpark DataFrame. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`__generate_metadata_profile`](../../reference/internal/data_profiling/__generate_metadata_profile.md) | — |
| [`__profile_dataframe_to_metadata`](../../reference/internal/data_profiling/__profile_dataframe_to_metadata.md) | — |
| [`__profile_metadata_to_records`](../../reference/internal/data_profiling/__profile_metadata_to_records.md) | — |
