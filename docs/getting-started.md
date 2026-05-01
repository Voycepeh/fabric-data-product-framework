# Getting Started (Fabric end-to-end)

This guide teaches the full journey: how to prepare context, use the notebook/template pattern in Microsoft Fabric, execute framework checks, and produce handover-ready outputs.

## What this framework gives you
The framework provides reusable controls for:
- Runtime context and naming checks.
- Source/output profiling.
- Drift and incremental safety gates.
- Data-quality and contract validation.
- Lineage records, run summary, and metadata-ready outputs.

See callable functions in [the generated function reference](reference/).

## Three-lane model (how to work)
Use this operating split throughout your implementation:
1. **Outside Fabric**: business context, stewardship, caveats, supporting inputs.
2. **Inside Fabric: Human-guided**: configure runtime, interpret results, transform, approve.
3. **Inside Fabric: Framework-run**: deterministic checks, logs, gates, and handover artifacts.

Read the canonical lifecycle in [lifecycle-operating-model.md](lifecycle-operating-model.md).

## End-to-end implementation path

### 1) Prepare outside Fabric
Before notebook runtime, prepare:
- Dataset purpose, steward/owner, intended usage, caveats.
- Supporting files (reference/mapping tables).
- Metadata and governance expectations.
- A dataset contract YAML (start from synthetic examples under `examples/`).

### 2) Validate locally first
Run local checks before Fabric execution:
```bash
python -m compileall src tests
PYTHONPATH=src pytest -q
```
Local smoke guide: [local-smoke-test.md](local-smoke-test.md).

### 3) Start from the Fabric template path
Use the reusable starter assets:
- Notebook template: `templates/notebooks/fabric_data_product_mvp.md`
- Fabric adapter helpers: `templates/fabric_adapters.py`
- Smoke-test example: `examples/fabric_smoke_test/`

Detailed run path: [fabric-smoke-test.md](fabric-smoke-test.md).

### 4) Build your notebook with the standard structure
Follow the six-notebook split so handover is teachable and repeatable:
- `00_governance_setup`
- `01_source_and_profile`
- `02_exploration_notes`
- `03_transform_and_model`
- `04_checks_and_gates`
- `05_handover_export`

Reference: [notebook-structure.md](notebook-structure.md).

### 5) Execute framework controls in the right order
In your Fabric notebook flow:
1. Build runtime context and validate naming.
2. Load and validate contract.
3. Declare/read source data.
4. Profile source and capture metadata.
5. Run schema drift + incremental safety checks.
6. Apply transformation logic (human-guided).
7. Add technical columns and prepare write pattern.
8. Profile output.
9. Execute DQ and runtime contract validation.
10. Capture lineage and build run summary outputs.

Implementation references:
- [contract-enforcement.md](contract-enforcement.md)
- [run-summary.md](run-summary.md)
- [lineage.md](lineage.md)
- [engine-model.md](engine-model.md)

### 6) Apply AI assistance safely (optional)
AI is for assistance, not accountability:
- Use Copilot/Fabric AI to draft suggestions (DQ rules, summaries, notes).
- Human reviews/approves any AI output.
- Framework validations and metadata records remain the control point.

Workflows:
- [workflows/ai-generated-dq-rules.md](workflows/ai-generated-dq-rules.md)
- [workflows/ai-transformation-summary.md](workflows/ai-transformation-summary.md)

## First successful outcome checklist
You are "running end to end" when you can show:
- Contract loaded and validated.
- Source and output profiles generated.
- Drift and incremental gates executed.
- DQ + contract checks executed and reviewed.
- Output written with expected technical columns.
- Lineage summary produced.
- Run summary rendered and metadata-ready records produced.

## Capability and safety notes
- Current maturity/status: [capability-status.md](capability-status.md)
- Public-safe repo boundaries: [public-repo-safety.md](public-repo-safety.md)
