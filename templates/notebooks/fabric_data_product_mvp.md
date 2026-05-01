# Fabric data product MVP notebook template

This guide explains how to use `fabric_data_product_mvp.py` as a readable,
copy-paste starter for a Fabric-first MVP workflow.

## 13-step MVP alignment

The starter aligns to the same high-level sequence:

1. Define data product context and runtime parameters.
2. Read source data safely.
3. Profile source data.
4. Explore and inspect source quality.
5. Explain transformation intent.
6. Apply transformation logic.
7. Produce output DataFrame.
8. Generate and run DQ checks.
9. Perform human review on DQ outcomes.
10. Generate governance suggestions.
11. Perform human governance approvals.
12. Generate lineage and transformation summary artifacts.
13. Produce handover-ready outputs.

## Safety defaults

- `DRY_RUN = True` by default.
- Writer stub skips writes in dry-run mode.
- Reader/writer stubs must be replaced intentionally.

## How to use

1. Copy the starter into a Fabric notebook.
2. Keep `DRY_RUN = True` for first execution.
3. Replace `fabric_reader()` with your source read logic.
4. Replace `transform()` with your transformation logic.
5. Replace `fabric_writer()` only after validating dry-run behavior.
6. Run end-to-end and review profile, DQ, governance, and lineage outputs.

## Related references

- `templates/notebooks/README.md`
- `docs/recipes/index.md`
- `src/README.md`
