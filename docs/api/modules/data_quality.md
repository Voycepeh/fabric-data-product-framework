# `data_quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/step-06d-controlled-outputs/assert_dq_passed.md) | function | Raise only after evidence materialization when error-severity rules fail. | — |
| [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) | function | Draft candidate DQ rules from metadata profiles or raw DataFrame fallback. | [`_extract_dq_rules`](../../reference/internal/data_quality/_extract_dq_rules.md) (internal), [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) (internal), [`_suggest_dq_rules`](../../reference/internal/data_quality/_suggest_dq_rules.md) (internal) |
| [`enforce_dq_rules`](../../reference/step-06c-pipeline-controls/enforce_dq_rules.md) | function | Run notebook-facing DQ rules and return a Spark DataFrame result. | [`_load_active_dq_rules`](../../reference/internal/data_quality/_load_active_dq_rules.md) (internal), [`_run_dq_rules`](../../reference/internal/data_quality/_run_dq_rules.md) (internal), [`_split_dq_rows`](../../reference/internal/data_quality/_split_dq_rows.md) (internal) |
| [`review_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rules.md) | function | Review AI-suggested DQ rules sequentially with explicit approve/reject decisions. | — |
| [`write_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/write_dq_rules.md) | function | Validate, build, and persist approved DQ rules. | [`_build_dq_rule_history`](../../reference/internal/data_quality/_build_dq_rule_history.md) (internal) |

Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`DQEnforcementResult`](../../reference/step-06c-pipeline-controls/DQEnforcementResult.md) | class | Structured DQ enforcement output for notebook-first usage. | — |
| [`review_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations.md) | function | Review active DQ rules and capture governed deactivation decisions. | — |
| [`validate_dq_rules`](../../reference/step-06c-pipeline-controls/validate_dq_rules.md) | function | Validate canonical DQ rules before enforcement. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_build_dq_rule_deactivations`](../../reference/internal/data_quality/_build_dq_rule_deactivations.md) | — |
| [`_build_dq_rule_history`](../../reference/internal/data_quality/_build_dq_rule_history.md) | [`write_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/write_dq_rules.md) |
| [`_extract_dq_rules`](../../reference/internal/data_quality/_extract_dq_rules.md) | [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) |
| [`_latest_dq_rule_versions`](../../reference/internal/data_quality/_latest_dq_rule_versions.md) | — |
| [`_load_active_dq_rule_metadata`](../../reference/internal/data_quality/_load_active_dq_rule_metadata.md) | — |
| [`_load_active_dq_rules`](../../reference/internal/data_quality/_load_active_dq_rules.md) | [`enforce_dq_rules`](../../reference/step-06c-pipeline-controls/enforce_dq_rules.md) |
| [`_parse_dq_rules_dict_from_text`](../../reference/internal/data_quality/_parse_dq_rules_dict_from_text.md) | — |
| [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) | [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) |
| [`_profile_for_dq`](../../reference/internal/data_quality/_profile_for_dq.md) | — |
| [`_resolve_action_by`](../../reference/internal/data_quality/_resolve_action_by.md) | — |
| [`_run_dq_rules`](../../reference/internal/data_quality/_run_dq_rules.md) | [`enforce_dq_rules`](../../reference/step-06c-pipeline-controls/enforce_dq_rules.md) |
| [`_split_dq_rows`](../../reference/internal/data_quality/_split_dq_rows.md) | [`enforce_dq_rules`](../../reference/step-06c-pipeline-controls/enforce_dq_rules.md) |
| [`_suggest_dq_rules`](../../reference/internal/data_quality/_suggest_dq_rules.md) | [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) |
