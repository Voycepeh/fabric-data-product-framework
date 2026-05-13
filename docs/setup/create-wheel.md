# Create Wheel

FabricOps Starter Kit is installed into Microsoft Fabric as a Python wheel. Build the wheel locally, then upload the generated `.whl` file into a Fabric Environment.

## Prerequisites

- VS Code
- Git
- Python `>=3.11`
- `uv` installed locally
- This repository cloned locally
- Access to a Microsoft Fabric workspace or Environment for the next step

## Local setup

From the repository root:

```bash
git checkout main
git pull
uv sync
```

## Validation checks

Run quick local checks before building:

```bash
uv run python -m pytest -q
uv run python -m compileall src
uv run python -m compileall src tests
```

## Build the package

```bash
uv build
```

## Find the wheel

Build artifacts are written to `dist/`:

- `dist/*.whl`
- `dist/*.tar.gz`

For Fabric custom libraries, upload the `.whl` file (not the `.tar.gz` source distribution).

## Versioning before rebuild

Keep versions aligned between:

- `pyproject.toml` under `[project].version`
- `src/fabricops_kit/__init__.py` in `__version__`

Use a patch bump for fixes and a minor bump for new capabilities. Avoid uploading different wheel files with the same version.

## Rebuild after changes

After code or dependency changes, rerun `uv build`, then upload the new wheel version to your Fabric Environment.

## Next step

[Run in Fabric →](run-in-fabric.md)
