# `lineage` module

## Module contents

- Public callables: 4
- Related internal helpers: 2
- Other internal objects: 17
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`_clean_list`](#clean-list) | Internal helper | Function | Normalize optional string lists by dropping blank values. | [`build_lineage_records`](#build-lineage-records) | [Jump](#clean-list) |
| [`_jsonable`](#jsonable) | Internal | Function | — | — | [Jump](#jsonable) |
| [`_safe_node_id`](#safe-node-id) | Internal helper | Function | Create Mermaid/graph-safe node identifiers from free-text names. | [`generate_mermaid_lineage`](#generate-mermaid-lineage) | [Jump](#safe-node-id) |
| [`_strip_fences`](#strip-fences) | Internal | Function | — | — | [Jump](#strip-fences) |
| [`_unique`](#unique) | Internal | Function | — | — | [Jump](#unique) |
| [`build_lineage_prompt_context`](#build-lineage-prompt-context) | Internal | Function | Build lineage prompt context. | — | [Jump](#build-lineage-prompt-context) |
| [`build_lineage_record`](#build-lineage-record) | Internal | Function | Build lineage record. | — | [Jump](#build-lineage-record) |
| [`build_lineage_record_from_steps`](#build-lineage-record-from-steps) | Internal | Function | Build lineage record from steps. | — | [Jump](#build-lineage-record-from-steps) |
| [`build_lineage_records`](#build-lineage-records) | Public | Function | Build lineage records. | — | [Jump](#build-lineage-records) |
| [`build_transformation_summary_generation_prompt`](#build-transformation-summary-generation-prompt) | Internal | Function | Build the instruction prompt string for AI transformation summaries. | — | [Jump](#build-transformation-summary-generation-prompt) |
| [`build_transformation_summary_markdown`](#build-transformation-summary-markdown) | Public | Function | Build transformation summary markdown. | — | [Jump](#build-transformation-summary-markdown) |
| [`build_transformation_summary_prompt_context`](#build-transformation-summary-prompt-context) | Internal | Function | Build the AI prompt context payload for transformation summaries. | — | [Jump](#build-transformation-summary-prompt-context) |
| [`build_transformation_summary_records`](#build-transformation-summary-records) | Internal | Function | Build transformation summary records. | — | [Jump](#build-transformation-summary-records) |
| [`generate_mermaid_lineage`](#generate-mermaid-lineage) | Public | Function | Generate mermaid lineage. | [`build_transformation_summary_markdown`](#build-transformation-summary-markdown) | [Jump](#generate-mermaid-lineage) |
| [`get_fabric_copilot_lineage_prompt`](#get-fabric-copilot-lineage-prompt) | Internal | Function | Get fabric copilot lineage prompt. | — | [Jump](#get-fabric-copilot-lineage-prompt) |
| [`LineageRecorder`](#lineagerecorder) | Public | Class | Lineagerecorder. | — | [Jump](#lineagerecorder) |
| [`normalize_transformation_summary_candidate`](#normalize-transformation-summary-candidate) | Internal | Function | Normalize one AI-generated transformation summary object. | — | [Jump](#normalize-transformation-summary-candidate) |
| [`parse_ai_transformation_summaries`](#parse-ai-transformation-summaries) | Internal | Function | Parse and validate AI output for transformation summaries. | — | [Jump](#parse-ai-transformation-summaries) |
| [`plot_lineage_networkx`](#plot-lineage-networkx) | Internal | Function | Plot lineage networkx. | — | [Jump](#plot-lineage-networkx) |
| [`transformation_reasons`](#transformation-reasons) | Internal | Function | Transformation reasons. | — | [Jump](#transformation-reasons) |
| [`transformation_summary`](#transformation-summary) | Internal | Function | Transformation summary. | — | [Jump](#transformation-summary) |
| [`TransformationStep`](#transformationstep) | Internal | Dataclass | Transformationstep. | — | [Jump](#transformationstep) |
| [`validate_lineage_steps`](#validate-lineage-steps) | Internal | Function | Validate lineage steps. | — | [Jump](#validate-lineage-steps) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_lineage_records`](#build-lineage-records) | Function | Build lineage records. | [`_clean_list`](#clean-list) |
| [`build_transformation_summary_markdown`](#build-transformation-summary-markdown) | Function | Build transformation summary markdown. | — |
| [`generate_mermaid_lineage`](#generate-mermaid-lineage) | Function | Generate mermaid lineage. | [`_safe_node_id`](#safe-node-id) |
| [`LineageRecorder`](#lineagerecorder) | Class | Lineagerecorder. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_clean_list`](#clean-list) | [`build_lineage_records`](#build-lineage-records) |
| [`_safe_node_id`](#safe-node-id) | [`generate_mermaid_lineage`](#generate-mermaid-lineage) |

## Full module API

::: fabric_data_product_framework.lineage
