# Lifecycle Operating Model

![FabricOps Starter Kit canonical lifecycle workflow](assets/mvp-flow.png)

FabricOps Starter Kit uses a 10-step lifecycle as a **business operating model** for data products in Microsoft Fabric. It is not only a notebook sequence: it connects governance intent, source expectations, exploration evidence, controlled pipeline enforcement, and handover obligations from start to finish.

## 10-step business operating model

### Step 1: Governance context  
**Actor:** Governance

Capture approved usage, ownership, and business agreement before technical work begins.

### Step 2: Configure runtime & startup checks  
**Actor:** Starter kit

Define shared runtime configuration and validate notebook startup conditions so every run begins from a known-good environment.

### Step 3: Define source + output contract expectations  
**Actor:** Starter kit

Set source and output contract expectations, including schema, keys, update pattern, and required controls.

### Step 4: Ingest, profile & store source data  
**Actor:** Starter kit

Ingest source data, profile it, and store source-aligned evidence for traceability.

### Step 5: Explore/profile data & draft contract metadata  
**Actor:** Analyst / data scientist notebook

Explore profiled source data, validate business meaning, and draft contract metadata proposals for review.

### Step 6: Execute controlled pipeline contract  
**Actor:** Engineering + starter kit

Pipeline notebooks enforce approved metadata deterministically. This includes:

- load approved contract
- validate schema + keys
- enforce approved DQ rules
- split accepted vs quarantined rows
- write outputs + evidence

### Step 7: Profile output & publish product contract  
**Actor:** Starter kit

Profile curated output and publish the downstream product contract and related metadata.

### Step 8: Suggest AI-assisted DQ rules  
**Actor:** AI-assisted + human review

Use AI to suggest candidate data quality rules from profiling and context. Suggestions remain advisory until approved.

### Step 9: Suggest AI-assisted column classification  
**Actor:** AI-assisted + human review

Use AI to suggest sensitivity and classification labels for columns. Suggestions remain advisory until approved.

### Step 10: Generate lineage & handover documentation  
**Actor:** AI-assisted handover generation

Generate lineage, operational evidence, and handover documentation for review and reuse.

## Metadata as the operating source of truth

The lifecycle is coordinated through approved metadata stored in Fabric metadata or lakehouse tables.

Core metadata includes:

- `contracts`
- `contract_columns`
- `contract_rules`
- `dataset_runs`
- `quality_results`
- `lineage_records`

Exploration notebooks draft and suggest metadata. Human reviewers approve it. Pipeline contract notebooks load approved metadata and enforce it deterministically.

## DQ rules and quarantine boundary

DQ rules validate row-level and column-level value quality during pipeline enforcement.

Approved DQ rules are enforced in pipeline contract notebooks. Rows that pass are written to curated or production output. Rows that fail are written to quarantine with failure reasons.

Optional AI mapping is only a remediation path for quarantined rows that failed `accepted_values` or in-list checks. AI can suggest mappings, but humans must approve mappings before pipeline notebooks reapply them and re-evaluate the affected rows.

Schema drift, data drift, freshness checks, and row-count monitoring remain part of the drift/contract layer, not the DQ rule engine.

## AI boundary and accountability

- AI suggestions happen in exploration notebooks.
- Step 8 and Step 9 are advisory only.
- Humans, governance owners, and data stewards approve.
- Human engineers enforce approved rules and labels in pipeline notebooks.
- AI does not directly approve or enforce governance controls.

## Related documentation

- For platform boundaries and store responsibilities, use the guidance in [Metadata and Contracts](metadata-and-contracts.md) and [Deployment and Promotion](deployment-and-promotion.md).
- For notebook role boundaries and sequencing, see [Notebook Structure](notebook-structure.md).
- For contract authoring/storage details, see [Metadata and Contracts](metadata-and-contracts.md).
- For environment promotion controls, see [Deployment and Promotion](deployment-and-promotion.md).
