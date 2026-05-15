# `business_context` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`draft_business_context`](../../reference/draft_business_context/) | function | Run Fabric AI to draft column business context suggestions. | — |
| [`review_business_context`](../../reference/review_business_context/) | function | Display interactive approval widget. | [`_require_ipywidgets`](../../reference/internal/business_context/_require_ipywidgets/) (internal) |
| [`write_business_context`](../../reference/write_business_context/) | function | Persist approved business context rows via metadata writer. | — |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_extract_column_business_context_suggestions`](../../reference/internal/business_context/_extract_column_business_context_suggestions/) | — |
| [`_parse_ai_dict_response`](../../reference/internal/business_context/_parse_ai_dict_response/) | — |
| [`_prepare_business_context_profile_input`](../../reference/internal/business_context/_prepare_business_context_profile_input/) | — |
| [`_require_ipywidgets`](../../reference/internal/business_context/_require_ipywidgets/) | [`review_business_context`](../../reference/review_business_context/) |
