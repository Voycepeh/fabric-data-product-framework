# FabricOps Starter Kit

FabricOps Starter Kit helps teams build **governed, quality-checked, AI-ready Microsoft Fabric notebooks**.

It moves teams from exploration to controlled pipeline delivery with reusable metadata, DQ evidence, lineage, and handover artifacts.

[Quick Start](quick-start.md){ .md-button .md-button--primary }

[Lifecycle Operating Model](lifecycle-operating-model.md){ .md-button }

## Framework at a glance

![FabricOps workspace notebook structure](assets/notebook-structure.png)

_Exploration explains the why. Pipeline contract notebooks enforce the approved what._

## Navigate by goal

| Goal | Start with |
| --- | --- |
| New user | [Quick Start](quick-start.md), [Notebook Structure](notebook-structure.md) |
| Understand the operating model | [Lifecycle Operating Model](lifecycle-operating-model.md), [Architecture](architecture/index.md) |
| Build governed pipelines | [Storage & Metadata Model](architecture/storage-model.md), [Metadata and Contracts](metadata-and-contracts.md), [Fabric-native Data Quality](architecture/data-quality-architecture.md) |
| Developer reference | [Function Reference](reference/index.md), [Fabric Wheel Install](setup/fabric-wheel-install.md) |

## Workflow at a glance

The workflow separates decision-making from enforcement:

- `00_env_config` defines reusable environment and storage settings.
- Exploration notebooks profile data, test assumptions, and draft AI-assisted suggestions.
- Approved contract metadata records required columns, DQ rules, classifications, and business keys.
- Pipeline contract notebooks enforce approved decisions and write controlled outputs.

## AI in the loop

AI suggests:

- metadata summaries
- DQ rules
- sensitivity classifications
- lineage and handover notes

Humans approve:

- governance decisions
- quality rules
- classifications
- release readiness

Pipelines enforce:

- approved contracts
- quality checks
- controlled outputs
- evidence capture

## What you get

Every pipeline should leave behind reusable evidence, not just output tables.

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
