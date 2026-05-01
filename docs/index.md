# Documentation Portal

Use this site as the **operating manual** for running and understanding the Fabric Data Product Framework MVP.

The canonical learning and execution path is:

1. [Quick Start](quick-start.md)
2. [MVP Workflow](mvp-workflow.md)
3. [Lifecycle Operating Model](lifecycle-operating-model.md)

## Documentation map (inventory)

| Page | Purpose | Read when | Status |
|---|---|---|---|
| [Home](index.md) | Portal and navigation | You need the right next doc | canonical |
| [Quick Start](quick-start.md) | Only end-to-end MVP runbook | You want to run the MVP now | canonical |
| [MVP Workflow](mvp-workflow.md) | Canonical 13-step workflow details | You need step-by-step meaning and outputs | canonical |
| [Lifecycle Operating Model](lifecycle-operating-model.md) | Human / Framework / AI / Fabric role split and handoffs | You are designing responsibilities and approvals | canonical |
| [Architecture](architecture.md) | System components and data/control flow | You need architecture context | canonical |
| [Fabric Smoke Test](fabric-smoke-test.md) | Fabric environment validation checklist | You are validating readiness or onboarding a new environment | supporting |
| [UV Wheel + Fabric Install Guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md) | Detailed packaging/install path | You need wheel build and Fabric Environment install details | reference |
| [Recipes](recipes/index.md) | Task-specific implementation recipes | You need a focused pattern for a specific task | supporting |
| [Capability Status](capability-status.md) | Implemented vs planned coverage by MVP step | You need maturity/status checks | reference |
| [API Overview](api/index.md) | Callable API entry point | You need callable function documentation | reference |

## Documentation maintenance guardrails

- Do not add a new onboarding page unless it has a distinct role not covered by Quick Start.
- Do not duplicate Quick Start run steps in other pages; link back instead.
- Any lifecycle sequence must align to the canonical 13-step MVP workflow.
- When adding capabilities, update [Capability Status](capability-status.md) and link from the relevant canonical page.
- Keep [README](../README.md) high-level and concise.
