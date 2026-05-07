# Metadata and Contracts

## Fabric-first contract model

FabricOps adopts Open Data Contract principles in a Fabric-first form. Contracts are authored and reviewed through notebooks or tables, stored as approved metadata records in a dedicated Fabric metadata target, and enforced by pipeline notebooks. ODCS YAML can be added later as an import/export format for teams that also use Git-based contract workflows.

Open Data Contract principles remain the design direction for compatibility, governance clarity, and long-term interoperability. In FabricOps, YAML is not required as the runtime editing model. Instead, approved metadata tables are the operational source of truth inside Fabric.

## Why not YAML-first in Fabric

YAML is valuable for Git workflows, portability, and external contract exchange. However, many Fabric teams operate primarily through notebooks, Spark DataFrames, Lakehouse tables, Warehouse tables, and Power BI stewardship views.

In that context, editing raw YAML inside notebooks is usually not the best review and approval experience for stewards or operators. FabricOps therefore uses notebook-friendly Python dicts/tables first, with ODCS YAML import/export planned later for interoperability.

## Source input contract vs output product contract

- **Source input contract**: the minimum expectations a pipeline needs from an upstream source to run safely (schema, required columns, keys, freshness, and quality thresholds). This does **not** imply FabricOps owns or controls the upstream producer.
- **Output product contract**: the expectations for produced downstream data (schema, metadata, classifications, and quality expectations) that consumers rely on.

## How contracts are edited in Fabric

In intended operation, `02_ex` and `03_pc` have distinct responsibilities:

- **`02_ex` notebook**
  - profiles source data
  - inspects schema, grain, keys, nulls, freshness, classifications, and candidate DQ rules
  - may use AI to suggest DQ rules/classifications
  - drafts contract metadata for review
  - records approved contract metadata after human/steward approval

- **`03_pc` notebook**
  - does not invent contract values or approvals
  - loads the latest approved contract from the metadata target
  - enforces required columns, business keys, approved DQ rules, and classifications
  - fails fast when contract requirements are not met

Example draft contract structure:

```python
SOURCE_INPUT_CONTRACT_DRAFT = {
    "contract_id": "student_events_source_input_v1",
    "contract_type": "source_input",
    "dataset_name": "student_events",
    "object_name": "raw_student_events",
    "version": "0.1.0",
    "status": "draft",
    "grain": "one row per student event",
    "required_columns": ["student_id", "event_id", "event_timestamp"],
    "optional_columns": ["event_description"],
    "business_keys": ["event_id"],
    "classifications": {
        "student_id": "confidential",
        "event_id": "internal"
    },
    "quality_rules": [
        {
            "rule_id": "event_id_not_null",
            "rule_type": "not_null",
            "column": "event_id",
            "severity": "critical"
        }
    ],
    "approved_by": None,
    "approval_note": None
}
```

## Metadata target as operational source of truth

The metadata target should be a dedicated Lakehouse or Warehouse per environment.

- Source/Unified/Product stores hold business data.
- Metadata stores FabricOps framework evidence.
- Approved contracts should not exist only as notebook variables.
- Approved contracts should not exist only as YAML files.
- Production pipelines must never read development metadata.

For promotion between environments, see [Deployment and Promotion](deployment-and-promotion.md).

## Recommended metadata tables

- **`FABRICOPS_CONTRACTS`**
  - one row per contract version
  - stores approval status, lifecycle status, semantic version, and full contract JSON

- **`FABRICOPS_CONTRACT_COLUMNS`**
  - one row per contract column
  - stores required flag, business key flag, classification, logical/physical type, and description

- **`FABRICOPS_CONTRACT_RULES`**
  - one row per approved DQ rule
  - stores rule type, target column, severity, status, and full rule JSON

- **`FABRICOPS_QUALITY_RESULTS`**
  - stores quality execution outcomes from pipeline runs

- **`FABRICOPS_DATASET_RUNS`**
  - stores run-level evidence such as run ID, dataset, source, target, status, and row counts

- **`FABRICOPS_LINEAGE_RECORDS`**
  - stores source/target lineage and transformation summaries

Optional: classifications can initially live in `FABRICOPS_CONTRACT_COLUMNS`. A dedicated classification table can be added later if needed.

## Notebook flow

`02_ex`
→ profile source
→ draft contract
→ review AI suggestions
→ approve contract
→ write metadata records

`03_pc`
→ load latest approved contract
→ enforce required columns
→ enforce DQ rules
→ apply runtime standards
→ write output and evidence

## ODCS relationship

ODCS remains the open-standard direction. FabricOps stores operational contracts as metadata records first inside Fabric. ODCS YAML import/export should be added later as an interoperability feature, allowing Fabric-native stewardship and runtime while preserving a path to open-standard contract exchange.
