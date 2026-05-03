# Runtime Contract Enforcement

Schema validation checks whether a YAML contract is structurally valid. Runtime enforcement checks whether actual source/output data matches the contract during execution.

## Upstream vs downstream

- **Upstream** validates required source columns and optional freshness using the configured watermark.
- **Downstream** validates guaranteed output columns and business-key grain uniqueness.

## Checks

- Required columns
- Grain validation (returns `duplicate_key_count`, `duplicate_row_count`, and backward-compatible `duplicate_count` mapped to duplicate rows)
- Freshness validation (`"1 day"`, `"2 days"`, `"24 hours"`, `"23 hours"`, `"25 hours"`)

Freshness compares `datetime.now(timezone.utc) - max_watermark` against the parsed threshold timedelta.

## Engine behavior

- `engine="pandas"` for local/laptop scale.
- `engine="spark"` for Fabric/lakehouse scale.
- `engine="auto"` detects dataframe type.
- Spark data is never converted to pandas.
- PySpark is imported lazily only when Spark paths execute.

## Example

```python
from fabric_data_product_framework.quality import validate_runtime_contracts, assert_contracts_valid

result = validate_runtime_contracts(source_df=df_source, output_df=df_output, contract=contract, engine="auto")
assert_contracts_valid(result)
```
