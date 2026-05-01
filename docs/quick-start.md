# Quick Start (MVP End-to-End Runbook)

This is the **only** end-to-end runbook for the Fabric Data Product Framework MVP.

## Canonical 13-step workflow this runbook executes

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

For detailed step semantics, see [MVP Workflow](mvp-workflow.md).

## Prerequisites

- Python and `uv` installed locally.
- Access to the target Microsoft Fabric workspace and Environment UI.
- Permission to upload a wheel to Fabric Environment.
- Synthetic/sample dataset for first validation run.

## 1) Clone and set up locally

```bash
git clone https://github.com/Voycepeh/fabric-data-product-framework.git
cd fabric-data-product-framework
```

Install dependencies using your standard project setup.

## 2) Validate local baseline

```bash
uv run python -m compileall src tests
uv run python -m pytest -q
```

## 3) Build the framework wheel

```bash
uv build
```

Expected output: a wheel file in `dist/`.

## 4) Upload/install wheel in Fabric Environment

1. Open your target Fabric **Environment**.
2. Upload the wheel from `dist/`.
3. Publish/update the Environment.
4. Attach the Environment to your MVP notebook.

Detailed UI flow: [UV Wheel + Fabric Install Guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md).

## 5) Open and run the MVP notebook template

Use:

- `templates/notebooks/fabric_data_product_mvp.py`
- `templates/notebooks/fabric_data_product_mvp.md` (usage notes)

Run the notebook end to end with safe defaults first (`USE_SAMPLE_DATA=True`, writes disabled).

## 6) Required user inputs before full run

Provide or confirm:

- Dataset purpose and steward/owner.
- Runtime identifiers (domain, source/target names, run context).
- Source declaration (table/path and ingestion assumptions).
- Transformation rationale and intended output behavior.
- Human approvals for DQ rules and governance labels.

## 7) Expected artifacts from a successful run

You should produce and review:

- Source profile and metadata artifacts.
- DQ candidate rules and approved DQ rule set.
- Governance/sensitivity suggestions and approved labels.
- Lineage records and transformation summary.
- Run summary outputs.
- Handover pack artifacts.

Use [Fabric Smoke Test](fabric-smoke-test.md) to verify evidence for each MVP step.

## 8) Success checklist

- Local checks pass.
- Wheel builds and installs in Fabric Environment.
- Notebook runs with sample data safely.
- Human reviews complete for DQ and governance gates.
- Artifacts for profile, DQ, governance, lineage, run summary, and handover are present.

## 9) Troubleshooting and next references

- [Fabric Smoke Test](fabric-smoke-test.md)
- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Architecture](architecture.md)
- [Recipes](recipes/index.md)
- [Function Reference](reference/SUMMARY.md)
