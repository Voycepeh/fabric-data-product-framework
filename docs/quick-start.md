# Quick Start: End-to-End Lifecycle Workflow

Use this page as the runbook for executing FabricOps Starter Kit in Microsoft Fabric.

## Prerequisites

- Python 3.11+ and `uv` installed locally.
- Access to a Microsoft Fabric workspace with Lakehouse/Warehouse and Environment permissions.
- A dataset with defined business purpose, ownership, and acceptance rules.

## 1) Install and prepare

```bash
git clone https://github.com/Voycepeh/FabricOps-Starter-Kit.git
cd FabricOps-Starter-Kit
uv sync --all-extras
uv build
```

For Fabric Environment install steps, use [Fabric Wheel Install](setup/fabric-wheel-install.md).

## 2) Open your Fabric notebook and load/create config

- Start from `templates/notebooks/fabric_data_product_mvp.md`.
- Attach the Fabric Environment that contains the package wheel.
- Create or load runtime/framework config (paths, dataset IDs, output targets, run context).

Canonical notebook flow:

- `00_env_config` = shared setup and runtime configuration baseline.
- `01_data_sharing_agreement_<agreement>` = governance context, approved usage, ownership, and restrictions.
- `02_ex_<agreement>_<topic>` = exploration, profiling, AI suggestions, and human decisions.
- `03_pc_<agreement>_<topic>` = approved enforcement, outputs, metadata, lineage, and handover.

## 3) Execute in canonical 10-step order

Follow this sequence (details in [Lifecycle Operating Model](lifecycle-operating-model.md)):

1. Define purpose, approved usage, and governance ownership.
2. Configure runtime, environment, and path rules.
3. Declare source contract and ingest source data.
4. Validate source against contract and capture metadata.
5. Explore data and capture transformation / DQ rationale.
6. Build production transformation and write target output.
7. Validate output and persist target metadata.
8. Generate, review, and configure DQ rules.
9. Generate and review classification / sensitivity suggestions.
10. Generate data lineage and handover documentation.

## 4) Validate completion criteria

A successful run should leave you with:

- source and output profiling artifacts,
- quality and drift results,
- written output table(s),
- governance metadata and reviewer decisions,
- lineage output,
- handover documentation artifacts.

## 5) Next references

- Canonical lifecycle detail: [Lifecycle Operating Model](lifecycle-operating-model.md)
- Notebook conventions: [Notebook Structure](notebook-structure.md)
- Architecture: [Architecture](architecture.md)
- Callable catalogue: [Reference](reference/index.md)
