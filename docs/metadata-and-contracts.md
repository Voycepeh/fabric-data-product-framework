# Metadata and Data Contract Assembly

![Data contract assembly from approved metadata evidence](assets/data-contract.png)

## 1. What it is

A FabricOps data contract is a human-readable and AI/machine-readable handover document for a data product.

It records what the data is, why it exists, how it can be used, what quality and governance rules apply, and who owns responsibility for it.

In FabricOps, the contract is assembled from approved metadata evidence instead of maintained as one large standalone contract file.

## 2. Why contract evidence is assembled in parts

Each workflow owns and approves the evidence it is responsible for:

| Workflow | Evidence it owns |
| --- | --- |
| Profiling | Schema/profile evidence, such as row counts, nulls, distinct counts, and min/max values |
| Data quality | Approved DQ rules and DQ execution evidence |
| Governance | Approved classifications, sensitivity, and usage constraints |
| Drift | Approved guardrails and drift results |
| Lineage | Transformation logic and source-to-output mapping evidence |
| Runtime summary | Run context, such as run id, notebook/pipeline, timestamps, status, and owner |

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

Use conceptual names where physical table names are not finalized.

## 4. Handover/export target

At handover, FabricOps joins approved metadata records by dataset, table, column, run, version, and approval status into the final contract view.

That assembled view is the operational data contract output.

Open Data Contract compatible YAML/JSON remains the export target for the assembled contract view.

## 5. Related pages

- [Assembled contract model](contract-model.md)
- [Metadata tables](metadata-tables.md)
- [Notebook structure](../notebook-structure.md)
- [Data Quality Rules System](../data-quality-rules-system.md)
