# Fabric data product MVP notebook template

This guide explains how to use `fabric_data_product_mvp.py` as a runnable, end-to-end Fabric MVP flow after attaching an Environment with the installed framework wheel.

## Lifecycle flow (run-all)

The template keeps one contract lifecycle in a single notebook flow:

1. Package and environment verification.
2. Runtime parameters (safe defaults).
3. Source declaration (sample mode by default).
4. Source profiling and metadata preview.
5. AI-assisted DQ rule candidates (with deterministic fallback).
6. Human approval checkpoint for DQ rules.
7. DQ validation and failure summary.
8. Drift guard checkpoints (baseline + compare model).
9. Transformation and technical columns.
10. Output profiling.
11. Governance classification suggestions (human approval required).
12. Lineage records and transformation summary.
13. Target write gate (disabled by default).
14. Run summary and AI handover context export.
15. Final release gate (`READY_FOR_FABRIC_WRITE` / `NOT_READY`).

## Safety defaults

- `USE_SAMPLE_DATA = True` by default.
- `ENABLE_FABRIC_WRITES = False` by default.
- AI-assisted flags default to `False` and deterministic fallback behavior remains runnable.
- Human approval remains explicit for DQ thresholds, governance labels, and release readiness.

## Related references

- `templates/notebooks/README.md`
- `docs/workflows/fabric-notebook-template.md`
- Generated function reference: `docs/reference/`
