# Create Wheel

FabricOps Starter Kit is installed into Microsoft Fabric as a Python wheel. Build the wheel locally, then upload the generated `.whl` file into a Fabric Environment.

## Prerequisites

- VS Code or another editor
- Git
- Python `>=3.11`
- `uv`
- Repository cloned locally
- Microsoft Fabric workspace / Environment access for the upload step

## Local setup

From the repository root:

```bash
git checkout main
git pull
uv sync
```

## Validation before build

Run quick checks before packaging:

```bash
uv run python -m pytest -q
uv run python -m compileall src tests
```

## Build the wheel

```bash
uv build
```

## Versioning before rebuild

Before rebuilding and uploading a new wheel:

- Align `pyproject.toml` `[project].version` and `src/fabricops_kit/__init__.py` `__version__`.
- Use a patch bump for fixes.
- Use a minor bump for new capabilities.
- Do not upload different wheel contents using the same version.

## Next step

[Run in Fabric →](run-in-fabric.md)
