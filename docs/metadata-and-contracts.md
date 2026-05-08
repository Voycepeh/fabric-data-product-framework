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



## Data contract vs handover document

A data contract and a handover document are related, but they are not the same thing.

The data contract is the structured agreement for a dataset. It defines what the source or output data should contain, how it may be used, which columns and keys matter, which quality rules must pass, which classifications apply, and who approved the contract.

The handover document is the wider operating guide for a human taking over the work. It explains the business context, notebook structure, design decisions, known caveats, transformation rationale, and where to find the important artifacts.

In FabricOps, the data contract is one important part of the handover package. It does not replace the handover document.

| Artifact | What it answers | Main reader | Stored as |
| --- | --- | --- | --- |
| Data contract | What must this dataset contain, what is approved, and what must be enforced? | Data engineer, steward, pipeline, AI assistant | Contract metadata records |
| Handover document | Why was the pipeline built this way, and how should a human take over? | Engineer, analyst, steward | Markdown or generated documentation |
| Metadata evidence | What happened during each run, and did the contract pass? | Pipeline owner, governance reviewer, AI assistant | Run, quality, schema, and lineage tables |

Put simply: the handover document tells the story; the data contract defines the enforceable agreement.

## Designed for humans and AI assistants

FabricOps stores contract information in two forms at the same time.

For humans, the contract should be readable as plain English sections, review tables, and notebook outputs. A steward should be able to review the dataset purpose, approved usage, columns, classifications, DQ rules, and approval status without reading raw code or YAML.

For AI assistants, the same contract should be stored as structured metadata records. This gives AI a reliable context pack for suggesting DQ rules, sensitivity classifications, lineage summaries, and documentation. It also reduces ambiguity because the AI reads approved metadata instead of guessing from free text.

| Audience | Needs | FabricOps design choice |
| --- | --- | --- |
| Human reviewer | Clear explanation, reviewable tables, approval context | Plain English docs, notebook displays, metadata tables |
| Pipeline notebook | Deterministic enforcement | Load approved contract records and fail fast when expectations are not met |
| AI assistant | Structured context for suggestions | Contract JSON, column records, profile records, DQ rule records, classification metadata |
| Governance reviewer | Evidence and audit trail | Approval fields, run records, quality results, lineage records |

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

### 7. Lineage and handover evidence

- source object
- target object
- transformation step
- transformation summary
- business reason
- notebook name
- code/run identifier
- run timestamp

## How notebooks use the contract

### Exploration notebook: 02_ex

The exploration notebook discovers and drafts the contract. It profiles source data, checks schema, nulls, keys, and freshness, uses AI to suggest DQ rules and classifications, supports steward review/approval, and writes approved metadata.

The exploration notebook is also where AI-readable context is prepared from profile records, column metadata, and draft contract content.

AI can suggest contract content in exploration, but humans approve the rules and classifications.

### Pipeline contract notebook: 03_pc

The pipeline notebook enforces the approved contract. It loads the latest approved contract, validates required columns and business keys, runs approved quality rules, applies runtime standards, writes output data, then writes run evidence, quality results, and lineage metadata.

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
