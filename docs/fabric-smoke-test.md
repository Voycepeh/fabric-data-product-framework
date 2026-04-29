# Fabric smoke test (first end-to-end run path)

Use this in-Fabric check for runtime behavior that cannot be validated locally.

## What Fabric testing covers
- PySpark execution path in notebook runtime.
- Lakehouse/OneLake read and write behavior.
- Notebook adapter wiring and `notebookutils` usage where applicable.
- Fabric AI function usage at execution time.
- Larger-scale profiling and end-to-end notebook smoke execution.

## Prerequisites
- Fabric workspace and Lakehouse.
- Small synthetic/safe source table.
- Framework package available in notebook environment.
- Dataset contract YAML available to the notebook.
- Metadata tables created (see [metadata-table-bootstrap.md](metadata-table-bootstrap.md)).

## Recommended first run mode
- `DRY_RUN = True`
- `PROFILE_ONLY = False`
- Small non-production source/target tables

## Minimal execution flow
1. Load and validate dataset contract.
2. Build runtime context.
3. Read source table via notebook adapters.
4. Run source profiling and metadata record shaping.
5. Run schema drift, incremental safety, DQ, and contract checks.
6. Write target only when gates pass.
7. Persist metadata outputs.
8. Review run summary and lineage/handover artifacts.

## Adapter wiring
Use `templates/fabric_adapters.py` wrappers:
- `fabric_reader(table_identifier)`
- `fabric_table_writer(df, table_identifier, mode="append", **options)`
- `metadata_writer(records, table_identifier, mode="append", **options)`
- `metadata_writer_with_schema_hint(records, table_identifier, mode="append", **options)`

## Related docs
- Local-only checks: [local-smoke-test.md](local-smoke-test.md)
- Lifecycle flow: [lifecycle-operating-model.md](lifecycle-operating-model.md)
