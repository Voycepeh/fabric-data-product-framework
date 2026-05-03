# `quality` module

!!! info "Module overview"
    This page summarizes public callables and related internal helpers.

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_quality_result_records`](#build_quality_result_records) | function | Build quality result records. | `_to_jsonable` (internal) |
| [`load_data_contract`](#load_data_contract) | function | Load data contract. | — |
| [`run_data_product`](#run_data_product) | function | Run data product. | `_effective_contract_dict` (internal), `_refresh_mode` (internal), `_runtime_validation_contract` (internal), `_write_dataframe_to_table` (internal), `_write_records_spark` (internal) |
| [`run_quality_rules`](#run_quality_rules) | function | Run quality rules. | `_normalize_severity` (internal), `_now_iso` (internal), `_pandas_rule` (internal), `_resolve_engine` (internal), `_result_from_counts` (internal), `_spark_rule` (internal), `_to_jsonable` (internal) |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_action_for` | — |
| `_add_pandas` | — |
| `_add_spark` | — |
| `_build_rule_id` | — |
| `_combine_contract_checks` | — |
| `_dict` | — |
| `_effective_contract_dict` | `run_data_product` |
| `_extract_fabric_ai_response_payload` | — |
| `_fabric_ai_dependencies_available` | — |
| `_json_safe` | — |
| `_jsonable` | — |
| `_normalize_severity` | `run_quality_rules` |
| `_now_iso` | `run_quality_rules` |
| `_pandas_rule` | `run_quality_rules` |
| `_parse_freshness_timedelta` | — |
| `_refresh_mode` | `run_data_product` |
| `_resolve_engine` | `run_quality_rules` |
| `_result_from_counts` | `run_quality_rules` |
| `_runtime_validation_contract` | `run_data_product` |
| `_severity_bucket` | — |
| `_skipped` | — |
| `_spark_rule` | `run_quality_rules` |
| `_strip_json_fences` | — |
| `_to_jsonable` | `build_quality_result_records`, `run_quality_rules` |
| `_write_dataframe_to_table` | `run_data_product` |
| `_write_records_spark` | `run_data_product` |

## Full module API

::: fabric_data_product_framework.quality
