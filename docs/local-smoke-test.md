# Local Smoke Test

Use this quick sequence to validate local quality gates before running in Fabric.

## Commands
1. `python -m compileall src tests`
2. `PYTHONPATH=src pytest -q`

## Notes
- Use local smoke test for syntax and behavior checks that do not require Fabric runtime services.
- Use [fabric-smoke-test.md](fabric-smoke-test.md) for minimal in-Fabric validation.
