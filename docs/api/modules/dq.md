# `dq` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/step-06d-controlled-outputs/assert_dq_passed.md) | function | Raise when any error-severity DQ rule failed after results are logged. | — |
| [`get_default_dq_rule_templates`](../../reference/step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates.md) | function | Return editable example data quality rules. | — |
| [`run_dq_rules`](../../reference/step-06c-pipeline-controls/run_dq_rules.md) | function | Run notebook-facing DQ rules and return a Spark DataFrame result. | [`_to_quality_rule`](../../reference/internal/dq/_to_quality_rule.md) (internal) |
| [`suggest_dq_rules_prompt`](../../reference/step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt.md) | function | Build a prompt for candidate DQ rule suggestions. | — |
| [`validate_dq_rules`](../../reference/step-06c-pipeline-controls/validate_dq_rules.md) | function | Validate notebook-facing DQ rules. | — |
| [`write_dq_results`](../../reference/step-06d-controlled-outputs/write_dq_results.md) | function | Write DQ result DataFrame to a lakehouse table. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_to_quality_rule`](../../reference/internal/dq/_to_quality_rule.md) | [`run_dq_rules`](../../reference/step-06c-pipeline-controls/run_dq_rules.md) |
