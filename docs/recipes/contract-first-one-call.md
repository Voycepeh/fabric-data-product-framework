# Contract-first one-call execution

## Purpose

Run a full contract-first workflow with one orchestrated execution call.

## Required inputs

- Active Spark session (`spark`) if the contract reads Spark sources.
- Valid data contract YAML.

## Example

```python
from fabricops_kit import (
    assert_data_product_passed,
    load_data_contract,
    run_data_product,
    validate_data_contract_shape,
)

contract_path = "contracts/examples/normalized_data_product_contract.yml"
contract = load_data_contract(contract_path)

shape_errors = validate_data_contract_shape(contract)
if shape_errors:
    raise ValueError(f"Contract shape errors: {shape_errors}")

result = run_data_product(spark, contract)
assert_data_product_passed(result)

print(result["status"])
print(result.get("run_id"))
```

## Expected output

- Contract loads and passes shape validation.
- Data product run returns a structured result.
- Gate assertion passes for successful runs.

## Common failures

- Contract shape/schema errors.
- Missing runtime parameters required by contract inputs.
- DQ or governance failures causing blocked run status.
