# Data quality (MVP)

This module provides a lightweight, contract-driven data quality engine for Fabric notebook pipelines.

## MVP scope

Supported rule types:

- `not_null`
- `unique`
- `unique_combination`
- `accepted_values`
- `range_check`
- `regex_check`
- `row_count_min`
- `row_count_between`
- `freshness_check`

This is intentionally minimal and not a Great Expectations replacement.

## Rule format

Rules are plain dictionaries (usually from `contract["quality_rules"]`) with fields like:

- `rule_id`
- `rule_type`
- `column` or `columns`
- `severity`: `info` | `warning` | `critical`
- rule-specific fields (`accepted_values`, `pattern`, `min_count`, `max_age_days`, etc.)
- `reason`

## Severity and gate behavior

Failed rule action mapping:

- `info` -> `allow`
- `warning` -> `warn`
- `critical` -> `block`

Overall run behavior:

- `failed` if any failed blocking rule
- `warning` if warning failures exist and no blocking failures
- `passed` otherwise

`assert_quality_gate()` raises `DataQualityError` when `can_continue=False`.

## Pandas vs Spark

- `engine="pandas"`: local/small data, tests, CSV/Excel workflows.
- `engine="spark"`: Fabric/lakehouse scale checks executed with Spark-native operations.
- `engine="auto"`: auto-detects pandas or Spark DataFrame.

Important constraints:

- No automatic Spark-to-pandas conversion.
- No module import-time PySpark dependency (Spark functions imported lazily in Spark helpers).

## Metadata shaping

Use `build_quality_result_records()` to flatten results into row records for metadata writers.

## Example

```python
from fabric_data_product_framework.quality import (
    run_quality_rules,
    assert_quality_gate,
)

quality_result = run_quality_rules(
    df_output,
    contract["quality_rules"],
    dataset_name=ctx["dataset_name"],
    table_name=ctx["target_table"],
    engine="spark",
)

assert_quality_gate(quality_result)
```

## Manual Fabric validation

Use this compact Spark notebook check when CI does not run Spark tests:

```python
from fabric_data_product_framework.quality import run_quality_rules, assert_quality_gate

rules = [
    {"rule_id": "DQ001", "rule_type": "not_null", "column": "customer_id", "severity": "critical"},
    {"rule_id": "DQ002", "rule_type": "range_check", "column": "amount", "min_value": 0, "max_value": 100000, "severity": "critical"},
]

quality_result = run_quality_rules(
    df_output,
    rules,
    dataset_name=ctx["dataset_name"],
    table_name=ctx["target_table"],
    engine="spark",
)

print(quality_result["status"], quality_result["can_continue"])
assert_quality_gate(quality_result)
```
