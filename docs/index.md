# FabricOps Starter Kit

FabricOps Starter Kit helps teams build **governed, quality-checked, AI-ready Microsoft Fabric notebooks**.

It moves teams from exploration to controlled pipeline delivery with reusable metadata, DQ evidence, lineage, and handover artifacts.

[Quick Start](quick-start.md){ .md-button .md-button--primary }

[Lifecycle Operating Model](lifecycle-operating-model.md){ .md-button }

![FabricOps workspace notebook structure](assets/notebook-structure.png)

_Exploration explains the why. Pipeline contract notebooks enforce the approved what._

## Navigate by goal

### New user

- [Quick Start](quick-start.md)
- [Notebook Structure](notebook-structure.md)

### Understand the operating model

- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Architecture](architecture.md)

### Build governed pipelines

- [Storage & Metadata Model](architecture/storage-model.md)
- [Metadata and Contracts](metadata-and-contracts.md)
- [Fabric-native Data Quality](architecture/dqx-inspired-fabric-native-dq.md)

### Developer reference

- [Function Reference](reference/index.md)
- [Fabric Wheel Install](setup/fabric-wheel-install.md)

## Workflow at a glance

1. `00_env_config` sets shared runtime and storage configuration.
2. Exploration notebooks profile data and draft AI-assisted suggestions.
3. Pipeline contract notebooks enforce approved decisions.
4. Metadata, DQ results, lineage, and handover artifacts are written as controlled outputs.

Exploration is where profiling and AI suggestions happen. Pipeline contract notebooks are where approved governance and quality decisions are enforced.

## AI in the loop

- AI suggests metadata summaries, DQ rules, sensitivity classification, lineage, and handover notes.
- Humans approve governance and quality decisions.
- Pipeline notebooks enforce approved rules and write controlled outputs.

## What you get

| Output | Purpose |
| --- | --- |
| Reusable config notebook | Standardizes environment and execution settings. |
| Exploration notebook pattern | Supports profiling and decision preparation. |
| Pipeline contract notebook | Executes approved rules in controlled pipelines. |
| Metadata tables | Capture reusable contracts and context. |
| DQ results | Record quality evidence for review and operations. |
| Lineage and handover documentation | Preserve traceability and team handover context. |

## Compatibility note

The Python package import path remains `fabricops_kit`.
