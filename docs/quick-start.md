# Quick Start

Use this page to get FabricOps Starter Kit running quickly in Microsoft Fabric. For deeper operating guidance, use the linked canonical docs.

## What you need

- A Microsoft Fabric workspace with notebook, Lakehouse/Warehouse, and environment access.
- Fabric notebook runtime (Fabric Runtime 1.3 / Python 3.11 recommended by this project).
- A prepared Fabric environment with the project wheel installed (see [Fabric Wheel Install](setup/fabric-wheel-install.md)).
- A clear data-sharing agreement context (purpose, ownership, approved usage).
- If you plan to use AI-assisted functions, your organisation must first enable tenant-level Fabric settings for **"Users can use Copilot and other features powered by Azure OpenAI"**.
- Depending on tenant/capacity region and organisation policy, data sent to Azure OpenAI may be processed outside your capacity's geographic region, compliance boundary, or national cloud instance, and may also be stored outside those boundaries where that setting is permitted.
- AI-assisted functions are optional: the core framework can run without them, but AI suggestion features will not work until the required organisation-level settings are approved and enabled.

## Start from these notebooks

Create or copy the reusable notebook set described in [Notebook Structure](notebook-structure.md):

- `00_env_config`
  - Environment configuration notebook for shared runtime/settings used by downstream notebooks.
- `01_data_sharing_agreement_<agreement>`
  - Agreement notebook to capture governance context for a specific data-sharing agreement.
- Pipeline notebooks for each agreement:
  - `02_ex_<agreement>_<topic>` for exploration/profiling and AI-assisted suggestions.
  - `03_pc_<agreement>_<pipeline>` for approved enforcement and production-style execution.

## Run them in this order

1. Configure the environment in `00_env_config`.
2. Capture agreement context in `01_data_sharing_agreement_<agreement>`.
3. Run exploration/profile work in `02_ex_<agreement>_<topic>`.
4. Run the approved pipeline contract in `03_pc_<agreement>_<pipeline>`.

## What to edit first

- Environment paths, connection/runtime values, and shared config in `00_env_config`.
- Agreement purpose, ownership, and approved usage in `01_data_sharing_agreement_<agreement>`.
- Source and output expectations for your dataset/pipeline.
- Approved DQ and classification decisions before enabling contract enforcement in `03_pc_<agreement>_<pipeline>`.

## What a successful first run should produce

- Config loaded.
- Agreement context captured.
- Source profile and metadata stored.
- Approved decisions available.
- Curated output written.
- DQ results and target metadata stored.
- Lineage and handover artifacts generated.

## Where to go next

- [Notebook Structure](notebook-structure.md)
- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Metadata and Contracts](metadata-and-contracts.md)
- [Functions / Reference](reference/index.md)
- [Fabric Wheel Install](setup/fabric-wheel-install.md)
