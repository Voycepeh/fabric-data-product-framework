# Storage model

This page explains where FabricOps Starter Kit artifacts should live so delivery remains repeatable, auditable, and easy to hand over.

## Overview

The storage model separates responsibilities across:

- **Lakehouse** for operational data and execution-adjacent metadata.
- **Warehouse** for SQL-first monitoring and BI consumption.
- **Repository files** for versioned contracts and documentation artifacts.
- **Fabric Environments** for runtime dependency control.
- **Notebooks** for orchestration and execution checkpoints.

Keeping these boundaries clear prevents operational drift and reduces ambiguity for first-time maintainers.

## Lakehouse responsibilities

Lakehouse is the primary persistence layer for pipeline execution and operational state.

Recommended contents:

1. Raw or bronze source-aligned tables.
2. Curated product-facing Lakehouse tables.
3. Metadata tables such as:
   - profile records,
   - schema snapshots,
   - partition snapshots,
   - DQ results,
   - DQ rule registry,
   - governance suggestions,
   - lineage,
   - run summaries,
   - quarantine rows.

JSON payload columns are acceptable for flexible or evolving metadata structures. For stable operational reporting, flatten high-value fields into explicit columns.

## Warehouse responsibilities

Warehouse is the SQL-friendly monitoring and serving layer. It is not a requirement to duplicate every Lakehouse curated table physically into Warehouse.

Use Warehouse for:

1. Reporting views over metadata and run-state tables.
2. Governance and DQ monitoring datasets.
3. Power BI semantic model sources.
4. Optional SQL-first serving tables/views for downstream consumers.

## Files and repository assets

The repository is the source of truth for versioned, human-reviewed artifacts.

Recommended contents:

1. Contract YAML files.
2. Example JSON rule payloads.
3. Markdown runbooks and handover notes.
4. Build outputs managed intentionally (for example, local `dist/` outputs should not be committed unless explicitly required).

## Fabric Environment responsibilities

Fabric Environments provide dependency consistency across notebook execution.

Use them to:

1. Install the locally built framework wheel.
2. Pin framework/runtime dependency versions.
3. Reuse consistent runtime configuration across related notebooks.

## Notebook responsibilities

Notebooks should stay orchestration-focused and explicit.

Typical responsibilities:

1. Load parameters and runtime context.
2. Execute source profiling.
3. Stage DQ candidate generation inputs.
4. Support human review checkpoints.
5. Run approved DQ checks.
6. Apply transformations.
7. Write target data outputs.
8. Persist metadata and run summaries.
9. Export AI context and summary artifacts for monitoring and handover.

## What should not live here

To keep responsibilities clear, avoid placing these in the wrong layer:

- Do not treat notebooks as long-term system-of-record storage.
- Do not keep approval-only governance decisions in ad hoc local files.
- Do not store curated operational monitoring solely in notebook markdown outputs.
- Do not bypass the rule registry with hidden one-off DQ logic when pipeline enforcement is expected.
- Do not rely on unpinned runtime dependencies when reproducibility is required.
