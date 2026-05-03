# `lineage` module

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `build_lineage_records` | function | Build lineage records. | `_clean_list` (internal) |
| `build_transformation_summary_markdown` | function | Build transformation summary markdown. | — |
| `generate_mermaid_lineage` | function | Generate mermaid lineage. | `_safe_node_id` (internal) |
| `LineageRecorder` | class | Lineagerecorder. | — |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_clean_list` | `build_lineage_records` |
| `_jsonable` | — |
| `_safe_node_id` | `generate_mermaid_lineage` |
| `_strip_fences` | — |
| `_unique` | — |

## Full module API

::: fabric_data_product_framework.lineage
