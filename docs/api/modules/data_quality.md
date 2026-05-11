# `data_quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/step-06d-controlled-outputs/assert_dq_passed.md) | function | Raise only after evidence materialization when error-severity rules fail. | — |
| [`enforce_dq_rules`](../../reference/step-06c-pipeline-controls/enforce_dq_rules.md) | function | Run notebook-facing DQ rules and return a Spark DataFrame result. | — |
| [`validate_dq_rules`](../../reference/step-06c-pipeline-controls/validate_dq_rules.md) | function | Validate canonical DQ rules before enforcement. | — |

Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) | function | Draft AI-suggested DQ rules for later human review and approval. | [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) (internal) |
| [`review_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations.md) | function | Review active DQ rules one at a time for governed deactivation actions. | — |
| [`review_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rules.md) | function | Review AI-suggested DQ rules sequentially with explicit approve/reject decisions. | — |
| [`write_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/write_dq_rules.md) | function | Persist human-approved DQ rules into governed metadata. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_latest_dq_rule_versions`](../../reference/internal/data_quality/_latest_dq_rule_versions.md) | — |
| [`_load_active_dq_rule_metadata`](../../reference/internal/data_quality/_load_active_dq_rule_metadata.md) | — |
| [`_parse_dq_rules_dict_from_text`](../../reference/internal/data_quality/_parse_dq_rules_dict_from_text.md) | — |
| [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) | [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) |
| [`_resolve_action_by`](../../reference/internal/data_quality/_resolve_action_by.md) | — |
