# Template Function Map

Start from the templates first. This page shows how the templates, lifecycle steps, and reusable modules fit together.

## Start from the templates

### [00_env_config](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb)
**Purpose:** Shared runtime configuration, Fabric checks, paths, and naming rules.

**Use when:** Setting up the workspace or validating the framework before running templates.

**Main modules:**
[`config`](../api/modules/config/) [`runtime`](../api/modules/runtime/) [`fabric_io`](../api/modules/fabric_io/)

### [Exploration notebook](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb)
**Purpose:** Profile source data, capture metadata, explore logic, and use AI for suggestions.

**Use when:** Understanding source data and preparing candidate DQ or governance rules.

**Main modules:**
[`fabric_io`](../api/modules/fabric_io/) [`profiling`](../api/modules/profiling/) [`metadata`](../api/modules/metadata/) [`ai`](../api/modules/ai/) [`dq`](../api/modules/dq/) [`governance`](../api/modules/governance/) [`drift`](../api/modules/drift/)

### [Pipeline contract notebook](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb)
**Purpose:** Run approved transformation, enforce rules, quarantine failures, write outputs, and store evidence.

**Use when:** Turning approved exploration into a repeatable production pipeline.

**Main modules:**
[`contracts`](../api/modules/contracts/) [`quality`](../api/modules/quality/) [`dq`](../api/modules/dq/) [`technical_columns`](../api/modules/technical_columns/) [`fabric_io`](../api/modules/fabric_io/) [`lineage`](../api/modules/lineage/) [`run_summary`](../api/modules/run_summary/) [`handover`](../api/modules/handover/) [`metadata`](../api/modules/metadata/)

## Lifecycle flow

1. Configure environment and runtime.
2. Confirm agreement, purpose, and ownership.
3. Read source data.
4. Profile source and store metadata.
5. Explore transformation logic.
6. Use AI to suggest DQ rules or classification.
7. Human reviews and approves.
8. Run the pipeline contract.
9. Enforce approved DQ rules.
10. Quarantine failed rows.
11. Write accepted output.
12. Profile output and store evidence.
13. Generate lineage and handover notes.

AI remains advisory; the approved pipeline contract is the enforcement point for production behavior.

## How to use the function pages

The module pages are the detailed API reference. This page is the workflow router.

Use module pages when you need signatures, parameters, return values, and implementation details:
- [Functions → Modules index](../api/modules/)
- [`config`](../api/modules/config/)
- [`fabric_io`](../api/modules/fabric_io/)
- [`quality`](../api/modules/quality/)
- [`lineage`](../api/modules/lineage/)

## Common recipes

- **Read from Fabric:** Use [`fabric_io`](../api/modules/fabric_io/) for lakehouse and warehouse read helpers.
- **Profile a source table:** Use [`profiling`](../api/modules/profiling/) and persist outputs with [`metadata`](../api/modules/metadata/).
- **Build AI-ready context:** Use [`profiling`](../api/modules/profiling/), [`metadata`](../api/modules/metadata/), and [`drift`](../api/modules/drift/) to provide structured evidence to prompts.
- **Suggest DQ rules:** Use [`ai`](../api/modules/ai/) with [`dq`](../api/modules/dq/) for draft rule generation.
- **Suggest column classification:** Use [`ai`](../api/modules/ai/) and apply policies from [`governance`](../api/modules/governance/).
- **Enforce approved DQ rules:** Use [`quality`](../api/modules/quality/) and [`dq`](../api/modules/dq/) inside the approved contract flow.
- **Quarantine failed rows:** Use quarantine and failure-path helpers in [`quality`](../api/modules/quality/) with write targets from [`fabric_io`](../api/modules/fabric_io/).
- **Write output table:** Use [`fabric_io`](../api/modules/fabric_io/) for controlled output writes.
- **Store metadata evidence:** Use [`metadata`](../api/modules/metadata/) and contract structures in [`contracts`](../api/modules/contracts/).
- **Generate lineage and handover:** Use [`lineage`](../api/modules/lineage/), [`run_summary`](../api/modules/run_summary/), and [`handover`](../api/modules/handover/).
