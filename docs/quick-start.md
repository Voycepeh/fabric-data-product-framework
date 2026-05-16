# Quick Start

Use this page to get FabricOps Starter Kit running quickly in Microsoft Fabric. For deeper operating guidance, use the linked canonical docs.

## What you need

- A Microsoft Fabric workspace with notebook, Lakehouse/Warehouse, and environment access.
- Fabric notebook runtime (Fabric Runtime 1.3 / Python 3.11 recommended by this project).
- A prepared Fabric environment with the project wheel installed (see [Run in Fabric](setup/run-in-fabric.md)).
- A clear data-sharing agreement context (purpose, ownership, approved usage).
- If you plan to use AI-assisted functions, your organisation must first enable the relevant **Copilot and Azure OpenAI Service** tenant settings in Fabric:
  - **Users can use Copilot and other features powered by Azure OpenAI**
  - **Data sent to Azure OpenAI can be processed outside your capacity's geographic region, compliance boundary, or national cloud instance** when required for your tenant/capacity region
  - **Data sent to Azure OpenAI can be stored outside your capacity's geographic region, compliance boundary, or national cloud instance** where your organisation permits that setting
- AI-assisted functions are optional: the core framework can run without them, but AI suggestion features will not work until the required organisation-level settings are approved and enabled.

## Start from these notebooks

Open and copy these real starter templates first:

| Template notebook | Purpose |
| --- | --- |
| [`00_env_config.ipynb`](../templates/notebooks/00_env_config.ipynb) | reusable environment config notebook |
| [`02_ex_agreement_topic.ipynb`](../templates/notebooks/02_ex_agreement_topic.ipynb) | exploration, profiling, AI-assisted suggestions, contract drafting |
| [`03_pc_agreement_pipeline_template.ipynb`](../templates/notebooks/03_pc_agreement_pipeline_template.ipynb) | approved pipeline execution, DQ enforcement, quarantine/output/metadata/lineage |

These are copy-ready starter notebooks. Rename and adapt them for your own agreement and pipeline.

For the minimal end-to-end sample sequence, see [`templates/notebooks/README.md`](../templates/notebooks/README.md).

After copying, use this canonical naming model for your working notebooks:

- `00_env_config`
- `01_da_<agreement>`
- `02_ex_<agreement>_<topic>`
- `03_pc_<agreement>_<pipeline>`
- `04_gov_<agreement>_<topic>` (future governance enrichment notebooks)

## Run them in this order

1. Configure the environment in `00_env_config`.
2. Capture agreement context in `01_da_<agreement>`.
3. Run exploration/profile work in `02_ex_<agreement>_<topic>`.
4. Run the approved pipeline contract in `03_pc_<agreement>_<pipeline>`.

## What to edit first

- Environment paths, connection/runtime values, and shared config in `00_env_config`.
- Agreement purpose, ownership, and approved usage in `01_da_<agreement>`.
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
- [Run in Fabric](setup/run-in-fabric.md)
