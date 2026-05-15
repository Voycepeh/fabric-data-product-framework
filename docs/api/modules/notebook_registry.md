# `notebook_registry` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`get_selected_agreement`](../../reference/get_selected_agreement/) | function | Return selected agreement from widget flow. | — |
| [`load_agreements`](../../reference/load_agreements/) | function | Load latest distinct agreement rows for widget selection. | [`_coerce_row_dicts`](../../reference/internal/notebook_registry/_coerce_row_dicts/) (internal), [`_latest_distinct_agreements`](../../reference/internal/notebook_registry/_latest_distinct_agreements/) (internal) |
| [`load_notebook_registry`](../../reference/load_notebook_registry/) | function | — | [`_coerce_row_dicts`](../../reference/internal/notebook_registry/_coerce_row_dicts/) (internal) |
| [`register_current_notebook`](../../reference/register_current_notebook/) | function | — | [`_runtime_context`](../../reference/internal/notebook_registry/_runtime_context/) (internal) |
| [`select_agreement`](../../reference/select_agreement/) | function | Render a widget dropdown and store selected agreement row in module state. | [`_agreement_option_label`](../../reference/internal/notebook_registry/_agreement_option_label/) (internal), [`_coerce_row_dicts`](../../reference/internal/notebook_registry/_coerce_row_dicts/) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_agreement_option_label`](../../reference/internal/notebook_registry/_agreement_option_label/) | [`select_agreement`](../../reference/select_agreement/) |
| [`_coerce_row_dicts`](../../reference/internal/notebook_registry/_coerce_row_dicts/) | [`load_agreements`](../../reference/load_agreements/), [`load_notebook_registry`](../../reference/load_notebook_registry/), [`select_agreement`](../../reference/select_agreement/) |
| [`_latest_distinct_agreements`](../../reference/internal/notebook_registry/_latest_distinct_agreements/) | [`load_agreements`](../../reference/load_agreements/) |
| [`_runtime_context`](../../reference/internal/notebook_registry/_runtime_context/) | [`register_current_notebook`](../../reference/register_current_notebook/) |
