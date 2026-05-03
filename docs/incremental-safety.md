# Incremental partition safety (MVP)

Incremental safety protects your pipeline from silently overwriting trusted historical partitions when source data changes unexpectedly.

## Why this exists

Incremental refresh can hide risk. If closed partitions are changed upstream, a normal incremental run might produce inconsistent downstream outputs unless changes are explicitly reviewed.

## Snapshot model

`build_partition_snapshot(...)` produces one JSON-safe row per partition with:

- dataset and table metadata
- partition identifier
- row and business key counts
- min/max watermark (optional)
- deterministic business key hash
- deterministic partition hash

## Closed partition detection (MVP simplification)

- `closed_partition_grace_days = 0`: all baseline partitions are closed
- parseable date partition: partition is closed if older than `UTC today - grace_days`
- non-date partition: treated as closed

## Default behavior

`compare_partition_snapshots(...)` blocks changed historical partitions by default and returns a structured result with:

- `status`: `passed`, `warning`, or `failed`
- `can_continue`: bool
- `changes`: drift records
- `summary` and applied `policy`

## Backfill and approval override

- `run_mode="backfill"` allows historical changes but emits warnings
- `allow_historical_changes=True` can allow changes
- when approval is required, provide `approval_reference` or the result blocks

## Pandas and Spark behavior

- pandas path is for local/small data and tests
- spark path uses native Spark aggregations and collects only final partition rows
- the framework never auto-converts Spark DataFrames to pandas

## Pipeline placement

Run this check after source ingestion and before transform/write, so unsafe incremental runs fail early.

```python
from fabric_data_product_framework.drift import (
    build_partition_snapshot,
    compare_partition_snapshots,
    assert_incremental_safe,
)

current_snapshots = build_partition_snapshot(
    df_source,
    dataset_name=ctx["dataset_name"],
    table_name=ctx["source_table"],
    partition_column="business_date",
    business_keys=["customer_id", "order_id"],
    watermark_column="updated_at",
    run_id=ctx["run_id"],
    engine="spark",
)

result = compare_partition_snapshots(
    baseline_snapshots=previous_accepted_snapshots,
    current_snapshots=current_snapshots,
)

assert_incremental_safe(result)
```
