# `governance` module

## Module contents

- Public callables: 2
- Related internal helpers: 3
- Other internal objects: 6
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`_column_name`](#column-name) | Internal helper | Function | — | [`classify_columns`](#classify-columns) | [Jump](#column-name) |
| [`_match_terms`](#match-terms) | Internal | Function | — | — | [Jump](#match-terms) |
| [`_normalize_columns`](#normalize-columns) | Internal helper | Function | — | [`classify_columns`](#classify-columns) | [Jump](#normalize-columns) |
| [`_phrase_in_text`](#phrase-in-text) | Internal | Function | — | — | [Jump](#phrase-in-text) |
| [`_spark_create_governance_metadata_dataframe`](#spark-create-governance-metadata-dataframe) | Internal | Function | — | — | [Jump](#spark-create-governance-metadata-dataframe) |
| [`_tokenize_text`](#tokenize-text) | Internal | Function | — | — | [Jump](#tokenize-text) |
| [`build_governance_classification_records`](#build-governance-classification-records) | Internal | Function | Build governance classification records. | — | [Jump](#build-governance-classification-records) |
| [`classify_column`](#classify-column) | Internal helper | Function | Classify column. | [`classify_columns`](#classify-columns) | [Jump](#classify-column) |
| [`classify_columns`](#classify-columns) | Public | Function | Classify columns. | — | [Jump](#classify-columns) |
| [`summarize_governance_classifications`](#summarize-governance-classifications) | Public | Function | Summarize governance classifications. | — | [Jump](#summarize-governance-classifications) |
| [`write_governance_classifications`](#write-governance-classifications) | Internal | Function | Write governance classifications. | — | [Jump](#write-governance-classifications) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`classify_columns`](#classify-columns) | Function | Classify columns. | [`_column_name`](#column-name), [`_normalize_columns`](#normalize-columns), [`classify_column`](#classify-column) |
| [`summarize_governance_classifications`](#summarize-governance-classifications) | Function | Summarize governance classifications. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_column_name`](#column-name) | [`classify_columns`](#classify-columns) |
| [`_normalize_columns`](#normalize-columns) | [`classify_columns`](#classify-columns) |
| [`classify_column`](#classify-column) | [`classify_columns`](#classify-columns) |

## Full module API

::: fabric_data_product_framework.governance
