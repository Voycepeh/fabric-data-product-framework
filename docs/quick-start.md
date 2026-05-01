# Quick Start (MVP Runbook)

Use this runbook to execute the canonical 13-step MVP lifecycle end to end in Microsoft Fabric.

For detailed wheel packaging commands, see the [UV wheel and Fabric environment guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md).

## 1) Local setup

1. Clone the repo and create your environment.
2. Install dependencies (project standard).
3. Confirm you can run Python and `uv` in your shell.

## 2) Run smoke tests locally

```bash
uv run python -m compileall src tests
uv run python -m pytest -q
```

## 3) Build the wheel

```bash
uv build
```

Use the generated wheel from `dist/` for Fabric Environment upload.

## 4) Upload wheel into Fabric

1. In Microsoft Fabric, open your target **Environment**.
2. Upload the wheel artifact from `dist/`.
3. Publish/update the Environment.
4. Attach the Environment to the MVP notebook.

For exact UI steps and troubleshooting, use the [UV wheel and Fabric environment guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md).

## 5) Run the MVP notebook template

1. Open the framework MVP notebook template in Fabric.
2. Set runtime/config parameters for your dataset.
3. Run the notebook flow (profile, validate, transform, and publish outputs).

Related workflow docs:
- [Fabric notebook template workflow](workflows/fabric-notebook-template.md)
- [Fabric smoke test checklist](fabric-smoke-test.md)

## 6) Review generated outputs

After execution, review:

- Metadata and profiling artifacts.
- Data quality results and accepted rules.
- Schema/data drift checks.
- Governance/sensitivity decisions.
- Lineage and transformation summaries.
- Handover package artifacts.

## Expected output

A successful run should leave you with a reproducible Fabric notebook execution plus persisted metadata, DQ/governance/drift evidence, lineage context, and handover-ready artifacts aligned to the canonical 13-step MVP lifecycle.
