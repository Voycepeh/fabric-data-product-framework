# MVP Wheel Release Checklist

This checklist is for preparing a clean wheel before uploading it into Microsoft Fabric for MVP testing.

## Steps

1. Pull latest `main`.
2. Confirm PR 69 and PR 70 are merged.
3. Check version alignment:
   `python scripts/check_release_ready.py`
4. Run local validation:
   - `python -m compileall src tests`
   - `PYTHONPATH=src pytest -q`
5. If using `uv`:
   - `uv sync`
   - `uv run python scripts/check_release_ready.py`
   - `uv run python -m compileall src tests`
   - `uv run python -m pytest -q`
6. Build wheel:
   `uv build`
7. Confirm `dist/` contains the expected wheel filename and version.
8. Upload the `.whl` to Fabric Environment custom libraries.
9. Publish/save the Environment.
10. Restart Fabric notebook session.
11. Run import/version check:

```python
import fabricops_kit as fdpf
print(fdpf.__file__)
print(getattr(fdpf, "__version__", "unknown"))
```

12. Run the Fabric MVP smoke test recipe.
13. Record evidence:
    - git commit SHA
    - package version
    - wheel filename
    - Fabric Environment
    - notebook name
    - test mode
    - result
    - known limitations

> ⚠️ Do not upload a changed wheel with the same version into Fabric. Bump both `pyproject.toml` and `src/fabricops_kit/__init__.py` `__version__`, rebuild, re-upload, publish, and restart the notebook session.
