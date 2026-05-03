# Schema Drift

Schema drift is any structural change between a baseline schema and the schema observed in the current pipeline run.

## Why schema drift matters for Fabric notebook pipelines

Notebook pipelines often assume fixed columns, data types, and ordering. Upstream schema changes can break joins, transformations, write operations, or downstream semantic models. Early schema drift checks provide a safety gate before costly pipeline stages.

## How schema snapshots work

`build_schema_snapshot` creates a JSON-safe snapshot from a pandas DataFrame with:

- `dataset_name`
- `table_name`
- `generated_at` (UTC ISO timestamp)
- `columns`

Each column record includes:

- `column_name`
- `ordinal_position`
- `data_type` (pandas dtype string)
- `nullable` (whether nulls are present)
- `column_hash` (deterministic hash from name, ordinal, dtype, nullable)


## Engine behavior (pandas and Spark)

- Use pandas mode for local/small datasets, tests, and laptop workflows.
- Use Spark mode for Fabric-scale/lakehouse workloads.
- `build_schema_snapshot(..., engine="auto")` detects `pandas` or `spark` defensively.
- The framework must never auto-convert Spark DataFrames to pandas.
- Spark schema snapshots read `df.schema.fields` only and do not scan or collect data.
- Pandas `nullable` is observed from values with `isna().any()`.
- Spark `nullable` is taken from schema metadata (`field.nullable`).

## How comparison works

`compare_schema_snapshots` compares baseline and current snapshots and reports:

- `status`: `passed`, `warning`, or `failed`
- `can_continue`: pipeline gate decision
- `changes`: per-column drift events
- `summary`: counts by drift category and severity

Supported drift event types:

- `column_added`
- `column_removed`
- `data_type_changed`
- `nullable_changed`
- `ordinal_changed`

## Default blocking behavior

`default_schema_drift_policy` applies these rules:

- Removed column: block by default
- Data type changed: block by default
- Added column: warning + block (requires approval by default)
- Nullable changed: warning
- Ordinal changed: info (warning can be enabled)

Use `assert_no_blocking_schema_drift(result)` to raise `SchemaDriftError` when blocking drift is present.

## Future metadata integration

This output is designed to connect later to framework metadata tables:

- `metadata_schema_snapshots` for persisted baseline/current snapshots
- `metadata_schema_drift_results` for persisted comparison outcomes and policy decisions

## Incremental refresh protection

Schema drift gates reduce incremental refresh risk by preventing runs from proceeding when key columns are removed or types change. This catches structural breaks before incremental partition logic and data quality rule execution are applied.

## Example

```python
import pandas as pd
from fabricops_kit.drift import (
    SchemaDriftError,
    build_schema_snapshot,
    compare_schema_snapshots,
    assert_no_blocking_schema_drift,
)

baseline_df = pd.DataFrame({
    "customer_id": [1, 2],
    "order_amount": [10.0, 20.0],
})

current_df = pd.DataFrame({
    "customer_id": [1, 2],
    "order_amount": [10.0, 20.0],
    "new_status": ["paid", "pending"],
})

baseline = build_schema_snapshot(baseline_df, dataset_name="synthetic_orders", table_name="source_orders")
current = build_schema_snapshot(current_df, dataset_name="synthetic_orders", table_name="source_orders")

result = compare_schema_snapshots(baseline, current)

try:
    assert_no_blocking_schema_drift(result)
except SchemaDriftError as exc:
    print("Schema drift requires review:", exc)
```
