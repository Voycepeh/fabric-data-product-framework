# `technical_columns` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`add_audit_columns`](../../reference/step-10-technical-columns-write-prep/add_audit_columns.md) | function | Add run tracking and audit columns for ingestion workflows. | [`_assert_columns_exist`](../../reference/internal/technical_columns/_assert_columns_exist.md) (internal), [`_bucket_values_pandas`](../../reference/internal/technical_columns/_bucket_values_pandas.md) (internal), [`_get_fabric_runtime_context`](../../reference/internal/technical_columns/_get_fabric_runtime_context.md) (internal), [`_resolve_engine`](../../reference/internal/technical_columns/_resolve_engine.md) (internal) |
| [`add_datetime_features`](../../reference/step-10-technical-columns-write-prep/add_datetime_features.md) | function | Add localized datetime feature columns derived from a UTC datetime column. | [`_assert_columns_exist`](../../reference/internal/technical_columns/_assert_columns_exist.md) (internal), [`_resolve_engine`](../../reference/internal/technical_columns/_resolve_engine.md) (internal) |
| [`add_hash_columns`](../../reference/step-10-technical-columns-write-prep/add_hash_columns.md) | function | Add business key and row-level SHA256 hash columns. | [`_assert_columns_exist`](../../reference/internal/technical_columns/_assert_columns_exist.md) (internal), [`_hash_row`](../../reference/internal/technical_columns/_hash_row.md) (internal), [`_non_technical_columns`](../../reference/internal/technical_columns/_non_technical_columns.md) (internal), [`_resolve_engine`](../../reference/internal/technical_columns/_resolve_engine.md) (internal) |
| [`default_technical_columns`](../../reference/step-10-technical-columns-write-prep/default_technical_columns.md) | function | Return framework-generated and legacy technical column names to ignore. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_assert_columns_exist`](../../reference/internal/technical_columns/_assert_columns_exist.md) | [`add_audit_columns`](../../reference/step-10-technical-columns-write-prep/add_audit_columns.md), [`add_datetime_features`](../../reference/step-10-technical-columns-write-prep/add_datetime_features.md), [`add_hash_columns`](../../reference/step-10-technical-columns-write-prep/add_hash_columns.md) |
| [`_bucket_values_pandas`](../../reference/internal/technical_columns/_bucket_values_pandas.md) | [`add_audit_columns`](../../reference/step-10-technical-columns-write-prep/add_audit_columns.md) |
| [`_get_fabric_runtime_context`](../../reference/internal/technical_columns/_get_fabric_runtime_context.md) | [`add_audit_columns`](../../reference/step-10-technical-columns-write-prep/add_audit_columns.md) |
| [`_hash_row`](../../reference/internal/technical_columns/_hash_row.md) | [`add_hash_columns`](../../reference/step-10-technical-columns-write-prep/add_hash_columns.md) |
| [`_non_technical_columns`](../../reference/internal/technical_columns/_non_technical_columns.md) | [`add_hash_columns`](../../reference/step-10-technical-columns-write-prep/add_hash_columns.md) |
| [`_resolve_engine`](../../reference/internal/technical_columns/_resolve_engine.md) | [`add_audit_columns`](../../reference/step-10-technical-columns-write-prep/add_audit_columns.md), [`add_datetime_features`](../../reference/step-10-technical-columns-write-prep/add_datetime_features.md), [`add_hash_columns`](../../reference/step-10-technical-columns-write-prep/add_hash_columns.md) |
| [`_safe_string`](../../reference/internal/technical_columns/_safe_string.md) | — |
