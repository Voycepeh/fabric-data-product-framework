# Quick Start: End-to-End Workflow

Use this page as the primary runbook for executing the framework end to end in Microsoft Fabric.

## Prerequisites

- Python 3.11+ and `uv` installed locally.
- Access to a Microsoft Fabric workspace with Lakehouse/Warehouse and Environment permissions.
- A dataset with defined business purpose, ownership, and acceptance rules.

## 1) Install and prepare

```bash
git clone https://github.com/Voycepeh/FabricOps-Starter-Kit.git
cd FabricOps-Starter-Kit
uv sync --all-extras
uv build
```

For Fabric Environment install steps, use [Fabric Wheel Install](setup/fabric-wheel-install.md).

## 2) Open your Fabric notebook and load/create config

- Start from `templates/notebooks/fabric_data_product_mvp.md`.
- Attach the Fabric Environment that contains the package wheel.
- Create or load runtime/framework config (paths, dataset IDs, output targets, run context).

## 3) Run the 13-step end-to-end workflow

This run path maps to the [Lifecycle Operating Model](lifecycle-operating-model.md):

1. Validate notebook naming.
2. Create/load runtime and path config.
3. Read source data.
4. Profile source metadata.
5. Generate or define quality checks.
6. Human review of quality/governance intent.
7. Apply quality checks.
8. Detect schema/profile/partition drift.
9. Run core transformations.
10. Add technical columns and write prep.
11. Write output and profile output.
12. Generate governance metadata and lineage.
13. Generate handover/run summary and validate final product readiness.

## 4) Validate completion criteria

A successful run should leave you with:

- source and output profiling artifacts,
- quality and drift results,
- written output table(s),
- governance metadata,
- lineage output,
- handover/run summary artifacts,
- explicit human sign-off for release decisions.

## 5) Next references

- Notebook conventions: [Notebook Structure](notebook-structure.md)
- Workflow model: [Lifecycle Operating Model](lifecycle-operating-model.md)
- Architecture: [Architecture](architecture.md)
- Callable catalogue: [Reference](reference/index.md)
