# `handover_documentation` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_handover_summary_prompt`](../../reference/step-10-lineage-handover-documentation/build_handover_summary_prompt.md) | function | Build the handover-summary prompt for AI-assisted run handoff drafting. | — |
| [`build_manual_handover_prompt_package`](../../reference/step-10-lineage-handover-documentation/build_manual_handover_prompt_package.md) | function | Build copy/paste prompt package for manual handover summary generation. | — |
| [`build_run_summary`](../../reference/step-10-lineage-handover-documentation/build_run_summary.md) | function | Build a handover-friendly summary for one data product run. | — |
| [`generate_handover_summary_with_fabric_ai`](../../reference/step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai.md) | function | Execute Fabric AI Functions to append handover summary suggestions. | — |
| [`parse_manual_ai_json_response`](../../reference/step-10-lineage-handover-documentation/parse_manual_ai_json_response.md) | function | Parse manual AI JSON output into Python objects. | — |
| [`render_run_summary_markdown`](../../reference/step-10-lineage-handover-documentation/render_run_summary_markdown.md) | function | Render a run summary dictionary into Markdown for handover notes. | [`_status_of`](../../reference/internal/handover_documentation/_status_of.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_status_of`](../../reference/internal/handover_documentation/_status_of.md) | [`render_run_summary_markdown`](../../reference/step-10-lineage-handover-documentation/render_run_summary_markdown.md) |
