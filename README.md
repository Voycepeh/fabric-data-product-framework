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

## 2) What problem it solves
Data teams often rebuild quality checks, drift controls, governance steps, and run documentation in every notebook. This framework standardises those controls so teams can focus on business transformation logic while keeping governance and release readiness consistent.

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
- AI-assisted notebook lineage: Copilot drafts lineage steps, framework validates/renders, human approves.

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
