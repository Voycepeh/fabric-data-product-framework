# Metadata tables

This page describes the approved metadata evidence FabricOps stores and how those records are assembled into a data contract view for handover.

Metadata tables are the source of truth. The contract is the assembled output, not a duplicated standalone source.

## Conceptual source-of-truth tables

Use these as conceptual names if exact physical table names are not finalized:

1. `FABRICOPS_PROFILE_RESULTS`
2. `FABRICOPS_DQ_RULES`
3. `FABRICOPS_DQ_RESULTS`
4. `FABRICOPS_GOVERNANCE_CLASSIFICATIONS`
5. `FABRICOPS_DRIFT_GUARDRAILS`
6. `FABRICOPS_DRIFT_RESULTS`
7. `FABRICOPS_LINEAGE_RECORDS`
8. `FABRICOPS_RUN_SUMMARY`

## What each table family contributes

| Table family | Typical fields | Ownership |
| --- | --- | --- |
| Profile results | dataset/table/column, data_type, row_count, null_count, distinct_count, min/max, profile_timestamp | Profiling workflow |
| DQ rules | dataset/table/column scope, rule_id, rule_type, severity, threshold/params, approval status, version | DQ workflow |
| DQ results | run_id, rule_id, pass/fail counts, status, sample failures, executed_at | DQ workflow |
| Governance classifications | dataset/table/column scope, classification label, sensitivity tier, usage constraints, approval status | Governance workflow |
| Drift guardrails | dataset/table/column scope, allowed schema/profile/partition bounds, status, version | Drift workflow |
| Drift results | run_id, drift type, observed value, expected bound, pass/fail, executed_at | Drift workflow |
| Lineage records | run_id, input objects, output objects, transformation metadata | Lineage workflow |
| Run summary | run_id, workspace/env, notebook/pipeline id, start/end time, status, owner | Runtime workflow |

## Assembly joins and identity keys

Contract assembly should join records by stable identity keys such as:

- dataset/domain identity
- table identity
- column identity (when column-level evidence applies)
- run_id
- version/effective window
- approval status

A stable composite key and/or hash key can prevent DQ, governance, drift, and profile evidence from becoming disconnected across workflow boundaries.

## Handover contract assembly

At handover, approved records are joined into a single contract view that captures:

- approved usage intent,
- schema and profiling evidence,
- approved DQ rules and run-time DQ evidence,
- approved governance classifications,
- drift guardrails and drift outcomes,
- lineage and runtime execution evidence.

That assembled view is the operational data contract for review, audit, and export.
