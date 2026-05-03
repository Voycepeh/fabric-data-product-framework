# `governance` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_classification_records`](#build_governance_classification_records) | function | Build governance classification records. | — |
| [`classify_column`](#classify_column) | function | Classify column. | `_match_terms` (internal), `_phrase_in_text` (internal) |
| [`classify_columns`](#classify_columns) | function | Classify columns. | `_column_name` (internal), `_normalize_columns` (internal) |
| [`summarize_governance_classifications`](#summarize_governance_classifications) | function | Summarize governance classifications. | — |
| [`write_governance_classifications`](#write_governance_classifications) | function | Write governance classifications. | `_spark_create_governance_metadata_dataframe` (internal) |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_column_name` | `classify_columns` |
| `_match_terms` | `classify_column` |
| `_normalize_columns` | `classify_columns` |
| `_phrase_in_text` | `classify_column` |
| `_spark_create_governance_metadata_dataframe` | `write_governance_classifications` |
| `_tokenize_text` | — |

## Full module API

::: fabric_data_product_framework.governance
