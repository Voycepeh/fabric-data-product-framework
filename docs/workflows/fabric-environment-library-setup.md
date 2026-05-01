# Fabric Environment custom library setup

Use this workflow to keep reusable logic in the framework library while keeping notebooks flow-oriented.

## Recommended workflow

1. Develop framework code locally in VS Code.
2. Run tests locally before packaging.
3. Build the wheel locally.
4. Upload the wheel to a Fabric Environment as a custom library.
5. Attach that Fabric Environment to execution notebooks.
6. Import framework modules directly from notebooks.
7. Keep notebooks thin and orchestration-focused.
8. Keep reusable logic in the framework package.

## Example local build commands

```bash
python -m pip install -U build
python -m build
```

The built wheel is produced in the `dist/` folder.

## Notebook usage note

After the Fabric Environment is attached, notebooks can import framework modules (for example, `import fabric_data_product_framework as fw`) and call reusable functions without embedding large utility code directly in notebook cells.
