# Fabric Data Product Framework

A reusable Fabric-first notebook framework that turns raw/source data into documented, profiled, quality-checked, drift-aware, governed, AI-ready data products.

## 1) What this framework is
This project is a **metadata-first data contract workflow** for Microsoft Fabric notebooks. It is not just a pipeline template: profiling metadata and contract metadata drive repeatable checks, AI-assisted drafting, human approvals, and handover artefacts.

## Relationship to Databricks Labs DQX
This framework takes architectural inspiration from Databricks Labs DQX, especially the pattern of profiling data, generating quality rule candidates, storing quality checks, applying checks, quarantining failures, and collecting summary metrics.
It is not a fork, clone, or replacement for DQX.
It is a Microsoft Fabric-native adaptation for teams working in Fabric Lakehouse, Warehouse, notebooks, Fabric environments, Fabric AI functions, and Microsoft Copilot.
Because Microsoft Fabric does not currently provide an exact one-for-one DQX implementation, this repo implements the same style of workflow using Fabric-native building blocks.

Architecture detail: [docs/architecture/dqx-inspired-fabric-native-dq.md](docs/architecture/dqx-inspired-fabric-native-dq.md)

## 2) What problems this framework solves
This framework is designed to close practical gaps that notebook-first data teams may face in Microsoft Fabric at the point of writing. Fabric provides the platform primitives. This repo adds reusable notebook patterns, metadata tables, validation logic, and AI-in-the-loop workflows so those primitives can be used consistently across data products.

| Fabric gap or practical pain point | What the framework adds | Why it matters |
|---|---|---|
| Fabric notebooks can only attach one default Lakehouse or Warehouse at a time. | Explicit environment and target path handling through `get_path`, `Housepath`, `lakehouse_table_read`, `lakehouse_table_write`, `warehouse_read`, and `warehouse_write`. | Pipelines can read from Source, write to Unified or Product, and support sandbox to release movement without hard-coding paths throughout the notebook. |
| Native profiling tools such as Data Wrangler and notebook exploration are useful, but their results are not automatically reusable pipeline metadata. | Profiling output is persisted through metadata tables using patterns like `ODI_METADATA_LOGGER`. | Metadata becomes an asset that can drive DQ rule generation, drift checks, governance review, lineage, AI context export, and handover. |
| Fabric does not provide an exact notebook-native equivalent of the Databricks DQX AI-assisted data quality workflow for this target use case. | A DQX-inspired pattern that profiles data, drafts candidate checks from metadata and business context, lets humans approve them, then runs them as part of the pipeline. | Teams get a repeatable quality workflow in Fabric notebooks without claiming this repo is a clone or replacement for DQX. |
| Governance metadata can live in separate products such as Microsoft Purview, but that does not automatically make it a notebook engineering control plane. | Lightweight Fabric-side governance metadata for owner, steward, approved usage, required sensitivity, column-level expectations, masking needs, and publish constraints. | Pipelines can directly check engineering-facing governance expectations before publishing or promoting a data product. |
| Lakehouse-oriented workflows can be exposed to schema drift unless expectations are explicitly checked. | Data contract and pipeline contract patterns that define expected columns, types, and allowed changes. | Missing, extra, or changed columns can fail or warn early before dashboards, downstream notebooks, or data products break. |
| Incremental refreshes can silently move bad or unexpected data forward. | Data drift and incremental safety guards for row count changes, null percentage shifts, distinct count changes, date range issues, changed prior-day data, overlaps, and missing windows. | Regular refreshes can fail fast before writing suspicious data into curated layers. |
| Low-code Fabric Data Pipeline or Copy Job patterns can handle some movement and checks, but reusable validation can become tedious for Python-first teams. | Notebook-first reusable Python/PySpark utilities and templates. | Python-proficient analysts, data scientists, and engineers can inspect, teach, debug, and extend the full flow in one familiar surface. |
| Handover needs more than code comments. | Run summaries, transformation summaries, lineage records, metadata exports, and AI-readable context. | A junior engineer, fresh graduate, or new maintainer can understand what the pipeline does, why it exists, what checks protect it, and what still needs human approval. |

AI is treated as a productivity layer, not as the owner of the data product. It can draft DQ rules from profiles, summarize transformation logic, propose lineage, translate business rules into executable checks, and suggest governance labels from metadata. Humans still approve business meaning, sensitive classifications, quality thresholds, and production readiness.

This framework is therefore not trying to replace Fabric. It is a lightweight layer on top of Fabric that makes notebook-based data product engineering more repeatable, inspectable, governed, quality-checked, drift-aware, and AI-ready.

## 3) Visual overview
Add the generated README images under [`docs/assets/`](docs/assets/) using these exact filenames:

| Image | Filename | Purpose |
|---|---|---|
| User benefits | `framework-benefits.png` | Shows what users gain from the framework. |
| Before and after | `before-after.png` | Shows the workflow improvement before vs after adoption. |
| MVP flow | `mvp-flow.png` | Shows the end-to-end MVP lifecycle at a glance. |

<p align="center">
  <img src="docs/assets/framework-benefits.png" alt="Fabric data product framework user benefits" width="850">
</p>

<p align="center">
  <img src="docs/assets/before-after.png" alt="Before and after adopting the Fabric data product framework" width="850">
</p>

<p align="center">
  <img src="docs/assets/mvp-flow.png" alt="Fabric data product framework MVP flow" width="850">
</p>

## 4) MVP lifecycle
The canonical 13-step lifecycle is documented in [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md), including the Mermaid flow and step-by-step responsibilities.

## 5) Module capabilities
Current capability status (implemented vs missing vs next build priorities) is maintained in [docs/capability-status.md](docs/capability-status.md).

## 6) AI-in-the-loop responsibilities
AI is used to **suggest, draft, explain, and accelerate**:
- DQ rule candidates from profiling + context.
- Sensitivity/governance draft labels from metadata.
- Transformation and lineage summaries for handover.

AI does **not** own the data product lifecycle.

## 7) What humans still own
Humans remain accountable for:
- Business purpose, approved usage, and consumer intent.
- DQ rule approval (accept/edit/reject).
- Sensitivity labels, masking decisions, and publish constraints.
- Production promotion readiness.

## 8) Current implementation status
- Canonical status: [docs/capability-status.md](docs/capability-status.md)
- Implementation detail: [docs/framework-status.md](docs/framework-status.md)
- Callable APIs: [src/README.md](src/README.md)

## 9) How to test the MVP end to end
- Local smoke test: [docs/local-smoke-test.md](docs/local-smoke-test.md)
- Fabric smoke test: [docs/fabric-smoke-test.md](docs/fabric-smoke-test.md)
- Quick start notebooks/examples: [docs/quick-start.md](docs/quick-start.md), [examples/fabric_smoke_test/README.md](examples/fabric_smoke_test/README.md)
- Run the actual-data MVP template: [docs/workflows/run-actual-data-mvp.md](docs/workflows/run-actual-data-mvp.md)

## 10) Roadmap
Roadmap and operating priorities:
- [docs/capability-status.md](docs/capability-status.md)
- [docs/product-plan.md](docs/product-plan.md)

## Start here
- Lifecycle and MVP flow: [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md)
- AI DQ workflow: [docs/workflows/ai-generated-dq-rules.md](docs/workflows/ai-generated-dq-rules.md)
- AI transformation summary workflow: [docs/workflows/ai-transformation-summary.md](docs/workflows/ai-transformation-summary.md)
- Fabric-native storage model: [docs/architecture/storage-model.md](docs/architecture/storage-model.md)
- Fabric Environment custom library setup: [docs/workflows/fabric-environment-library-setup.md](docs/workflows/fabric-environment-library-setup.md)
- Credits: [docs/credits.md](docs/credits.md)
- Function/API reference: [src/README.md](src/README.md)

## Callable Function Reference
See [src/README.md](src/README.md) for callable APIs and minimal usage examples.
