# FabricOps Starter Kit

FabricOps Starter Kit is a lightweight, Fabric-first, metadata-led, AI-assisted notebook operating model for governed data products.

Use this page as the front door into the core FabricOps workflow.

<div class="center-cta">
  <a class="md-button md-button--primary" href="quick-start/">Start with Quick Start</a>
  <a class="md-button" href="reference/">Browse Functions</a>
</div>

## 1. Lifecycle workflow

FabricOps starts with a clear operating workflow.

Governance defines approved usage and business context. Analysts profile source data, validate business meaning, and prepare AI-assisted suggestions. Engineers enforce approved metadata through repeatable pipeline contracts. Handover is generated from approved metadata, lineage, quality results, and runtime evidence.

![FabricOps lifecycle operating model overview](assets/mvp-flow.png)

<div class="center-cta">
  <a class="md-button" href="lifecycle-operating-model/">View Lifecycle Operating Model</a>
</div>

## 2. Notebook model

FabricOps keeps the notebook structure simple so ownership is clear.

![FabricOps governance and workspace model](assets/notebook-structure.png)

| Notebook | Purpose |
|---|---|
| `00_env_config` | Defines environment paths, workspace settings, and shared reusable configuration once per workspace. |
| `01_data_sharing_agreement_<agreement>` | Captures approved usage, restrictions, business context, ownership, and governance context for the agreement. |
| `02_ex_<agreement>_<topic>` | Supports analyst and data scientist exploration, profiling, business meaning validation, AI-assisted DQ suggestions, and AI-assisted classification suggestions. |
| `03_pc_<agreement>_<pipeline>` | Acts as the engineer-owned pipeline contract. It is run-all-safe, schedulable, and enforces approved metadata, DQ rules, checks, lineage, and outputs. |

<div class="center-cta">
  <a class="md-button" href="notebook-structure/">View Notebook Structure</a>
</div>

## 3. How the data contract is assembled

A FabricOps data contract is assembled from approved metadata evidence. It is not manually written from scratch.

The contract combines approved usage, schema and profile evidence, DQ rules and results, governance classification, drift checks, lineage, runtime summaries, ownership, and approvals.

![Data contract assembly from approved metadata evidence](assets/data-contract.png)

<div class="center-cta">
  <a class="md-button" href="metadata-and-contracts/">View Metadata and Contracts</a>
</div>

## 4. Choose where to go next

These pages provide supporting detail beyond the core workflow above.

| Page | Use it when you want to |
|---|---|
| [Architecture overview](architecture/) | Understand the wider FabricOps platform shape and data flow. |
| [Deployment and promotion](deployment-and-promotion/) | Understand how work moves from development to production. |
| [Fabric wheel install](setup/fabric-wheel-install/) | Install the package into Fabric notebooks. |
