# `ai` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`check_fabric_ai_functions_available`](../../reference/step-07-ai-rule-generation-review/check_fabric_ai_functions_available.md) | function | Best-effort check for Fabric AI Functions availability. | — |
| [`configure_fabric_ai_functions`](../../reference/step-07-ai-rule-generation-review/configure_fabric_ai_functions.md) | function | Configure Fabric AI Functions default settings when available. | — |
| [`generate_dq_rule_candidates_with_fabric_ai`](../../reference/step-07-ai-rule-generation-review/generate_dq_rule_candidates_with_fabric_ai.md) | function | Generate DQ candidate suggestions as an enriched DataFrame. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`generate_governance_candidates_with_fabric_ai`](../../reference/step-12-governance-classification/generate_governance_candidates_with_fabric_ai.md) | function | Generate governance label candidate suggestions as an enriched DataFrame. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`generate_handover_summary_with_fabric_ai`](../../reference/step-13-lineage-summary-handover/generate_handover_summary_with_fabric_ai.md) | function | Generate handover summary suggestions as an enriched DataFrame. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) | [`generate_dq_rule_candidates_with_fabric_ai`](../../reference/step-07-ai-rule-generation-review/generate_dq_rule_candidates_with_fabric_ai.md), [`generate_governance_candidates_with_fabric_ai`](../../reference/step-12-governance-classification/generate_governance_candidates_with_fabric_ai.md), [`generate_handover_summary_with_fabric_ai`](../../reference/step-13-lineage-summary-handover/generate_handover_summary_with_fabric_ai.md) |
