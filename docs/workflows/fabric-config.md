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
from fabric_data_product_framework import load_fabric_config, get_path

# %run 00_config
config = load_fabric_config(CONFIG)
lh_in = get_path("Sandbox", "Source", config=config)
```

## Public-safe configuration

- Do **not** commit real workspace IDs.
- Do **not** commit real lakehouse/house IDs.
- Do **not** commit internal house names.
