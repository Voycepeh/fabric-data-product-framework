# `data_lineage` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_lineage_from_notebook_code`](../../reference/build_lineage_from_notebook_code/) | function | Scan, optionally enrich, and validate lineage from notebook source code. | [`_enrich_lineage_steps_with_ai`](../../reference/internal/data_lineage/_enrich_lineage_steps_with_ai/) (internal) |
| [`build_lineage_handover_markdown`](../../reference/build_lineage_handover_markdown/) | function | Create a concise markdown handover summary from lineage execution results. | — |
| [`build_lineage_records`](../../reference/build_lineage_records/) | function | Build compact lineage records for downstream metadata sinks. | — |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`plot_lineage_steps`](../../reference/plot_lineage_steps/) | function | Render lineage steps as a directed graph figure. | — |
| [`scan_notebook_cells`](../../reference/scan_notebook_cells/) | function | Scan multiple notebook cells and append cell references to lineage steps. | — |
| [`scan_notebook_lineage`](../../reference/scan_notebook_lineage/) | function | Extract deterministic lineage steps from notebook code using AST parsing. | [`_call_name`](../../reference/internal/data_lineage/_call_name/) (internal), [`_flatten_chain`](../../reference/internal/data_lineage/_flatten_chain/) (internal), [`_name`](../../reference/internal/data_lineage/_name/) (internal), [`_resolve_write_target`](../../reference/internal/data_lineage/_resolve_write_target/) (internal), [`_step`](../../reference/internal/data_lineage/_step/) (internal) |
| [`validate_lineage_steps`](../../reference/validate_lineage_steps/) | function | Validate lineage step structure and flag records requiring human review. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_build_lineage_record_from_steps`](../../reference/internal/data_lineage/_build_lineage_record_from_steps/) | — |
| [`_call_name`](../../reference/internal/data_lineage/_call_name/) | [`scan_notebook_lineage`](../../reference/scan_notebook_lineage/) |
| [`_enrich_lineage_steps_with_ai`](../../reference/internal/data_lineage/_enrich_lineage_steps_with_ai/) | [`build_lineage_from_notebook_code`](../../reference/build_lineage_from_notebook_code/) |
| [`_fallback_copilot_lineage_prompt`](../../reference/internal/data_lineage/_fallback_copilot_lineage_prompt/) | — |
| [`_flatten_chain`](../../reference/internal/data_lineage/_flatten_chain/) | [`scan_notebook_lineage`](../../reference/scan_notebook_lineage/) |
| [`_literal`](../../reference/internal/data_lineage/_literal/) | — |
| [`_name`](../../reference/internal/data_lineage/_name/) | [`scan_notebook_lineage`](../../reference/scan_notebook_lineage/) |
| [`_resolve_write_target`](../../reference/internal/data_lineage/_resolve_write_target/) | [`scan_notebook_lineage`](../../reference/scan_notebook_lineage/) |
| [`_step`](../../reference/internal/data_lineage/_step/) | [`scan_notebook_lineage`](../../reference/scan_notebook_lineage/) |
