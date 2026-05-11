# `data_quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Recommended notebook entrypoints

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/step-06d-controlled-outputs/assert_dq_passed.md) | function | Raise only after evidence materialization when error-severity rules fail. | — |
| [`validate_dq_rules`](../../reference/step-06c-pipeline-controls/validate_dq_rules.md) | function | Validate canonical DQ rules before enforcement. | — |

## Advanced helpers

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) | function | Draft candidate DQ rules from metadata profiles or raw DataFrame fallback. | [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) (internal) |
| [`enforce_dq_rules`](../../reference/step-06c-pipeline-controls/enforce_dq_rules.md) | function | Enforce approved DQ rules and return structured deterministic outputs. | — |
| [`write_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/write_dq_rules.md) | function | Validate, build, and persist approved DQ rules. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_latest_dq_rule_versions`](../../reference/internal/data_quality/_latest_dq_rule_versions.md) | — |
| [`_load_active_dq_rule_metadata`](../../reference/internal/data_quality/_load_active_dq_rule_metadata.md) | — |
| [`_parse_dq_rules_dict_from_text`](../../reference/internal/data_quality/_parse_dq_rules_dict_from_text.md) | — |
| [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) | [`draft_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules.md) |
