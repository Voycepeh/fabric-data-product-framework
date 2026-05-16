# Fabric dry run path

## Purpose

Use this recipe to validate Fabric setup and workflow wiring without
committing to a full production write path.

## Required inputs

- Fabric notebook runtime.
- Valid Fabric config path.
- Source table already available in Fabric.

## Example

```python
from fabricops_kit.data_quality import run_dq_workflow
from fabricops_kit.fabric_input_output import (
    read_lakehouse_table,
    load_config,
)
from fabricops_kit.data_profiling import profile_dataframe

DRY_RUN = True

cfg = load_config(CONFIG)

dataset_name = "orders"
table_name = "orders_source"

source_df = read_lakehouse_table(cfg, "Sandbox", "source", table_name, spark_session=spark)
profile = profile_dataframe(source_df, dataset_name=dataset_name, engine="spark")

quality_contract = {
    "rules": [
        {
            "rule_id": "order_id_not_null",
            "rule_type": "not_null",
            "column": "order_id",
            "severity": "critical",
        },
    ],
}

dq_result = run_dq_workflow(
    spark,
    source_df,
    quality_contract,
    dataset_name=dataset_name,
    table_name=table_name,
)

print("DRY_RUN =", DRY_RUN)
print(profile)
print(dq_result)
```

## Expected output

- Source table loads successfully.
- Profile is generated.
- DQ workflow returns results without requiring a full production write.

## Common failures

- Missing Fabric config path.
- Wrong lakehouse environment or target.
- Using local-only helpers instead of Spark/Fabric helpers.
