# Fabric Data Product Framework

A reusable Fabric-first notebook framework that turns raw/source data into documented, profiled, quality-checked, drift-aware, governed, AI-ready data products.

## 1) What this framework is
This project is a **metadata-first data contract workflow** for Microsoft Fabric notebooks. It is not just a pipeline template: profiling metadata and contract metadata drive repeatable checks, AI-assisted drafting, human approvals, and handover artefacts.

## 2) What problem it solves
Data teams often rebuild quality checks, drift controls, governance steps, and run documentation in every notebook. This framework standardises those controls so teams can focus on business transformation logic while keeping governance and release readiness consistent.

## 3) MVP lifecycle
The canonical 13-step lifecycle is documented in [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md), including the Mermaid flow and step-by-step responsibilities.

## 4) Module capabilities
Current capability status (implemented vs missing vs next build priorities) is maintained in [docs/capability-status.md](docs/capability-status.md).

## 5) AI-in-the-loop responsibilities
AI is used to **suggest, draft, explain, and accelerate**:
- DQ rule candidates from profiling + context.
- Sensitivity/governance draft labels from metadata.
- Transformation and lineage summaries for handover.

AI does **not** own the data product lifecycle.

## 6) What humans still own
Humans remain accountable for:
- Business purpose, approved usage, and consumer intent.
- DQ rule approval (accept/edit/reject).
- Sensitivity labels, masking decisions, and publish constraints.
- Production promotion readiness.

## 7) Current implementation status
- Canonical status: [docs/capability-status.md](docs/capability-status.md)
- Implementation detail: [docs/framework-status.md](docs/framework-status.md)
- Callable APIs: [src/README.md](src/README.md)

## 8) How to test the MVP end to end
- Local smoke test: [docs/local-smoke-test.md](docs/local-smoke-test.md)
- Fabric smoke test: [docs/fabric-smoke-test.md](docs/fabric-smoke-test.md)
- Quick start notebooks/examples: [docs/quick-start.md](docs/quick-start.md), [examples/fabric_smoke_test/README.md](examples/fabric_smoke_test/README.md)

## 9) Roadmap
Roadmap and operating priorities:
- [docs/capability-status.md](docs/capability-status.md)
- [docs/product-plan.md](docs/product-plan.md)

## Start here
- Lifecycle and MVP flow: [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md)
- AI DQ workflow: [docs/workflows/ai-generated-dq-rules.md](docs/workflows/ai-generated-dq-rules.md)
- AI transformation summary workflow: [docs/workflows/ai-transformation-summary.md](docs/workflows/ai-transformation-summary.md)
- Function/API reference: [src/README.md](src/README.md)

## Callable Function Reference
See [src/README.md](src/README.md) for callable APIs and minimal usage examples.
