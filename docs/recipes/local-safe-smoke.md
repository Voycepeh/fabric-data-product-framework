# Local-safe smoke path

## Purpose

Use this recipe to test framework logic locally with a small in-memory dataset
and without Fabric lakehouse reads or writes.

## Required inputs

- Python environment with project dependencies installed.
- Small pandas DataFrame.
- No Fabric runtime required.

## Example

```python
import pandas as pd

from fabric_data_product_framework.lineage import (
    build_lineage_records,
    build_transformation_summary_markdown,
    generate_mermaid_lineage,
)
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.quality import run_quality_rules

dataset_name = "orders_local"
table_name = "orders"
run_id = "local-smoke-001"

df = pd.DataFrame(
    {
        "order_id": [1, 2, 3],
        "customer_id": ["C1", "C2", "C3"],
        "amount": [10.0, 25.5, 30.0],
    }
)

profile = profile_dataframe(df, dataset_name=dataset_name, engine="pandas")

rules = [
    {
        "rule_id": "order_id_not_null",
        "rule_type": "not_null",
        "column": "order_id",
        "severity": "critical",
    },
    {
        "rule_id": "amount_not_null",
        "rule_type": "not_null",
        "column": "amount",
        "severity": "warning",
    },
]

dq_result = run_quality_rules(
    df,
    rules,
    dataset_name=dataset_name,
    table_name=f"local.{table_name}",
    engine="pandas",
)

steps = [
    {
        "step_id": "1",
        "step_name": "ingest_local_dataframe",
        "input_name": "inline_dataframe",
        "output_name": "orders_local_df",
        "transformation_type": "ingest",
    },
    {
        "step_id": "2",
        "step_name": "run_local_quality_checks",
        "input_name": "orders_local_df",
        "output_name": "dq_result",
        "transformation_type": "quality",
    },
]

lineage_records = build_lineage_records(
    dataset_name=dataset_name,
    run_id=run_id,
    source_tables=["local.inline_dataframe"],
    target_table=f"local.{table_name}",
    transformation_steps=steps,
)

summary = {
    "dataset_name": dataset_name,
    "run_id": run_id,
    "source_tables": ["local.inline_dataframe"],
    "target_table": f"local.{table_name}",
    "step_count": len(steps),
    "steps": steps,
    "columns_used": ["order_id", "customer_id", "amount"],
    "columns_created": [],
}

mermaid = generate_mermaid_lineage(
    source_tables=["local.inline_dataframe"],
    target_table=f"local.{table_name}",
    transformation_steps=steps,
)

summary_md = build_transformation_summary_markdown(summary)

print(profile)
print(dq_result)
print(lineage_records)
print(mermaid)
print(summary_md)
```

## Expected output

- Profile summary for the sample DataFrame.
- Data quality results for the small rule set.
- Lineage records for the local smoke path.
- Mermaid text for quick lineage inspection.
- Markdown transformation summary.

## Common failures

- Import errors usually mean the project is not installed or `PYTHONPATH=src`
  is not set.
- Wrong DQ helper usage usually means a Spark/Fabric workflow function was
  used instead of the local-safe rule runner.

## Related references

- `src/README.md`
- `docs/reference/`
