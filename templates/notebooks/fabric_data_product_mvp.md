# Fabric data product MVP notebook template

Use `templates/notebooks/fabric_data_product_mvp.py` as a copy/paste starter for Microsoft Fabric notebooks.

## How to use

1. Create a new Fabric notebook.
2. Copy the template script into notebook cells (or import it as a `.py` notebook source).
3. Replace `DATASET_CONTRACT_PATH` with your contract file path.
4. Set the notebook parameters (`WORKSPACE`, `LAKEHOUSE`, `SOURCE_TABLE`, `TARGET_TABLE`, `ENVIRONMENT`, `DRY_RUN`, `PROFILE_ONLY`).

## Wire adapters

Replace placeholder adapters with your implementation:
- `fabric_reader(table_identifier)`
- `fabric_table_writer(df, table_identifier, mode="append", **options)`
- `metadata_writer(records, table_identifier, mode="append", **options)`

This keeps the framework generic and portable.

## Where to implement transformations

Edit only the user block:

- `# USER TRANSFORMATION START`
- `# USER TRANSFORMATION END`

Keep EDA/debug-only cells out of scheduled runs (freeze or remove them).

## Metadata output mapping

`write_multiple_metadata_outputs` writes each output key to a mapped table:
- `dataset_runs`
- `column_profiles`
- `schema_snapshots`
- `schema_drift_results`
- `quality_results` (optional for future use)

Adjust `metadata_table_mapping` to your environment.

## Dry run and profile-only modes

- `DRY_RUN=True`: skips target writes and metadata writes.
- `PROFILE_ONLY=True`: bypasses transformation logic and profiles source-like output.

## Lifecycle alignment

The template maps directly to the 14-stage framework lifecycle from contract validation through metadata outputs and run summary.
