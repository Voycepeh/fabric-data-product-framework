# `runtime` module

Public callables: 4  
Related internal helpers: 3  
Other internal objects: 3  
Deprecated objects: 0

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [NotebookNamingError](#notebooknamingerror) | Internal helper | Class | Raised when notebook naming validation fails. | `assert_notebook_name_valid` | [API](#notebooknamingerror) |
| [UnsupportedDataFrameEngineError](#unsupporteddataframeengineerror) | Internal | Class | Unsupporteddataframeengineerror. | — | [API](#unsupporteddataframeengineerror) |
| [assert_notebook_name_valid](#assert-notebook-name-valid) | Public | Function | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — | [API](#assert-notebook-name-valid) |
| [build_runtime_context](#build-runtime-context) | Public | Function | Build a standard runtime context dictionary for Fabric notebooks. | — | [API](#build-runtime-context) |
| [detect_dataframe_engine](#detect-dataframe-engine) | Internal | Function | Detect dataframe engine. | — | [API](#detect-dataframe-engine) |
| [generate_run_id](#generate-run-id) | Public | Function | Generate a notebook-safe run identifier. | `build_runtime_context` | [API](#generate-run-id) |
| [get_current_timestamp_utc](#get-current-timestamp-utc) | Internal helper | Function | Return the current UTC timestamp in ISO-8601 format. | `build_runtime_context` | [API](#get-current-timestamp-utc) |
| [normalize_name](#normalize-name) | Internal helper | Function | Normalize a value for safe Fabric notebook and table-style naming. | `generate_run_id`, `validate_notebook_name` | [API](#normalize-name) |
| [validate_engine](#validate-engine) | Internal | Function | Validate engine. | — | [API](#validate-engine) |
| [validate_notebook_name](#validate-notebook-name) | Public | Function | Validate a Fabric notebook name against required prefixes and format. | `assert_notebook_name_valid` | [API](#validate-notebook-name) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `assert_notebook_name_valid` | Function | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — |
| `build_runtime_context` | Function | Build a standard runtime context dictionary for Fabric notebooks. | — |
| `generate_run_id` | Function | Generate a notebook-safe run identifier. | — |
| `validate_notebook_name` | Function | Validate a Fabric notebook name against required prefixes and format. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `NotebookNamingError` | `assert_notebook_name_valid` |
| `get_current_timestamp_utc` | `build_runtime_context` |
| `normalize_name` | `generate_run_id`, `validate_notebook_name` |

## Full module API

::: fabric_data_product_framework.runtime
