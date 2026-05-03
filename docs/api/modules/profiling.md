# `profiling` module

Public callables: 4  
Related internal helpers: 5  
Other internal objects: 3  
Deprecated objects: 1

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [ColumnProfile](#columnprofile) | Internal helper | Dataclass | Columnprofile. | `profile_dataframe` | [API](#columnprofile) |
| [DataFrameProfile](#dataframeprofile) | Internal helper | Dataclass | Dataframeprofile. | `profile_dataframe` | [API](#dataframeprofile) |
| [ODI_METADATA_LOGGER](#odi-metadata-logger) | Internal | Function | Compatibility wrapper kept for existing Fabric notebook workflows. | — | [API](#odi-metadata-logger) |
| [build_ai_quality_context](#build-ai-quality-context) | Public | Function | Build deterministic AI-ready context from standard metadata profile rows. | — | [API](#build-ai-quality-context) |
| [flatten_profile_for_metadata](#flatten-profile-for-metadata) | Internal | Function | Flatten a profile dictionary into metadata-friendly row records. | — | [API](#flatten-profile-for-metadata) |
| [get_profiled_columns](#get-profiled-columns) | Internal helper | Function | Return non-technical column names from a Spark DataFrame. | `profile_dataframe_to_metadata` | [API](#get-profiled-columns) |
| [is_min_max_supported_type](#is-min-max-supported-type) | Internal helper | Function | Return whether min/max aggregation is safe for a Spark type string. | `profile_dataframe_to_metadata` | [API](#is-min-max-supported-type) |
| [profile_dataframe](#profile-dataframe) | Public | Function | Build a lightweight profile for pandas or Spark-like DataFrames. | — | [API](#profile-dataframe) |
| [profile_dataframe_to_metadata](#profile-dataframe-to-metadata) | Public | Function | Profile a Spark/Fabric DataFrame into ODI-compatible metadata rows. | `profile_dataframe` | [API](#profile-dataframe-to-metadata) |
| [profile_metadata_to_records](#profile-metadata-to-records) | Public | Function | Convert Spark metadata profile rows into JSON-friendly dictionaries. | `build_ai_quality_context`, `profile_dataframe` | [API](#profile-metadata-to-records) |
| [summarize_profile](#summarize-profile) | Deprecated | Function | Deprecated legacy API. | — | [API](#summarize-profile) |
| [to_jsonable](#to-jsonable) | Internal helper | Function | Convert a value recursively into JSON-serializable primitives. | `profile_dataframe` | [API](#to-jsonable) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `build_ai_quality_context` | Function | Build deterministic AI-ready context from standard metadata profile rows. | — |
| `profile_dataframe` | Function | Build a lightweight profile for pandas or Spark-like DataFrames. | — |
| `profile_dataframe_to_metadata` | Function | Profile a Spark/Fabric DataFrame into ODI-compatible metadata rows. | — |
| `profile_metadata_to_records` | Function | Convert Spark metadata profile rows into JSON-friendly dictionaries. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `ColumnProfile` | `profile_dataframe` |
| `DataFrameProfile` | `profile_dataframe` |
| `get_profiled_columns` | `profile_dataframe_to_metadata` |
| `is_min_max_supported_type` | `profile_dataframe_to_metadata` |
| `to_jsonable` | `profile_dataframe` |

## Full module API

::: fabric_data_product_framework.profiling
