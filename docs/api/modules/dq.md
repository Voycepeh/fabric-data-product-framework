# `dq` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Recommended notebook entrypoints

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/step-06d-controlled-outputs/assert_dq_passed.md) | function | Raise only after evidence materialization when error-severity rules fail. | — |
| [`profile_for_dq`](../../reference/step-08-ai-assisted-dq-suggestions/profile_for_dq.md) | function | Profile a Spark DataFrame into one row per source column for DQ rule suggestion. | — |
| [`run_dq_rules`](../../reference/step-06c-pipeline-controls/run_dq_rules.md) | function | Run notebook-facing DQ rules and return a Spark DataFrame result. | — |
| [`suggest_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/suggest_dq_rules.md) | function | Generate row-wise AI DQ suggestions using Fabric AI Functions. | — |
| [`validate_dq_rules`](../../reference/step-06c-pipeline-controls/validate_dq_rules.md) | function | Validate canonical DQ rules before enforcement. | — |

## Advanced helpers

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`AI_SUGGESTABLE_DQ_RULE_TYPES`](../../reference/step-08-ai-assisted-dq-suggestions/AI_SUGGESTABLE_DQ_RULE_TYPES.md) | constant | — | — |
| [`build_dq_rule_candidate_prompt`](../../reference/step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt.md) | function | Build the DQ-candidate prompt used in AI-assisted quality drafting. | — |
| [`build_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/build_dq_rule_deactivations.md) | function | Build append-only inactive metadata rows for governed DQ rule deactivation. | — |
| [`build_dq_rule_history`](../../reference/step-08-ai-assisted-dq-suggestions/build_dq_rule_history.md) | function | Build append-only active metadata rows for approved DQ rules. | — |
| [`build_manual_dq_rule_prompt_package`](../../reference/step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package.md) | function | Build copy/paste prompt package for manual DQ candidate generation. | — |
| [`extract_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/extract_dq_rules.md) | function | Extract notebook-shaped AI responses and deduplicate candidate DQ rules by ``rule_id``. | [`_parse_dq_rules_dict_from_text`](../../reference/internal/dq/_parse_dq_rules_dict_from_text.md) (internal) |
| [`generate_dq_rule_candidates_with_fabric_ai`](../../reference/step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai.md) | function | Append AI-suggested DQ rule candidates to a profiling DataFrame. | — |
| [`load_active_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/load_active_dq_rules.md) | function | Load latest active approved rules from append-only metadata history. | [`_latest_dq_rule_versions`](../../reference/internal/dq/_latest_dq_rule_versions.md) (internal) |
| [`review_dq_rule_deactivations`](../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations.md) | function | Review active DQ rules one at a time for governed deactivation actions. | — |
| [`split_dq_rows`](../../reference/step-08-ai-assisted-dq-suggestions/split_dq_rows.md) | function | Split source rows into valid rows, quarantine rows, and one-row-per-failure evidence. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_latest_dq_rule_versions`](../../reference/internal/dq/_latest_dq_rule_versions.md) | [`load_active_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/load_active_dq_rules.md) |
| [`_load_active_dq_rule_metadata`](../../reference/internal/dq/_load_active_dq_rule_metadata.md) | — |
| [`_parse_dq_rules_dict_from_text`](../../reference/internal/dq/_parse_dq_rules_dict_from_text.md) | [`extract_dq_rules`](../../reference/step-08-ai-assisted-dq-suggestions/extract_dq_rules.md) |
