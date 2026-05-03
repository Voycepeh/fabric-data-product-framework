# `profiling` module

## Module contents

- Public callables: 2
- Related internal helpers: 5
- Other internal objects: 5
- Deprecated objects: 1

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`build_ai_quality_context`](#build-ai-quality-context) | Internal | Function | Build deterministic AI-ready context from standard metadata profile rows. | — | [Jump](#build-ai-quality-context) |
| [`ColumnProfile`](#columnprofile) | Internal helper | Dataclass | Columnprofile. | [`profile_dataframe`](#profile-dataframe) | [Jump](#columnprofile) |
| [`DataFrameProfile`](#dataframeprofile) | Internal helper | Dataclass | Dataframeprofile. | [`profile_dataframe`](#profile-dataframe) | [Jump](#dataframeprofile) |
| [`flatten_profile_for_metadata`](#flatten-profile-for-metadata) | Internal | Function | Flatten a profile dictionary into metadata-friendly row records. | — | [Jump](#flatten-profile-for-metadata) |
| [`get_profiled_columns`](#get-profiled-columns) | Internal | Function | Return non-technical column names from a Spark DataFrame. | — | [Jump](#get-profiled-columns) |
| [`is_min_max_supported_type`](#is-min-max-supported-type) | Internal | Function | Return whether min/max aggregation is safe for a Spark type string. | — | [Jump](#is-min-max-supported-type) |
| [`ODI_METADATA_LOGGER`](#odi-metadata-logger) | Internal | Function | Compatibility wrapper kept for existing Fabric notebook workflows. | — | [Jump](#odi-metadata-logger) |
| [`profile_dataframe`](#profile-dataframe) | Public | Function | Build a lightweight profile for pandas or Spark-like DataFrames. | — | [Jump](#profile-dataframe) |
| [`profile_dataframe_to_metadata`](#profile-dataframe-to-metadata) | Internal helper | Function | Profile a Spark/Fabric DataFrame into ODI-compatible metadata rows. | [`profile_dataframe`](#profile-dataframe) | [Jump](#profile-dataframe-to-metadata) |
| [`profile_metadata_to_records`](#profile-metadata-to-records) | Internal helper | Function | Convert Spark metadata profile rows into JSON-friendly dictionaries. | [`profile_dataframe`](#profile-dataframe) | [Jump](#profile-metadata-to-records) |
| [`summarize_profile`](#summarize-profile) | Deprecated | Function | Deprecated legacy API. | — | [Jump](#summarize-profile) |
| [`to_jsonable`](#to-jsonable) | Internal helper | Function | Convert a value recursively into JSON-serializable primitives. | [`profile_dataframe`](#profile-dataframe) | [Jump](#to-jsonable) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`profile_dataframe`](#profile-dataframe) | Function | Build a lightweight profile for pandas or Spark-like DataFrames. | [`ColumnProfile`](#columnprofile), [`DataFrameProfile`](#dataframeprofile), [`profile_dataframe_to_metadata`](#profile-dataframe-to-metadata), [`profile_metadata_to_records`](#profile-metadata-to-records), [`to_jsonable`](#to-jsonable) |
| [`summarize_profile`](#summarize-profile) | Function | Deprecated legacy API. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`ColumnProfile`](#columnprofile) | [`profile_dataframe`](#profile-dataframe) |
| [`DataFrameProfile`](#dataframeprofile) | [`profile_dataframe`](#profile-dataframe) |
| [`profile_dataframe_to_metadata`](#profile-dataframe-to-metadata) | [`profile_dataframe`](#profile-dataframe) |
| [`profile_metadata_to_records`](#profile-metadata-to-records) | [`profile_dataframe`](#profile-dataframe) |
| [`to_jsonable`](#to-jsonable) | [`profile_dataframe`](#profile-dataframe) |

## Full module API

::: fabric_data_product_framework.profiling
