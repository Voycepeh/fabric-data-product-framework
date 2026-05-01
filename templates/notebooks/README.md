# Notebook templates

This folder contains reusable notebook starters for Microsoft Fabric workflows.

## Included files

- `fabric_data_product_mvp.py`: primary MVP starter notebook template.
- `fabric_data_product_mvp.md`: practical guidance aligned to the canonical 13-step workflow.

## Suggested usage

1. Start with `docs/quick-start.md`.
2. Run local validation checks.
3. Move the template into Fabric and configure runtime inputs.
4. Keep DQ/governance human-review checkpoints before enabling writes.

## Packaging note

Build and upload the framework wheel into a Fabric Environment, then attach that Environment to notebooks and import from `fabric_data_product_framework`.

Use `docs/UV_WHEEL_FABRIC_INSTALL_GUIDE.md` for exact build and install steps.
