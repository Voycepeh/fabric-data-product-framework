# Fabric data product MVP notebook template

This guide explains how to use `fabric_data_product_mvp.py` as a runnable, end-to-end Fabric lifecycle workflow after attaching an Environment with the installed framework wheel.

## Lifecycle flow (run-all)

Use the canonical 10-step order from the [Lifecycle Operating Model](../../docs/lifecycle-operating-model.md):

1. Purpose and governance ownership.
2. Runtime, environment, and path setup.
3. Source contract declaration and source ingestion.
4. Source contract validation and metadata profiling.
5. Exploration and transformation / DQ rationale capture.
6. Production transformation and target output write path.
7. Output validation and target metadata persistence.
8. AI-assisted DQ rule generation/review/configuration.
9. AI-assisted classification/sensitivity suggestion review.
10. AI-assisted lineage and handover documentation generation.

## Safety defaults

- `USE_SAMPLE_DATA = True` by default.
- `ENABLE_FABRIC_WRITES = False` by default.
- AI-assisted flags default to `False` and deterministic fallback behavior remains runnable.
- Human approval remains explicit for DQ thresholds, governance labels, and release readiness.

## Related references

- `templates/notebooks/README.md`
- `docs/workflows/fabric-notebook-template.md`
- Generated function reference: `docs/reference/`
