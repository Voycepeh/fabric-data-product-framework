# `quality` module

## Module contents

- Public callables: 3
- Related internal helpers: 20
- Other internal objects: 60
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`_action_for`](#action-for) | Internal | Function | — | — | [Jump](#action-for) |
| [`_add_pandas`](#add-pandas) | Internal | Function | — | — | [Jump](#add-pandas) |
| [`_add_spark`](#add-spark) | Internal | Function | — | — | [Jump](#add-spark) |
| [`_build_rule_id`](#build-rule-id) | Internal | Function | — | — | [Jump](#build-rule-id) |
| [`_combine_contract_checks`](#combine-contract-checks) | Internal | Function | — | — | [Jump](#combine-contract-checks) |
| [`_dict`](#dict) | Internal | Function | Return a dictionary or an empty default for optional config fragments. | — | [Jump](#dict) |
| [`_effective_contract_dict`](#effective-contract-dict) | Internal helper | Function | — | [`run_data_product`](#run-data-product) | [Jump](#effective-contract-dict) |
| [`_extract_fabric_ai_response_payload`](#extract-fabric-ai-response-payload) | Internal | Function | — | — | [Jump](#extract-fabric-ai-response-payload) |
| [`_fabric_ai_dependencies_available`](#fabric-ai-dependencies-available) | Internal | Function | — | — | [Jump](#fabric-ai-dependencies-available) |
| [`_json_safe`](#json-safe) | Internal | Function | — | — | [Jump](#json-safe) |
| [`_jsonable`](#jsonable) | Internal | Function | — | — | [Jump](#jsonable) |
| [`_normalize_severity`](#normalize-severity) | Internal helper | Function | — | [`run_quality_rules`](#run-quality-rules) | [Jump](#normalize-severity) |
| [`_now_iso`](#now-iso) | Internal helper | Function | — | [`run_quality_rules`](#run-quality-rules) | [Jump](#now-iso) |
| [`_pandas_rule`](#pandas-rule) | Internal helper | Function | — | [`run_quality_rules`](#run-quality-rules) | [Jump](#pandas-rule) |
| [`_parse_freshness_timedelta`](#parse-freshness-timedelta) | Internal | Function | — | — | [Jump](#parse-freshness-timedelta) |
| [`_refresh_mode`](#refresh-mode) | Internal helper | Function | — | [`run_data_product`](#run-data-product) | [Jump](#refresh-mode) |
| [`_resolve_engine`](#resolve-engine) | Internal helper | Function | — | [`run_quality_rules`](#run-quality-rules) | [Jump](#resolve-engine) |
| [`_result_from_counts`](#result-from-counts) | Internal helper | Function | — | [`run_quality_rules`](#run-quality-rules) | [Jump](#result-from-counts) |
| [`_runtime_validation_contract`](#runtime-validation-contract) | Internal helper | Function | — | [`run_data_product`](#run-data-product) | [Jump](#runtime-validation-contract) |
| [`_severity_bucket`](#severity-bucket) | Internal | Function | — | — | [Jump](#severity-bucket) |
| [`_skipped`](#skipped) | Internal | Function | — | — | [Jump](#skipped) |
| [`_spark_rule`](#spark-rule) | Internal helper | Function | — | [`run_quality_rules`](#run-quality-rules) | [Jump](#spark-rule) |
| [`_strip_json_fences`](#strip-json-fences) | Internal | Function | — | — | [Jump](#strip-json-fences) |
| [`_to_jsonable`](#to-jsonable) | Internal helper | Function | — | [`run_quality_rules`](#run-quality-rules) | [Jump](#to-jsonable) |
| [`_write_dataframe_to_table`](#write-dataframe-to-table) | Internal helper | Function | — | [`run_data_product`](#run-data-product) | [Jump](#write-dataframe-to-table) |
| [`_write_records_spark`](#write-records-spark) | Internal helper | Function | — | [`run_data_product`](#run-data-product) | [Jump](#write-records-spark) |
| [`add_dq_failure_columns`](#add-dq-failure-columns) | Internal | Function | Add dq failure columns. | — | [Jump](#add-dq-failure-columns) |
| [`assert_contracts_valid`](#assert-contracts-valid) | Internal | Function | Assert contracts valid. | — | [Jump](#assert-contracts-valid) |
| [`assert_data_product_passed`](#assert-data-product-passed) | Internal | Function | Assert data product passed. | — | [Jump](#assert-data-product-passed) |
| [`assert_quality_gate`](#assert-quality-gate) | Internal | Function | Assert quality gate. | — | [Jump](#assert-quality-gate) |
| [`build_contract_validation_records`](#build-contract-validation-records) | Internal helper | Function | Build contract validation records. | [`run_data_product`](#run-data-product) | [Jump](#build-contract-validation-records) |
| [`build_dq_rule_records`](#build-dq-rule-records) | Internal | Function | Build dq rule records. | — | [Jump](#build-dq-rule-records) |
| [`build_drift_contract`](#build-drift-contract) | Internal | Function | Build drift contract. | — | [Jump](#build-drift-contract) |
| [`build_governance_contract`](#build-governance-contract) | Internal | Function | Build governance contract. | — | [Jump](#build-governance-contract) |
| [`build_layman_rule_records`](#build-layman-rule-records) | Internal | Function | Build layman rule records. | — | [Jump](#build-layman-rule-records) |
| [`build_metadata_contract`](#build-metadata-contract) | Internal | Function | Build metadata contract. | — | [Jump](#build-metadata-contract) |
| [`build_quality_contract`](#build-quality-contract) | Internal | Function | Build quality contract. | — | [Jump](#build-quality-contract) |
| [`build_quality_result_records`](#build-quality-result-records) | Internal helper | Function | Build quality result records. | [`run_data_product`](#run-data-product) | [Jump](#build-quality-result-records) |
| [`build_quality_rule_generation_prompt`](#build-quality-rule-generation-prompt) | Internal | Function | Build quality rule generation prompt. | — | [Jump](#build-quality-rule-generation-prompt) |
| [`build_quality_rule_prompt_context`](#build-quality-rule-prompt-context) | Internal | Function | Build quality rule prompt context. | — | [Jump](#build-quality-rule-prompt-context) |
| [`build_quarantine_rule_coverage_records`](#build-quarantine-rule-coverage-records) | Internal | Function | Build quarantine rule coverage records. | — | [Jump](#build-quarantine-rule-coverage-records) |
| [`build_quarantine_summary_records`](#build-quarantine-summary-records) | Internal | Function | Build quarantine summary records. | — | [Jump](#build-quarantine-summary-records) |
| [`build_rule_registry_records`](#build-rule-registry-records) | Internal | Function | Build rule registry records. | — | [Jump](#build-rule-registry-records) |
| [`build_runtime_context_from_contract`](#build-runtime-context-from-contract) | Internal helper | Function | Build runtime context from contract. | [`run_data_product`](#run-data-product) | [Jump](#build-runtime-context-from-contract) |
| [`build_runtime_contract`](#build-runtime-contract) | Internal | Function | Build runtime contract. | — | [Jump](#build-runtime-contract) |
| [`build_source_contract`](#build-source-contract) | Internal | Function | Build source contract. | — | [Jump](#build-source-contract) |
| [`build_target_contract`](#build-target-contract) | Internal | Function | Build target contract. | — | [Jump](#build-target-contract) |
| [`compile_layman_rule_to_quality_rule`](#compile-layman-rule-to-quality-rule) | Internal | Function | Compile layman rule to quality rule. | — | [Jump](#compile-layman-rule-to-quality-rule) |
| [`compile_layman_rules_to_quality_rules`](#compile-layman-rules-to-quality-rules) | Internal | Function | Compile layman rules to quality rules. | — | [Jump](#compile-layman-rules-to-quality-rules) |
| [`ContractValidationError`](#contractvalidationerror) | Internal | Class | Contractvalidationerror. | — | [Jump](#contractvalidationerror) |
| [`data_product_contract_to_dict`](#data-product-contract-to-dict) | Internal | Function | Data product contract to dict. | — | [Jump](#data-product-contract-to-dict) |
| [`DataProductContract`](#dataproductcontract) | Internal | Dataclass | Dataproductcontract. | — | [Jump](#dataproductcontract) |
| [`DataQualityError`](#dataqualityerror) | Internal | Class | Dataqualityerror. | — | [Jump](#dataqualityerror) |
| [`DriftContract`](#driftcontract) | Internal | Dataclass | Driftcontract. | — | [Jump](#driftcontract) |
| [`generate_dq_rule_candidates`](#generate-dq-rule-candidates) | Internal | Function | Generate dq rule candidates. | — | [Jump](#generate-dq-rule-candidates) |
| [`generate_dq_rule_candidates_with_fabric_ai`](#generate-dq-rule-candidates-with-fabric-ai) | Internal | Function | Generate dq rule candidates with fabric ai. | — | [Jump](#generate-dq-rule-candidates-with-fabric-ai) |
| [`GovernanceContract`](#governancecontract) | Internal | Dataclass | Governancecontract. | — | [Jump](#governancecontract) |
| [`load_data_contract`](#load-data-contract) | Public | Function | Load data contract. | — | [Jump](#load-data-contract) |
| [`load_dq_rules`](#load-dq-rules) | Internal | Function | Load dq rules. | — | [Jump](#load-dq-rules) |
| [`MetadataContract`](#metadatacontract) | Internal | Dataclass | Metadatacontract. | — | [Jump](#metadatacontract) |
| [`normalize_data_product_contract`](#normalize-data-product-contract) | Internal helper | Function | Normalize data product contract. | [`load_data_contract`](#load-data-contract), [`run_data_product`](#run-data-product) | [Jump](#normalize-data-product-contract) |
| [`normalize_dq_rule`](#normalize-dq-rule) | Internal | Function | Normalize dq rule. | — | [Jump](#normalize-dq-rule) |
| [`normalize_dq_rules`](#normalize-dq-rules) | Internal | Function | Normalize dq rules. | — | [Jump](#normalize-dq-rules) |
| [`normalize_quality_rule_candidate`](#normalize-quality-rule-candidate) | Internal | Function | Normalize quality rule candidate. | — | [Jump](#normalize-quality-rule-candidate) |
| [`parse_ai_quality_rule_candidates`](#parse-ai-quality-rule-candidates) | Internal | Function | Parse ai quality rule candidates. | — | [Jump](#parse-ai-quality-rule-candidates) |
| [`QualityContract`](#qualitycontract) | Internal | Dataclass | Qualitycontract. | — | [Jump](#qualitycontract) |
| [`run_data_product`](#run-data-product) | Public | Function | Run data product. | — | [Jump](#run-data-product) |
| [`run_dq_rules`](#run-dq-rules) | Internal | Function | Run dq rules. | — | [Jump](#run-dq-rules) |
| [`run_dq_workflow`](#run-dq-workflow) | Internal helper | Function | Run dq workflow. | [`run_data_product`](#run-data-product) | [Jump](#run-dq-workflow) |
| [`run_quality_rules`](#run-quality-rules) | Public | Function | Run quality rules. | — | [Jump](#run-quality-rules) |
| [`RuntimeContract`](#runtimecontract) | Internal | Dataclass | Runtimecontract. | — | [Jump](#runtimecontract) |
| [`SourceContract`](#sourcecontract) | Internal | Dataclass | Sourcecontract. | — | [Jump](#sourcecontract) |
| [`split_valid_and_quarantine`](#split-valid-and-quarantine) | Internal helper | Function | Split valid and quarantine. | [`run_data_product`](#run-data-product) | [Jump](#split-valid-and-quarantine) |
| [`store_dq_rules`](#store-dq-rules) | Internal | Function | Store dq rules. | — | [Jump](#store-dq-rules) |
| [`TargetContract`](#targetcontract) | Internal | Dataclass | Targetcontract. | — | [Jump](#targetcontract) |
| [`validate_ai_quality_rule_candidate`](#validate-ai-quality-rule-candidate) | Internal | Function | Validate ai quality rule candidate. | — | [Jump](#validate-ai-quality-rule-candidate) |
| [`validate_data_contract_shape`](#validate-data-contract-shape) | Internal helper | Function | Validate data contract shape. | [`run_data_product`](#run-data-product) | [Jump](#validate-data-contract-shape) |
| [`validate_downstream_contract`](#validate-downstream-contract) | Internal | Function | Validate downstream contract. | — | [Jump](#validate-downstream-contract) |
| [`validate_freshness`](#validate-freshness) | Internal | Function | Validate freshness. | — | [Jump](#validate-freshness) |
| [`validate_grain`](#validate-grain) | Internal | Function | Validate grain. | — | [Jump](#validate-grain) |
| [`validate_required_columns`](#validate-required-columns) | Internal | Function | Validate required columns. | — | [Jump](#validate-required-columns) |
| [`validate_runtime_contracts`](#validate-runtime-contracts) | Internal helper | Function | Validate runtime contracts. | [`run_data_product`](#run-data-product) | [Jump](#validate-runtime-contracts) |
| [`validate_upstream_contract`](#validate-upstream-contract) | Internal | Function | Validate upstream contract. | — | [Jump](#validate-upstream-contract) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`load_data_contract`](#load-data-contract) | Function | Load data contract. | [`normalize_data_product_contract`](#normalize-data-product-contract) |
| [`run_data_product`](#run-data-product) | Function | Run data product. | [`_effective_contract_dict`](#effective-contract-dict), [`_refresh_mode`](#refresh-mode), [`_runtime_validation_contract`](#runtime-validation-contract), [`_write_dataframe_to_table`](#write-dataframe-to-table), [`_write_records_spark`](#write-records-spark), [`build_contract_validation_records`](#build-contract-validation-records), [`build_quality_result_records`](#build-quality-result-records), [`build_runtime_context_from_contract`](#build-runtime-context-from-contract), [`normalize_data_product_contract`](#normalize-data-product-contract), [`run_dq_workflow`](#run-dq-workflow), [`split_valid_and_quarantine`](#split-valid-and-quarantine), [`validate_data_contract_shape`](#validate-data-contract-shape), [`validate_runtime_contracts`](#validate-runtime-contracts) |
| [`run_quality_rules`](#run-quality-rules) | Function | Run quality rules. | [`_normalize_severity`](#normalize-severity), [`_now_iso`](#now-iso), [`_pandas_rule`](#pandas-rule), [`_resolve_engine`](#resolve-engine), [`_result_from_counts`](#result-from-counts), [`_spark_rule`](#spark-rule), [`_to_jsonable`](#to-jsonable) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_effective_contract_dict`](#effective-contract-dict) | [`run_data_product`](#run-data-product) |
| [`_normalize_severity`](#normalize-severity) | [`run_quality_rules`](#run-quality-rules) |
| [`_now_iso`](#now-iso) | [`run_quality_rules`](#run-quality-rules) |
| [`_pandas_rule`](#pandas-rule) | [`run_quality_rules`](#run-quality-rules) |
| [`_refresh_mode`](#refresh-mode) | [`run_data_product`](#run-data-product) |
| [`_resolve_engine`](#resolve-engine) | [`run_quality_rules`](#run-quality-rules) |
| [`_result_from_counts`](#result-from-counts) | [`run_quality_rules`](#run-quality-rules) |
| [`_runtime_validation_contract`](#runtime-validation-contract) | [`run_data_product`](#run-data-product) |
| [`_spark_rule`](#spark-rule) | [`run_quality_rules`](#run-quality-rules) |
| [`_to_jsonable`](#to-jsonable) | [`run_quality_rules`](#run-quality-rules) |
| [`_write_dataframe_to_table`](#write-dataframe-to-table) | [`run_data_product`](#run-data-product) |
| [`_write_records_spark`](#write-records-spark) | [`run_data_product`](#run-data-product) |
| [`build_contract_validation_records`](#build-contract-validation-records) | [`run_data_product`](#run-data-product) |
| [`build_quality_result_records`](#build-quality-result-records) | [`run_data_product`](#run-data-product) |
| [`build_runtime_context_from_contract`](#build-runtime-context-from-contract) | [`run_data_product`](#run-data-product) |
| [`normalize_data_product_contract`](#normalize-data-product-contract) | [`load_data_contract`](#load-data-contract), [`run_data_product`](#run-data-product) |
| [`run_dq_workflow`](#run-dq-workflow) | [`run_data_product`](#run-data-product) |
| [`split_valid_and_quarantine`](#split-valid-and-quarantine) | [`run_data_product`](#run-data-product) |
| [`validate_data_contract_shape`](#validate-data-contract-shape) | [`run_data_product`](#run-data-product) |
| [`validate_runtime_contracts`](#validate-runtime-contracts) | [`run_data_product`](#run-data-product) |

## Full module API

::: fabric_data_product_framework.quality
