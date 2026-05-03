# `quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_quality_result_records`](#build_quality_result_records) | function | Build quality result records. | [`_to_jsonable`](../../reference/internal/quality/_to_jsonable.md) (internal) |
| [`load_data_contract`](#load_data_contract) | function | Load data contract. | — |
| [`run_data_product`](#run_data_product) | function | Run data product. | [`_effective_contract_dict`](../../reference/internal/quality/_effective_contract_dict.md) (internal), [`_refresh_mode`](../../reference/internal/quality/_refresh_mode.md) (internal), [`_runtime_validation_contract`](../../reference/internal/quality/_runtime_validation_contract.md) (internal), [`_write_dataframe_to_table`](../../reference/internal/quality/_write_dataframe_to_table.md) (internal), [`_write_records_spark`](../../reference/internal/quality/_write_records_spark.md) (internal) |
| [`run_quality_rules`](#run_quality_rules) | function | Run quality rules. | [`_normalize_severity`](../../reference/internal/quality/_normalize_severity.md) (internal), [`_now_iso`](../../reference/internal/quality/_now_iso.md) (internal), [`_pandas_rule`](../../reference/internal/quality/_pandas_rule.md) (internal), [`_resolve_engine`](../../reference/internal/quality/_resolve_engine.md) (internal), [`_result_from_counts`](../../reference/internal/quality/_result_from_counts.md) (internal), [`_spark_rule`](../../reference/internal/quality/_spark_rule.md) (internal), [`_to_jsonable`](../../reference/internal/quality/_to_jsonable.md) (internal) |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| [`_action_for`](../../reference/internal/quality/_action_for.md) | — |
| [`_add_pandas`](../../reference/internal/quality/_add_pandas.md) | — |
| [`_add_spark`](../../reference/internal/quality/_add_spark.md) | — |
| [`_build_rule_id`](../../reference/internal/quality/_build_rule_id.md) | — |
| [`_combine_contract_checks`](../../reference/internal/quality/_combine_contract_checks.md) | — |
| [`_dict`](../../reference/internal/quality/_dict.md) | — |
| [`_effective_contract_dict`](../../reference/internal/quality/_effective_contract_dict.md) | `run_data_product` |
| [`_extract_fabric_ai_response_payload`](../../reference/internal/quality/_extract_fabric_ai_response_payload.md) | — |
| [`_fabric_ai_dependencies_available`](../../reference/internal/quality/_fabric_ai_dependencies_available.md) | — |
| [`_json_safe`](../../reference/internal/quality/_json_safe.md) | — |
| [`_jsonable`](../../reference/internal/quality/_jsonable.md) | — |
| [`_normalize_severity`](../../reference/internal/quality/_normalize_severity.md) | `run_quality_rules` |
| [`_now_iso`](../../reference/internal/quality/_now_iso.md) | `run_quality_rules` |
| [`_pandas_rule`](../../reference/internal/quality/_pandas_rule.md) | `run_quality_rules` |
| [`_parse_freshness_timedelta`](../../reference/internal/quality/_parse_freshness_timedelta.md) | — |
| [`_refresh_mode`](../../reference/internal/quality/_refresh_mode.md) | `run_data_product` |
| [`_resolve_engine`](../../reference/internal/quality/_resolve_engine.md) | `run_quality_rules` |
| [`_result_from_counts`](../../reference/internal/quality/_result_from_counts.md) | `run_quality_rules` |
| [`_runtime_validation_contract`](../../reference/internal/quality/_runtime_validation_contract.md) | `run_data_product` |
| [`_severity_bucket`](../../reference/internal/quality/_severity_bucket.md) | — |
| [`_skipped`](../../reference/internal/quality/_skipped.md) | — |
| [`_spark_rule`](../../reference/internal/quality/_spark_rule.md) | `run_quality_rules` |
| [`_strip_json_fences`](../../reference/internal/quality/_strip_json_fences.md) | — |
| [`_to_jsonable`](../../reference/internal/quality/_to_jsonable.md) | `build_quality_result_records`, `run_quality_rules` |
| [`_write_dataframe_to_table`](../../reference/internal/quality/_write_dataframe_to_table.md) | `run_data_product` |
| [`_write_records_spark`](../../reference/internal/quality/_write_records_spark.md) | `run_data_product` |

## Full module API

::: fabric_data_product_framework.quality
