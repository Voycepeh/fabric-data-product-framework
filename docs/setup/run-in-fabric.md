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

Example verification:

```python
import fabricops_kit
from fabricops_kit import data_profiling, data_quality, data_governance
```
