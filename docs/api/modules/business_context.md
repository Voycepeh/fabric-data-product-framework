# `business_context` module

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
| [`capture_column_business_context`](../../reference/capture_column_business_context/) | function | Display interactive approval widget. | [`_require_ipywidgets`](../../reference/internal/business_context/_require_ipywidgets.md) (internal) |
| [`extract_column_business_context_suggestions`](../../reference/extract_column_business_context_suggestions/) | function | Parse AI suggestion rows from Spark DataFrames or ``list[dict]`` payloads. | [`_parse_ai_dict_response`](../../reference/internal/business_context/_parse_ai_dict_response.md) (internal) |
| [`prepare_business_context_profile_input`](../../reference/prepare_business_context_profile_input/) | function | — | — |
| [`suggest_column_business_contexts`](../../reference/suggest_column_business_contexts/) | function | Run Fabric AI to draft column business context suggestions. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_parse_ai_dict_response`](../../reference/internal/business_context/_parse_ai_dict_response.md) | [`extract_column_business_context_suggestions`](../../reference/extract_column_business_context_suggestions/) |
| [`_require_ipywidgets`](../../reference/internal/business_context/_require_ipywidgets.md) | [`capture_column_business_context`](../../reference/capture_column_business_context/) |
