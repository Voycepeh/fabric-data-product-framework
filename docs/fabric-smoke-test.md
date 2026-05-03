# Fabric smoke test (MVP 13-step checklist)

Use synthetic data only (for example: `sample_orders_source`, `sample_orders_product`).

Status legend:
- **Executable now**: runs locally/DRY_RUN with current template/example.
- **DRY_RUN stubbed**: placeholder path is wired, full runtime action is mocked.
- **Fabric AI/Copilot required**: needs actual Fabric AI/Copilot notebook runtime to be fully exercised.

| MVP step | Expected callable or notebook section | Expected artifact | How to verify in Fabric | Current execution status |
|---|---|---|---|---|
| 1 Define data product | section 1 context setup | `data_product_context` | Context artifact is present in final artifact map | Executable now |
| 2 Setup config and environment | section 2 runtime setup | `runtime_config` | Runtime config is present and includes dry-run context | Executable now |
| 3 Declare source and ingest data | source declaration + reader path | `source_declaration` | In DRY_RUN, synthetic dataframe exists; in Fabric, adapter reads table | DRY_RUN stubbed |
| 4 Profile source and capture metadata | `profile_dataframe` | `source_profile` | Source profile contains row/column details | Executable now |
| 5 Explore data | exploration notes section | `exploration_notes` | Exploration notes artifact is recorded | Executable now |
| 6 Explain transformation logic | rationale section | `transformation_rationale` | Rationale artifact exists | Executable now |
| 7 Build transformation pipeline | transform section | `output_table` | Output rows produced in DRY_RUN; Fabric write path remains adapter-based | DRY_RUN stubbed |
| 8 AI generate DQ rules | DQ candidate generation section | `dq_candidate_rules` | Deterministic/stub candidate rules generated | Executable now (stubbed AI) |
| 9 Human review DQ rules | approval + gate section | `approved_dq_rules` | Approved rules list exists and gate result recorded | Executable now |
| 10 AI suggest sensitivity labels | governance classification section | `sensitivity_suggestions` | Suggestions generated via classifier heuristic (or AI in Fabric) | Executable now (stubbed AI) |
| 11 Human review and governance gate | governance approval section | `approved_governance_labels` | Approved governance labels artifact exists | Executable now |
| 12 AI generated lineage and transformation summary | lineage build section | `lineage_record` | Lineage record generated with framework helper | Executable now (AI summary optional) |
| 13 Handover starter kit pack | handover + validation section | `handover_pack` | Pack includes `profile`, `dq`, `governance`, `lineage`, `run_summary`, `caveats`; validation passes | Executable now |

For fully AI-authored outputs (steps 8/10/12), run in Fabric notebook runtime with configured AI/Copilot and keep human approval before production use.
