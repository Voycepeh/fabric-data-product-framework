# Fabric smoke test (first end-to-end run path)

## Purpose
This guide provides the first practical end-to-end smoke test path for running the framework in a Microsoft Fabric notebook with minimal custom wiring.

## Prerequisites
- A Microsoft Fabric workspace and Lakehouse.
- A small synthetic or otherwise safe source table.
- The framework package available to the notebook runtime.
- A dataset contract YAML file available to the notebook.
- Metadata tables created (see [metadata-table-bootstrap.md](metadata-table-bootstrap.md)).

## Recommended first run mode
Use these settings for the first validation run:
- `DRY_RUN = True`
- `PROFILE_ONLY = False`
- Start with a small source table.
- Avoid production target tables on the first run.

## Adapter wiring
Use the copyable notebook adapter functions from `templates/fabric_adapters.py`:
- `fabric_reader(table_identifier)`
- `fabric_table_writer(df, table_identifier, mode="append", **options)`
- `metadata_writer(records, table_identifier, mode="append", **options)`
- `metadata_writer_with_schema_hint(records, table_identifier, mode="append", **options)`

These functions rely on notebook-provided `spark` and do not define or import a Spark session.

## Minimal execution flow
1. Load and validate dataset contract.
2. Build runtime context.
3. Read source table using adapter.
4. Profile source and shape metadata records.
5. Execute gates (schema drift, incremental safety, DQ, contract validation).
6. Write target table only when gates pass.
7. Write metadata outputs.
8. Review run summary and metadata tables.

## Troubleshooting
- **Import error**: ensure framework package is available in notebook environment.
- **Table identifier error**: verify `schema.table` or `lakehouse.schema.table` naming.
- **`createDataFrame` inference errors**: use `metadata_writer_with_schema_hint` for nested fields.
- **Schema drift blocks write**: update contract/allowed policy or baseline snapshot process.
- **DQ failure**: inspect failing rule rows in `metadata.quality_results`.
- **Contract mismatch**: compare expected vs actual columns and nullability.
- **Metadata table not found**: run bootstrap steps before notebook run.

## Safety recommendations
- Run in dev/sandbox first.
- Prefer synthetic/safe source tables.
- Start with dry run.
- Confirm metadata rows before scheduled execution.

## Related files
- `docs/metadata-table-bootstrap.md`
- `examples/fabric_smoke_test/`
- `templates/notebooks/fabric_data_product_mvp.md`
