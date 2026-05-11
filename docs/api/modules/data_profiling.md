# `data_profiling` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_ai_quality_context`](../../reference/step-04-ingest-profile-store/build_ai_quality_context.md) | function | Build deterministic AI-ready context from standard metadata profile rows. | — |
| [`generate_metadata_profile`](../../reference/step-04-ingest-profile-store/generate_metadata_profile.md) | function | Generate standard metadata profile rows for a Spark/Fabric DataFrame. | — |
| [`profile_dataframe_to_metadata`](../../reference/step-04-ingest-profile-store/profile_dataframe_to_metadata.md) | function | Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows. | — |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`profile_dataframe`](../../reference/step-04-ingest-profile-store/profile_dataframe.md) | function | Build a lightweight profile from a PySpark DataFrame. | — |
| [`profile_metadata_to_records`](../../reference/step-04-ingest-profile-store/profile_metadata_to_records.md) | function | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — |

## Related internal helpers

No module-level internal helpers detected.
