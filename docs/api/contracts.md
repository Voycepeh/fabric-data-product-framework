# Contracts API Reference

## Module purpose
`fabric_data_product_framework.config` validates contract files, while `fabric_data_product_framework.data_contract` orchestrates contract-first execution.

## Core public callables
- `load_dataset_contract(path)`
- `validate_dataset_contract(contract, schema_path=None)`
- `load_data_contract(path_or_dict)`
- `run_data_product(spark, contract, transform=None, source_df=None, write=None, write_target=True, write_metadata=True)`

## Typical chaining
1. load/validate contract.
2. normalize with `load_data_contract`.
3. execute end-to-end flow with `run_data_product`.
4. evaluate run summary and gates.
