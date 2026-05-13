# Create Wheel

FabricOps Starter Kit is installed into Microsoft Fabric as a Python wheel. Build the wheel locally, then upload the generated `.whl` file into a Fabric Environment.

## Prerequisites

- Python installed locally
- `uv` installed
- This repository cloned locally

## Build the package

From the repository root:

```bash
uv sync
uv build
```

## Find the wheel

Build artifacts are written to `dist/`:

- `dist/*.whl`
- `dist/*.tar.gz`

For Fabric custom libraries, upload the `.whl` file (not the `.tar.gz` source distribution).

## Rebuild after changes

After code or dependency changes, rerun:

```bash
uv build
```

Then upload the new wheel version to your Fabric Environment.

## Next step

[Run in Fabric →](run-in-fabric.md)
