# Fabric Data Product Framework

## What this is
A reusable Microsoft Fabric notebook framework for turning raw or source data into governed, quality-checked, handover-ready data products.

It abstracts the repeatable 80% of pipeline work so teams can focus on the dataset-specific 20%: business meaning, transformation logic, and data nuance.

## Why this exists
This framework is designed to make Fabric data products easier to:
- build
- review
- govern
- operate
- hand over

It is especially intended for teams where people may know Python or data analysis, but may not yet know Fabric engineering best practices.

## Operating model

| Actor | Owns |
|---|---|
| Functional People | Purpose, definitions, usage, caveats, governance approval, handover acceptance |
| Technical People | Source declaration, EDA, transformation logic, contracts, DQ rules, exception review |
| AI | Drafting, summarising, recommending, explaining, candidate rules, lineage and handover narrative |
| Framework | Profiling, metadata logging, drift checks, DQ execution, validation, write pattern, handover export |

Functional people define meaning. Technical people turn meaning into data products. AI accelerates documentation and reasoning. The framework makes the process repeatable, validated, and handover-ready.

## Lifecycle at a glance

| Step | Stage | Primary actor | Where it happens |
|---:|---|---|---|
| 1 | Dataset purpose and steward agreement | Functional People | Governance doc / metadata table |
| 2 | Business metadata entry | Functional People | Metadata table / form |
| 3 | Governance labeling and usage controls | Functional People | Governance doc / metadata table |
| 4 | Data contract draft | Technical People | Contract file / notebook |
| 5 | Notebook parameters and source declaration | Technical People | Main pipeline notebook |
| 6 | Source profiling | Framework | Profiling notebook / utility |
| 7 | Source metadata logging | Framework | Metadata table |
| 8 | EDA notes and data nuance explanation | Technical People | Separate EDA notebook |
| 9 | Schema drift, data drift, and incremental safety checks | Framework | Checks notebook / reusable gate |
| 10 | Transformation pipeline | Technical People | Main pipeline notebook |
| 11 | Technical columns and write pattern | Framework | Main pipeline notebook |
| 12 | Output profiling | Framework | Profiling utility / metadata table |
| 13 | DQ rules and contract validation | Technical People + Framework | Checks notebook / pipeline gate |
| 14 | Lineage and transformation summary | Framework + AI + Technical People | Handover notebook |
| 15 | Handover package and AI context export | Framework + AI, accepted by Functional People | Handover notebook |

## Quick start
1. Define purpose, steward, usage, and business metadata.
2. Draft governance labels and data contract expectations.
3. Configure the notebook parameters and declared sources.
4. Run source profiling and metadata logging.
5. Complete the separate EDA notes notebook.
6. Build the transformation pipeline.
7. Run drift, incremental, DQ, and contract checks.
8. Export lineage, run summary, AI context, and handover package.

## More documentation
- [Lifecycle operating model](docs/lifecycle-operating-model.md)
- [Notebook structure](docs/notebook-structure.md)
- [AI in the loop](docs/ai-in-the-loop.md)
- [Functional responsibilities](docs/functional-responsibilities.md)
- [Technical responsibilities](docs/technical-responsibilities.md)
- [Framework responsibilities](docs/framework-responsibilities.md)
- [Handover package](docs/handover-package.md)

## Callable Function Reference
See [src/README.md](src/README.md) for callable API references.
