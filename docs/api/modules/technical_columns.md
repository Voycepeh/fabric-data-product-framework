# `technical_columns` module

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`add_audit_columns`](#add_audit_columns) | function | Add run tracking and audit columns for ingestion workflows. | `_assert_columns_exist` (internal), `_bucket_values_pandas` (internal), `_get_fabric_runtime_context` (internal), `_resolve_engine` (internal) |
| [`add_datetime_features`](#add_datetime_features) | function | Add localized datetime feature columns derived from a UTC datetime column. | `_assert_columns_exist` (internal), `_resolve_engine` (internal) |
| [`add_hash_columns`](#add_hash_columns) | function | Add business key and row-level SHA256 hash columns. | `_assert_columns_exist` (internal), `_hash_row` (internal), `_non_technical_columns` (internal), `_resolve_engine` (internal) |
| [`default_technical_columns`](#default_technical_columns) | function | Return framework-generated and legacy technical column names to ignore. | — |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_assert_columns_exist` | `add_audit_columns`, `add_datetime_features`, `add_hash_columns` |
| `_bucket_values_pandas` | `add_audit_columns` |
| `_get_fabric_runtime_context` | `add_audit_columns` |
| `_hash_row` | `add_hash_columns` |
| `_non_technical_columns` | `add_hash_columns` |
| `_resolve_engine` | `add_audit_columns`, `add_datetime_features`, `add_hash_columns` |
| `_safe_string` | — |

## Full module API

::: fabric_data_product_framework.technical_columns
