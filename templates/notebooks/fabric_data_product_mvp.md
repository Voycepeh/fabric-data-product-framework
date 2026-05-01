# Fabric data product MVP notebook template

This guide explains how to use `fabric_data_product_mvp.py` as a runnable Fabric MVP workflow after attaching an Environment with the installed framework wheel.

## Canonical 13-step flow (run-all)

1. Define dataset purpose and steward.
2. Setup config and environment.
3. Declare source and ingest data.
4. Profile source and capture metadata.
5. Explore data.
6. Explain transformation logic.
7. Build transformation pipeline.
8. AI-generate DQ rules.
9. Human review DQ rules.
10. AI suggest sensitivity labels.
11. Human review and governance gate.
12. AI-generated lineage and transformation summary.
13. Run summary and handover pack.

## Safety defaults

- `USE_SAMPLE_DATA = True` by default.
- `ENABLE_FABRIC_WRITES = False` by default.
- AI-assisted flags default to `False` with deterministic fallback behavior.
- Human approval remains explicit for DQ thresholds, governance labels, and release readiness.

## Related references

- `templates/notebooks/README.md`
- `docs/quick-start.md`
- `docs/mvp-workflow.md`
