# Fabric Data Product Framework

A metadata-first, AI-in-the-loop framework for running Microsoft Fabric data product workflows end to end.

## What this repository provides

- Reusable Python framework utilities in `src/`.
- MVP notebook templates in `templates/notebooks/`.
- Public documentation and runbooks in `docs/`.

## Canonical documentation path

For onboarding and execution, follow:

1. [Docs Home](docs/index.md)
2. [Quick Start](docs/quick-start.md)
3. [MVP Workflow](docs/mvp-workflow.md)
4. [Lifecycle Operating Model](docs/lifecycle-operating-model.md)

## Supporting references

- [Architecture](docs/architecture.md)
- [Fabric Smoke Test](docs/fabric-smoke-test.md)
- [UV Wheel + Fabric Install Guide](docs/UV_WHEEL_FABRIC_INSTALL_GUIDE.md)
- [Capability Status](docs/capability-status.md)
- [Function Reference](https://voycepeh.github.io/fabric-data-product-framework/reference/)

## MVP workflow summary

1. Define dataset purpose and steward.
2. Setup config and environment.
3. Declare source and ingest data.
4. Profile source and capture metadata.
5. Explore data.
6. Explain transformation logic.
7. Build transformation pipeline.
8. AI-generate DQ rules.
9. Human review DQ rules.
10. AI suggest sensitivity labels.
11. Human review and governance gate.
12. AI-generated lineage and transformation summary.
13. Run summary and handover pack.

## Callable Function Reference

Use the generated docs reference: <https://voycepeh.github.io/fabric-data-product-framework/reference/>.
