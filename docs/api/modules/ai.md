# `ai` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_dq_rule_candidate_prompt`](../../reference/step-08-dq-rule-generation-review/build_dq_rule_candidate_prompt.md) | function | Build the DQ-candidate prompt used in AI-assisted quality drafting. | [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_governance_candidate_prompt`](../../reference/step-09-classification-sensitivity/build_governance_candidate_prompt.md) | function | Build the governance-candidate prompt for AI-assisted classification drafts. | [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_handover_summary_prompt`](../../reference/step-10-lineage-handover-documentation/build_handover_summary_prompt.md) | function | Build the handover-summary prompt for AI-assisted run handoff drafting. | [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_manual_dq_rule_prompt_package`](../../reference/step-08-dq-rule-generation-review/build_manual_dq_rule_prompt_package.md) | function | Build copy/paste prompt package for manual DQ candidate generation. | [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows.md) (internal) |
| [`build_manual_governance_prompt_package`](../../reference/step-09-classification-sensitivity/build_manual_governance_prompt_package.md) | function | Build copy/paste prompt package for manual governance suggestion generation. | [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows.md) (internal) |
| [`build_manual_handover_prompt_package`](../../reference/step-10-lineage-handover-documentation/build_manual_handover_prompt_package.md) | function | Build copy/paste prompt package for manual handover summary generation. | [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows.md) (internal) |
| [`check_fabric_ai_functions_available`](../../reference/step-01-governance-purpose-ownership/check_fabric_ai_functions_available.md) | function | Check whether Fabric AI Functions can be imported in the current runtime. | — |
| [`configure_fabric_ai_functions`](../../reference/step-01-governance-purpose-ownership/configure_fabric_ai_functions.md) | function | Apply optional default Fabric AI Function configuration. | — |
| [`generate_dq_rule_candidates_with_fabric_ai`](../../reference/step-08-dq-rule-generation-review/generate_dq_rule_candidates_with_fabric_ai.md) | function | Append AI-suggested DQ rule candidates to a profiling DataFrame. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`generate_governance_candidates_with_fabric_ai`](../../reference/step-09-classification-sensitivity/generate_governance_candidates_with_fabric_ai.md) | function | Execute Fabric AI Functions to append governance suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`generate_handover_summary_with_fabric_ai`](../../reference/step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai.md) | function | Execute Fabric AI Functions to append handover summary suggestions. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`parse_manual_ai_json_response`](../../reference/step-10-lineage-handover-documentation/parse_manual_ai_json_response.md) | function | Parse manual AI JSON output into Python objects. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows.md) | [`build_manual_dq_rule_prompt_package`](../../reference/step-08-dq-rule-generation-review/build_manual_dq_rule_prompt_package.md), [`build_manual_governance_prompt_package`](../../reference/step-09-classification-sensitivity/build_manual_governance_prompt_package.md), [`build_manual_handover_prompt_package`](../../reference/step-10-lineage-handover-documentation/build_manual_handover_prompt_package.md) |
| [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) | [`generate_dq_rule_candidates_with_fabric_ai`](../../reference/step-08-dq-rule-generation-review/generate_dq_rule_candidates_with_fabric_ai.md), [`generate_governance_candidates_with_fabric_ai`](../../reference/step-09-classification-sensitivity/generate_governance_candidates_with_fabric_ai.md), [`generate_handover_summary_with_fabric_ai`](../../reference/step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai.md) |
| [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template.md) | [`build_dq_rule_candidate_prompt`](../../reference/step-08-dq-rule-generation-review/build_dq_rule_candidate_prompt.md), [`build_governance_candidate_prompt`](../../reference/step-09-classification-sensitivity/build_governance_candidate_prompt.md), [`build_handover_summary_prompt`](../../reference/step-10-lineage-handover-documentation/build_handover_summary_prompt.md) |
