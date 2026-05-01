# Quick Start (MVP Runbook)

Use this as the **single end-to-end runbook** for the Fabric Data Product Framework MVP.

## Canonical 13-step workflow covered by this runbook

1. Define dataset purpose and steward
2. Setup config and environment
3. Declare source and ingest data
4. Profile source and capture metadata
5. Explore data
6. Explain transformation logic
7. Build transformation pipeline
8. AI-generate DQ rules
9. Human review DQ rules
10. AI suggest sensitivity labels
11. Human review and governance gate
12. AI-generated lineage and transformation summary
13. Run summary and handover pack

For detailed step behavior and ownership, see [MVP Workflow](mvp-workflow.md) and [Lifecycle Operating Model](lifecycle-operating-model.md).

## 1) Local setup

1. Clone the repo.
2. Install project dependencies.
3. Confirm `uv` and Python run in your shell.

## 2) Validate locally

```bash
uv run python -m compileall src tests
uv run python -m pytest -q
```

## 3) Build the wheel

```bash
uv build
```

Upload the generated wheel from `dist/` to your Fabric Environment.

## 4) Install in Fabric Environment

1. Open your target Fabric **Environment**.
2. Upload the wheel.
3. Publish/update the Environment.
4. Attach it to your notebook.

For full install details, use [UV Wheel + Fabric Install Guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md).

## 5) Run the MVP notebook

1. Open `templates/notebooks/fabric_data_product_mvp.py` in Fabric notebook form (or use the markdown template as guidance).
2. Configure runtime inputs for your dataset.
3. Execute the notebook through the full MVP workflow.

Use [Fabric Smoke Test](fabric-smoke-test.md) to validate expected evidence per step.

## 6) Review output artifacts

Confirm artifacts for profile, DQ, governance, lineage, run summary, and handover are generated and reviewable.

## 7) Continue with supporting references

- [Recipes](recipes/index.md)
- [Architecture](architecture.md)
- [Capability Status](capability-status.md)
- [API Overview](api/index.md)
