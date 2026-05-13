# FabricOps Starter Kit

FabricOps Starter Kit is a lightweight, Fabric-first, metadata-led, AI-assisted notebook operating model for governed data products.

<div class="center-cta">
  <a class="md-button md-button--primary" href="quick-start.md">Start with Quick Start</a>
  <a class="md-button" href="reference/index.md">Browse Functions</a>
</div>

## Lifecycle workflow

![Role-Based Lifecycle Workflow](assets/mvp-flow.png)

Governance stewards define agreement context and approved usage.

Analysts profile source data and validate business meaning and DQ rule validity.

Engineers enforce approved metadata through deterministic pipeline contracts.

Handover is generated from approved metadata, lineage, quality results, and runtime evidence.

- [Lifecycle Operating Model](lifecycle-operating-model.md)

## Notebook model

The notebook model separates responsibilities while preserving a single metadata trail across the lifecycle:

- **00_env_config** defines environment paths once per workspace.
- **01_data_sharing_agreement** captures approved usage, restrictions, and governance context.
- **02_ex** notebooks are analyst / data scientist exploration notebooks for profiling, business meaning, AI-assisted DQ suggestions, and AI-assisted classification suggestions.
- **03_pc** notebooks are engineer-owned pipeline contracts that enforce approved metadata, DQ rules, checks, lineage, and outputs.

- [Notebook Structure](notebook-structure.md)
- [Quick Start](quick-start.md)

## Data contract assembly

![Data contract assembly from approved metadata evidence](assets/data-contract.png)

A FabricOps data contract is assembled from approved metadata evidence, not manually typed from scratch. It combines dataset purpose, schema/profile, DQ rules and results, governance classification, drift checks, lineage, runtime summary, ownership, and approvals.

- [Metadata and Contracts](metadata-and-contracts.md)

## Choose where to go next

| Topic | Go to |
| --- | --- |
| Platform and design foundations | [Architecture](architecture.md) |
| Promote from validation to governed release | [Deployment and Promotion](deployment-and-promotion.md) |
| Install the package in Fabric notebooks | [Fabric Wheel Install](setup/fabric-wheel-install.md) |
| Explore public callable APIs | [Functions](reference/index.md) |
