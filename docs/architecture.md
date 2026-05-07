# FabricOps operating architecture

![Generic platform architecture for FabricOps Starter Kit](assets/data-platform-architecture.png)

*Figure: A generic platform shape with source systems, development and production workspaces, layered data stores, and governed consumption outputs.*

## Why this architecture exists

FabricOps Starter Kit supports the canonical 10-step lifecycle workflow in Microsoft Fabric where teams move data from source systems to governed, consumption-ready outputs.

In practice, Fabric projects read from and write to multiple lakehouses, warehouses, files, workspaces, and environments. A Fabric notebook usually runs with one default attached item, so reusable configuration and path resolution helpers are needed to make cross-store and cross-environment data movement reliable and repeatable.

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

For environment promotion controls, see [Deployment and Promotion](deployment-and-promotion.md). For contract editing and storage behavior, see [Metadata and Contracts](metadata-and-contracts.md).


## Explore detailed architecture subpages

For implementation-level details, use these focused pages:

- [Storage & Metadata Model](architecture/storage-model.md) explains where metadata, contracts, profiles, data quality results, lineage, and runtime artifacts live.
- [Fabric-native Data Quality](architecture/dqx-inspired-fabric-native-dq.md) describes the Fabric-native DQ operating pattern inspired by DQX.

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

Function-level behavior stays in API/reference documentation, while this page stays focused on platform shape. For lifecycle sequencing and actor ownership, see [Lifecycle Operating Model](lifecycle-operating-model.md).
