# `governance` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_classification_records`](../../reference/step-09-classification-sensitivity/build_governance_classification_records.md) | function | Execute the `build_governance_classification_records` workflow step in FabricOps. | — |
| [`classify_column`](../../reference/step-09-classification-sensitivity/classify_column.md) | function | Execute the `classify_column` workflow step in FabricOps. | [`_match_terms`](../../reference/internal/governance/_match_terms.md) (internal), [`_phrase_in_text`](../../reference/internal/governance/_phrase_in_text.md) (internal) |
| [`classify_columns`](../../reference/step-09-classification-sensitivity/classify_columns.md) | function | Execute the `classify_columns` workflow step in FabricOps. | [`_column_name`](../../reference/internal/governance/_column_name.md) (internal), [`_normalize_columns`](../../reference/internal/governance/_normalize_columns.md) (internal) |
| [`summarize_governance_classifications`](../../reference/step-09-classification-sensitivity/summarize_governance_classifications.md) | function | Execute the `summarize_governance_classifications` workflow step in FabricOps. | — |
| [`write_governance_classifications`](../../reference/step-09-classification-sensitivity/write_governance_classifications.md) | function | Execute the `write_governance_classifications` workflow step in FabricOps. | [`_spark_create_governance_metadata_dataframe`](../../reference/internal/governance/_spark_create_governance_metadata_dataframe.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_column_name`](../../reference/internal/governance/_column_name.md) | [`classify_columns`](../../reference/step-09-classification-sensitivity/classify_columns.md) |
| [`_match_terms`](../../reference/internal/governance/_match_terms.md) | [`classify_column`](../../reference/step-09-classification-sensitivity/classify_column.md) |
| [`_normalize_columns`](../../reference/internal/governance/_normalize_columns.md) | [`classify_columns`](../../reference/step-09-classification-sensitivity/classify_columns.md) |
| [`_phrase_in_text`](../../reference/internal/governance/_phrase_in_text.md) | [`classify_column`](../../reference/step-09-classification-sensitivity/classify_column.md) |
| [`_spark_create_governance_metadata_dataframe`](../../reference/internal/governance/_spark_create_governance_metadata_dataframe.md) | [`write_governance_classifications`](../../reference/step-09-classification-sensitivity/write_governance_classifications.md) |
| [`_tokenize_text`](../../reference/internal/governance/_tokenize_text.md) | — |
