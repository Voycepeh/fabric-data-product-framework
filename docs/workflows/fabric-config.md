# Fabric config loading

Use `load_fabric_config(...)` to load environment and target house mappings at notebook runtime.

## Public-safe configuration

- Do **not** commit real workspace IDs.
- Do **not** commit real lakehouse/house IDs.
- Do **not** commit internal house names.

Use `configs/fabric_houses.example.yaml` as the public template.

## Where to store real config

- In Fabric notebooks, store real config in Lakehouse Files and load it at runtime (for example `Files/configs/fabric_houses.yaml`).
- For local development, use ignored files such as `configs/fabric_houses.yaml` or `configs/*.local.yaml`.

## Runtime usage

```python
from fabric_data_product_framework.fabric_notebook import load_fabric_config, get_path

fabric_config = load_fabric_config("Files/configs/fabric_houses.yaml")
lh_in = get_path("Sandbox", "Source", config=fabric_config)
```
