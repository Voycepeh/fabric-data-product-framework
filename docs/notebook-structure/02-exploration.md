# `02_ex_<agreement>_<topic>`

`02_ex_<agreement>_<topic>` is the exploration and proposal notebook in the FabricOps Starter Kit lifecycle.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open template notebook</a>

## Purpose

`02_ex` is where analysts and data scientists investigate source data, test shaping ideas, and capture evidence that informs governance and pipeline contracts.

This notebook is for exploration and proposal. It is not the production enforcement notebook.

## Ownership

- Primary owner: Analyst / Data Scientist
- Collaboration partners: Governance steward, data engineer

## Naming convention

- Pattern: `02_ex_<agreement>_<topic>`
- Example: `02_ex_agreement_customer_orders`
- The agreement segment should align to the related `01_data_sharing_agreement_<agreement>` notebook.

## What belongs in `02_ex`

- Source investigation and data profiling
- Discovery of source quirks and edge cases
- Exploratory transforms to test joins, mappings, filters, and shaping logic
- AI-assisted DQ suggestion drafting
- AI-assisted classification/sensitivity candidate suggestions
- Findings summaries and metadata evidence capture
- Proposal notes for governance updates and future `03_pc` logic

## What does not belong in `02_ex`

- Governance approval decisions (owned by `01_data_sharing_agreement`)
- Final run-all-safe production transform logic (owned by `03_pc`)
- Production enforcement of approved DQ rules (owned by `03_pc`)
- Scheduled pipeline execution responsibilities

## Recommended notebook flow

1. **Introduction and scope**
   - Agreement ID
   - Topic
   - Source being explored
   - Question being answered
   - Approved usage context from the data sharing agreement
2. **Configuration and setup**
   - Import shared config from `00_env_config`
   - Validate notebook naming convention
   - Resolve environment paths, lakehouse/warehouse names, and metadata targets
3. **Data ingestion for exploration**
   - Load source data
   - Run basic count/schema checks
   - Register or inspect source metadata where relevant
4. **Data exploration and profiling**
   - Profile source columns
   - Inspect nulls, distinct counts, min/max, duplicates, distributions, sample records
   - Capture analyst observations
5. **Exploratory transforms**
   - Test joins, filters, mappings, derived columns, date/time logic, deduplication logic, and other shaping ideas
   - Make clear these are exploratory until moved into `03_pc`
6. **AI-assisted proposals**
   - AI-assisted DQ suggestions
   - AI-assisted classification / sensitivity suggestions
   - AI-assisted summarisation of findings
   - AI-assisted lineage notes if useful
   - State clearly that AI output is advisory and requires human validation/approval
7. **Findings and proposal**
   - Freeze the important findings
   - Explain why downstream transformations or controls are needed
   - Identify proposed metadata updates for `01_data_sharing_agreement`
   - Identify proposed pipeline logic for `03_pc`
8. **Handoff**
   - Governance updates go to `01_data_sharing_agreement` for approval
   - Approved rules/classifications are later consumed by `03_pc`
   - Production transformation and enforcement belong in `03_pc`

**Principle:** “02_ex is allowed to contain exploratory transformation logic, but final repeatable run-all-safe transformation logic belongs in 03_pc.”

## AI boundary

AI can assist exploration by generating candidate rules, candidate classifications, and concise finding summaries.

AI output in `02_ex` is advisory only. Human validation is required before governance approval and before any production enforcement behavior.

## Handoff to `01_data_sharing_agreement` and `03_pc`

- `02_ex` captures evidence and proposal rationale.
- `01_data_sharing_agreement` owns governance approval and approved metadata state.
- `03_pc` loads approved metadata/rules/classifications and enforces deterministic logic in run-all-safe scheduled execution.

## Examples

- Exploratory example: test deduplication variants and record why one candidate key is most stable.
- Proposal example: propose a `not_null` and pattern check candidate from profile evidence.
- Contract handoff example: document the transform idea in `02_ex`, then implement its production-safe version in `03_pc` after approval.

## Cross-links

- [Canonical notebook structure](../notebook-structure.md)
- [01 data sharing agreement notebook](01-data-sharing-agreement.md)
- [03 pipeline contract notebook](03-pipeline-contract.md)
- [Data quality rules system](../data-quality-rules-system.md)
- [Metadata and contracts](../metadata-and-contracts.md)
