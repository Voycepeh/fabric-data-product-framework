# `dq_review` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Recommended notebook entrypoints

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| — | — | No recommended entrypoints configured. | — |

## Advanced helpers

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`review_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations.md) | function | Review active DQ rules one at a time for governed deactivation actions. | [`_require_ipywidgets`](../../reference/internal/dq_review/_require_ipywidgets.md) (internal) |
| [`review_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rules.md) | function | Review AI-suggested DQ rules sequentially with explicit approve/reject decisions. | [`_require_ipywidgets`](../../reference/internal/dq_review/_require_ipywidgets.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_require_ipywidgets`](../../reference/internal/dq_review/_require_ipywidgets.md) | [`review_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations.md), [`review_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rules.md) |
