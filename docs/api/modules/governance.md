# `governance` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_classification_records`](#build_governance_classification_records) | function | Build governance classification records. | — |
| [`classify_column`](#classify_column) | function | Classify column. | [`_match_terms`](../../reference/internal/governance/_match_terms.md) (internal), [`_phrase_in_text`](../../reference/internal/governance/_phrase_in_text.md) (internal) |
| [`classify_columns`](#classify_columns) | function | Classify columns. | [`_column_name`](../../reference/internal/governance/_column_name.md) (internal), [`_normalize_columns`](../../reference/internal/governance/_normalize_columns.md) (internal) |
| [`summarize_governance_classifications`](#summarize_governance_classifications) | function | Summarize governance classifications. | — |
| [`write_governance_classifications`](#write_governance_classifications) | function | Write governance classifications. | [`_spark_create_governance_metadata_dataframe`](../../reference/internal/governance/_spark_create_governance_metadata_dataframe.md) (internal) |

## Public callable details

### build_governance_classification_records

::: fabric_data_product_framework.governance.build_governance_classification_records

### classify_column

::: fabric_data_product_framework.governance.classify_column

### classify_columns

::: fabric_data_product_framework.governance.classify_columns

### summarize_governance_classifications

::: fabric_data_product_framework.governance.summarize_governance_classifications

### write_governance_classifications

::: fabric_data_product_framework.governance.write_governance_classifications

??? note "Internal helpers (collapsed)"

    Internal helpers are documented separately for maintainers:

    - [`_column_name`](../../reference/internal/governance/_column_name.md) (used by: `classify_columns`)
    - [`_match_terms`](../../reference/internal/governance/_match_terms.md) (used by: `classify_column`)
    - [`_normalize_columns`](../../reference/internal/governance/_normalize_columns.md) (used by: `classify_columns`)
    - [`_phrase_in_text`](../../reference/internal/governance/_phrase_in_text.md) (used by: `classify_column`)
    - [`_spark_create_governance_metadata_dataframe`](../../reference/internal/governance/_spark_create_governance_metadata_dataframe.md) (used by: `write_governance_classifications`)
    - [`_tokenize_text`](../../reference/internal/governance/_tokenize_text.md)
