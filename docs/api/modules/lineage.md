# `lineage` module

Public callables: 4  
Related internal helpers: 2  
Other internal objects: 17  
Deprecated objects: 0

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [LineageRecorder](#lineagerecorder) | Public | Class | Lineagerecorder. | — | [API](#lineagerecorder) |
| [TransformationStep](#transformationstep) | Internal | Dataclass | Transformationstep. | — | [API](#transformationstep) |
| [_clean_list](#-clean-list) | Internal helper | Function | Normalize optional string lists by dropping blank values. | `build_lineage_records` | [API](#-clean-list) |
| [_jsonable](#-jsonable) | Internal | Function | — | — | [API](#-jsonable) |
| [_safe_node_id](#-safe-node-id) | Internal helper | Function | Create Mermaid/graph-safe node identifiers from free-text names. | `generate_mermaid_lineage` | [API](#-safe-node-id) |
| [_strip_fences](#-strip-fences) | Internal | Function | — | — | [API](#-strip-fences) |
| [_unique](#-unique) | Internal | Function | — | — | [API](#-unique) |
| [build_lineage_prompt_context](#build-lineage-prompt-context) | Internal | Function | Build lineage prompt context. | — | [API](#build-lineage-prompt-context) |
| [build_lineage_record](#build-lineage-record) | Internal | Function | Build lineage record. | — | [API](#build-lineage-record) |
| [build_lineage_record_from_steps](#build-lineage-record-from-steps) | Internal | Function | Build lineage record from steps. | — | [API](#build-lineage-record-from-steps) |
| [build_lineage_records](#build-lineage-records) | Public | Function | Build lineage records. | — | [API](#build-lineage-records) |
| [build_transformation_summary_generation_prompt](#build-transformation-summary-generation-prompt) | Internal | Function | Build the instruction prompt string for AI transformation summaries. | — | [API](#build-transformation-summary-generation-prompt) |
| [build_transformation_summary_markdown](#build-transformation-summary-markdown) | Public | Function | Build transformation summary markdown. | — | [API](#build-transformation-summary-markdown) |
| [build_transformation_summary_prompt_context](#build-transformation-summary-prompt-context) | Internal | Function | Build the AI prompt context payload for transformation summaries. | — | [API](#build-transformation-summary-prompt-context) |
| [build_transformation_summary_records](#build-transformation-summary-records) | Internal | Function | Build transformation summary records. | — | [API](#build-transformation-summary-records) |
| [generate_mermaid_lineage](#generate-mermaid-lineage) | Public | Function | Generate mermaid lineage. | `build_transformation_summary_markdown` | [API](#generate-mermaid-lineage) |
| [get_fabric_copilot_lineage_prompt](#get-fabric-copilot-lineage-prompt) | Internal | Function | Get fabric copilot lineage prompt. | — | [API](#get-fabric-copilot-lineage-prompt) |
| [normalize_transformation_summary_candidate](#normalize-transformation-summary-candidate) | Internal | Function | Normalize one AI-generated transformation summary object. | — | [API](#normalize-transformation-summary-candidate) |
| [parse_ai_transformation_summaries](#parse-ai-transformation-summaries) | Internal | Function | Parse and validate AI output for transformation summaries. | — | [API](#parse-ai-transformation-summaries) |
| [plot_lineage_networkx](#plot-lineage-networkx) | Internal | Function | Plot lineage networkx. | — | [API](#plot-lineage-networkx) |
| [transformation_reasons](#transformation-reasons) | Internal | Function | Transformation reasons. | — | [API](#transformation-reasons) |
| [transformation_summary](#transformation-summary) | Internal | Function | Transformation summary. | — | [API](#transformation-summary) |
| [validate_lineage_steps](#validate-lineage-steps) | Internal | Function | Validate lineage steps. | — | [API](#validate-lineage-steps) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `build_lineage_records` | Function | Build lineage records. | `_clean_list` (internal) |
| `build_transformation_summary_markdown` | Function | Build transformation summary markdown. | — |
| `generate_mermaid_lineage` | Function | Generate mermaid lineage. | `_safe_node_id` (internal) |
| `LineageRecorder` | Class | Lineagerecorder. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `_clean_list` | `build_lineage_records` |
| `_safe_node_id` | `generate_mermaid_lineage` |

## Full module API

::: fabric_data_product_framework.lineage
