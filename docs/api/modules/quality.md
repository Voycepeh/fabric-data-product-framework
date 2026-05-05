# `quality` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`load_data_contract`](../../reference/step-03-source-contract-ingestion/load_data_contract.md) | function | Load a data contract used by ingestion, quality, and metadata checks. | — |
| [`run_data_product`](../../reference/step-06-production-transformation-output/run_data_product.md) | function | Run the starter kit workflow end-to-end for a data product outcome. | [`_effective_contract_dict`](../../reference/internal/quality/_effective_contract_dict.md) (internal), [`_refresh_mode`](../../reference/internal/quality/_refresh_mode.md) (internal), [`_runtime_validation_contract`](../../reference/internal/quality/_runtime_validation_contract.md) (internal), [`_write_dataframe_to_table`](../../reference/internal/quality/_write_dataframe_to_table.md) (internal), [`_write_records_spark`](../../reference/internal/quality/_write_records_spark.md) (internal) |
| [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) | function | Run configured data quality rules against a DataFrame. | [`_normalize_severity`](../../reference/internal/quality/_normalize_severity.md) (internal), [`_now_iso`](../../reference/internal/quality/_now_iso.md) (internal), [`_pandas_rule`](../../reference/internal/quality/_pandas_rule.md) (internal), [`_resolve_engine`](../../reference/internal/quality/_resolve_engine.md) (internal), [`_result_from_counts`](../../reference/internal/quality/_result_from_counts.md) (internal), [`_spark_rule`](../../reference/internal/quality/_spark_rule.md) (internal), [`_to_jsonable`](../../reference/internal/quality/_to_jsonable.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_action_for`](../../reference/internal/quality/_action_for.md) | — |
| [`_add_pandas`](../../reference/internal/quality/_add_pandas.md) | — |
| [`_add_spark`](../../reference/internal/quality/_add_spark.md) | — |
| [`_build_rule_id`](../../reference/internal/quality/_build_rule_id.md) | — |
| [`_combine_contract_checks`](../../reference/internal/quality/_combine_contract_checks.md) | — |
| [`_dict`](../../reference/internal/quality/_dict.md) | — |
| [`_effective_contract_dict`](../../reference/internal/quality/_effective_contract_dict.md) | [`run_data_product`](../../reference/step-06-production-transformation-output/run_data_product.md) |
| [`_json_safe`](../../reference/internal/quality/_json_safe.md) | — |
| [`_jsonable`](../../reference/internal/quality/_jsonable.md) | — |
| [`_normalize_severity`](../../reference/internal/quality/_normalize_severity.md) | [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) |
| [`_now_iso`](../../reference/internal/quality/_now_iso.md) | [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) |
| [`_pandas_rule`](../../reference/internal/quality/_pandas_rule.md) | [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) |
| [`_parse_freshness_timedelta`](../../reference/internal/quality/_parse_freshness_timedelta.md) | — |
| [`_refresh_mode`](../../reference/internal/quality/_refresh_mode.md) | [`run_data_product`](../../reference/step-06-production-transformation-output/run_data_product.md) |
| [`_resolve_engine`](../../reference/internal/quality/_resolve_engine.md) | [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) |
| [`_result_from_counts`](../../reference/internal/quality/_result_from_counts.md) | [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) |
| [`_runtime_validation_contract`](../../reference/internal/quality/_runtime_validation_contract.md) | [`run_data_product`](../../reference/step-06-production-transformation-output/run_data_product.md) |
| [`_severity_bucket`](../../reference/internal/quality/_severity_bucket.md) | — |
| [`_skipped`](../../reference/internal/quality/_skipped.md) | — |
| [`_spark_rule`](../../reference/internal/quality/_spark_rule.md) | [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) |
| [`_strip_json_fences`](../../reference/internal/quality/_strip_json_fences.md) | — |
| [`_to_jsonable`](../../reference/internal/quality/_to_jsonable.md) | [`run_quality_rules`](../../reference/step-08-dq-rule-generation-review/run_quality_rules.md) |
| [`_write_dataframe_to_table`](../../reference/internal/quality/_write_dataframe_to_table.md) | [`run_data_product`](../../reference/step-06-production-transformation-output/run_data_product.md) |
| [`_write_records_spark`](../../reference/internal/quality/_write_records_spark.md) | [`run_data_product`](../../reference/step-06-production-transformation-output/run_data_product.md) |
