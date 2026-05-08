# Metadata tables

FabricOps stores approved contract definitions and run evidence in Fabric metadata tables (for example, in a dedicated Lakehouse or Warehouse), so runtime pipelines can enforce approved expectations and produce auditable evidence.

## Core metadata records

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

- lineage summary links or generated views
- transformation rationale summaries
- handover-oriented run context for operations and governance

## Column identity and joins

Rules should not float separately from profile records. DQ rules, classification records, and runtime evidence should join back to profiled column records.

Use a stable column identity based on workspace/data-store identity, schema (where relevant), table name, and column name. This can be stored as a composite key and/or hash key.

| Key | Purpose |
| --- | --- |
| `column_contract_key` | Stable key for joining column profile, DQ rules, and classification records |
| `run_id` | Identifies one pipeline execution |
| `profile_timestamp` | Identifies when a profile snapshot was captured |
| `contract_version` | Identifies which approved contract state was enforced |

## DQ and classification follow the same operating pattern

| Pattern | Data quality | Classification |
| --- | --- | --- |
| Target | Column or table | Column or table |
| Draft source | Profiling, AI suggestion, human review | Profiling, AI suggestion, steward review |
| Stored metadata | Rule type, threshold, severity, status | Sensitivity label, exposure rule, approval status |
| Approval | Engineer or steward | Steward or governance reviewer |
| Enforcement | Fail, warn, quarantine, or log | Mask, exclude, flag, or require approval |
| Evidence | Quality result records | Classification audit or review records |

AI can suggest DQ rules and classifications, but approved metadata remains the source of truth that humans review and `03_pc` enforces.
