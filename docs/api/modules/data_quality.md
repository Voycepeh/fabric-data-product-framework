# `data_quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/assert_dq_passed/) | function | Raise only after evidence materialization when error-severity rules fail. | — |
| [`draft_dq_rules`](../../reference/draft_dq_rules/) | function | Draft candidate DQ rules from metadata profiles or raw DataFrame fallback. | [`_extract_dq_rules`](../../reference/internal/data_quality/_extract_dq_rules/) (internal), [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input/) (internal), [`_suggest_dq_rules`](../../reference/internal/data_quality/_suggest_dq_rules/) (internal) |
| [`enforce_dq`](../../reference/enforce_dq/) | function | Enforce approved DQ rules and return structured deterministic outputs. | [`_load_active_dq_rules`](../../reference/internal/data_quality/_load_active_dq_rules/) (internal), [`_run_dq_rules`](../../reference/internal/data_quality/_run_dq_rules/) (internal), [`_split_dq_rows`](../../reference/internal/data_quality/_split_dq_rows/) (internal) |
| [`get_dq_review_results`](../../reference/get_dq_review_results/) | function | Collect current approved/rejected DQ review results from widget state. | — |
| [`load_dq_rules`](../../reference/load_dq_rules/) | function | Load latest active approved DQ rules from append-only metadata history. | [`_load_active_dq_rules`](../../reference/internal/data_quality/_load_active_dq_rules/) (internal) |
| [`review_dq_rules`](../../reference/review_dq_rules/) | function | Review AI-suggested DQ rules sequentially with explicit approve/reject decisions. | [`_require_ipywidgets`](../../reference/internal/data_quality/_require_ipywidgets/) (internal) |
| [`write_dq_rules`](../../reference/write_dq_rules/) | function | Validate, build, and persist approved DQ rules. | [`_build_dq_rule_history`](../../reference/internal/data_quality/_build_dq_rule_history/) (internal) |

Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`review_dq_rule_deactivations`](../../reference/review_dq_rule_deactivations/) | function | Review active DQ rules one at a time for governed deactivation actions. | [`_require_ipywidgets`](../../reference/internal/data_quality/_require_ipywidgets/) (internal) |
| [`validate_dq_rules`](../../reference/validate_dq_rules/) | function | Validate canonical DQ rules before enforcement. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_build_dq_rule_deactivations`](../../reference/internal/data_quality/_build_dq_rule_deactivations/) | — |
| [`_build_dq_rule_history`](../../reference/internal/data_quality/_build_dq_rule_history/) | [`write_dq_rules`](../../reference/write_dq_rules/) |
| [`_extract_dq_rules`](../../reference/internal/data_quality/_extract_dq_rules/) | [`draft_dq_rules`](../../reference/draft_dq_rules/) |
| [`_latest_dq_rule_versions`](../../reference/internal/data_quality/_latest_dq_rule_versions/) | — |
| [`_load_active_dq_rule_metadata`](../../reference/internal/data_quality/_load_active_dq_rule_metadata/) | — |
| [`_load_active_dq_rules`](../../reference/internal/data_quality/_load_active_dq_rules/) | [`enforce_dq`](../../reference/enforce_dq/), [`load_dq_rules`](../../reference/load_dq_rules/) |
| [`_parse_dq_rules_dict_from_text`](../../reference/internal/data_quality/_parse_dq_rules_dict_from_text/) | — |
| [`_prepare_dq_profile_input`](../../reference/internal/data_quality/_prepare_dq_profile_input/) | [`draft_dq_rules`](../../reference/draft_dq_rules/) |
| [`_profile_for_dq`](../../reference/internal/data_quality/_profile_for_dq/) | — |
| [`_require_ipywidgets`](../../reference/internal/data_quality/_require_ipywidgets/) | [`review_dq_rule_deactivations`](../../reference/review_dq_rule_deactivations/), [`review_dq_rules`](../../reference/review_dq_rules/) |
| [`_resolve_action_by`](../../reference/internal/data_quality/_resolve_action_by/) | — |
| [`_run_dq_rules`](../../reference/internal/data_quality/_run_dq_rules/) | [`enforce_dq`](../../reference/enforce_dq/) |
| [`_split_dq_rows`](../../reference/internal/data_quality/_split_dq_rows/) | [`enforce_dq`](../../reference/enforce_dq/) |
| [`_suggest_dq_rules`](../../reference/internal/data_quality/_suggest_dq_rules/) | [`draft_dq_rules`](../../reference/draft_dq_rules/) |
