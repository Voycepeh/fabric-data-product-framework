# Metadata and Data Contract Assembly

## 1. What it is

FabricOps still produces a data contract.

The difference is where that contract comes from: FabricOps assembles it from approved metadata evidence instead of maintaining one large standalone contract object as the primary source of truth.

## 2. Why contract evidence is assembled in parts

Each workflow owns and approves the evidence it is responsible for:

| Workflow | Evidence it owns |
| --- | --- |
| Profiling | Schema/profile evidence (row counts, nulls, distinct counts, min/max) |
| Data quality | Approved DQ rules and DQ execution evidence |
| Governance | Approved classifications, sensitivity, and usage constraints |
| Drift | Approved guardrails and drift results |
| Lineage | Transformation and source-to-output mapping evidence |
| Runtime summary | Run context (run id, notebook/pipeline, timestamps, status, owner) |

This keeps ownership clear and avoids duplicating one workflow's evidence inside another workflow's authoring layer.

## 3. Metadata tables as source of truth

Approved metadata tables are the source of truth. Conceptual table families include:

- `FABRICOPS_PROFILE_RESULTS`
- `FABRICOPS_DQ_RULES`
- `FABRICOPS_DQ_RESULTS`
- `FABRICOPS_GOVERNANCE_CLASSIFICATIONS`
- `FABRICOPS_DRIFT_GUARDRAILS`
- `FABRICOPS_DRIFT_RESULTS`
- `FABRICOPS_LINEAGE_RECORDS`
- `FABRICOPS_RUN_SUMMARY`

(Use conceptual names where physical table names are not finalized.)

## 4. Handover/export target

At handover, FabricOps joins approved metadata records (for example by dataset, table, column, run, version, and approval status) into the final contract view.

That assembled handover view is the operational data contract output.

Open Data Contract compatible YAML/JSON remains the export target for this assembled contract view.

## 5. Related pages

- [Assembled contract model](metadata-and-contracts/contract-model.md)
- [Metadata tables](metadata-and-contracts/metadata-tables.md)
- [Notebook Structure](notebook-structure.md)
- [Data Quality Rules System](data-quality-rules-system.md)
