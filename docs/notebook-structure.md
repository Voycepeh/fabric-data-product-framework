# Notebook Structure

Use this six-notebook split for a teachable and handover-friendly implementation.

| Notebook | Stable convention |
| --- | --- |
| `00_governance_setup` | Capture purpose, owner/steward, usage boundaries, and governance context. |
| `01_source_and_profile` | Declare source data and run source profiling. |
| `02_exploration_notes` | Record transformation rationale, caveats, and decisions. |
| `03_transform_and_model` | Apply transformation logic and prepare outputs. |
| `04_checks_and_gates` | Run DQ, drift, and incremental safety checks. |
| `05_handover_export` | Export lineage, run summary, and handover context. |

## Stable notebook standards

- Keep AI-generated content reviewable and explicitly human-approved.
- Keep run artifacts reproducible, including profiles, DQ results, lineage, and handover outputs.

For workflow steps and execution order, use [Quick Start](quick-start.md).
