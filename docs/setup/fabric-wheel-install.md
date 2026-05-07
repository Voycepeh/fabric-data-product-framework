# UV Wheel Build and Fabric Install Guide

## Purpose

Use this guide to package this repository as a distributable Python wheel (`.whl`) with `uv`, then install that wheel into a Microsoft Fabric **Environment**.

This keeps workflow notebooks focused on data product logic while loading framework capabilities from a versioned package, instead of copying helper code between notebooks.

## Prerequisites

Before starting, confirm you have:

- VS Code
- Git
- Python `>=3.11` (matches `pyproject.toml`)
- `uv` installed locally
- Access to a Microsoft Fabric workspace and Environment management
- This repository cloned locally

## Local setup in VS Code

From a terminal in the repo root:

```bash
git checkout main
git pull
uv sync
```

Run validation checks before building:

```bash
# Test suite (this repo has pytest configured)
uv run python -m pytest -q

# Lightweight compile sanity check
uv run python -m compileall src
```

If you are making release-bound changes, you can also compile tests:

```bash
uv run python -m compileall src tests
```

## Build the wheel

Build package artifacts:

```bash
uv build
```

Expected output location:

- `dist/*.whl` (wheel)
- `dist/*.tar.gz` (source distribution)

At a high level:

- `.whl`: prebuilt install artifact (recommended for Fabric Environments)
- `.tar.gz`: source archive for source-based installs/build pipelines

For Fabric notebook environments, upload the `.whl` artifact.

## Versioning before rebuild

Package version currently needs to stay aligned between:

- `pyproject.toml` under `[project].version`
- `src/fabricops_kit/__init__.py` in `__version__`

Recommended versioning practice for this framework:

- **Patch bump** (`0.1.0` -> `0.1.1`) for small fixes (docs/runtime-safe adjustments)
- **Minor bump** (`0.1.0` -> `0.2.0`) for new framework capabilities

After bumping version:

1. Rebuild with `uv build`
2. Upload the new wheel to Fabric
3. Publish the Environment
4. Restart notebook session

Avoid uploading multiple different wheel files with the **same version** while iterating; it makes Fabric runtime verification and team handover confusing.

## Upload and install into Microsoft Fabric

Fabric UI labels can change slightly by tenant/release. The flow is generally:

1. Open your Fabric workspace.
2. Open an existing **Environment** (or create one).
3. In Environment libraries, use **Custom libraries** to upload the wheel from `dist/`.
4. Save/publish the Environment.
5. Wait for the Environment publish/install step to finish.
6. Attach that Environment to your notebook.
7. Restart the notebook session/kernel after the library change.
8. Run import verification cells.

You may also see **Public libraries** in the same UI area; for this repo package, use the custom wheel upload path.

## Verify inside a Fabric notebook

The package import path for this repository is:

```python
import fabricops_kit as fdpf
```

Practical verification cells:

```python
import fabricops_kit as fdpf

print("Package loaded:", fdpf.__name__)
print("Module path:", fdpf.__file__)
print("Package version:", getattr(fdpf, "__version__", "unknown"))
```

```python
from fabricops_kit.profiling import profile_dataframe
import pandas as pd

sample_df = pd.DataFrame(
    {
        "order_id": [1, 2, 3],
        "amount": [10.0, 20.5, 30.25],
        "status": ["NEW", "PAID", "NEW"],
    }
)

profile = profile_dataframe(sample_df, dataset_name="wheel_install_smoke", engine="auto")
print("Profile keys:", list(profile.keys())[:10])
```

```python
import fabricops_kit
print([name for name in dir(fabricops_kit) if not name.startswith("_")][:25])
```

## Use with the current Fabric notebook workflow

After wheel installation, use this flow:

1. Attach the Environment (with the uploaded wheel) to the notebook session.
2. Run `00_env_config.ipynb` to load environment/runtime config.
3. Run `01_data_sharing_agreement_<agreement>` to capture governance context (where used).
4. Run `02_ex_<agreement>_<topic>` for profiling and AI-assisted suggestions.
5. Obtain human approval for DQ/classification decisions.
6. Run `03_pc_<agreement>_<topic>` to enforce approved rules and write outputs/metadata.

For long-term maintainability, prefer package imports from `fabricops_kit` over `%run 00_config`-style helper reuse.

## Troubleshooting

- **Old framework behavior still appears:** old wheel version may still be active in the Environment or running session.
- **Import still fails after upload:** restart notebook session/kernel and confirm Environment publish finished.
- **Wrong Environment attached:** verify notebook is bound to the Environment where your wheel was uploaded.
- **Import path mismatch:** use `import fabricops_kit` (module name), not package distribution name with hyphens.
- **Missing dependencies:** check `pyproject.toml` dependencies and rebuild/re-upload.
- **Runtime dependency conflict in Fabric:** review Fabric Environment libraries (custom/public) for conflicting versions.
- **Wheel built before version bump:** increment version, rebuild, re-upload, publish, restart.
- **Imported version is not the version you expected:** ensure both `pyproject.toml` and `src/fabricops_kit/__init__.py` were bumped, rebuild the wheel, re-upload it, publish the Environment, and restart the notebook session.
- **Local tests pass but Fabric calls fail:** some runtime behavior depends on Fabric-only execution context and must be validated in Fabric.

## Recommended release checklist

1. Pull latest `main`.
2. Run local checks (`uv sync`, tests, compile checks).
3. Bump package version in `pyproject.toml`.
4. Run `uv build`.
5. Upload the new wheel to Fabric Environment custom libraries.
6. Publish/save the Environment.
7. Restart notebook session.
8. Run notebook smoke test end to end using the 00/01/02/03 operating model.
9. Record tested package version in handover/release notes.
