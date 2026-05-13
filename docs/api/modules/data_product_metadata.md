# `data_product_metadata` module

<div class="api-status-block">
  <span class="api-chip api-chip-internal">Advanced supporting module</span>
  <div class="api-chip-subtitle">Used by workflow references but not promoted as a primary notebook module.</div>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| — | — | No recommended entrypoints configured. | — |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_dq_rule_key`](../../reference/build_dq_rule_key/) | function | — | [`_sha256_key`](../../reference/internal/metadata/_sha256_key.md) (internal) |
| [`build_metadata_column_key`](../../reference/build_metadata_column_key/) | function | — | [`_sha256_key`](../../reference/internal/metadata/_sha256_key.md) (internal) |
| [`build_metadata_table_key`](../../reference/build_metadata_table_key/) | function | — | [`_sha256_key`](../../reference/internal/metadata/_sha256_key.md) (internal) |
| [`write_column_business_context`](../../reference/write_column_business_context/) | function | — | — |
| [`write_column_governance_context`](../../reference/write_column_governance_context/) | function | — | — |
| [`write_metadata_rows`](../../reference/write_metadata_rows/) | function | Write metadata rows to a lakehouse metadata table. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_extract_columns_from_profile`](../../reference/internal/metadata/_extract_columns_from_profile.md) | — |
| [`_key_part`](../../reference/internal/metadata/_key_part.md) | — |
| [`_now_utc_iso`](../../reference/internal/metadata/_now_utc_iso.md) | — |
| [`_resolve_action_by`](../../reference/internal/metadata/_resolve_action_by.md) | — |
| [`_sha256_key`](../../reference/internal/metadata/_sha256_key.md) | [`build_dq_rule_key`](../../reference/build_dq_rule_key/), [`build_metadata_column_key`](../../reference/build_metadata_column_key/), [`build_metadata_table_key`](../../reference/build_metadata_table_key/) |
