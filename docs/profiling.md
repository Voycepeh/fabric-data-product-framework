# Profiling

Use `profile_dataframe` with explicit engine choice:

- `engine="pandas"` for small/local CSV/Excel/laptop workflows.
- `engine="spark"` for Fabric-scale lakehouse tables.
- `engine="auto"` to detect engine.

Spark profiling uses Spark-native aggregations and **does not** auto-convert Spark DataFrames to pandas.

Current Spark MVP behavior:
- row count and column metrics are computed with Spark aggregate operations.
- sample values and top values are collected with explicit caps.
- duplicate row count/pct are intentionally left `None` by default to avoid expensive full-row distinct scans.

## Metadata-shaped output

Use `flatten_profile_for_metadata` to transform a dataset profile into column-level metadata rows suitable for appending into metadata tables.

```python
from fabric_data_product_framework.profiling import (
    default_technical_columns,
    flatten_profile_for_metadata,
    profile_dataframe,
)

source_profile = profile_dataframe(
    df_source,
    dataset_name="synthetic_orders",
    engine="spark",
)

metadata_rows = flatten_profile_for_metadata(
    source_profile,
    table_name="source.synthetic_orders",
    run_id=ctx["run_id"],
    table_stage="source",
    exclude_columns=default_technical_columns(),
)
```
