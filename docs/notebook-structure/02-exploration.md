# `02_ex_<agreement>_<topic>`

Exploration and proposal notebook for analyst/data scientist-led investigation of source data before governance approval and production enforcement.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open template notebook</a>

## Purpose

`02_ex` is where analysts and data scientists explore source data, test shaping logic, and capture evidence that informs governance and pipeline contracts. It is intentionally iterative and analysis-first.

`02_ex` should reuse `00_env_config` for shared config and validation instead of redefining environment setup.

`02_ex` should inspect existing metadata before profiling from scratch. Existing profile rows, approved DQ rules, governance labels, business context, and prior runtime evidence should be reused where current enough.

DQ rule suggestion and DQ rule review in `02_ex` are analyst/engineer data-quality control decisions, not governance approval decisions.

## Ownership

- Primary owner: Analyst / Data Scientist
- Typical collaborators: Data steward, governance owner, data engineer

## Naming convention

- Notebook pattern: `02_ex_<agreement>_<topic>`
- `<agreement>` maps to the governance agreement notebook (`01_data_sharing_agreement_<agreement>`)
- `<topic>` describes the exploration question/domain focus

## What belongs in `02_ex`

- Source data profiling and discovery
- Source quirk investigation and analyst observations
- Exploratory transforms (joins, filters, mappings, derived fields, date/time logic, deduplication ideas)
- AI-assisted DQ suggestion drafting (advisory)
- DQ review widget-based analyst/engineer approval for DQ control decisions
- AI-assisted classification/sensitivity candidate drafting (advisory)
- Metadata evidence and rationale that informs governance updates and downstream pipeline decisions

## What does not belong in `02_ex`

- Governance approval authority
- Final approval-state metadata ownership
- Scheduled, run-all-safe production enforcement
- Final deterministic production transformation contract

`02_ex` does **not** approve governance controls and does **not** enforce approved DQ rules in production. Governance covers usage, ownership, sensitivity/classification, and restrictions; DQ rule approval is owned by analysts/engineers.

## Recommended notebook flow

1. **Introduction and scope**
   - Agreement ID
   - Topic
   - Source being explored
   - Question being answered
   - Approved usage context from the data sharing agreement
2. **Configuration and setup**
   - Import shared config from `00_env_config`
   - Reuse shared runtime checks and naming policy from `00_env_config`
   - Resolve environment paths and source access options
3. **Inspect existing metadata and decide whether to reuse, refresh, or extend evidence**
   - Review existing profile rows, approved DQ rules, governance labels, business context, and prior proposal/runtime evidence
   - Decide whether evidence is current enough to reuse or needs refresh
4. **Data ingestion for exploration**
   - Load source data
   - Run basic count/schema checks
   - Register or inspect source metadata where relevant
5. **Data exploration and profiling**
   - Profile source columns
   - Inspect nulls, distinct counts, min/max, duplicates, distributions, sample records
   - Capture analyst observations
6. **Exploratory transforms**
   - Test joins, filters, mappings, derived columns, date/time logic, deduplication logic, and other shaping ideas
   - Mark exploratory logic clearly until promoted into pipeline contract execution
7. **AI-assisted proposals**
   - AI-assisted DQ suggestions
   - AI-assisted classification/sensitivity suggestions
   - AI-assisted summarisation of findings
   - AI-assisted lineage notes when useful
   - Clearly state AI output is advisory and requires human validation/approval
8. **Findings and proposal**
   - Freeze important findings
   - Explain why downstream transformations or controls are needed
   - Identify proposed metadata updates for `01_data_sharing_agreement`
   - Identify proposed pipeline logic for `03_pc`
9. **Handoff**
   - Governance updates go to `01_data_sharing_agreement` for approval
   - Approved rules/classifications are later consumed by `03_pc`
   - Production transformation and enforcement belong in `03_pc`

**Principle:** “02_ex is allowed to contain exploratory transformation logic, but final repeatable run-all-safe transformation logic belongs in 03_pc.”

## AI boundary

- AI suggestions in `02_ex` are advisory drafts, not approvals.
- Human reviewers validate evidence and proposals before governance metadata is updated.
- Governance control authority remains in `01_data_sharing_agreement`; execution enforcement remains in `03_pc`.

## Handoff to `01_data_sharing_agreement` and `03_pc`

- Promote validated governance proposals from `02_ex` into `01_data_sharing_agreement_<agreement>` for official approval/state management.
- Promote approved transformation and enforcement requirements into `03_pc_<agreement>_<pipeline>` for deterministic scheduled execution.

## Examples

- Explore source null behaviors and propose candidate required-field rules for analyst/engineer DQ review.
- Trial date standardization logic and document why a deterministic transform should be implemented in `03_pc`.
- Use AI to suggest classification candidates, then record analyst rationale and hand off for governance approval.

## Cross-links

- [Canonical notebook structure](../notebook-structure.md)
- [01 data sharing agreement role](../notebook-structure.md#notebook-roles-and-responsibilities)
- [03 pipeline contract notebook](03-pipeline-contract.md)
- [Data quality rules system](../data-quality-rules-system.md)
- [Metadata and contracts](../metadata-and-contracts.md)
