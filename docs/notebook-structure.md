# Notebook Structure

FabricOps Starter Kit uses a notebook-first operating model: exploration notebooks explain the *why*, pipeline contract notebooks enforce the approved *what*, and environment configuration keeps runtime setup reusable and safe.

![Workspace notebook setup](assets/notebook-structure.png)

*Figure: Notebook organization in a Fabric workspace, linking shared configuration and agreement context to exploration and production pipeline notebooks.*

## Recommended workspace layout

```text
Workspace
├── 00_env_config
├── 01_data_sharing_agreement_<agreement>
├── 02_ex_<agreement>_<topic>
└── 03_pc_<agreement>_<pipeline>
```

- **`00_env_config`**: shared environment setup (stores, paths, runtime switches, smoke checks).
- **`01_data_sharing_agreement_<agreement>`**: governance notebook describing approved usage, scope, and guardrails.
- **`02_ex_<agreement>_<topic>`**: exploration and reasoning notebook for source understanding and AI-assisted proposals.
- **`03_pc_<agreement>_<pipeline>`**: run-all-safe pipeline notebook that enforces approved contract behavior.

## The three main notebook types

| Notebook type | Purpose | Run mode | Owner |
|---|---|---|---|
| 00_env_config | Environment setup, paths, runtime settings, smoke checks | Reused by other notebooks | Platform / engineering |
| 02_ex_<agreement>_<topic> | Profiling, exploration, AI-assisted suggestions, business reasoning | Human-led / not scheduled | Analyst / engineer |
| 03_pc_<agreement>_<pipeline> | Approved contract enforcement, DQ checks, output, metadata, lineage | Run-all-safe / scheduled | Data engineer |

`01_data_sharing_agreement_<agreement>` sits alongside these as the governance and approved-usage notebook that anchors policy decisions.

## How notebooks relate to the lifecycle

For full end-to-end sequencing, see [Lifecycle Operating Model](lifecycle-operating-model.md). This page focuses only on where work belongs.

## 1. Governance and environment setup

Handled by:
- `00_env_config`
- `01_data_sharing_agreement_<agreement>`

Covers:
- approved usage
- source and target stores
- runtime config
- naming rules
- smoke checks

## 2. Exploration notebook

Handled by:
- `02_ex_<agreement>_<topic>`

Covers:
- source profiling
- schema discovery
- transformation reasoning
- AI-suggested DQ rules
- AI-suggested sensitivity classifications
- proposed contract metadata

**Important boundary:** AI suggestions happen here, but nothing is enforced here.

## 3. Pipeline contract notebook

Handled by:
- `03_pc_<agreement>_<pipeline>`

Covers:
- loading approved contract metadata
- validating required columns and business keys
- enforcing approved DQ rules
- applying approved classifications
- writing output tables
- writing metadata, profiling, lineage, and handover evidence

**Important boundary:** The pipeline notebook should be run-all-safe.

## What goes where

| Work item | 00_env_config | 02_ex | 03_pc |
|---|---:|---:|---:|
| Define lakehouse / warehouse paths | Yes | No | Load only |
| Explore source data | No | Yes | No |
| Generate AI DQ suggestions | No | Yes | No |
| Approve DQ rules | No | Record decision | Enforce only |
| Enforce DQ rules | No | No | Yes |
| Generate AI classification suggestions | No | Yes | No |
| Apply approved classifications | No | No | Yes |
| Write output data | No | Usually no | Yes |
| Write run evidence | No | Optional | Yes |
| Generate lineage / handover | No | Optional draft | Yes |

## Naming convention

Use consistent, sortable prefixes so notebook purpose is clear at a glance:

- `00_env_config`
- `01_data_sharing_agreement_student_lifecycle`
- `02_ex_student_lifecycle_source_profile`
- `03_pc_student_lifecycle_source_to_unified`

## Common mistakes

- Do not put exploration-only diagnostic cells inside scheduled pipeline runs.
- Do not enforce AI-generated rules before human or steward approval.
- Do not hardcode dev/prod paths inside pipeline notebooks.
- Do not use `03_pc` notebooks for open-ended discovery.
- Do not duplicate lifecycle explanation here; link to the [Lifecycle Operating Model](lifecycle-operating-model.md) instead.

## Related documentation

- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Function Reference](reference/function-reference.md)
- [Architecture](architecture.md)
- [Metadata and Contracts](metadata-and-contracts.md)
- [Deployment and Promotion](deployment-and-promotion.md)
