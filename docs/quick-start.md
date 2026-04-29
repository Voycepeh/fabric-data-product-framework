# Quick Start

Use this page when you want the shortest path to run the framework end to end.  
For full onboarding detail, see [getting-started.md](getting-started.md).

## 1) Prepare outside Fabric
- Confirm business purpose, steward, approved usage, and caveats.
- Prepare supporting inputs (mapping/reference data and required metadata).

## 2) Run local smoke test
```bash
python -m compileall src tests
PYTHONPATH=src pytest -q
```

## 3) Run minimal Fabric notebook flow
1. Open the framework notebook/template in Fabric.
2. Set runtime parameters and declare source inputs.
3. Run profiling/drift/contract + DQ checks.
4. Apply transformation logic and review outcomes.
5. Review run summary, lineage, and handover artifacts.

See [fabric-smoke-test.md](fabric-smoke-test.md) for step-by-step Fabric validation.

## 4) Use the lifecycle model
- Lane overview: [README.md](../README.md#lane-handoff-overview)
- Full 13-step lifecycle: [lifecycle-operating-model.md](lifecycle-operating-model.md)

## 5) Function/API reference
See [src/README.md](../src/README.md) for callable function usage.
