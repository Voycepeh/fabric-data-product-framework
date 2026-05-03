# `lineage` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_lineage_from_notebook_code`](#build_lineage_from_notebook_code) | function | Scan, optionally enrich, and validate lineage from notebook source code. | — |
| [`build_lineage_handover_markdown`](#build_lineage_handover_markdown) | function | Create a concise markdown handover summary from lineage execution results. | — |
| [`build_lineage_record_from_steps`](#build_lineage_record_from_steps) | function | Create metadata-ready lineage records from validated lineage steps. | — |
| [`build_lineage_records`](#build_lineage_records) | function | Build compact lineage records for downstream metadata sinks. | — |
| [`enrich_lineage_steps_with_ai`](#enrich_lineage_steps_with_ai) | function | Optionally enrich deterministic lineage steps using an AI helper callable. | — |
| [`fallback_copilot_lineage_prompt`](#fallback_copilot_lineage_prompt) | function | Build a fallback Copilot prompt for manual lineage enrichment. | — |
| [`plot_lineage_steps`](#plot_lineage_steps) | function | Render lineage steps as a directed graph figure. | — |
| [`scan_notebook_cells`](#scan_notebook_cells) | function | Scan multiple notebook cells and append cell references to lineage steps. | — |
| [`scan_notebook_lineage`](#scan_notebook_lineage) | function | Extract deterministic lineage steps from notebook code using AST parsing. | [`_call_name`](../reference/internal/lineage/_call_name.md) (internal), [`_flatten_chain`](../reference/internal/lineage/_flatten_chain.md) (internal), [`_name`](../reference/internal/lineage/_name.md) (internal), [`_resolve_write_target`](../reference/internal/lineage/_resolve_write_target.md) (internal), [`_step`](../reference/internal/lineage/_step.md) (internal) |
| [`validate_lineage_steps`](#validate_lineage_steps) | function | Validate lineage step structure and flag records requiring human review. | — |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| [`_call_name`](../reference/internal/lineage/_call_name.md) | `scan_notebook_lineage` |
| [`_flatten_chain`](../reference/internal/lineage/_flatten_chain.md) | `scan_notebook_lineage` |
| [`_literal`](../reference/internal/lineage/_literal.md) | — |
| [`_name`](../reference/internal/lineage/_name.md) | `scan_notebook_lineage` |
| [`_resolve_write_target`](../reference/internal/lineage/_resolve_write_target.md) | `scan_notebook_lineage` |
| [`_step`](../reference/internal/lineage/_step.md) | `scan_notebook_lineage` |

## Full module API

::: fabric_data_product_framework.lineage
