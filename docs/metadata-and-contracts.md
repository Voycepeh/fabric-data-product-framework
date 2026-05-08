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

FabricOps uses ODCS as design inspiration for interoperability and governance clarity, but not as a YAML-first runtime requirement. In FabricOps, contracts are collected and reviewed through notebooks and tables, stored as metadata records in Fabric, and enforced by pipeline notebooks. ODCS YAML or JSON import/export can be added later for teams that need cross-platform exchange.

## FabricOps data contract model

FabricOps uses one data contract model with two perspectives.

| Perspective | What it means | Examples |
| --- | --- | --- |
| Input expectations | What the pipeline expects from the source before it can run safely | Source object, required columns, business keys, freshness, minimum quality thresholds |
| Output expectations | What the pipeline promises to produce for downstream users | Target object, output schema, descriptions, classifications, approved DQ rules, consumer-facing metadata |

> **One contract model, two perspectives.** Input expectations protect the pipeline. Output expectations protect downstream consumers.

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

AI can suggest contract content in exploration, but humans approve the rules and classifications.

### Pipeline contract notebook: 03_pc

The pipeline notebook enforces the approved contract. It loads the latest approved contract, validates required columns and business keys, runs approved quality rules, applies runtime standards, writes output data, then writes run evidence, quality results, and lineage metadata.

Pipeline notebooks should not invent rules at runtime. They enforce rules that were already approved.

## Where to find the implementation helpers

The callable implementation details are maintained in the generated Function Reference so this page does not become a second source of truth.

- [Step 3: Declare source contract & ingest source data](reference.md#step-3-declare-source-contract--ingest-source-data)
- [Step 4: Validate source against contract & capture metadata](reference.md#step-4-validate-source-against-contract--capture-metadata)
- [Step 7: Validate output & persist target metadata](reference.md#step-7-validate-output--persist-target-metadata)
- [Step 8: Generate, review & configure DQ rules](reference.md#step-8-generate-review--configure-dq-rules)
- [Step 9: Generate & review classification / sensitivity suggestions](reference.md#step-9-generate--review-classification--sensitivity-suggestions)
- [Step 10: Generate data lineage and handover documentation](reference.md#step-10-generate-data-lineage-and-handover-documentation)
