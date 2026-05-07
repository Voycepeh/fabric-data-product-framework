# FabricOps operating architecture

![Generic platform architecture for FabricOps Starter Kit](../assets/data-platform-architecture.png)

*Figure: A generic platform shape with source systems, development and production workspaces, layered data stores, and governed consumption outputs.*

FabricOps Starter Kit is a Fabric-native operating model for repeatable
 data product delivery. It combines local engineering discipline with
notebook-first execution so teams can move from exploration to governed
production handover without changing platforms.

## Why this architecture exists

FabricOps Starter Kit supports the canonical 10-step lifecycle workflow in Microsoft Fabric where teams move data from source systems to governed, consumption-ready outputs.

In practice, Fabric projects read from and write to multiple lakehouses,
warehouses, files, workspaces, and environments. A Fabric notebook
usually runs with one default attached item, so reusable configuration
and path resolution helpers are needed to make cross-store and
cross-environment data movement reliable and repeatable.

## The end-to-end story

1. **Develop locally in VS Code.**
   Engineers build and test reusable logic in the Python package, alongside contracts and documentation.
2. **Build the wheel.**
   The package is built as a wheel so the same tested code can be installed in Fabric.
3. **Install in a Fabric Environment.**
   Fabric Environments pin the framework and dependencies for consistent notebook execution.
4. **Configure runtime context in `00_env_config`.**
   Notebook runs initialize environment-specific settings before pipeline logic begins.
5. **Run exploration notebooks.**
   Teams profile sources, inspect schemas, and capture context needed for data product decisions.
6. **Run pipeline contract notebooks.**
   Contract-driven notebooks validate source assumptions, apply transformation logic, and write outputs.
7. **Persist across Source, Unified, and Product stores.**
   Data flows from source-aligned ingestion to unified modeling and product-ready datasets.
8. **Capture metadata tables.**
   Profiling, schema state, lineage, DQ results, summaries, and run context are written as durable metadata.
9. **Maintain a DQ rule registry.**
   Candidate and approved rules are stored centrally and reused by execution notebooks.
10. **Keep AI in the loop with human accountability.**
    AI suggests rule candidates, classifications, summaries, and context packaging; humans approve before rules become enforceable.
11. **Enforce in pipelines.**
    Approved rules run during notebook pipelines, with failed rows and quality metrics persisted for auditability.
12. **Monitor through Warehouse or Power BI.**
    SQL-friendly monitoring views and BI models expose operational and governance status.
13. **Complete handover with documentation.**
    Teams publish run summaries and architecture-aware documentation for downstream owners.

## Platform shape

The operating shape aligns to four layers.

### 1) Multiple source systems

Typical source inputs include:

- enterprise lakehouses
- warehouses
- files and object storage
- APIs
- SharePoint
- manual file drops
- other upstream systems

### 2) Development workspace

Development is where notebooks, rules, profiling, and transformations are tested before release. It uses a three-layer store pattern:

- **Source** (or **Raw**) for source-aligned landing data
- **Unified** (or **Bronze/Silver** depending on team naming) for cleaning, standardization, and reusable logic
- **Product** (or **Gold**) for validated, consumption-ready development outputs

### 3) Production workspace

Production runs the same Source → Unified → Product pattern so promotion remains consistent and auditable:

- **Source / Raw**
- **Unified / Bronze-Silver**
- **Product / Gold**

This mapping keeps transformation intent understandable across teams even when naming conventions differ.

### 4) Consumption outputs

Production-ready outputs are consumed through:

- Power BI semantic models, dashboards, and reports
- downstream applications and agents
- exports and integration feeds
- handover packs for support and ownership transition

## Metadata store

Source, Unified, and Product stores hold business data. FabricOps metadata should live in a dedicated metadata target that holds framework evidence, including:

- contracts and contract versions
- contract column definitions
- approved data quality rules
- approved classifications
- run logs and dataset run evidence
- quality execution results
- lineage records
- handover records

Each environment should have its own metadata target. Development metadata and production metadata must remain separate.

For environment promotion controls, see [Deployment and Promotion](../deployment-and-promotion.md). For contract editing and storage behavior, see [Metadata and Contracts](../metadata-and-contracts.md).

## Core design principles

- **Fabric-native execution:** notebooks and Fabric storage are first-class, not afterthoughts.
- **Reusable logic, explicit orchestration:** package code handles repeatable logic while notebooks stay readable and operational.
- **AI-assisted, human-approved governance:** AI accelerates suggestion and summarization, but humans remain accountable for approval and enforcement decisions.
- **Monitoring by default:** metadata and DQ outputs are persisted in forms suitable for Warehouse SQL and Power BI.
- **Handover-friendly delivery:** architecture and run artifacts are organized so first-time readers can understand the operating model before diving into function-level references.

## Explore detailed architecture subpages

- Read the [Storage model](storage-model.md) page for responsibility boundaries across Lakehouse, Warehouse, files, environments, and notebooks.
- Read the [Data quality architecture](data-quality-architecture.md) page for the AI-in-the-loop quality lifecycle and governance flow.

## Cross-cutting controls

Across all layers, the framework keeps execution governed with reusable controls:

- orchestration and run control
- metadata capture
- lineage notes and run traceability
- data quality rule generation and validation
- governance and approved usage context
- monitoring and operational evidence
- security-aware configuration and path handling

## Where functions fit

Function-level behavior stays in API/reference documentation, while this page stays focused on platform shape. For lifecycle sequencing and actor ownership, see [Lifecycle Operating Model](../lifecycle-operating-model.md). For callable details, see the [Function Reference](../reference/index.md).
