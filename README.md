# FabricOps Starter Kit

A practical starter kit for building governed, quality-checked, AI-ready notebooks in Microsoft Fabric.

Documentation: https://voycepeh.github.io/FabricOps-Starter-Kit/

## Start here

- [Quick Start](https://voycepeh.github.io/FabricOps-Starter-Kit/quick-start/)
- [Lifecycle Operating Model](https://voycepeh.github.io/FabricOps-Starter-Kit/lifecycle-operating-model/)
- [Architecture](https://voycepeh.github.io/FabricOps-Starter-Kit/architecture/)
- [Notebook Structure](https://voycepeh.github.io/FabricOps-Starter-Kit/notebook-structure/)
- [Metadata and Contracts](https://voycepeh.github.io/FabricOps-Starter-Kit/metadata-and-contracts/)
- [Function Reference](https://voycepeh.github.io/FabricOps-Starter-Kit/reference/)
- [Fabric Wheel Install](https://voycepeh.github.io/FabricOps-Starter-Kit/setup/fabric-wheel-install/)

## Why this starter kit exists

![Before vs after using the starter kit](docs/assets/before-after.png)

Fabric notebooks often begin as analysis work and then become recurring operations. This starter kit gives that transition a reusable structure for configuration, checks, governance review, lineage, and handover.

Read more: [Quick Start](https://voycepeh.github.io/FabricOps-Starter-Kit/quick-start/) · [Lifecycle Operating Model](https://voycepeh.github.io/FabricOps-Starter-Kit/lifecycle-operating-model/)

## What users get

![Benefits of the FabricOps Starter Kit](docs/assets/framework-benefits.png)

Teams get reusable patterns for profiling, quality checks, sensitivity review, lineage, metadata logging, and handover so these controls do not have to be rebuilt in every notebook.

Read more: [Function Reference](https://voycepeh.github.io/FabricOps-Starter-Kit/reference/) · [Metadata and Contracts](https://voycepeh.github.io/FabricOps-Starter-Kit/metadata-and-contracts/)

## How it fits into a Fabric data platform

![Generic data platform architecture](docs/assets/data-platform-architecture.png)

The kit supports repeatable notebook execution across development and production patterns, with explicit handling for cross-store and cross-workspace data flows.

Read more: [Architecture](https://voycepeh.github.io/FabricOps-Starter-Kit/architecture/)

## Notebook operating model

![Workspace notebook setup](docs/assets/notebook-structure.png)

The notebook model keeps shared runtime context clear: one environment config can support many agreements and notebooks, and one agreement can branch into multiple notebook paths.

Read more: [Notebook Structure](https://voycepeh.github.io/FabricOps-Starter-Kit/notebook-structure/)

## Canonical lifecycle workflow

![FabricOps Starter Kit canonical lifecycle workflow](docs/assets/mvp-flow.png)

The project follows a canonical 10-step lifecycle: governance-first, controlled engineering execution, then optional AI-assisted drafting and summarization.

Read more: [Lifecycle Operating Model](https://voycepeh.github.io/FabricOps-Starter-Kit/lifecycle-operating-model/)

## What problems it aims to solve

- Repetitive notebook setup and path handling.
- Non-reusable profiling and validation outputs.
- Slow, manual quality/governance drafting and review loops.
- Weak lineage and handover evidence for operational ownership transfer.

For contract behavior and storage, see [Metadata and Contracts](https://voycepeh.github.io/FabricOps-Starter-Kit/metadata-and-contracts/). For Fabric-native DQ architecture, see [Architecture > Fabric-native Data Quality](https://voycepeh.github.io/FabricOps-Starter-Kit/architecture/data-quality-architecture/).

## AI in the loop

AI assists with metadata summaries, data quality rule suggestions, sensitivity classification suggestions, lineage, and handover notes.
Humans approve governance and quality decisions.
Pipeline notebooks enforce approved decisions.

## Scope

This is a Fabric-first notebook starter kit.
It is not a full data platform, orchestration system, or governance product.
