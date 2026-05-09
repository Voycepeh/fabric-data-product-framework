# `data_lineage` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Recommended notebook entrypoints

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_lineage_from_notebook_code`](../../reference/step-10-lineage-handover-documentation/build_lineage_from_notebook_code.md) | function | Scan, optionally enrich, and validate lineage from notebook source code. | — |

## Advanced helpers

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_lineage_handover_markdown`](../../reference/step-10-lineage-handover-documentation/build_lineage_handover_markdown.md) | function | Create a concise markdown handover summary from lineage execution results. | — |
| [`build_lineage_record_from_steps`](../../reference/step-10-lineage-handover-documentation/build_lineage_record_from_steps.md) | function | Create metadata-ready lineage records from validated lineage steps. | — |
| [`build_lineage_records`](../../reference/step-10-lineage-handover-documentation/build_lineage_records.md) | function | Build compact lineage records for downstream metadata sinks. | — |
| [`enrich_lineage_steps_with_ai`](../../reference/step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai.md) | function | Optionally enrich deterministic lineage steps using an AI helper callable. | — |
| [`fallback_copilot_lineage_prompt`](../../reference/step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt.md) | function | Build a fallback Copilot prompt for manual lineage enrichment. | — |
| [`plot_lineage_steps`](../../reference/step-10-lineage-handover-documentation/plot_lineage_steps.md) | function | Render lineage steps as a directed graph figure. | — |
| [`scan_notebook_cells`](../../reference/step-10-lineage-handover-documentation/scan_notebook_cells.md) | function | Scan multiple notebook cells and append cell references to lineage steps. | — |
| [`scan_notebook_lineage`](../../reference/step-10-lineage-handover-documentation/scan_notebook_lineage.md) | function | Extract deterministic lineage steps from notebook code using AST parsing. | [`_call_name`](../../reference/internal/lineage/_call_name.md) (internal), [`_flatten_chain`](../../reference/internal/lineage/_flatten_chain.md) (internal), [`_name`](../../reference/internal/lineage/_name.md) (internal), [`_resolve_write_target`](../../reference/internal/lineage/_resolve_write_target.md) (internal), [`_step`](../../reference/internal/lineage/_step.md) (internal) |
| [`validate_lineage_steps`](../../reference/step-10-lineage-handover-documentation/validate_lineage_steps.md) | function | Validate lineage step structure and flag records requiring human review. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_call_name`](../../reference/internal/lineage/_call_name.md) | [`scan_notebook_lineage`](../../reference/step-10-lineage-handover-documentation/scan_notebook_lineage.md) |
| [`_flatten_chain`](../../reference/internal/lineage/_flatten_chain.md) | [`scan_notebook_lineage`](../../reference/step-10-lineage-handover-documentation/scan_notebook_lineage.md) |
| [`_literal`](../../reference/internal/lineage/_literal.md) | — |
| [`_name`](../../reference/internal/lineage/_name.md) | [`scan_notebook_lineage`](../../reference/step-10-lineage-handover-documentation/scan_notebook_lineage.md) |
| [`_resolve_write_target`](../../reference/internal/lineage/_resolve_write_target.md) | [`scan_notebook_lineage`](../../reference/step-10-lineage-handover-documentation/scan_notebook_lineage.md) |
| [`_step`](../../reference/internal/lineage/_step.md) | [`scan_notebook_lineage`](../../reference/step-10-lineage-handover-documentation/scan_notebook_lineage.md) |
