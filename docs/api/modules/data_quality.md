# `data_quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Recommended notebook entrypoints

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_dq_passed`](../../reference/step-06d-controlled-outputs/assert_dq_passed.md) | function | Raise when any error-severity DQ rule failed after results are logged. | — |
| [`run_dq_rules`](../../reference/step-06c-pipeline-controls/run_dq_rules.md) | function | Execute the `run_dq_rules` workflow step in FabricOps. | [`_to_quality_rule`](../../reference/internal/quality/_to_quality_rule.md) (internal) |
| [`split_valid_and_quarantine`](../../reference/step-06c-pipeline-controls/split_valid_and_quarantine.md) | function | Execute the `split_valid_and_quarantine` workflow step in FabricOps. | — |
| [`suggest_dq_rules_prompt`](../../reference/step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt.md) | function | Build a prompt for candidate DQ rule suggestions. | — |
| [`validate_dq_rules`](../../reference/step-06c-pipeline-controls/validate_dq_rules.md) | function | Validate notebook-facing DQ rules. | — |

## Advanced helpers

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_dq_rule_candidate_prompt`](../../reference/step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt.md) | function | Build the DQ-candidate prompt used in AI-assisted quality drafting. | — |
| [`build_manual_dq_rule_prompt_package`](../../reference/step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package.md) | function | Build copy/paste prompt package for manual DQ candidate generation. | — |
| [`DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE`](../../reference/step-08-ai-assisted-dq-suggestions/DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE.md) | constant | Default prompt template used to draft candidate DQ rules. | — |
| [`generate_dq_rule_candidates_with_fabric_ai`](../../reference/step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai.md) | function | Append AI-suggested DQ rule candidates to a profiling DataFrame. | — |
| [`get_default_dq_rule_templates`](../../reference/step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates.md) | function | Return editable example data quality rules. | — |
| [`run_data_product`](../../reference/step-06a-transformation-logic/run_data_product.md) | function | Run the starter kit workflow end-to-end for a data product outcome. | — |
| [`run_quality_rules`](../../reference/step-06c-pipeline-controls/run_quality_rules.md) | function | Execute quality rules against a dataframe and return structured results. | — |
| [`suggest_accepted_value_mapping_prompt`](../../reference/step-08-ai-assisted-dq-suggestions/suggest_accepted_value_mapping_prompt.md) | function | Build a constrained prompt for accepted-value mapping suggestions. | — |
| [`suggest_closest_accepted_value`](../../reference/step-08-ai-assisted-dq-suggestions/suggest_closest_accepted_value.md) | function | Suggest a deterministic closest accepted value using ``difflib``. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_to_quality_rule`](../../reference/internal/dq/_to_quality_rule.md) | [`run_dq_rules`](../../reference/step-06c-pipeline-controls/run_dq_rules.md) |
