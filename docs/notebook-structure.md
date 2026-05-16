# Notebook Structure

Notebook Structure is the canonical guide for notebook ownership, lifecycle boundaries, and execution behavior in FabricOps Starter Kit.

![Governance-Centered Workspace Model](assets/notebook-structure.png)

## Revised notebook sequence

Use the following sequence for the lifecycle:

```text
00_env_config
01_da_<agreement>
02_ex_<agreement>_<topic>
03_pc_<agreement>_<source>_to_<target>
04_gov_<agreement>_<dataset>_<table>
```

## Workspace layout

```text
Governance Workspace
└── 01_da_<agreement>                     (agreement-level approval evidence)

Environment Workspace (Sandbox / Dev-Test / Prod)
├── 00_env_config
├── 02_ex_<agreement>_<topic>             (1-many)
├── 03_pc_<agreement>_<source>_to_<target> (1-many)
├── 04_gov_<agreement>_<dataset>_<table>  (1-many)
└── Local metadata/evidence lakehouse
```

## Notebook roles and boundaries

| Notebook | Primary ownership | Scope | What belongs here | What does **not** belong here |
|---|---|---|---|---|
| `00_env_config` | Platform / engineering | Environment bootstrap and runtime config | Build `CONFIG`, set metadata lakehouse routing, define AI prompts, runtime settings, and path targets. | Agreement approvals, profiling, pipeline transforms, column governance decisions. |
| `01_da_<agreement>` | Governance steward / data owner | Agreement-level approval evidence | Capture and write agreement-level approval evidence to `METADATA_DATA_AGREEMENT`; register notebook in `METADATA_NOTEBOOK_REGISTRY`. | Table/column business context review and classification/PII governance review. |
| `02_ex_<agreement>_<topic>` | Analyst / data scientist | Exploration and profiling evidence | Require existing `agreement_id`; register under that agreement; profile data and write evidence tied to `agreement_id`, `environment_name`, `dataset_name`, `table_name`, and `column_name`. | Defining new agreements, final governance approval decisions. |
| `03_pc_<agreement>_<source>_to_<target>` | Data engineer | Pipeline contract execution evidence | Require existing `agreement_id`; register under that agreement; execute transformation/DQ/pipeline work and write evidence tied to `agreement_id`. | Defining agreements or standalone governance approvals outside agreement context. |
| `04_gov_<agreement>_<dataset>_<table>` | Governance steward / data owner | Column-level governance enrichment (planned stage) | Documented operating stage after profile/pipeline evidence exists; reviews per-column business context and classification/PII/confidentiality and is expected to write `METADATA_COLUMN_CONTEXT` and `METADATA_COLUMN_GOVERNANCE` once template support is added. | Agreement creation and environment bootstrap. |

## Cross-notebook enforcement rules

- All downstream notebooks (`02_ex`, `03_pc`, `04_gov`) must declare `agreement_id`.
- Before doing work, downstream notebooks must validate that `agreement_id` exists in `METADATA_DATA_AGREEMENT`.
- All notebooks must register themselves in `METADATA_NOTEBOOK_REGISTRY` under the `agreement_id` to avoid stray notebooks.

## Metadata routing rule (required)

Do not use `spark.table("METADATA_*")` or implicit/default lakehouse assumptions.

Always use `read_lakehouse_table` and `write_lakehouse_table` with `CONFIG`, `env_name`, and the `metadata` target.

## Governance flow across notebooks

- `01_da` captures agreement-level approval evidence once and publishes it for reuse.
- `02_ex` and `03_pc` run under an existing agreement and produce profiling/pipeline evidence.
- `04_gov` is the documented next operating stage for column-level enrichment; until a dedicated template notebook is added, treat it as planned guidance.
- Human approval remains the control authority for governance outcomes.

## Notebook details

- [`00_env_config`](notebook-structure/00-env-config.md)
- [`01_da_<agreement>`](notebook-structure/01-data-sharing-agreement.md)
- [`02_ex_<agreement>_<topic>`](notebook-structure/02-exploration.md)
- [`03_pc_<agreement>_<source>_to_<target>`](notebook-structure/03-pipeline-contract.md)
- [`04_gov_<agreement>_<dataset>_<table>`](notebook-structure/04-governance-enrichment.md)

## Related pages

- [Workflow](workflow.md)
- [Metadata and Data Contract Assembly](metadata-and-contracts.md)
- [Data Quality Rules System](data-quality-rules-system.md)
