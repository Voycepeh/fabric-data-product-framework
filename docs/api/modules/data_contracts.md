# `data_contracts` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_contract_column_records`](../../reference/step-07-output-profile-product-contract/build_contract_column_records.md) | function | Build normalized contract-column metadata records for persistence. | [`_now_utc_iso`](../../reference/internal/data_contracts/_now_utc_iso.md) (internal) |
| [`build_contract_header_record`](../../reference/step-07-output-profile-product-contract/build_contract_header_record.md) | function | Build one header row for FABRICOPS_CONTRACTS. | [`_now_utc_iso`](../../reference/internal/data_contracts/_now_utc_iso.md) (internal) |
| [`build_contract_records`](../../reference/step-07-output-profile-product-contract/build_contract_records.md) | function | Build grouped contract header, column, and rule metadata payloads. | — |
| [`build_contract_rule_records`](../../reference/step-07-output-profile-product-contract/build_contract_rule_records.md) | function | Build quality-rule metadata records from a validated contract. | [`_now_utc_iso`](../../reference/internal/data_contracts/_now_utc_iso.md) (internal) |
| [`build_contract_summary`](../../reference/step-07-output-profile-product-contract/build_contract_summary.md) | function | Build a concise contract summary for reviews and handover. | — |
| [`contract_records_to_spark`](../../reference/step-07-output-profile-product-contract/contract_records_to_spark.md) | function | Convert record dictionaries into a Spark DataFrame when Spark is available. | — |
| [`extract_business_keys`](../../reference/step-03-source-contract-ingestion-pattern/extract_business_keys.md) | function | Extract business-key column names from a normalized contract. | — |
| [`extract_classifications`](../../reference/step-03-source-contract-ingestion-pattern/extract_classifications.md) | function | Extract column classification mappings from a normalized contract. | — |
| [`extract_optional_columns`](../../reference/step-03-source-contract-ingestion-pattern/extract_optional_columns.md) | function | Extract optional column names from a normalized contract. | — |
| [`extract_quality_rules`](../../reference/step-03-source-contract-ingestion-pattern/extract_quality_rules.md) | function | Extract raw quality-rule definitions from a normalized contract. | — |
| [`extract_required_columns`](../../reference/step-03-source-contract-ingestion-pattern/extract_required_columns.md) | function | Extract required column names from a normalized contract. | — |
| [`get_executable_quality_rules`](../../reference/step-06c-pipeline-controls/get_executable_quality_rules.md) | function | Return normalized quality rules ready for pipeline enforcement. | — |
| [`load_contract_from_lakehouse`](../../reference/step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse.md) | function | Load one contract by ID/version from Fabric metadata storage. | [`_select_latest`](../../reference/internal/data_contracts/_select_latest.md) (internal), [`_to_records`](../../reference/internal/data_contracts/_to_records.md) (internal) |
| [`load_latest_approved_contract`](../../reference/step-03-source-contract-ingestion-pattern/load_latest_approved_contract.md) | function | Load the latest approved contract for a dataset/object pair. | [`_select_latest`](../../reference/internal/data_contracts/_select_latest.md) (internal), [`_to_records`](../../reference/internal/data_contracts/_to_records.md) (internal) |
| [`normalize_contract_dict`](../../reference/step-03-source-contract-ingestion-pattern/normalize_contract_dict.md) | function | Normalize a notebook-authored contract dictionary to a stable shape. | — |
| [`validate_contract_dict`](../../reference/step-03-source-contract-ingestion-pattern/validate_contract_dict.md) | function | Validate a contract dictionary and return error strings without raising. | — |
| [`write_contract_to_lakehouse`](../../reference/step-07-output-profile-product-contract/write_contract_to_lakehouse.md) | function | Validate and persist contract records into Fabric metadata tables. | — |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_now_utc_iso`](../../reference/internal/data_contracts/_now_utc_iso.md) | [`build_contract_column_records`](../../reference/step-07-output-profile-product-contract/build_contract_column_records.md), [`build_contract_header_record`](../../reference/step-07-output-profile-product-contract/build_contract_header_record.md), [`build_contract_rule_records`](../../reference/step-07-output-profile-product-contract/build_contract_rule_records.md) |
| [`_select_latest`](../../reference/internal/data_contracts/_select_latest.md) | [`load_contract_from_lakehouse`](../../reference/step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse.md), [`load_latest_approved_contract`](../../reference/step-03-source-contract-ingestion-pattern/load_latest_approved_contract.md) |
| [`_to_records`](../../reference/internal/data_contracts/_to_records.md) | [`load_contract_from_lakehouse`](../../reference/step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse.md), [`load_latest_approved_contract`](../../reference/step-03-source-contract-ingestion-pattern/load_latest_approved_contract.md) |
