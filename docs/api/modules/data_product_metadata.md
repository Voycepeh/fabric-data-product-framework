# `data_product_metadata` module

<div class="api-status-block">
  <span class="api-chip api-chip-internal">Advanced supporting module</span>
  <div class="api-chip-subtitle">Used by workflow references but not promoted as a primary notebook module.</div>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`get_selected_agreement`](../../reference/get_selected_agreement/) | function | Return selected agreement from widget flow. | — |
| [`load_agreements`](../../reference/load_agreements/) | function | Load latest distinct agreement rows for widget selection. | [`_coerce_row_dicts`](../../reference/internal/metadata/_coerce_row_dicts/) (internal), [`_latest_distinct_agreements`](../../reference/internal/metadata/_latest_distinct_agreements/) (internal) |
| [`load_notebook_registry`](../../reference/load_notebook_registry/) | function | — | [`_coerce_row_dicts`](../../reference/internal/metadata/_coerce_row_dicts/) (internal) |
| [`register_current_notebook`](../../reference/register_current_notebook/) | function | — | [`_runtime_context`](../../reference/internal/metadata/_runtime_context/) (internal) |
| [`select_agreement`](../../reference/select_agreement/) | function | Render a widget dropdown and store selected agreement row in module state. | [`_agreement_option_label`](../../reference/internal/metadata/_agreement_option_label/) (internal), [`_coerce_row_dicts`](../../reference/internal/metadata/_coerce_row_dicts/) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_agreement_option_label`](../../reference/internal/metadata/_agreement_option_label/) | [`select_agreement`](../../reference/select_agreement/) |
| [`_coerce_row_dicts`](../../reference/internal/metadata/_coerce_row_dicts/) | [`load_agreements`](../../reference/load_agreements/), [`load_notebook_registry`](../../reference/load_notebook_registry/), [`select_agreement`](../../reference/select_agreement/) |
| [`_extract_columns_from_profile`](../../reference/internal/metadata/_extract_columns_from_profile/) | — |
| [`_key_part`](../../reference/internal/metadata/_key_part/) | — |
| [`_latest_distinct_agreements`](../../reference/internal/metadata/_latest_distinct_agreements/) | [`load_agreements`](../../reference/load_agreements/) |
| [`_now_utc_iso`](../../reference/internal/metadata/_now_utc_iso/) | — |
| [`_resolve_action_by`](../../reference/internal/metadata/_resolve_action_by/) | — |
| [`_runtime_context`](../../reference/internal/metadata/_runtime_context/) | [`register_current_notebook`](../../reference/register_current_notebook/) |
| [`_sha256_key`](../../reference/internal/metadata/_sha256_key/) | — |
