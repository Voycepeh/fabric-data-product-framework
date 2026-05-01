# Storage model (Fabric-native)

This page defines where framework artifacts live across Lakehouse, Warehouse, files, Fabric Environments, and notebooks.

## Lakehouse layer

Primary storage and execution-adjacent persistence:
1. Raw/bronze source tables.
2. Curated data product tables.
3. Metadata tables for:
   - profile records,
   - schema snapshots,
   - partition snapshots,
   - DQ results,
   - DQ rule registry,
   - governance suggestions,
   - lineage,
   - run summary,
   - quarantine rows.

JSON payload columns are acceptable for flexible metadata and evolving structures. For stable operational reporting, flatten key fields into explicit columns where useful.

## Warehouse layer

Consumption and monitoring surface:
1. SQL-friendly reporting views over metadata tables.
2. Governance and DQ monitoring views.
3. Source layer for Power BI semantic models.
4. Optional curated serving layer for downstream SQL-first consumers.

## Files and repository assets

Versioned artifacts and local development files:
1. Contract YAML files.
2. Example JSON rule payloads.
3. Markdown handover artifacts.
4. Local package build outputs (`dist/`) should not be committed unless explicitly required.

## Fabric Environment layer

Runtime dependency management:
1. Install custom wheel built locally.
2. Pin framework/runtime dependencies.
3. Reuse the same environment across related notebooks to keep execution consistent.

## Notebook layer

Execution/orchestration flow should remain thin and explicit:
1. Execution and orchestration.
2. Parameter loading.
3. Source profiling.
4. DQ candidate generation.
5. Human review cells.
6. DQ execution.
7. Transformation.
8. Target writes.
9. Metadata writes.
10. AI context and run summary export.
