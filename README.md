# Fabric Data Product Framework

A Microsoft Fabric-first framework for building governed, quality-checked, drift-aware, contract-validated, handover-ready data products in Fabric notebooks.

## What this framework is
A reusable framework and notebook pattern for standardizing the control-plane work around a dataset: profiling, drift checks, quality checks, contract validation, lineage, and run artifacts.

## Why it exists
Data teams repeatedly rebuild the same delivery controls. This framework keeps those controls consistent so practitioners can focus on business logic and interpretation.

## Who it is for
- Data practitioners and analysts who are comfortable with Python notebooks.
- Junior-to-mid engineers who need a clear, testable Fabric operating model.
- Teams that want AI assistance without removing human accountability.

## Three-lane operating model
| Lane | Responsibility |
|---|---|
| Outside Fabric | Prepare purpose, approved usage, caveats, and supporting context before runtime. |
| Inside Fabric: Human-guided | Configure parameters, interpret profiles, write transformations, review exceptions, approve outcomes. |
| Inside Fabric: Framework-run | Run deterministic checks, enforce gates, log metadata, and produce handover artifacts. |

## Where AI fits
AI supports drafting and summarisation inside the human-guided and framework-run lanes. It does not replace approval or framework gates.

**Boundary:** AI proposes. Humans approve. The framework validates and records.

## Start here
- Lifecycle and notebook journey: [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md)
- AI workflow and guardrails: [docs/workflows/ai-generated-dq-rules.md](docs/workflows/ai-generated-dq-rules.md)
- Capability status: [docs/capability-status.md](docs/capability-status.md)
- Local testing: [docs/local-smoke-test.md](docs/local-smoke-test.md)
- Fabric testing: [docs/fabric-smoke-test.md](docs/fabric-smoke-test.md)
- Function/API reference: [src/README.md](src/README.md)

## Documentation map
- [Getting started](docs/getting-started.md)
- [Lifecycle operating model](docs/lifecycle-operating-model.md)
- [Notebook structure](docs/notebook-structure.md)
- [Contract enforcement](docs/contract-enforcement.md)
- [Run summary](docs/run-summary.md)
- [Lineage](docs/lineage.md)
- [Public repo safety](docs/public-repo-safety.md)


## Callable Function Reference
See [src/README.md](src/README.md) for callable APIs and minimal usage examples.
