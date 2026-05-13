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

See [Metadata and Data Contract Assembly](metadata-and-contracts/) for the assembled contract model and metadata tables.

## Choose where to go next

| Topic | Go to |
| --- | --- |
| End-to-end role flow from stewardship to handover | [Lifecycle Operating Model](lifecycle-operating-model/) |
| Notebook ownership, governance flow, and environment usage | [Notebook Structure](notebook-structure/) |
| Metadata-backed contract assembly and export path | [Metadata and Data Contract Assembly](metadata-and-contracts/) |
| Public callable catalogue and API usage | [Function Reference](reference/) |

- **00_env_config** defines environment paths once per workspace.
- **01_data_sharing_agreement** captures approved usage, restrictions, and governance context.
- **02_ex** notebooks are analyst / data scientist exploration notebooks for profiling, business meaning, AI-assisted DQ suggestions, and AI-assisted classification suggestions.
- **03_pc** notebooks are engineer-owned pipeline contracts that enforce approved metadata, DQ rules, checks, lineage, and outputs.

- [Notebook Structure](notebook-structure.md)
- [Quick Start](quick-start.md)

- Governance stewards define agreement context and approved usage once.
- Analysts validate source meaning and DQ rule validity.
- Engineers enforce approved metadata through deterministic pipeline contracts.
- Handover is generated from approved metadata, lineage, quality results, and runtime evidence.
