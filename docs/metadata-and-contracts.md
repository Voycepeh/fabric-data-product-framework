# Data Contracts and Metadata

## What is a data contract?

A data contract is the agreement that makes a dataset safe to use. It defines what the data should contain, how it may be used, which quality checks must pass, who approved it, and what downstream users or pipelines can rely on.



| Question | Why it matters |
| --- | --- |
| What dataset are we using or producing? | Identifies the exact source or output table. |
| What is the approved usage? | Prevents reuse outside the approved purpose. |
| What columns should exist? | Catches schema changes early. |
| Which columns are required? | Prevents silent missing critical fields. |
| What are the business keys and grain? | Makes joins, deduplication, and row meaning clear. |
| What data quality rules must pass? | Stops bad data from flowing downstream unnoticed. |
| Which columns are sensitive? | Supports classification, masking, and governance review. |
| Who approved the contract? | Gives ownership and accountability. |
| What happened during the run? | Supports audit, lineage, troubleshooting, and handover. |

The data contract is the promise between the notebook, the data engineer, the data steward, and the downstream consumer.

## What is the Open Data Contract Standard?

The Open Data Contract Standard (ODCS) is a structured way to describe data contracts, commonly as YAML or JSON. It covers core ideas such as schema definitions, quality expectations, ownership, service-level expectations, governance metadata, and contract versioning.

FabricOps uses ODCS as design inspiration for interoperability and governance clarity, but not as a YAML-first runtime requirement. FabricOps follows the spirit of ODCS, but chooses a table-first operational model so contracts can be reviewed, queried, governed, and enforced inside Fabric. In FabricOps, contracts are collected and reviewed through notebooks and tables, stored as metadata records in Fabric, and enforced by pipeline notebooks. ODCS YAML or JSON import/export can be added later for teams that need cross-platform exchange.

## Why FabricOps is not YAML-first

YAML is useful for Git-based contract workflows, portability, and exchange with other tools. A YAML or JSON version of the contract can be useful later for interoperability with ODCS-style workflows.

FabricOps does not make YAML the primary editing or runtime model because many Fabric teams work mainly through notebooks, Spark DataFrames, Lakehouse tables, Warehouse tables, and Power BI stewardship views.

For those users, editing raw YAML is usually not the easiest review experience. Data stewards and analysts often need to see contracts as tables, notebook outputs, or Power BI-friendly metadata records.

FabricOps therefore uses a Fabric-native flow:

1. Exploration notebooks profile the data and draft the contract.
2. Humans review and approve the contract content.
3. Approved contract metadata is stored in Fabric metadata tables.
4. Pipeline notebooks load the approved metadata and enforce it.
5. YAML or JSON export can be added later as an interoperability layer.

In short: YAML is a good exchange format, but Fabric metadata tables are the operational source of truth.

## FabricOps data contract model

FabricOps uses one data contract model with two perspectives.

| Perspective | What it means | Examples |
| --- | --- | --- |
| Input expectations | What the pipeline expects from the source before it can run safely | Source object, required columns, business keys, freshness, minimum quality thresholds |
| Output expectations | What the pipeline promises to produce for downstream users | Target object, output schema, descriptions, classifications, approved DQ rules, consumer-facing metadata |

> **One contract model, two perspectives.** Input expectations protect the pipeline. Output expectations protect downstream consumers.




## The 03_pc notebook is the executable contract

In FabricOps, the pipeline contract starts in the notebook.

The 03_pc notebook is the executable version of the contract. It contains the source expectations, output expectations, quality rules, approved classification metadata to load and enforce, transformation logic, runtime checks, and evidence writing.

The metadata tables do not replace the notebook. They make the notebook contract queryable, reviewable, AI-readable, and auditable.

The data contract is the structured metadata summary of what the 03_pc notebook declares, checks, enforces, and records.

| Contract view | Meaning |
| --- | --- |
| 03_pc notebook | Executable contract and enforcement logic |
| Metadata tables | Queryable contract records and run evidence |
| Handover document | Human narrative explaining why the pipeline exists and how to take over |
| Generated contract summary | Human and AI-readable summary of the approved contract state |

## From metadata logger to contract metadata

FabricOps extends the metadata logger pattern.

The basic pattern is:

1. Profile a table.
2. Store column-level metadata.
3. Attach approved DQ rules to profiled columns.
4. Attach approved classification or sensitivity decisions to profiled columns.
5. Run the rules inside 03_pc.
6. Store quality results, classification evidence, schema snapshots, and run evidence.
7. Generate a contract summary from the stored metadata.

Profile first, attach controls to profiled columns, enforce in 03_pc, then store evidence.

| Metadata layer | Purpose |
| --- | --- |
| Profile metadata | Captures table, schema, column, type, nulls, distincts, min/max, and run timestamp |
| DQ rule metadata | Stores approved quality rules joined to profiled columns |
| Classification metadata | Stores approved sensitivity and governance decisions joined to profiled columns |
| Runtime evidence | Stores rule results, row counts, failures, warnings, and run status |
| Contract summary | Presents the current approved contract in a readable form |
| Handover evidence | Explains transformation rationale, lineage summary context, caveats, and ownership context |

## Column identity and joins

Rules should not float separately from the profile. DQ rules, classification records, and runtime evidence should join back to the profiled column records.

Use a stable column identity based on:

- workspace or data store identity
- schema name where relevant
- table name
- column name

This can be stored as a composite key and/or a hash key.

| Key | Purpose |
| --- | --- |
| column_contract_key | Stable key for joining column profile, DQ rules, and classification records |
| run_id | Identifies one pipeline execution |
| profile_timestamp | Identifies when a profile snapshot was captured |
| contract_version | Identifies which approved contract state was enforced |

The stable column key identifies the column across runs. The run ID and timestamp identify what happened during a specific execution.

## DQ rules and classification use the same pattern

Data quality and classification are different controls, but FabricOps should treat them with the same operating pattern.

| Pattern | Data quality | Classification |
| --- | --- | --- |
| Target | Column or table | Column or table |
| Draft source | Profiling, AI suggestion, human review | Profiling, AI suggestion, steward review |
| Stored metadata | Rule type, threshold, severity, status | Sensitivity label, exposure rule, approval status |
| Approval | Engineer or steward | Steward or governance reviewer |
| Enforcement | Fail, warn, quarantine, or log | Mask, exclude, flag, or require approval |
| Evidence | Quality result records | Classification audit or review records |

AI can suggest DQ rules and classifications, but approved metadata remains the source of truth that humans review and 03_pc enforces.

FabricOps uses two metadata categories:

1. **Runtime contract metadata** used or produced directly by 03_pc: profile metadata, approved DQ rules, approved classification rules or labels, quality results, and run evidence.
2. **Generated handover evidence** produced after notebook completion (especially in handover/documentation phases): transformation summaries, lineage summaries or diagrams, handover summaries, and AI context packs.

Lineage and transformation rationale can later be persisted as first-class metadata tables, but the first practical implementation can treat them as generated handover evidence rather than runtime enforcement metadata.

## Data contract vs handover document

A data contract and a handover document are related, but they are not the same thing.

The data contract is the structured agreement for a dataset. It defines what the source or output data should contain, how it may be used, which columns and keys matter, which quality rules must pass, which classifications apply, and who approved the contract.

The handover document is the wider operating guide for a human taking over the work. It explains the business context, notebook structure, design decisions, known caveats, transformation rationale, and where to find the important artifacts.

In FabricOps, the 03_pc notebook is the executable contract and the data contract is the enforceable metadata summary of what it declares and enforces.

The handover document is the human story, and the data contract is part of that handover package. It does not replace the handover document.

| Artifact | What it answers | Main reader | Stored as |
| --- | --- | --- | --- |
| Data contract | What must this dataset contain, what is approved, and what must be enforced? | Data engineer, steward, pipeline, AI assistant | Contract metadata records |
| Handover document | Why was the pipeline built this way, and how should a human take over? | Engineer, analyst, steward | Markdown or generated documentation |
| Metadata evidence | What happened during each run, and did the contract pass? | Pipeline owner, governance reviewer, AI assistant | Run, quality, and schema evidence tables |

Put simply: the handover document tells the story; the 03_pc notebook executes the contract; and the data contract captures the enforceable metadata summary.

## Designed for humans and AI assistants

FabricOps stores contract information in two forms at the same time.

For humans, the contract should be readable as plain English sections, review tables, and notebook outputs. A steward should be able to review the dataset purpose, approved usage, columns, classifications, DQ rules, and approval status without reading raw code or YAML.

For AI assistants, the same contract should be stored as structured metadata records. This gives AI a reliable context pack for suggesting DQ rules, sensitivity classifications, lineage summaries, and documentation. It also reduces ambiguity because the AI reads approved metadata instead of guessing from free text.

| Audience | Needs | FabricOps design choice |
| --- | --- | --- |
| Human reviewer | Clear explanation, reviewable tables, approval context | Plain English docs, notebook displays, metadata tables |
| Pipeline notebook | Deterministic enforcement | Load approved contract records and fail fast when expectations are not met |
| AI assistant | Structured context for suggestions | Contract JSON, column records, profile records, DQ rule records, classification metadata |
| Governance reviewer | Evidence and audit trail | Approval fields, run records, quality results, and generated handover evidence |

AI can suggest rules, classifications, and documentation, but the approved contract remains the source of truth that humans review and pipelines enforce.

## What FabricOps stores in metadata

FabricOps stores approved contract definitions and run evidence in Fabric metadata tables (for example, in a dedicated Lakehouse or Warehouse), so runtime pipelines can enforce approved expectations and produce auditable evidence.

### 1. Contract header

- contract id
- version
- status
- dataset name
- source object
- target object
- data agreement id
- approved usage
- owner/steward
- approval fields
- full contract JSON

### 2. Contract columns

- column name
- data type
- required flag
- business key flag
- nullable flag
- description
- classification
- source mapping
- output visibility
- steward notes

### 3. Contract rules

- rule id
- rule type
- target column
- severity
- threshold
- rule status
- rule JSON
- approval fields

### 4. Dataset run evidence

- run id
- contract id/version
- source object
- target object
- row counts
- run status
- runtime info
- error summary

### 5. Quality results

- run id
- rule id
- target column
- pass/fail counts
- result status
- severity
- sample failures where available
- execution timestamp

### 6. Schema/profile snapshots

- table name
- column name
- data type
- row count
- null count/percent
- distinct count/percent
- min/max values
- run timestamp

### 7. Optional generated lineage and handover evidence

- source object
- target object
- transformation step
- transformation summary
- business reason
- notebook name
- code/run identifier
- run timestamp

Lineage and transformation rationale may later be persisted as first-class metadata, but the first implementation can treat them as generated handover evidence rather than mandatory runtime enforcement tables.

## How notebooks use the contract

### Exploration notebook: 02_ex

The exploration notebook discovers and drafts the contract. It profiles source data, checks schema, nulls, keys, and freshness, uses AI to suggest DQ rules and classifications, supports steward review/approval, and writes approved metadata.

The exploration notebook is also where AI-readable context is prepared from profile records, column metadata, and draft contract content.

AI can suggest contract content in exploration, but humans approve the rules and classifications.

### Pipeline contract notebook: 03_pc

The pipeline notebook enforces the approved contract. It loads the latest approved contract, validates required columns and business keys, runs approved quality rules, loads and enforces approved classification metadata, applies runtime standards, writes output data, then writes runtime evidence and quality results. Lineage and handover documentation are generated post-run or during handover workflows.

The pipeline contract notebook should read approved contract metadata, not free-form handover prose.

Pipeline notebooks should not invent rules at runtime. They enforce rules that were already approved.



## Where to find the implementation helpers

The callable implementation details are maintained in the generated Function Reference so this page does not become a second source of truth.

- [Step 3: Declare source contract & ingest source data](reference.md#step-3-declare-source-contract--ingest-source-data)
- [Step 4: Validate source against contract & capture metadata](reference.md#step-4-validate-source-against-contract--capture-metadata)
- [Step 7: Validate output & persist target metadata](reference.md#step-7-validate-output--persist-target-metadata)
- [Step 8: Generate, review & configure DQ rules](reference.md#step-8-generate-review--configure-dq-rules)
- [Step 9: Generate & review classification / sensitivity suggestions](reference.md#step-9-generate--review-classification--sensitivity-suggestions)
- [Step 10: Generate data lineage and handover documentation](reference.md#step-10-generate-data-lineage-and-handover-documentation)
