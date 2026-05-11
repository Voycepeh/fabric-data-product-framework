# Notebook Structure

This is the canonical page for notebook roles in FabricOps Starter Kit.

![Workspace notebook setup](assets/notebook-structure.png)

## Recommended workspace layout

```text
Workspace
├── 00_env_config
├── 01_data_sharing_agreement_<agreement>
├── 02_ex_<agreement>_<topic>
└── 03_pc_<agreement>_<pipeline>
```

## Notebook naming, ownership, run mode, and scope

| Notebook | Primary ownership | Run mode | What belongs here |
|---|---|---|---|
| `00_env_config` | Platform / engineering | Reused by other notebooks | Shared environment config, paths, runtime settings, smoke checks, reusable config objects. |
| `01_data_sharing_agreement_<agreement>` | Data owner + governance steward | Human-reviewed, updated when agreement changes | Approved usage intent, policy boundaries, and agreement context. |
| `02_ex_<agreement>_<topic>` | Analyst / engineer | Human-led exploration, not scheduled | Profiling, discovery, exploratory transforms, AI-assisted suggestions for DQ/classification candidates and metadata evidence. |
| `03_pc_<agreement>_<pipeline>` | Data engineer | Run-all-safe, schedulable pipeline execution | Enforces only approved metadata and rules, performs deterministic transforms, writes outputs and runtime evidence. |

## AI boundary (must stay explicit)

- AI suggestions happen in `02_ex`.
- Human review and approval happen before promotion into approved metadata/config.
- `03_pc` enforces only approved rules/classifications and must remain run-all-safe.

## What goes where

| Work item | `00_env_config` | `01_data_sharing_agreement` | `02_ex` | `03_pc` |
|---|---:|---:|---:|---:|
| Define environment paths/runtime config | Yes | No | Read-only | Read-only |
| Record approved usage boundaries | No | Yes | Reference | Enforce usage-aligned logic |
| Profile source data | No | No | Yes | Optional checks only |
| Generate AI suggestions | No | No | Yes | No |
| Approve/edit/reject candidate rules | No | Yes/Shared review | Draft + review workflow | No |
| Enforce approved DQ rules/classifications | No | No | No | Yes |
| Write curated outputs and run evidence | No | No | Optional draft artifacts | Yes |

## Notebook details

- [`00_env_config`](notebook-structure/00-env-config.md)
- [`02_ex_<agreement>_<topic>`](notebook-structure/02-exploration.md)
- [`03_pc_<agreement>_<pipeline>`](notebook-structure/03-pipeline-contract.md)

## Related pages

- [Metadata and Data Contract Assembly](metadata-and-contracts.md)
- [Assembled contract model](metadata-and-contracts/contract-model.md)
- [Data Quality Rules System](data-quality-rules-system.md)
- [Lifecycle Operating Model](lifecycle-operating-model.md)
