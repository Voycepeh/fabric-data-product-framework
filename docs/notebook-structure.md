# Notebook Structure

![Workspace notebook setup](assets/notebook-structure.png)

*Figure: Notebook organization in a Fabric workspace, linking shared configuration and agreement context to exploration and production pipeline notebooks.*

Notebook structure should follow the end-to-end delivery flow, not isolated utility functions.

## How the structure supports the lifecycle

A well-structured notebook sequence keeps implementation and governance aligned:

1. **Purpose**: define business intent and approved usage context.
2. **Config**: load reusable environment and runtime configuration.
3. **Ingestion**: declare source inputs and ingest data.
4. **Exploration/profiling**: profile and inspect source behavior.
5. **Core transformation**: build and explain transformation logic.
6. **Standardization**: apply reusable cleaning rules and technical columns.
7. **Output**: publish validated output tables/files.
8. **Metadata**: write run evidence and governance metadata.
9. **Lineage**: capture upstream/downstream traceability notes.
10. **Handover**: produce concise summaries and support artifacts.

## Notebook role guidance

- Use shared environment/config notebooks to avoid repeating runtime setup.
- Keep exploration notebooks separate from scheduled operational notebooks.
- Keep pipeline notebooks executable end to end so validation, publish, metadata, lineage, and handover are produced in one governed run.

For architecture boundaries, see [Architecture](architecture.md). For full flow sequencing, see [Lifecycle Operating Model](lifecycle-operating-model.md).

## Core notebook responsibilities

### `00_env_config`

- Defines Source, Unified, Product, and Metadata targets for the current environment.
- Should remain environment-local (dev config in dev, prod config in prod).
- Must not accidentally point production notebooks to development stores.

### `01_data_sharing_agreement_<agreement>`

- Captures governance-approved purpose, allowed usage, ownership, and restrictions.
- Links notebook execution to an approved agreement record before implementation begins.
- Provides the business guardrails used by both exploration and production pipeline notebooks.

### `02_ex_<agreement>_<topic>`

- Profiles source data and explains the transformation *why*.
- Drafts source input contract expectations and proposed metadata records.
- Reviews AI-suggested DQ rules and classifications (advisory only).
- Records approved contract metadata only after human/steward approval.

### `03_pc_<agreement>_<topic>`

- Loads approved contract metadata records from the metadata target.
- Enforces required columns, business keys, approved DQ rules, classifications, and runtime standards.
- Writes controlled outputs plus profiling/run/lineage evidence.
- Must be run-all-safe for governed operations.

> Exploration explains the why. Pipeline enforces the approved what.

## Related documentation

- Contract metadata model details: [Metadata and Contracts](metadata-and-contracts.md).
- Promotion of notebooks and metadata: [Deployment and Promotion](deployment-and-promotion.md).
- Business lifecycle responsibilities: [Lifecycle Operating Model](lifecycle-operating-model.md).
- Platform boundaries and stores: [Architecture](architecture.md).
