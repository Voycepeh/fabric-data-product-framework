# `data_quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/#assert_dq_passed) | function | Raise only after evidence materialization when error-severity rules fail. | — |
| [`draft_dq_rules`](../../reference/#draft_dq_rules) | function | Draft candidate DQ rules from metadata profiles or raw DataFrame fallback. | [`_extract_dq_rules`](../../reference/internal/data_quality/_extract_dq_rules.md) (internal), [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) (internal), [`_suggest_dq_rules`](../../reference/internal/data_quality/_suggest_dq_rules.md) (internal) |
| [`enforce_dq_rules`](../../reference/#enforce_dq_rules) | function | Run notebook-facing DQ rules and return a Spark DataFrame result. | [`_load_active_dq_rules`](../../reference/internal/data_quality/_load_active_dq_rules.md) (internal), [`_run_dq_rules`](../../reference/internal/data_quality/_run_dq_rules.md) (internal), [`_split_dq_rows`](../../reference/internal/data_quality/_split_dq_rows.md) (internal) |
| [`review_dq_rules`](../../reference/#review_dq_rules) | function | Review AI-suggested DQ rules sequentially with explicit approve/reject decisions. | [`_require_ipywidgets`](../../reference/internal/data_quality/_require_ipywidgets.md) (internal) |
| [`write_dq_rules`](../../reference/#write_dq_rules) | function | Validate, build, and persist approved DQ rules. | [`_build_dq_rule_history`](../../reference/internal/data_quality/_build_dq_rule_history.md) (internal) |

Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`review_dq_rule_deactivations`](../../reference/#review_dq_rule_deactivations) | function | Review active DQ rules one at a time for governed deactivation actions. | [`_require_ipywidgets`](../../reference/internal/data_quality/_require_ipywidgets.md) (internal) |
| [`validate_dq_rules`](../../reference/#validate_dq_rules) | function | Validate canonical DQ rules before enforcement. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_build_dq_rule_deactivations`](../../reference/internal/data_quality/_build_dq_rule_deactivations.md) | — |
| [`_build_dq_rule_history`](../../reference/internal/data_quality/_build_dq_rule_history.md) | [`write_dq_rules`](../../reference/#write_dq_rules) |
| [`_extract_dq_rules`](../../reference/internal/data_quality/_extract_dq_rules.md) | [`draft_dq_rules`](../../reference/#draft_dq_rules) |
| [`_latest_dq_rule_versions`](../../reference/internal/data_quality/_latest_dq_rule_versions.md) | — |
| [`_load_active_dq_rule_metadata`](../../reference/internal/data_quality/_load_active_dq_rule_metadata.md) | — |
| [`_load_active_dq_rules`](../../reference/internal/data_quality/_load_active_dq_rules.md) | [`enforce_dq_rules`](../../reference/#enforce_dq_rules) |
| [`_parse_dq_rules_dict_from_text`](../../reference/internal/data_quality/_parse_dq_rules_dict_from_text.md) | — |
| [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input.md) | [`draft_dq_rules`](../../reference/#draft_dq_rules) |
| [`_profile_for_dq`](../../reference/internal/data_quality/_profile_for_dq.md) | — |
| [`_require_ipywidgets`](../../reference/internal/data_quality/_require_ipywidgets.md) | [`review_dq_rule_deactivations`](../../reference/#review_dq_rule_deactivations), [`review_dq_rules`](../../reference/#review_dq_rules) |
| [`_resolve_action_by`](../../reference/internal/data_quality/_resolve_action_by.md) | — |
| [`_run_dq_rules`](../../reference/internal/data_quality/_run_dq_rules.md) | [`enforce_dq_rules`](../../reference/#enforce_dq_rules) |
| [`_split_dq_rows`](../../reference/internal/data_quality/_split_dq_rows.md) | [`enforce_dq_rules`](../../reference/#enforce_dq_rules) |
| [`_suggest_dq_rules`](../../reference/internal/data_quality/_suggest_dq_rules.md) | [`draft_dq_rules`](../../reference/#draft_dq_rules) |
