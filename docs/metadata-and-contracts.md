# Metadata and Data Contract Assembly

FabricOps still produces a data contract. The difference is that the contract is assembled from approved metadata evidence instead of authored and maintained as one large standalone object.

A FabricOps data contract is the final joined view of:
- dataset identity and approved usage,
- schema and profiling metadata,
- approved DQ rules and DQ execution evidence,
- approved governance classifications,
- drift guardrails and drift results,
- lineage and transformation evidence,
- runtime and handover summary.

![FabricOps data contract assembly](assets/data-contract.png)

## 1. What this page is

This section explains how FabricOps metadata becomes a handover-ready contract view.

FabricOps does not abandon data contracts. Instead, it keeps each workflow's evidence in approved metadata tables, then assembles the final contract at handover.

## 2. Why the contract is assembled in parts

Each workflow owns the evidence it is responsible for:

| Workflow | Owns |
| --- | --- |
| Profiling | Source/output profile, row counts, nulls, distinct counts, min/max values |
| Data quality | Approved DQ rules, DQ execution results, quarantine evidence |
| Governance | Approved classifications, sensitivity labels, usage constraints |
| Drift | Schema/profile/partition guardrails and drift results |
| Lineage | Transformation path and source-to-output mapping |
| Runtime summary | Run ID, environment, notebook, timestamps, status, owner |

This avoids a duplicated contract source of truth. Metadata evidence stays with its owning workflow, and handover assembles the joined contract view.

## 3. Metadata tables are the source of truth

Conceptual table names (exact physical names may vary by implementation):

- `FABRICOPS_PROFILE_RESULTS`
- `FABRICOPS_DQ_RULES`
- `FABRICOPS_DQ_RESULTS`
- `FABRICOPS_GOVERNANCE_CLASSIFICATIONS`
- `FABRICOPS_DRIFT_GUARDRAILS`
- `FABRICOPS_DRIFT_RESULTS`
- `FABRICOPS_LINEAGE_RECORDS`
- `FABRICOPS_RUN_SUMMARY`

## 4. The assembled contract view

At handover, FabricOps joins approved metadata records by dataset/table/column/run/version/approval status.

The assembled output becomes the data contract view for the table and the handover artifact used for audit and operational continuity.

## 5. Open Data Contract compatibility

FabricOps should be able to export the assembled handover contract into an Open Data Contract compatible YAML/JSON structure.

This export is an end-state handover capability, not the primary authoring workflow for rules. Teams continue authoring and approving DQ, governance, and drift metadata inside their owning workflows.

## 6. What changed

- FabricOps no longer frames a standalone contract subsystem as the primary source of truth.
- Approved metadata tables are the source of truth.
- Handover assembles the final contract view from workflow-owned evidence.

## Related pages

- [Assembled contract model](metadata-and-contracts/contract-model.md)
- [Metadata tables](metadata-and-contracts/metadata-tables.md)
- [Notebook Structure](notebook-structure.md)
- [Data Quality Rules System](data-quality-rules-system.md)
