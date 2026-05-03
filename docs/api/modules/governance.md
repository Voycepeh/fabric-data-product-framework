# `governance` module

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `classify_columns` | function | Classify columns. | `_column_name` (internal), `_normalize_columns` (internal) |
| `summarize_governance_classifications` | function | Summarize governance classifications. | — |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_column_name` | `classify_columns` |
| `_match_terms` | — |
| `_normalize_columns` | `classify_columns` |
| `_phrase_in_text` | — |
| `_spark_create_governance_metadata_dataframe` | — |
| `_tokenize_text` | — |

## Full module API

::: fabric_data_product_framework.governance
