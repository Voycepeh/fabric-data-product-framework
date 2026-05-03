# Fabric config loading

Use `load_fabric_config(...)` to validate and load a user-supplied framework `CONFIG` object at notebook runtime.

`load_fabric_config` does **not** create Fabric resources (workspaces, lakehouses, warehouses, tables, or files).

## Reusable config notebook/file

Maintain a reusable `00_config` notebook (or equivalent Python file) that builds config sections with helper functions:

- `create_path_config`
- `create_notebook_runtime_config`
- `create_ai_prompt_config`
- `create_quality_config`
- `create_governance_config`
- `create_lineage_config`
- `create_framework_config`

## Runtime usage

```python
from fabricops_kit import load_fabric_config, get_path

# %run 00_config
config = load_fabric_config(CONFIG)
lh_in = get_path("Sandbox", "Source", config=config)
```

## Public-safe configuration

- Do **not** commit real workspace IDs.
- Do **not** commit real lakehouse/house IDs.
- Do **not** commit internal house names.


## AI prompt template override in `00_config`

```python
from fabricops_kit import (
    create_ai_prompt_config,
    create_framework_config,
    create_governance_config,
    create_lineage_config,
    create_notebook_runtime_config,
    create_path_config,
    create_quality_config,
    load_fabric_config,
)

ai_prompt_config = create_ai_prompt_config(
    dq_rule_candidate_template="Generate DQ candidates for {dataset_name}. Context: {business_context}. Row={column_name}",
    governance_candidate_template="Suggest governance labels for {dataset_name}. Context: {business_context}. Row={column_name}",
    handover_summary_template="Summarize handover for context {business_context}. Row={summary}",
)

CONFIG = create_framework_config(
    path_config=create_path_config({...}),
    notebook_runtime_config=create_notebook_runtime_config(["00_", "01_", "02_", "03_"]),
    ai_prompt_config=ai_prompt_config,
    quality_config=create_quality_config(),
    governance_config=create_governance_config(),
    lineage_config=create_lineage_config(),
)

config = load_fabric_config(CONFIG)
```

With this pattern, project teams edit prompt templates in `00_config` without changing `ai.py`.
