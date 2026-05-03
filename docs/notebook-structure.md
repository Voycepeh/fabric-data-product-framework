# Notebook Structure

Use this finalized notebook model in each Fabric environment workspace.

```text
<env> Workspace
├── 00_env_config
│   └── One reusable config notebook per environment workspace
│
├── 01_data_sharing_agreement_<agreement>
│   └── Governance, approved usage, permissions, restrictions
│
├── Exploration notebooks (many)
│   ├── 02_ex_<agreement>_source_profile
│   └── 02_ex_<agreement>_event_logic
│
└── Pipeline contract notebooks (many)
    ├── 03_pc_<agreement>_<from>_to_<to>
    │   └── Executable pipeline + handover
    └── 03_pc_<agreement>_<from>_to_<to>
        └── Executable pipeline + handover
```

## Notebook roles

- `00_env_config` is the shared runtime/config notebook for that environment workspace.
- `01_data_sharing_agreement_<agreement>` is the governance artifact for one agreement.
- `02_ex_<agreement>_*` notebooks are manual exploration notebooks and are not scheduled.
- `03_pc_<agreement>_<from>_to_<to>` notebooks are scheduled operational notebooks and include executable pipeline logic plus handover in the same notebook.

## Relationship model

- One agreement can connect to many exploration notebooks.
- One agreement can connect to many pipeline contract notebooks.
- Pipeline stage movement is encoded inside `<from>_to_<to>`, not by changing notebook type prefixes.

For workflow steps and execution order, use [Quick Start](quick-start.md).
