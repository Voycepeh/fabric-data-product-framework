# `business_context` module

<div class="api-status-block">
  <span class="api-chip api-chip-internal">Advanced supporting module</span>
  <div class="api-chip-subtitle">Used by workflow references but not promoted as a primary notebook module.</div>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`draft_business_context`](../../reference/draft_business_context/) | function | Compatibility-friendly short alias for :func:`suggest_column_business_contexts`. | — |
| [`review_business_context`](../../reference/review_business_context/) | function | Compatibility-friendly short alias for :func:`capture_column_business_context`. | — |
| [`write_business_context`](../../reference/write_business_context/) | function | Persist approved business context rows via metadata writer. | — |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_parse_ai_dict_response`](../../reference/internal/business_context/_parse_ai_dict_response/) | — |
| [`_require_ipywidgets`](../../reference/internal/business_context/_require_ipywidgets/) | — |
