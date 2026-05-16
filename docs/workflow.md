# FabricOps Workflow

![FabricOps workflow overview](assets/mvp-flow.png)

This page explains the canonical 13-step FabricOps workflow. The workflow connects human decisions, AI assistance, Fabric notebook execution, metadata evidence, pipeline contracts, and handover outputs. AI suggests, humans approve where governance or data quality judgment is required, and the framework validates, logs, and packages evidence for handover.

## 1. Governance steward

Governance stewards define the data sharing agreement and approved usage once, including business context, classification, and sensitivity/PII handling.

AI role: AI suggests governance metadata candidates, and a human governance steward approves controls.

## 2. Analyst / data scientist

Analysts and data scientists profile source data, validate business meaning, and review DQ rule candidates.

AI role: AI applies/suggests candidate rules, and humans validate rule validity.

## 3. Data engineer

Data engineers build and run pipeline contracts that:

- load approved metadata
- move source to target
- enforce approved DQ rules
- quarantine failures
- write runtime evidence

## 4. Handover / data contract

Handover is generated from approved metadata, lineage, quality results, and execution evidence.

AI role: AI generates handover from approved metadata-backed records; no human is needed for generation.

## 5. Metadata / contract store (source of truth)

The metadata-backed contract store is the operational source of truth:

- `contracts`
- `contract_columns`
- `contract_rules`
- `quality_results`
- `lineage_records`

## 6. Core operational loop: Step 5 → Step 2

Pipeline execution evidence feeds back into governance metadata.

This Step 5 → Step 2 loop is the core operational loop between governance and engineering.

## AI touchpoints

- Step 2 — Governance metadata: AI suggests, human approves.
- Step 4 — DQ rules: AI applies/suggests candidates, human validates rule validity.
- Step 6 — Handover: AI generates from approved metadata and evidence; no human needed for generation.

## Related documentation

- [Notebook Structure](notebook-structure.md)
- [Metadata and Data Contract Assembly](metadata-and-contracts.md)
- [Data Quality Rules System](data-quality-rules-system.md)
