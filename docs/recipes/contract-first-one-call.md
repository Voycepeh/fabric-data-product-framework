# Contract-first one-call recipe

## Purpose
Execute the data product using one primary callable (`run_data_product`) driven by a contract file.

## When to use it
- Standardized runs for handover and reproducibility.
- Enforcing contract-first controls.
- Reducing notebook orchestration boilerplate.

## Required inputs
- A valid dataset contract YAML.
- Runtime context (paths/engine/options) as required by the contract.

## Copy-paste code
```python
from fabric_data_product_framework.contracts import (
    load_data_contract,
    validate_data_contract_shape,
    run_data_product,
    assert_data_product_passed,
)

contract_path = "contracts/examples/normalized_data_product_contract.yml"
contract = load_data_contract(contract_path)
validate_data_contract_shape(contract)

result = run_data_product(contract=contract)
assert_data_product_passed(result)

print(result)
```

## Expected output
- Contract loads and validates against expected shape.
- Execution returns structured run results with artifact references.
- `assert_data_product_passed` succeeds for passing runs.

## Common failures
- Contract schema validation errors.
- Missing contract-required runtime fields.
- Downstream DQ or drift failures causing run status to fail.

## Related function groups
See [src/README.md](../../src/README.md) section: Contract-first orchestration and contract models.
