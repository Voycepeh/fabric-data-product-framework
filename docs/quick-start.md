# Quick Start

## Public-safe reminder
Do not commit real organisational data, secrets, tenant details, internal table names, workspace names, screenshots, or production metadata.

## Minimal flow

1. Define purpose, steward, usage, and business metadata.
2. Draft governance labels and contract expectations.
3. Configure notebook parameters and declared sources.
4. Run profiling and metadata logging.
5. Build transformations and technical columns.
6. Run drift, incremental, quality, and contract checks.
7. Export lineage and handover context.

## Short code examples

### Contract validation

```python
from fabric_data_product_framework.config import load_and_validate_dataset_contract

contract, errors = load_and_validate_dataset_contract(
    "examples/configs/sample_dataset_contract.yaml"
)
```

### DataFrame profiling

```python
import pandas as pd
from fabric_data_product_framework.profiling import flatten_profile_for_metadata, profile_dataframe

df = pd.DataFrame({"customer_id": [1, 2, 3], "amount": [10.5, 20.0, 30.0]})
profile = profile_dataframe(df, dataset_name="synthetic_orders")
```

### Technical columns

```python
from fabric_data_product_framework.technical_columns import add_standard_technical_columns

df_output = add_standard_technical_columns(
    df_output,
    run_id=ctx["run_id"],
    environment=ctx["environment"],
    source_table=ctx["source_table"],
    watermark_column="updated_at",
    business_keys=["customer_id"],
    engine="spark",
)
```

### Schema drift check

```python
from fabric_data_product_framework.drift import compare_schema_snapshots

result = compare_schema_snapshots(baseline_snapshot, current_snapshot)
```

### Incremental safety check

```python
from fabric_data_product_framework.incremental import assert_incremental_safe, build_partition_snapshot, compare_partition_snapshots

current_partition_snapshots = build_partition_snapshot(
    df_source,
    dataset_name="synthetic_orders",
    table_name="source.synthetic_orders",
    partition_column="business_date",
    business_keys=["customer_id", "order_id"],
    watermark_column="updated_at",
    engine="spark",
)

safety_result = compare_partition_snapshots(
    previous_partition_snapshots,
    current_partition_snapshots,
)

assert_incremental_safe(safety_result)
```

### Data quality gate

```python
from fabric_data_product_framework.quality import assert_quality_gate, run_quality_rules

quality_result = run_quality_rules(
    df_output,
    contract.get("quality_rules", []),
    dataset_name=ctx["dataset_name"],
    table_name=ctx["target_table"],
    engine="spark",
)

assert_quality_gate(quality_result)
```

### Notebook runtime helper

```python
from fabric_data_product_framework.runtime import assert_notebook_name_valid, build_runtime_context

ctx = build_runtime_context(
    dataset_name="synthetic_orders",
    environment="dev",
    source_table="source.synthetic_orders",
    target_table="product.synthetic_orders",
    notebook_name="source_to_product_synthetic_orders",
)

assert_notebook_name_valid(
    ctx["notebook_name"],
    allowed_prefixes=["source_to_product_", "bronze_to_silver_", "silver_to_gold_"],
)
```

## Execution engines

The framework exposes engine-aware dataframe APIs with `engine="auto" | "pandas" | "spark"`.

- **pandas**: local and synthetic workloads
- **spark**: Fabric/lakehouse-scale workloads
- **auto**: runtime engine detection

See [engine model](engine-model.md) for full behavior details.

## First runnable notebook MVP

Copy `templates/notebooks/fabric_data_product_mvp.py` into a Fabric notebook to run a full MVP flow from contract validation to metadata outputs.

Wire only three adapters to start testing in your environment:

- `fabric_reader`
- `fabric_table_writer`
- `metadata_writer`
