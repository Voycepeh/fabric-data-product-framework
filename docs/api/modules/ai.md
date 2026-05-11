# `ai` module

<div class="api-status-block">
  <span class="api-chip api-chip-internal">Advanced supporting module</span>
  <div class="api-chip-subtitle">Used by workflow references but not promoted as a primary notebook module.</div>
</div>

## Recommended notebook entrypoints

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| — | — | No recommended entrypoints configured. | — |

## Advanced helpers

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_candidate_prompt`](../../reference/step-09-ai-assisted-classification/build_governance_candidate_prompt.md) | function | Build the governance-candidate prompt for AI-assisted classification drafts. | [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_handover_summary_prompt`](../../reference/step-10-lineage-handover-documentation/build_handover_summary_prompt.md) | function | Build the handover-summary prompt for AI-assisted run handoff drafting. | [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template.md) (internal) |
| [`build_manual_governance_prompt_package`](../../reference/step-09-ai-assisted-classification/build_manual_governance_prompt_package.md) | function | Build copy/paste prompt package for manual governance suggestion generation. | [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows.md) (internal) |
| [`build_manual_handover_prompt_package`](../../reference/step-10-lineage-handover-documentation/build_manual_handover_prompt_package.md) | function | Build copy/paste prompt package for manual handover summary generation. | [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows.md) (internal) |
| [`generate_governance_candidates_with_fabric_ai`](../../reference/step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai.md) | function | Execute Fabric AI Functions to append governance suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`generate_handover_summary_with_fabric_ai`](../../reference/step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai.md) | function | Execute Fabric AI Functions to append handover summary suggestions. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) (internal) |
| [`parse_manual_ai_json_response`](../../reference/step-10-lineage-handover-documentation/parse_manual_ai_json_response.md) | function | Parse manual AI JSON output into Python objects. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows.md) | [`build_manual_governance_prompt_package`](../../reference/step-09-ai-assisted-classification/build_manual_governance_prompt_package.md), [`build_manual_handover_prompt_package`](../../reference/step-10-lineage-handover-documentation/build_manual_handover_prompt_package.md) |
| [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe.md) | [`generate_governance_candidates_with_fabric_ai`](../../reference/step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai.md), [`generate_handover_summary_with_fabric_ai`](../../reference/step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai.md) |
| [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template.md) | [`build_governance_candidate_prompt`](../../reference/step-09-ai-assisted-classification/build_governance_candidate_prompt.md), [`build_handover_summary_prompt`](../../reference/step-10-lineage-handover-documentation/build_handover_summary_prompt.md) |
