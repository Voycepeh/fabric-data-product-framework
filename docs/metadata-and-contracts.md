# Metadata and Contracts

A data contract is the agreement that makes a dataset safe to use.

In FabricOps, the contract is assembled from configuration, approved usage, profiling results, quality rules, sensitivity classification, transformation logic, and runtime evidence produced by the notebooks.

![FabricOps data contract assembly](assets/data-contract.png)

*The contract is reviewed by humans and enforced by the pipeline notebook.*

## What questions does the contract answer?

| Question | FabricOps evidence |
| --- | --- |
| What data is this? | Source table, output table, schema, profile, and lineage context. |
| How can it be used? | Data sharing agreement and approved usage boundaries. |
| What columns must exist? | Required schema and pipeline contract checks. |
| What quality must pass? | Approved DQ rules, thresholds, and runtime quality outcomes. |
| Which data is sensitive? | Classification labels, review status, and enforcement metadata. |
| Who approved it? | Owner, steward, governance, and engineering approvals. |

The goal is simple: make the pipeline understandable, reviewable, and safe to operate.

A new engineer should be able to open the contract notebook, understand the dataset purpose, see what rules are enforced, and find evidence from the latest run.

## How FabricOps assembles the contract

| Source | What it contributes |
| --- | --- |
| `00_env_config` | Runtime configuration and environment paths. |
| `01_data_sharing_agreement` | Approved usage, boundaries, and governance context. |
| `02_ex` notebooks | Profiling, exploration, AI-assisted suggestions, and rationale. |
| `03_pc` notebooks | Enforced transformation, validation, DQ checks, and metadata writes. |
| Metadata tables | Runtime evidence, profiles, summaries, approvals, and audit history. |

## Where to go next

| Page | Use it for |
| --- | --- |
| [Contract model](metadata-and-contracts/contract-model.md) | Understand what the FabricOps contract model means. |
| [Metadata tables](metadata-and-contracts/metadata-tables.md) | See what evidence is stored and how records connect. |
| [Notebook responsibilities](metadata-and-contracts/notebook-responsibilities.md) | Understand which notebook owns each contract task. |
| [Data quality rules system](workflows/data-quality-rules-system.md) | Turn approved expectations into enforceable checks. |
| [Data quality architecture](architecture/data-quality-architecture.md) | Understand how quality enforcement fits the architecture. |
