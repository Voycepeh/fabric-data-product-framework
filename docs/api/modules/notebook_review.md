# `notebook_review` module

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
| [`review_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations.md) | function | Review active DQ rules one at a time for governed deactivation actions. | [`_require_ipywidgets`](../../reference/internal/notebook_review/_require_ipywidgets.md) (internal) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_require_ipywidgets`](../../reference/internal/notebook_review/_require_ipywidgets.md) | [`review_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations.md) |
