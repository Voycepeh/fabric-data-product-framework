# Contract-first one-call recipe

## Purpose
Execute the data product from a contract using `run_data_product` with explicit contract validation and gate assertion.

## When to use it
- Standardized runs for handover and reproducibility.
- Contract-first governance and quality enforcement.
- Minimal orchestration notebooks.

## Required inputs
- Active Spark session (`spark`) when source data is read by Spark.
- A valid data product contract YAML.

## Copy-paste code
```python
from fabric_data_product_framework import (
    load_data_contract,
    validate_data_contract_shape,
    run_data_product,
    assert_data_product_passed,
)

contract_path = "contracts/examples/normalized_data_product_contract.yml"
contract = load_data_contract(contract_path)
errors = validate_data_contract_shape(contract)
if errors:
    raise ValueError(f"Contract shape errors: {errors}")

result = run_data_product(spark, contract)
assert_data_product_passed(result)

print(result["status"])
print(result.get("run_id"))
```

## Expected output
- Contract loads and passes shape validation.
- `run_data_product` returns structured execution result.
- `assert_data_product_passed` raises no exception for successful runs.

## Common failures
- Contract schema/shape errors.
- Missing runtime/source settings required by the contract.
- Downstream quality/drift failures causing blocked status.

## Related function groups
See [src/README.md](../../src/README.md) section: Contract-first orchestration and contract models.
