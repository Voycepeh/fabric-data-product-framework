# `quality` module

Public callables: 3  
Related internal helpers: 20  
Other internal objects: 60  
Deprecated objects: 0

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [ContractValidationError](#contractvalidationerror) | Internal | Class | Contractvalidationerror. | — | [API](#contractvalidationerror) |
| [DataProductContract](#dataproductcontract) | Internal | Dataclass | Dataproductcontract. | — | [API](#dataproductcontract) |
| [DataQualityError](#dataqualityerror) | Internal | Class | Dataqualityerror. | — | [API](#dataqualityerror) |
| [DriftContract](#driftcontract) | Internal | Dataclass | Driftcontract. | — | [API](#driftcontract) |
| [GovernanceContract](#governancecontract) | Internal | Dataclass | Governancecontract. | — | [API](#governancecontract) |
| [MetadataContract](#metadatacontract) | Internal | Dataclass | Metadatacontract. | — | [API](#metadatacontract) |
| [QualityContract](#qualitycontract) | Internal | Dataclass | Qualitycontract. | — | [API](#qualitycontract) |
| [RuntimeContract](#runtimecontract) | Internal | Dataclass | Runtimecontract. | — | [API](#runtimecontract) |
| [SourceContract](#sourcecontract) | Internal | Dataclass | Sourcecontract. | — | [API](#sourcecontract) |
| [TargetContract](#targetcontract) | Internal | Dataclass | Targetcontract. | — | [API](#targetcontract) |
| [_action_for](#-action-for) | Internal | Function | — | — | [API](#-action-for) |
| [_add_pandas](#-add-pandas) | Internal | Function | — | — | [API](#-add-pandas) |
| [_add_spark](#-add-spark) | Internal | Function | — | — | [API](#-add-spark) |
| [_build_rule_id](#-build-rule-id) | Internal | Function | — | — | [API](#-build-rule-id) |
| [_combine_contract_checks](#-combine-contract-checks) | Internal | Function | — | — | [API](#-combine-contract-checks) |
| [_dict](#-dict) | Internal | Function | Return a dictionary or an empty default for optional config fragments. | — | [API](#-dict) |
| [_effective_contract_dict](#-effective-contract-dict) | Internal helper | Function | — | `run_data_product` | [API](#-effective-contract-dict) |
| [_extract_fabric_ai_response_payload](#-extract-fabric-ai-response-payload) | Internal | Function | — | — | [API](#-extract-fabric-ai-response-payload) |
| [_fabric_ai_dependencies_available](#-fabric-ai-dependencies-available) | Internal | Function | — | — | [API](#-fabric-ai-dependencies-available) |
| [_json_safe](#-json-safe) | Internal | Function | — | — | [API](#-json-safe) |
| [_jsonable](#-jsonable) | Internal | Function | — | — | [API](#-jsonable) |
| [_normalize_severity](#-normalize-severity) | Internal helper | Function | — | `run_quality_rules` | [API](#-normalize-severity) |
| [_now_iso](#-now-iso) | Internal helper | Function | — | `run_quality_rules` | [API](#-now-iso) |
| [_pandas_rule](#-pandas-rule) | Internal helper | Function | — | `run_quality_rules` | [API](#-pandas-rule) |
| [_parse_freshness_timedelta](#-parse-freshness-timedelta) | Internal | Function | — | — | [API](#-parse-freshness-timedelta) |
| [_refresh_mode](#-refresh-mode) | Internal helper | Function | — | `run_data_product` | [API](#-refresh-mode) |
| [_resolve_engine](#-resolve-engine) | Internal helper | Function | — | `run_quality_rules` | [API](#-resolve-engine) |
| [_result_from_counts](#-result-from-counts) | Internal helper | Function | — | `run_quality_rules` | [API](#-result-from-counts) |
| [_runtime_validation_contract](#-runtime-validation-contract) | Internal helper | Function | — | `run_data_product` | [API](#-runtime-validation-contract) |
| [_severity_bucket](#-severity-bucket) | Internal | Function | — | — | [API](#-severity-bucket) |
| [_skipped](#-skipped) | Internal | Function | — | — | [API](#-skipped) |
| [_spark_rule](#-spark-rule) | Internal helper | Function | — | `run_quality_rules` | [API](#-spark-rule) |
| [_strip_json_fences](#-strip-json-fences) | Internal | Function | — | — | [API](#-strip-json-fences) |
| [_to_jsonable](#-to-jsonable) | Internal helper | Function | — | `run_quality_rules` | [API](#-to-jsonable) |
| [_write_dataframe_to_table](#-write-dataframe-to-table) | Internal helper | Function | — | `run_data_product` | [API](#-write-dataframe-to-table) |
| [_write_records_spark](#-write-records-spark) | Internal helper | Function | — | `run_data_product` | [API](#-write-records-spark) |
| [add_dq_failure_columns](#add-dq-failure-columns) | Internal | Function | Add dq failure columns. | — | [API](#add-dq-failure-columns) |
| [assert_contracts_valid](#assert-contracts-valid) | Internal | Function | Assert contracts valid. | — | [API](#assert-contracts-valid) |
| [assert_data_product_passed](#assert-data-product-passed) | Internal | Function | Assert data product passed. | — | [API](#assert-data-product-passed) |
| [assert_quality_gate](#assert-quality-gate) | Internal | Function | Assert quality gate. | — | [API](#assert-quality-gate) |
| [build_contract_validation_records](#build-contract-validation-records) | Internal helper | Function | Build contract validation records. | `run_data_product` | [API](#build-contract-validation-records) |
| [build_dq_rule_records](#build-dq-rule-records) | Internal | Function | Build dq rule records. | — | [API](#build-dq-rule-records) |
| [build_drift_contract](#build-drift-contract) | Internal | Function | Build drift contract. | — | [API](#build-drift-contract) |
| [build_governance_contract](#build-governance-contract) | Internal | Function | Build governance contract. | — | [API](#build-governance-contract) |
| [build_layman_rule_records](#build-layman-rule-records) | Internal | Function | Build layman rule records. | — | [API](#build-layman-rule-records) |
| [build_metadata_contract](#build-metadata-contract) | Internal | Function | Build metadata contract. | — | [API](#build-metadata-contract) |
| [build_quality_contract](#build-quality-contract) | Internal | Function | Build quality contract. | — | [API](#build-quality-contract) |
| [build_quality_result_records](#build-quality-result-records) | Internal helper | Function | Build quality result records. | `run_data_product` | [API](#build-quality-result-records) |
| [build_quality_rule_generation_prompt](#build-quality-rule-generation-prompt) | Internal | Function | Build quality rule generation prompt. | — | [API](#build-quality-rule-generation-prompt) |
| [build_quality_rule_prompt_context](#build-quality-rule-prompt-context) | Internal | Function | Build quality rule prompt context. | — | [API](#build-quality-rule-prompt-context) |
| [build_quarantine_rule_coverage_records](#build-quarantine-rule-coverage-records) | Internal | Function | Build quarantine rule coverage records. | — | [API](#build-quarantine-rule-coverage-records) |
| [build_quarantine_summary_records](#build-quarantine-summary-records) | Internal | Function | Build quarantine summary records. | — | [API](#build-quarantine-summary-records) |
| [build_rule_registry_records](#build-rule-registry-records) | Internal | Function | Build rule registry records. | — | [API](#build-rule-registry-records) |
| [build_runtime_context_from_contract](#build-runtime-context-from-contract) | Internal helper | Function | Build runtime context from contract. | `run_data_product` | [API](#build-runtime-context-from-contract) |
| [build_runtime_contract](#build-runtime-contract) | Internal | Function | Build runtime contract. | — | [API](#build-runtime-contract) |
| [build_source_contract](#build-source-contract) | Internal | Function | Build source contract. | — | [API](#build-source-contract) |
| [build_target_contract](#build-target-contract) | Internal | Function | Build target contract. | — | [API](#build-target-contract) |
| [compile_layman_rule_to_quality_rule](#compile-layman-rule-to-quality-rule) | Internal | Function | Compile layman rule to quality rule. | — | [API](#compile-layman-rule-to-quality-rule) |
| [compile_layman_rules_to_quality_rules](#compile-layman-rules-to-quality-rules) | Internal | Function | Compile layman rules to quality rules. | — | [API](#compile-layman-rules-to-quality-rules) |
| [data_product_contract_to_dict](#data-product-contract-to-dict) | Internal | Function | Data product contract to dict. | — | [API](#data-product-contract-to-dict) |
| [generate_dq_rule_candidates](#generate-dq-rule-candidates) | Internal | Function | Generate dq rule candidates. | — | [API](#generate-dq-rule-candidates) |
| [generate_dq_rule_candidates_with_fabric_ai](#generate-dq-rule-candidates-with-fabric-ai) | Internal | Function | Generate dq rule candidates with fabric ai. | — | [API](#generate-dq-rule-candidates-with-fabric-ai) |
| [load_data_contract](#load-data-contract) | Public | Function | Load data contract. | — | [API](#load-data-contract) |
| [load_dq_rules](#load-dq-rules) | Internal | Function | Load dq rules. | — | [API](#load-dq-rules) |
| [normalize_data_product_contract](#normalize-data-product-contract) | Internal helper | Function | Normalize data product contract. | `load_data_contract`, `run_data_product` | [API](#normalize-data-product-contract) |
| [normalize_dq_rule](#normalize-dq-rule) | Internal | Function | Normalize dq rule. | — | [API](#normalize-dq-rule) |
| [normalize_dq_rules](#normalize-dq-rules) | Internal | Function | Normalize dq rules. | — | [API](#normalize-dq-rules) |
| [normalize_quality_rule_candidate](#normalize-quality-rule-candidate) | Internal | Function | Normalize quality rule candidate. | — | [API](#normalize-quality-rule-candidate) |
| [parse_ai_quality_rule_candidates](#parse-ai-quality-rule-candidates) | Internal | Function | Parse ai quality rule candidates. | — | [API](#parse-ai-quality-rule-candidates) |
| [run_data_product](#run-data-product) | Public | Function | Run data product. | — | [API](#run-data-product) |
| [run_dq_rules](#run-dq-rules) | Internal | Function | Run dq rules. | — | [API](#run-dq-rules) |
| [run_dq_workflow](#run-dq-workflow) | Internal helper | Function | Run dq workflow. | `run_data_product` | [API](#run-dq-workflow) |
| [run_quality_rules](#run-quality-rules) | Public | Function | Run quality rules. | — | [API](#run-quality-rules) |
| [split_valid_and_quarantine](#split-valid-and-quarantine) | Internal helper | Function | Split valid and quarantine. | `run_data_product` | [API](#split-valid-and-quarantine) |
| [store_dq_rules](#store-dq-rules) | Internal | Function | Store dq rules. | — | [API](#store-dq-rules) |
| [validate_ai_quality_rule_candidate](#validate-ai-quality-rule-candidate) | Internal | Function | Validate ai quality rule candidate. | — | [API](#validate-ai-quality-rule-candidate) |
| [validate_data_contract_shape](#validate-data-contract-shape) | Internal helper | Function | Validate data contract shape. | `run_data_product` | [API](#validate-data-contract-shape) |
| [validate_downstream_contract](#validate-downstream-contract) | Internal | Function | Validate downstream contract. | — | [API](#validate-downstream-contract) |
| [validate_freshness](#validate-freshness) | Internal | Function | Validate freshness. | — | [API](#validate-freshness) |
| [validate_grain](#validate-grain) | Internal | Function | Validate grain. | — | [API](#validate-grain) |
| [validate_required_columns](#validate-required-columns) | Internal | Function | Validate required columns. | — | [API](#validate-required-columns) |
| [validate_runtime_contracts](#validate-runtime-contracts) | Internal helper | Function | Validate runtime contracts. | `run_data_product` | [API](#validate-runtime-contracts) |
| [validate_upstream_contract](#validate-upstream-contract) | Internal | Function | Validate upstream contract. | — | [API](#validate-upstream-contract) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `load_data_contract` | Function | Load data contract. | — |
| `run_data_product` | Function | Run data product. | `_effective_contract_dict` (internal), `_refresh_mode` (internal), `_runtime_validation_contract` (internal), `_write_dataframe_to_table` (internal), `_write_records_spark` (internal) |
| `run_quality_rules` | Function | Run quality rules. | `_normalize_severity` (internal), `_now_iso` (internal), `_pandas_rule` (internal), `_resolve_engine` (internal), `_result_from_counts` (internal), `_spark_rule` (internal), `_to_jsonable` (internal) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `_effective_contract_dict` | `run_data_product` |
| `_normalize_severity` | `run_quality_rules` |
| `_now_iso` | `run_quality_rules` |
| `_pandas_rule` | `run_quality_rules` |
| `_refresh_mode` | `run_data_product` |
| `_resolve_engine` | `run_quality_rules` |
| `_result_from_counts` | `run_quality_rules` |
| `_runtime_validation_contract` | `run_data_product` |
| `_spark_rule` | `run_quality_rules` |
| `_to_jsonable` | `run_quality_rules` |
| `_write_dataframe_to_table` | `run_data_product` |
| `_write_records_spark` | `run_data_product` |
| `build_contract_validation_records` | `run_data_product` |
| `build_quality_result_records` | `run_data_product` |
| `build_runtime_context_from_contract` | `run_data_product` |
| `normalize_data_product_contract` | `load_data_contract`, `run_data_product` |
| `run_dq_workflow` | `run_data_product` |
| `split_valid_and_quarantine` | `run_data_product` |
| `validate_data_contract_shape` | `run_data_product` |
| `validate_runtime_contracts` | `run_data_product` |

## Full module API

::: fabric_data_product_framework.quality
