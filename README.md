# Fabric Data Product Framework

A metadata-first, AI-in-the-loop, Fabric-first notebook framework for building documented, profiled, quality-checked, drift-aware, governed, and handover-ready data products.

## What this framework is
- A reusable Microsoft Fabric notebook workflow.
- Built for Python-proficient data practitioners who need repeatable data product delivery.
- The **data product itself is treated as the contract**.
- Metadata, profile results, DQ rules, governance labels, lineage, and run summaries become reusable contract artifacts.
- AI proposes; humans approve; the framework validates, logs, and packages artifacts.

## What problems it solves

| Problem | Framework response |
|---|---|
| Repetitive notebook setup and Fabric path handling | Reusable runtime/config and notebook workflow structure. |
| Profiling results are not reusable metadata | Profiling artifacts are captured as reusable metadata outputs. |
| Manual DQ rule writing is slow | AI-assisted and deterministic DQ candidate generation with human approval. |
| Schema drift, data drift, and incremental refresh risk | Drift/safety checks are integrated into the data product path. |
| Governance and sensitivity review are disconnected from execution | Governance suggestions and approval artifacts are included in the same workflow. |
| Handover is hard when logic lives only in notebooks | Lineage, run summaries, and handover pack artifacts are assembled for transfer. |

## DQX-inspired, Fabric-native
This framework is inspired by Databricks Labs DQX patterns (profiling, quality rule generation, quality check storage, check execution, and quarantine/summary metrics), but it is **not** a fork, clone, or replacement for DQX.

This repository adapts that pattern to Microsoft Fabric notebooks, Lakehouse/Warehouse, Fabric AI functions, and Copilot-style workflows.

## Visual overview

These visuals summarize the user benefits, workflow improvement, and canonical MVP flow.

### What users get
![Framework benefits](docs/assets/framework-benefits.png)

### Before vs after
![Before and after](docs/assets/before-after.png)

### MVP flow
![MVP flow](docs/assets/mvp-flow.png)

## MVP workflow
1. Define data product
2. Setup config and environment
3. Declare source and ingest data
4. Profile source and capture metadata
5. Explore data
6. Explain transformation logic
7. Build transformation pipeline
8. AI generate DQ rules from metadata, profile, and context
9. Human review DQ rules
10. AI suggest sensitivity labels
11. Human review and governance gate
12. AI generated lineage and transformation summary
13. Handover framework pack

## Role split
- **Human led:** 1, 5, 6, 9, 11
- **Framework led:** 2, 3, 4, 7, 13
- **AI assisted:** 8, 10, 12

## What AI does and does not do
AI helps draft DQ rules, sensitivity labels, lineage, transformation summaries, and handover notes.

Humans still approve business meaning, DQ thresholds, sensitivity classification, governance gates, and release readiness.

## Build and install in Fabric
This framework can be packaged as a wheel with `uv` and installed into a Microsoft Fabric Environment so notebooks import reusable framework code instead of copy-pasting helper cells. After attaching the Environment, run the MVP notebook template end to end.

Guide: [docs/UV_WHEEL_FABRIC_INSTALL_GUIDE.md](docs/UV_WHEEL_FABRIC_INSTALL_GUIDE.md).

## Start here
- Fabric notebook template: [templates/notebooks/fabric_data_product_mvp.md](templates/notebooks/fabric_data_product_mvp.md)
- Fabric smoke-test checklist: [docs/fabric-smoke-test.md](docs/fabric-smoke-test.md)
- Canonical MVP workflow: [docs/mvp-workflow.md](docs/mvp-workflow.md)
- Lifecycle and sequence: [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md)
- Function reference: [src/README.md](src/README.md)
- Notebook recipes: [docs/recipes/index.md](docs/recipes/index.md)
- Capability status: [docs/capability-status.md](docs/capability-status.md)

## Documentation site
Rendered documentation is published on GitHub Pages at <https://voycepeh.github.io/fabric-data-product-framework/>.

The files under `docs/api/` are source markdown files for mkdocstrings and are best viewed through the published docs site.

## Build documentation locally
- `python -m pip install -e "[dev,docs]"`
- `python -m mkdocs build`
- `python -m mkdocs serve`

## Testing
- Local tests: `python -m pytest`
- Synthetic smoke example: `PYTHONPATH=src python examples/mvp_fabric_smoke_test.py`
- Fabric test path: [docs/fabric-smoke-test.md](docs/fabric-smoke-test.md)

## Callable Function Reference
See [src/README.md](src/README.md).
