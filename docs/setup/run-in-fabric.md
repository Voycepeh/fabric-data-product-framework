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
2. Restart the notebook session if needed after library updates.

## Verify import

Use imports that match the current package structure.

- Use `fabricops_kit.data_profiling` (current module path).
- Do not use stale imports like `fabricops_kit.profiling`.

Verification cells:

```python
import fabricops_kit as fdpf

print(fdpf.__name__)
print(fdpf.__file__)
print(getattr(fdpf, "__version__", "unknown"))
```

## Use with notebook workflow

After imports work:

1. Attach the published Environment to the notebook session.
2. Run `00_env_config`.
3. Run `01_data_sharing_agreement_<agreement>` where used.
4. Run `02_ex_<agreement>_<topic>` for profiling and AI-assisted suggestions.
5. Get human approval for DQ and classification decisions.
6. Run `03_pc_<agreement>_<pipeline>` to enforce rules and write outputs or metadata.

- [Quick Start](../quick-start.md)
- [Deployment](../deployment-and-promotion.md)

## Troubleshooting

- Old wheel still active: publish Environment and restart notebook session.
- Import fails after upload: confirm publish completed, then restart.
- Wrong Environment attached: verify notebook binding.
- Import path mismatch: use `fabricops_kit.data_profiling`, not `fabricops_kit.profiling`.
- Missing dependencies: review dependencies, rebuild, and re-upload wheel.
- Fabric runtime dependency conflict: check other custom/public libraries in the Environment.
- Version mismatch: align versions in `pyproject.toml` and `__init__.py`, then rebuild and re-upload.
- Local tests pass but Fabric context fails: validate in Fabric runtime context.

## Release checklist

1. Pull latest `main`.
2. Run local checks.
3. Bump package version.
4. Run `uv build`.
5. Upload wheel to Fabric Environment.
6. Publish Environment.
7. Restart notebook session.
8. Run a Fabric smoke test.
9. Record the tested package version.
