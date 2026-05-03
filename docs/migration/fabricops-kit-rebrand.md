# FabricOps Starter Kit rebrand migration

## What changed
- **Old brand:** Fabric Data Product Framework
- **New brand:** FabricOps Starter Kit
- **Old import:** `fabric_data_product_framework`
- **New import:** `fabricops_kit`

## Import migration
Before:
```python
from fabric_data_product_framework import load_fabric_config
```

After:
```python
from fabricops_kit import load_fabric_config
```

## Deprecated aliases
- `ODI_METADATA_LOGGER` is deprecated and now forwards to `generate_metadata_profile` with a `DeprecationWarning`.
- `fabric_data_product_framework` package imports still work temporarily via a compatibility shim.

## Recommended action for Fabric notebooks
1. Update notebook imports to `fabricops_kit`.
2. Replace `ODI_METADATA_LOGGER(...)` with `generate_metadata_profile(...)`.
3. Keep compatibility imports only during transition; plan full cleanup in your next release cycle.
