# Contract model

This page is the conceptual source of truth for what a FabricOps data contract contains.

## What a FabricOps data contract must answer

| Contract question | Contract evidence |
| --- | --- |
| What dataset is used or produced? | Source and target object identifiers, agreed dataset purpose, and schema context. |
| What is the approved usage? | Approved usage boundaries from the data sharing agreement and governance review. |
| What columns must exist? | Expected schema and structural column definitions. |
| What are required columns? | Mandatory fields that must be present and non-null for the contract to pass. |
| What are business keys and grain? | Key columns and row-grain definition used for uniqueness and joins. |
| What DQ rules must pass? | Approved rule set, severity, and threshold expectations. |
| Which columns are sensitive? | Approved sensitivity/classification labels and handling requirements. |
| Who approved it? | Named owners/stewards and approval checkpoints. |
| What run evidence is captured? | DQ results, failed-row evidence, schema/runtime snapshots, and run summaries. |

## Contract lifecycle (conceptual)

1. Define approved usage and dataset intent.
2. Profile source data and draft candidate metadata.
3. Review and approve DQ and classification metadata.
4. Persist approved contract metadata.
5. Enforce approved contract metadata in `03_pc` pipeline runs.
6. Persist runtime evidence for audit, monitoring, and handover.

## Relationship to notebook execution

`03_pc` notebooks enforce approved contract metadata at runtime. Notebook ownership and role boundaries are defined in [Notebook Structure](../notebook-structure.md).
