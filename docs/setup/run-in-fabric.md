# Run in Fabric

After the wheel is built, upload it to a Microsoft Fabric Environment, publish the Environment, attach it to notebooks, and verify imports.

## Upload wheel to Fabric Environment

1. Open your Fabric workspace.
2. Go to **Environment**.
3. Open **Custom libraries**.
4. Upload the `.whl` file from `dist/`.
5. Save and publish the Environment.

## Attach Environment to notebooks

1. Attach the published Environment to your notebook.
2. Restart the notebook session after library updates.

## Verify import

Use imports that match the current package structure.

- Use `fabricops_kit.data_profiling` (current module path).
- Do not use stale imports like `fabricops_kit.profiling`.

Verification cells:

```python
import fabricops_kit

print(fabricops_kit.__file__)
print(getattr(fabricops_kit, "__version__", "unknown"))
```

## Use with notebook workflow

After imports work:

1. Attach the published Environment to the notebook session.
2. Run `00_env_config`.
3. Run `01_data_sharing_agreement_<agreement>` where used.
4. Run `02_ex_<agreement>_<topic>` to profile data and prepare AI-assisted DQ/classification suggestions.
5. Get human approval for DQ/classification decisions before enforcement.
6. Run `03_pc_<agreement>_<pipeline>` to enforce approved metadata, DQ rules, checks, lineage, and outputs.

- [Quick Start](../quick-start.md)
- [Deployment](../deployment-and-promotion.md)

## Troubleshooting

- Old wheel still active: publish Environment and restart session.
- Import fails after upload: check the Environment is attached.
- Wrong module path: use current `fabricops_kit` module names.
- Missing dependencies: add dependency to package config and rebuild.
- Fabric runtime conflict: pin or simplify dependency.
- Version mismatch: bump wheel version and re-upload.

## Release checklist

1. Pull latest `main`.
2. Run local checks.
3. Bump version.
4. Run `uv build`.
5. Upload wheel.
6. Publish Environment.
7. Restart notebook session.
8. Smoke test import and one notebook.
9. Record tested version.
