# FabricOps Starter Kit

FabricOps Starter Kit helps teams build **governed, quality-checked, AI-ready Microsoft Fabric notebooks**.

It moves teams from exploration to controlled pipeline delivery with reusable metadata, DQ evidence, lineage, and handover artifacts.

[Quick Start](quick-start.md){ .md-button .md-button--primary }

[Understand the lifecycle](lifecycle-operating-model.md){ .md-button .md-button--primary }

## Framework at a glance

![FabricOps workspace notebook structure](assets/notebook-structure.png)

_Exploration explains the why. Pipeline contract notebooks enforce the approved what._

## Plug and play setup

Configure once, start from the notebook templates, and use the callable function reference when customising behavior.

| Template | Use it for | Start here |
| --- | --- | --- |
| `00_env_config.ipynb` | Configuring shared environment, storage, and runtime settings before template execution. | [Open template](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb) |
| `02_ex_agreement_topic.ipynb` | Running exploration profiling to draft governed metadata and quality requirements. | [Open template](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb) |
| `03_pc_agreement_source_to_target.ipynb` | Enforcing approved contracts and quality checks in a controlled pipeline flow. | [Open template](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb) |

<div class="center-cta">

[Browse all callable functions](reference/index.md){ .md-button .md-button--primary }

</div>

## Navigate by goal

| Goal | Start with |
| --- | --- |
| Plug and play setup | [Quick Start](quick-start.md), [`00_env_config.ipynb`](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb), [`02_ex_agreement_topic.ipynb`](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb), [`03_pc_agreement_source_to_target.ipynb`](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb) |
| Understand lifecycle decisions and controls | [Lifecycle Operating Model](lifecycle-operating-model.md), [Architecture](architecture/index.md) |
| Read code-level API docs | [Function Reference](reference/index.md), [Module API Catalog](api/modules/index.md) |

## Compatibility note

The Python package import path remains `fabricops_kit`.
