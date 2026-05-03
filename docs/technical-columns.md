# Technical columns helpers

Technical columns make Fabric notebook outputs easier to operate, troubleshoot, and hand over.

## Why technical columns exist

They provide a consistent way to:
- track run-level audit context (`run_id`, pipeline name, environment)
- preserve source lineage hints (source system/table/extract timestamp)
- support incremental processing (watermark values)
- support dedup/upsert patterns (row hash and business key hash)
- standardize datetime split fields for downstream consumers

## Recommended audit columns

Use `default_technical_columns()` for the framework baseline list. The helper includes commonly-used names such as:
- `_pipeline_run_id`
- `_source_table`
- `_record_loaded_timestamp`
- `_watermark_value`
- `_row_hash`
- `_business_key_hash`

## Pandas vs Spark behavior

All public helpers accept `engine="auto" | "pandas" | "spark"`.

- `pandas` path is for local/small workflows and tests.
- `spark` path is for Fabric/lakehouse scale.
- `auto` uses dataframe detection.

Important guarantees:
- No automatic Spark-to-pandas conversion.
- No PySpark import at module import time (Spark functions are imported lazily inside Spark branches).

## Datetime conversion pattern (Asia/Singapore / UTC+8)

`add_datetime_parts(...)` supports a notebook-friendly standardization pattern:
- convert UTC timestamps to `Asia/Singapore`
- derive date (`YYYY-MM-DD`)
- derive time (`HH:MM:SS`)
- derive hour (`0-23`)
- derive 30-minute block (`HH:00` / `HH:30`)

## End-to-end helper

Use one call to apply the standard pattern:

```python
from fabricops_kit.technical_columns import add_standard_technical_columns

df_output = add_standard_technical_columns(
    df_output,
    run_id=ctx["run_id"],
    pipeline_name="synthetic_orders_pipeline",
    environment=ctx["environment"],
    source_system="synthetic_source",
    source_table=ctx["source_table"],
    watermark_column="updated_at",
    business_keys=["customer_id"],
    engine="spark",
)
```

## Ignore technical columns during profiling

When flattening profile output for metadata tables, exclude technical columns:

```python
from fabricops_kit.profiling import (
    default_technical_columns,
    flatten_profile_for_metadata,
)

rows = flatten_profile_for_metadata(
    profile,
    table_name="product.synthetic_orders",
    run_id=ctx["run_id"],
    table_stage="output",
    exclude_columns=default_technical_columns(),
)
```
