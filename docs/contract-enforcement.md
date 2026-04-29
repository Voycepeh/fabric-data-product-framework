# Runtime Contract Enforcement

Schema validation checks whether a YAML contract is structurally valid. Runtime enforcement checks whether actual source/output data matches the contract during execution.

## Upstream vs downstream

- **Upstream** validates required source columns and optional freshness using the configured watermark.
- **Downstream** validates guaranteed output columns and business-key grain uniqueness.

## Checks

- Required columns
- Grain validation
- Freshness validation (`"2 days"`, `"1 day"`, `"24 hours"` supported)

## Engine behavior

- `engine="pandas"` for local/laptop scale.
- `engine="spark"` for Fabric/lakehouse scale.
- `engine="auto"` detects dataframe type.
- Spark data is never converted to pandas.
- PySpark is imported lazily only when Spark paths execute.

## Example

```python
from fabric_data_product_framework.contracts import validate_runtime_contracts, assert_contracts_valid

result = validate_runtime_contracts(source_df=df_source, output_df=df_output, contract=contract, engine="auto")
assert_contracts_valid(result)
```
