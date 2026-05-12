# Assembled Contract Model

This page describes the assembled handover shape of a FabricOps data contract.

FabricOps still produces a data contract. The contract is assembled from approved metadata evidence across profiling, DQ, governance, drift, lineage, and runtime workflows.

## What the assembled contract must answer

| Contract question | Assembled evidence source |
| --- | --- |
| What dataset is used or produced? | Dataset/table identity and approved usage metadata |
| What is the approved usage? | Governance approval and usage constraints metadata |
| What columns exist and how do they behave? | Profile and schema evidence |
| What quality expectations are approved? | Approved DQ rule metadata |
| What quality evidence was observed in this run? | DQ results and quarantine evidence |
| What drift boundaries are approved and what drift occurred? | Drift guardrails and drift results |
| How was the output produced? | Lineage and transformation evidence |
| When and where did this run execute? | Runtime/run summary metadata |

## Conceptual assembled shape (handover view)

```yaml
dataset:
  name: ...
  domain: ...
  approved_usage: ...
schema_profile:
  columns: [...]
  profile_summary: ...
quality:
  approved_rules: [...]
  execution_results: [...]
governance:
  classifications: [...]
  usage_constraints: [...]
drift:
  guardrails: [...]
  run_results: [...]
lineage:
  inputs: [...]
  transformations: [...]
runtime:
  run_id: ...
  environment: ...
  executed_at: ...
  status: ...
```

## Open Data Contract export target

The assembled handover view is the right place to generate an Open Data Contract compatible export (YAML/JSON) for external review and interoperability.

If full compatibility is not yet implemented in a given deployment, treat this as the target export model rather than a claim of complete implementation.
