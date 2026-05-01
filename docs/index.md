# Documentation Portal

Use this site as the operating manual for running and understanding the Fabric Data Product Framework MVP.

## Canonical user path

1. [Quick Start](quick-start.md)
2. [MVP Workflow](mvp-workflow.md)
3. [Lifecycle Operating Model](lifecycle-operating-model.md)

Supporting pages:

- [Architecture](architecture.md)
- [Fabric Smoke Test](fabric-smoke-test.md)
- [UV Wheel + Fabric Install Guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md)
- [Capability Status](capability-status.md)
- [Function Reference](reference/SUMMARY.md)

## Documentation map (inventory)

| Page | Purpose | Read when | Status |
|---|---|---|---|
| [Home](index.md) | Portal and navigation | You need the right next doc | canonical |
| [Quick Start](quick-start.md) | Only end-to-end MVP runbook | You want to run the MVP now | canonical |
| [MVP Workflow](mvp-workflow.md) | Canonical 13-step workflow details | You need step-by-step meaning and outputs | canonical |
| [Lifecycle Operating Model](lifecycle-operating-model.md) | Human/Framework/AI/Fabric roles and handoffs | You are designing responsibilities and approvals | canonical |
| [Architecture](architecture.md) | System components and runtime flow | You need architecture context | supporting reference |
| [Fabric Smoke Test](fabric-smoke-test.md) | Fabric validation checklist | You are validating readiness | supporting reference |
| [UV Wheel + Fabric Install Guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md) | Wheel build and Fabric install details | You are packaging and deploying to Fabric | supporting reference |
| [Recipes](recipes/index.md) | Task-specific how-to playbooks | You need focused implementation patterns | recipe |
| [Capability Status](capability-status.md) | Implemented vs planned capability view | You need delivery/maturity status | supporting reference |
| [Function Reference](reference/SUMMARY.md) | Generated callable reference | You need function-level details | developer/internal |

## Documentation maintenance guardrails

- Quick Start is the only end-to-end runbook.
- Do not create another onboarding page unless it has a distinct purpose.
- Any lifecycle mention must map to the canonical 13-step MVP workflow.
- Do not duplicate wheel build steps outside the UV guide.
- Do not duplicate function reference content outside `/reference/`.
- Recipes must stay task-specific and non-canonical.
