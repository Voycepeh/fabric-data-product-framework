# Quick Start: End-to-End Notebook Runbook

Use this page as the concise runbook for executing FabricOps Starter Kit in Microsoft Fabric.

## Prerequisites

- Microsoft Fabric notebook runtime target: **Fabric Runtime 1.3 (Python 3.11)**.
- Local development runtime: Python **>=3.11** with `uv` installed.
- Access to a Microsoft Fabric workspace with:
  - Fabric Environment permission (to attach environments/install wheel artifacts), and
  - Lakehouse and/or Warehouse access for source and output operations.
- A dataset agreement context with defined purpose, ownership, and usage constraints.

## 1) Install and prepare

```bash
git clone https://github.com/Voycepeh/FabricOps-Starter-Kit.git
cd FabricOps-Starter-Kit
uv sync --all-extras
uv build
```

To install the built wheel in Fabric, follow [Fabric Wheel Install](setup/fabric-wheel-install.md).

## 2) Open your Fabric notebook workflow

- Attach the Fabric Environment that contains the built package wheel.
- Use the current starter notebooks and naming pattern from [Notebook Structure](notebook-structure.md).
- Run notebooks in this operating sequence:

1. `00_env_config.ipynb`
   - Reusable environment and runtime configuration notebook.
2. `01_data_sharing_agreement_<agreement>`
   - Governance agreement capture: approved usage, ownership, and restrictions.
3. `02_ex_<agreement>_<topic>`
   - Exploration and profiling, transformation rationale, AI-suggested DQ rules, and AI-suggested classification/sensitivity labels.
4. `03_pc_<agreement>_<topic>`
   - Pipeline contract execution with approved DQ enforcement, approved classification enforcement, output writes, metadata capture, lineage generation, and handover artifact creation.

## 3) Clarify exploration vs. pipeline enforcement

- AI suggestions are produced in exploration/assistive workflows (typically `02_ex_*`).
- Human approval is required before any DQ rule or classification/sensitivity rule is treated as enforceable.
- Pipeline contract notebooks (`03_pc_*`) enforce only approved decisions.

## 4) Keep the canonical lifecycle reference

Use the canonical 10-step lifecycle as the control flow reference, and use [Lifecycle Operating Model](lifecycle-operating-model.md) for full detail.

## 5) Validate completion criteria

A successful quick-start run should leave:

- environment config loaded,
- agreement/governance context captured,
- source profile and schema metadata captured,
- approved DQ/classification decisions available,
- pipeline output written,
- DQ results and target metadata stored,
- lineage and handover notes generated.

## 6) Next references

- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Notebook Structure](notebook-structure.md)
- [Architecture](architecture.md)
- [Storage & Metadata Model](architecture/storage-model.md)
- [Fabric-native Data Quality](architecture/dqx-inspired-fabric-native-dq.md)
- [Metadata and Contracts](metadata-and-contracts.md)
- [Function Reference](reference/index.md)
- [Fabric Wheel Install](setup/fabric-wheel-install.md)
