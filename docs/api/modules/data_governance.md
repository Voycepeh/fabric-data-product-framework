# `data_governance` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_candidate_prompt`](../../reference/step-09-ai-assisted-classification/build_governance_candidate_prompt.md) | function | Build the governance-candidate prompt for AI-assisted classification drafts. | — |
| [`build_governance_classification_records`](../../reference/step-09-ai-assisted-classification/build_governance_classification_records.md) | function | Build metadata-ready governance classification records from column suggestions. | — |
| [`build_manual_governance_prompt_package`](../../reference/step-09-ai-assisted-classification/build_manual_governance_prompt_package.md) | function | Build copy/paste prompt package for manual governance suggestion generation. | — |
| [`classify_column`](../../reference/step-09-ai-assisted-classification/classify_column.md) | function | Classify one column using term matching, metadata cues, and business context. | [`_match_terms`](../../reference/internal/data_governance/_match_terms.md) (internal), [`_phrase_in_text`](../../reference/internal/data_governance/_phrase_in_text.md) (internal) |
| [`classify_columns`](../../reference/step-09-ai-assisted-classification/classify_columns.md) | function | Classify multiple columns and return normalized governance suggestions. | [`_column_name`](../../reference/internal/data_governance/_column_name.md) (internal), [`_normalize_columns`](../../reference/internal/data_governance/_normalize_columns.md) (internal) |
| [`generate_governance_candidates_with_fabric_ai`](../../reference/step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai.md) | function | Execute Fabric AI Functions to append governance suggestions to a DataFrame. | — |
| [`summarize_governance_classifications`](../../reference/step-09-ai-assisted-classification/summarize_governance_classifications.md) | function | Summarize governance classification outputs into review-friendly counts. | — |
| [`write_governance_classifications`](../../reference/step-09-ai-assisted-classification/write_governance_classifications.md) | function | Persist governance classifications to a metadata destination. | [`_spark_create_governance_metadata_dataframe`](../../reference/internal/data_governance/_spark_create_governance_metadata_dataframe.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_column_name`](../../reference/internal/data_governance/_column_name.md) | [`classify_columns`](../../reference/step-09-ai-assisted-classification/classify_columns.md) |
| [`_match_terms`](../../reference/internal/data_governance/_match_terms.md) | [`classify_column`](../../reference/step-09-ai-assisted-classification/classify_column.md) |
| [`_normalize_columns`](../../reference/internal/data_governance/_normalize_columns.md) | [`classify_columns`](../../reference/step-09-ai-assisted-classification/classify_columns.md) |
| [`_phrase_in_text`](../../reference/internal/data_governance/_phrase_in_text.md) | [`classify_column`](../../reference/step-09-ai-assisted-classification/classify_column.md) |
| [`_spark_create_governance_metadata_dataframe`](../../reference/internal/data_governance/_spark_create_governance_metadata_dataframe.md) | [`write_governance_classifications`](../../reference/step-09-ai-assisted-classification/write_governance_classifications.md) |
| [`_tokenize_text`](../../reference/internal/data_governance/_tokenize_text.md) | — |
