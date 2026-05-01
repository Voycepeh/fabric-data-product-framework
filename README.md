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
This framework is inspired by [Databricks Labs DQX](https://databrickslabs.github.io/dqx/docs/guide/ai_assisted_quality_checks_generation/) patterns (profiling, quality rule generation, quality check storage, check execution, and quarantine/summary metrics), but it is **not** a fork, clone, or replacement for DQX.

This repository adapts that pattern to Microsoft Fabric notebooks, Lakehouse/Warehouse, Fabric AI functions, and Copilot-style workflows.

## Visual overview

These visuals summarize the user benefits, workflow improvement, and canonical MVP flow.

### What users get
![Framework benefits](docs/assets/framework-benefits.png)

### Before vs after
![Before and after](docs/assets/before-after.png)

### MVP flow
![MVP flow](docs/assets/mvp-flow.png)

## How does AI comes into play?
AI helps draft DQ rules, sensitivity labels, lineage, transformation summaries, and handover notes.
We do it via creating functions within this framework that allow us to prompt the native [AI function](https://learn.microsoft.com/en-us/fabric/data-science/ai-functions/overview?tabs=pandas-pyspark%2Cpandas) or standardize prompts that we manually generate and paste into copilot.

Start here:
- Docs homepage: <https://voycepeh.github.io/fabric-data-product-framework/>
- Quick Start runbook: [docs/quick-start.md](docs/quick-start.md)
- Canonical lifecycle: [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Build and install in Fabric guide: [docs/UV_WHEEL_FABRIC_INSTALL_GUIDE.md](docs/UV_WHEEL_FABRIC_INSTALL_GUIDE.md)
- List of available function: [generated function reference](docs/reference/index.md)
