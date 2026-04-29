# Local Smoke Test

Use local validation for logic that does **not** require Fabric runtime services.

## What local testing covers
- Unit and integration tests in `tests/`.
- Import and syntax checks.
- Pandas/small-sample execution paths.
- Contract, drift, incremental, and DQ rule logic.
- Documentation sanity for examples/commands.

## Commands
1. `python -m compileall src tests`
2. `PYTHONPATH=src pytest -q`

## What local testing does not cover
- PySpark execution in Fabric runtime.
- Lakehouse and OneLake read/write behavior.
- `notebookutils` integration.
- Fabric AI function execution.
- Large-scale profiling performance.

For those checks, run [fabric-smoke-test.md](fabric-smoke-test.md).
