# `ai` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| — | — | No recommended entrypoints configured. | — |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_candidate_prompt`](../../reference/build_governance_candidate_prompt/) | function | Build the governance-candidate prompt for AI-assisted classification drafts. | [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template/) (internal) |
| [`build_handover_summary_prompt`](../../reference/build_handover_summary_prompt/) | function | Build the handover-summary prompt for AI-assisted run handoff drafting. | [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template/) (internal) |
| [`build_manual_governance_prompt_package`](../../reference/build_manual_governance_prompt_package/) | function | Build copy/paste prompt package for manual governance suggestion generation. | [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows/) (internal) |
| [`build_manual_handover_prompt_package`](../../reference/build_manual_handover_prompt_package/) | function | Build copy/paste prompt package for manual handover summary generation. | [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows/) (internal) |
| [`generate_governance_candidates_with_fabric_ai`](../../reference/generate_governance_candidates_with_fabric_ai/) | function | Execute Fabric AI Functions to append governance suggestions to a DataFrame. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe/) (internal) |
| [`generate_handover_summary_with_fabric_ai`](../../reference/generate_handover_summary_with_fabric_ai/) | function | Execute Fabric AI Functions to append handover summary suggestions. | [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe/) (internal) |
| [`parse_manual_ai_json_response`](../../reference/parse_manual_ai_json_response/) | function | Parse manual AI JSON output into Python objects. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_compact_sample_rows`](../../reference/internal/ai/_compact_sample_rows/) | [`build_manual_governance_prompt_package`](../../reference/build_manual_governance_prompt_package/), [`build_manual_handover_prompt_package`](../../reference/build_manual_handover_prompt_package/) |
| [`_require_fabric_ai_dataframe`](../../reference/internal/ai/_require_fabric_ai_dataframe/) | [`generate_governance_candidates_with_fabric_ai`](../../reference/generate_governance_candidates_with_fabric_ai/), [`generate_handover_summary_with_fabric_ai`](../../reference/generate_handover_summary_with_fabric_ai/) |
| [`_resolve_prompt_template`](../../reference/internal/ai/_resolve_prompt_template/) | [`build_governance_candidate_prompt`](../../reference/build_governance_candidate_prompt/), [`build_handover_summary_prompt`](../../reference/build_handover_summary_prompt/) |
