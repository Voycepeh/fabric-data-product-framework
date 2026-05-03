# `lineage` module

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `build_lineage_from_notebook_code` | function | — | — |
| `build_lineage_handover_markdown` | function | — | — |
| `build_lineage_record_from_steps` | function | — | — |
| `build_lineage_records` | function | — | — |
| `enrich_lineage_steps_with_ai` | function | — | — |
| `fallback_copilot_lineage_prompt` | function | — | — |
| `plot_lineage_steps` | function | — | — |
| `scan_notebook_cells` | function | — | — |
| `scan_notebook_lineage` | function | — | `_call_name` (internal), `_flatten_chain` (internal), `_name` (internal), `_resolve_write_target` (internal), `_step` (internal) |
| `validate_lineage_steps` | function | — | — |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_call_name` | `scan_notebook_lineage` |
| `_flatten_chain` | `scan_notebook_lineage` |
| `_literal` | — |
| `_name` | `scan_notebook_lineage` |
| `_resolve_write_target` | `scan_notebook_lineage` |
| `_step` | `scan_notebook_lineage` |

## Full module API

::: fabric_data_product_framework.lineage
