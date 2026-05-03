# `governance` module

Public callables: 5  
Related internal helpers: 5  
Other internal objects: 1  
Deprecated objects: 0

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [_column_name](#-column-name) | Internal helper | Function | — | `classify_columns` | [API](#-column-name) |
| [_match_terms](#-match-terms) | Internal helper | Function | — | `classify_column` | [API](#-match-terms) |
| [_normalize_columns](#-normalize-columns) | Internal helper | Function | — | `classify_columns` | [API](#-normalize-columns) |
| [_phrase_in_text](#-phrase-in-text) | Internal helper | Function | — | `classify_column` | [API](#-phrase-in-text) |
| [_spark_create_governance_metadata_dataframe](#-spark-create-governance-metadata-dataframe) | Internal helper | Function | — | `write_governance_classifications` | [API](#-spark-create-governance-metadata-dataframe) |
| [_tokenize_text](#-tokenize-text) | Internal | Function | — | — | [API](#-tokenize-text) |
| [build_governance_classification_records](#build-governance-classification-records) | Public | Function | Build governance classification records. | `write_governance_classifications` | [API](#build-governance-classification-records) |
| [classify_column](#classify-column) | Public | Function | Classify column. | `classify_columns` | [API](#classify-column) |
| [classify_columns](#classify-columns) | Public | Function | Classify columns. | — | [API](#classify-columns) |
| [summarize_governance_classifications](#summarize-governance-classifications) | Public | Function | Summarize governance classifications. | — | [API](#summarize-governance-classifications) |
| [write_governance_classifications](#write-governance-classifications) | Public | Function | Write governance classifications. | — | [API](#write-governance-classifications) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `build_governance_classification_records` | Function | Build governance classification records. | — |
| `classify_column` | Function | Classify column. | `_match_terms` (internal), `_phrase_in_text` (internal) |
| `classify_columns` | Function | Classify columns. | `_column_name` (internal), `_normalize_columns` (internal) |
| `summarize_governance_classifications` | Function | Summarize governance classifications. | — |
| `write_governance_classifications` | Function | Write governance classifications. | `_spark_create_governance_metadata_dataframe` (internal) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `_column_name` | `classify_columns` |
| `_match_terms` | `classify_column` |
| `_normalize_columns` | `classify_columns` |
| `_phrase_in_text` | `classify_column` |
| `_spark_create_governance_metadata_dataframe` | `write_governance_classifications` |

## Full module API

::: fabric_data_product_framework.governance
