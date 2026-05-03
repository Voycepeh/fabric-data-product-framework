# `runtime` module

## Module contents

- Public callables: 4
- Related internal helpers: 3
- Other internal objects: 3
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`assert_notebook_name_valid`](#assert-notebook-name-valid) | Public | Function | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — | [Jump](#assert-notebook-name-valid) |
| [`build_runtime_context`](#build-runtime-context) | Public | Function | Build a standard runtime context dictionary for Fabric notebooks. | — | [Jump](#build-runtime-context) |
| [`detect_dataframe_engine`](#detect-dataframe-engine) | Internal | Function | Detect dataframe engine. | — | [Jump](#detect-dataframe-engine) |
| [`generate_run_id`](#generate-run-id) | Public | Function | Generate a notebook-safe run identifier. | [`build_runtime_context`](#build-runtime-context) | [Jump](#generate-run-id) |
| [`get_current_timestamp_utc`](#get-current-timestamp-utc) | Internal helper | Function | Return the current UTC timestamp in ISO-8601 format. | [`build_runtime_context`](#build-runtime-context) | [Jump](#get-current-timestamp-utc) |
| [`normalize_name`](#normalize-name) | Internal helper | Function | Normalize a value for safe Fabric notebook and table-style naming. | [`generate_run_id`](#generate-run-id), [`validate_notebook_name`](#validate-notebook-name) | [Jump](#normalize-name) |
| [`NotebookNamingError`](#notebooknamingerror) | Internal helper | Class | Raised when notebook naming validation fails. | [`assert_notebook_name_valid`](#assert-notebook-name-valid) | [Jump](#notebooknamingerror) |
| [`UnsupportedDataFrameEngineError`](#unsupporteddataframeengineerror) | Internal | Class | Unsupporteddataframeengineerror. | — | [Jump](#unsupporteddataframeengineerror) |
| [`validate_engine`](#validate-engine) | Internal | Function | Validate engine. | — | [Jump](#validate-engine) |
| [`validate_notebook_name`](#validate-notebook-name) | Public | Function | Validate a Fabric notebook name against required prefixes and format. | [`assert_notebook_name_valid`](#assert-notebook-name-valid) | [Jump](#validate-notebook-name) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_notebook_name_valid`](#assert-notebook-name-valid) | Function | Raise :class:`NotebookNamingError` when a notebook name is invalid. | [`NotebookNamingError`](#notebooknamingerror) |
| [`build_runtime_context`](#build-runtime-context) | Function | Build a standard runtime context dictionary for Fabric notebooks. | [`get_current_timestamp_utc`](#get-current-timestamp-utc) |
| [`generate_run_id`](#generate-run-id) | Function | Generate a notebook-safe run identifier. | [`normalize_name`](#normalize-name) |
| [`validate_notebook_name`](#validate-notebook-name) | Function | Validate a Fabric notebook name against required prefixes and format. | [`normalize_name`](#normalize-name) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`get_current_timestamp_utc`](#get-current-timestamp-utc) | [`build_runtime_context`](#build-runtime-context) |
| [`normalize_name`](#normalize-name) | [`generate_run_id`](#generate-run-id), [`validate_notebook_name`](#validate-notebook-name) |
| [`NotebookNamingError`](#notebooknamingerror) | [`assert_notebook_name_valid`](#assert-notebook-name-valid) |

## Full module API

::: fabric_data_product_framework.runtime
