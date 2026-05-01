# Fabric data product MVP notebook template

This page explains how to use
`templates/notebooks/fabric_data_product_mvp.py` as a safe,
copy-pasteable starter for Microsoft Fabric.

The default mode is `DRY_RUN = True`, so a first run does not write
production outputs.

## Recommended first-run path

1. Open `templates/notebooks/fabric_data_product_mvp.py`.
2. Create a new Fabric notebook.
3. Copy/paste the template into Fabric.
4. Confirm the parameter block keeps `DRY_RUN = True`.
5. Run all cells to validate this sequence:
   profile → DQ → governance → lineage → handover.
6. Replace the transformation section marker with domain logic.
7. Replace Fabric adapters (`fabric_reader`, `fabric_writer`) only after
   dry run succeeds.

## What the template covers (13-step sequence)

1. Define data product.
2. Setup config and environment.
3. Declare source and ingest data.
4. Profile source and capture metadata.
5. Explore data.
6. Explain transformation logic.
7. Build transformation pipeline (replace-section marker included).
8. AI generate DQ rules (Copilot prompt block included).
9. Human review DQ rules.
10. AI suggest sensitivity labels (Copilot prompt block included).
11. Human review and governance gate.
12. AI generated lineage and transformation summary
    (Copilot prompt block included).
13. Handover framework pack (Copilot prompt block included)
    plus final run summary cell.

## Parameter and safety behavior

The starter has a clear parameter block at the top:

- `DRY_RUN` (default `True`)
- `ENVIRONMENT`
- `RUN_ID`
- `SOURCE_TABLE`
- `TARGET_TABLE`
- `NOTEBOOK_NAME`
- `APPROVED_USAGE`

Safety defaults:

- In dry run, source data is synthetic and local/Fabric-safe.
- In dry run, output stays in-memory (no production write).
- Production-like reads/writes require explicit replacement of adapter
  placeholders.

## Human vs framework responsibilities

The template includes a dedicated section clarifying responsibilities:

- **Human fills this in**: business context, source/target bindings,
  transformation logic, and approvals.
- **Framework generates this**: profiles, DQ execution outputs,
  governance suggestions, lineage shape, and validation checks.

## Related pages

- `templates/notebooks/README.md`
- `docs/fabric-smoke-test.md`
- `docs/mvp-workflow.md`
- `src/README.md`
