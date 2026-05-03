# `technical_columns` module

## Module contents

- Public callables: 4
- Related internal helpers: 6
- Other internal objects: 1
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`_assert_columns_exist`](#assert-columns-exist) | Internal helper | Function | — | [`add_audit_columns`](#add-audit-columns), [`add_datetime_features`](#add-datetime-features), [`add_hash_columns`](#add-hash-columns) | [Jump](#assert-columns-exist) |
| [`_bucket_values_pandas`](#bucket-values-pandas) | Internal helper | Function | — | [`add_audit_columns`](#add-audit-columns) | [Jump](#bucket-values-pandas) |
| [`_get_fabric_runtime_context`](#get-fabric-runtime-context) | Internal helper | Function | — | [`add_audit_columns`](#add-audit-columns) | [Jump](#get-fabric-runtime-context) |
| [`_hash_row`](#hash-row) | Internal helper | Function | — | [`add_hash_columns`](#add-hash-columns) | [Jump](#hash-row) |
| [`_non_technical_columns`](#non-technical-columns) | Internal helper | Function | — | [`add_hash_columns`](#add-hash-columns) | [Jump](#non-technical-columns) |
| [`_resolve_engine`](#resolve-engine) | Internal helper | Function | — | [`add_audit_columns`](#add-audit-columns), [`add_datetime_features`](#add-datetime-features), [`add_hash_columns`](#add-hash-columns) | [Jump](#resolve-engine) |
| [`_safe_string`](#safe-string) | Internal | Function | — | — | [Jump](#safe-string) |
| [`add_audit_columns`](#add-audit-columns) | Public | Function | Add run tracking and audit columns for ingestion workflows. | — | [Jump](#add-audit-columns) |
| [`add_datetime_features`](#add-datetime-features) | Public | Function | Add localized datetime feature columns derived from a UTC datetime column. | — | [Jump](#add-datetime-features) |
| [`add_hash_columns`](#add-hash-columns) | Public | Function | Add business key and row-level SHA256 hash columns. | — | [Jump](#add-hash-columns) |
| [`default_technical_columns`](#default-technical-columns) | Public | Function | Return framework-generated and legacy technical column names to ignore. | — | [Jump](#default-technical-columns) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`add_audit_columns`](#add-audit-columns) | Function | Add run tracking and audit columns for ingestion workflows. | [`_assert_columns_exist`](#assert-columns-exist), [`_bucket_values_pandas`](#bucket-values-pandas), [`_get_fabric_runtime_context`](#get-fabric-runtime-context), [`_resolve_engine`](#resolve-engine) |
| [`add_datetime_features`](#add-datetime-features) | Function | Add localized datetime feature columns derived from a UTC datetime column. | [`_assert_columns_exist`](#assert-columns-exist), [`_resolve_engine`](#resolve-engine) |
| [`add_hash_columns`](#add-hash-columns) | Function | Add business key and row-level SHA256 hash columns. | [`_assert_columns_exist`](#assert-columns-exist), [`_hash_row`](#hash-row), [`_non_technical_columns`](#non-technical-columns), [`_resolve_engine`](#resolve-engine) |
| [`default_technical_columns`](#default-technical-columns) | Function | Return framework-generated and legacy technical column names to ignore. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_assert_columns_exist`](#assert-columns-exist) | [`add_audit_columns`](#add-audit-columns), [`add_datetime_features`](#add-datetime-features), [`add_hash_columns`](#add-hash-columns) |
| [`_bucket_values_pandas`](#bucket-values-pandas) | [`add_audit_columns`](#add-audit-columns) |
| [`_get_fabric_runtime_context`](#get-fabric-runtime-context) | [`add_audit_columns`](#add-audit-columns) |
| [`_hash_row`](#hash-row) | [`add_hash_columns`](#add-hash-columns) |
| [`_non_technical_columns`](#non-technical-columns) | [`add_hash_columns`](#add-hash-columns) |
| [`_resolve_engine`](#resolve-engine) | [`add_audit_columns`](#add-audit-columns), [`add_datetime_features`](#add-datetime-features), [`add_hash_columns`](#add-hash-columns) |

## Full module API

::: fabric_data_product_framework.technical_columns
