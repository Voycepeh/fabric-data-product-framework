# Notebook templates

This folder contains reusable notebook starters for Microsoft Fabric workflows.

## Included files

- `fabric_data_product_mvp.py`: primary MVP starter notebook template.
- `fabric_data_product_mvp.md`: usage notes aligned to the 13-step MVP flow.

## Design goals

- Keep a DRY_RUN-first setup for safe initial execution.
- Keep profile -> DQ -> governance -> lineage -> handover sequence explicit.
- Keep clear separation between human-authored logic and framework outputs.
- Keep notebook content copy-pasteable and readable in raw GitHub view.

## Suggested usage

1. Start with the local-safe recipe from `docs/recipes/local-safe-smoke.md`.
2. Move to `fabric_data_product_mvp.py` in a Fabric notebook.
3. Replace reader/writer stubs and transformation logic.
4. Keep validation and governance review checkpoints before enabling writes.

## Package-based usage in Fabric

For reusable notebook execution, build and upload the framework wheel to a Fabric Environment first, then attach that Environment to your notebook and import from `fabric_data_product_framework`. Prefer this over long-term `%run 00_config`-style helper sharing, which can remain only as a legacy fallback during migration.
