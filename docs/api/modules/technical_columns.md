# `technical_columns` module

Public callables: 4  
Related internal helpers: 6  
Other internal objects: 1  
Deprecated objects: 0

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [_assert_columns_exist](#-assert-columns-exist) | Internal helper | Function | — | `add_audit_columns`, `add_datetime_features`, `add_hash_columns` | [API](#-assert-columns-exist) |
| [_bucket_values_pandas](#-bucket-values-pandas) | Internal helper | Function | — | `add_audit_columns` | [API](#-bucket-values-pandas) |
| [_get_fabric_runtime_context](#-get-fabric-runtime-context) | Internal helper | Function | — | `add_audit_columns` | [API](#-get-fabric-runtime-context) |
| [_hash_row](#-hash-row) | Internal helper | Function | — | `add_hash_columns` | [API](#-hash-row) |
| [_non_technical_columns](#-non-technical-columns) | Internal helper | Function | — | `add_hash_columns` | [API](#-non-technical-columns) |
| [_resolve_engine](#-resolve-engine) | Internal helper | Function | — | `add_audit_columns`, `add_datetime_features`, `add_hash_columns` | [API](#-resolve-engine) |
| [_safe_string](#-safe-string) | Internal | Function | — | — | [API](#-safe-string) |
| [add_audit_columns](#add-audit-columns) | Public | Function | Add run tracking and audit columns for ingestion workflows. | — | [API](#add-audit-columns) |
| [add_datetime_features](#add-datetime-features) | Public | Function | Add localized datetime feature columns derived from a UTC datetime column. | — | [API](#add-datetime-features) |
| [add_hash_columns](#add-hash-columns) | Public | Function | Add business key and row-level SHA256 hash columns. | — | [API](#add-hash-columns) |
| [default_technical_columns](#default-technical-columns) | Public | Function | Return framework-generated and legacy technical column names to ignore. | — | [API](#default-technical-columns) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `add_audit_columns` | Function | Add run tracking and audit columns for ingestion workflows. | `_assert_columns_exist` (internal), `_bucket_values_pandas` (internal), `_get_fabric_runtime_context` (internal), `_resolve_engine` (internal) |
| `add_datetime_features` | Function | Add localized datetime feature columns derived from a UTC datetime column. | `_assert_columns_exist` (internal), `_resolve_engine` (internal) |
| `add_hash_columns` | Function | Add business key and row-level SHA256 hash columns. | `_assert_columns_exist` (internal), `_hash_row` (internal), `_non_technical_columns` (internal), `_resolve_engine` (internal) |
| `default_technical_columns` | Function | Return framework-generated and legacy technical column names to ignore. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `_assert_columns_exist` | `add_audit_columns`, `add_datetime_features`, `add_hash_columns` |
| `_bucket_values_pandas` | `add_audit_columns` |
| `_get_fabric_runtime_context` | `add_audit_columns` |
| `_hash_row` | `add_hash_columns` |
| `_non_technical_columns` | `add_hash_columns` |
| `_resolve_engine` | `add_audit_columns`, `add_datetime_features`, `add_hash_columns` |

## Full module API

::: fabric_data_product_framework.technical_columns
