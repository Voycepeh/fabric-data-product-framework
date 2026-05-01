# Fabric smoke test (MVP 13-step path)

Use this checklist in Fabric to validate the MVP workflow end to end with synthetic data.

## Preconditions
- Use synthetic-only data and placeholder identifiers.
- Recommended flags: `DRY_RUN=True` on first pass.
- Use notebook template in `templates/notebooks/fabric_data_product_mvp.py`.

## Checklist

| MVP step | Expected callable or notebook section | Expected artifact | How to verify in Fabric | Status |
|---|---|---|---|---|
| 1 Define data product | Section 1 | `data_product_context` | Context dict/markdown exists in notebook output. | ☐ |
| 2 Setup config and environment | `build_runtime_context`, config cell | `runtime_config` | Runtime context prints expected paths/mode. | ☐ |
| 3 Declare source and ingest data | source declaration + `read_table`/adapter | `source_declaration` | Synthetic table read succeeds. | ☐ |
| 4 Profile source and capture metadata | `profile_dataframe`, metadata flatten/write | `source_profile` | Profile output persisted or printed. | ☐ |
| 5 Explore data | EDA section | `exploration_notes` | Notes/TODO captured. | ☐ |
| 6 Explain transformation logic | rationale section | `transformation_rationale` | Rationale artifact captured. | ☐ |
| 7 Build transformation pipeline | transform + write section | `output_table` | Output write succeeds (or DRY_RUN simulated). | ☐ |
| 8 AI generate DQ rules | AI DQ notebook section | `dq_candidate_rules` | Candidates generated or dry-run stub stored. | ☐ |
| 9 Human review DQ rules | review section + rule freeze | `approved_dq_rules` | Approved rules record saved. | ☐ |
| 10 AI suggest sensitivity labels | sensitivity suggestion section | `sensitivity_suggestions` | Suggestions generated or dry-run stub stored. | ☐ |
| 11 Human review and governance gate | governance review section | `approved_governance_labels` | Governance approval artifact recorded. | ☐ |
| 12 AI generated lineage and transformation summary | lineage summary section | `lineage_record` | Lineage + transformation summary generated. | ☐ |
| 13 Handover framework pack | handover assembly/export section | `handover_pack` | Pack contains DQ, governance, lineage, profile, run summary, caveats. | ☐ |

## Must-prove outcomes
- Safe synthetic source table can be read.
- Source profile is generated and stored.
- DQ candidates can be generated or stubbed in dry run.
- DQ rules can be reviewed and frozen.
- DQ gates can run.
- Sensitivity labels can be suggested or stubbed in dry run.
- Governance review artifact can be recorded.
- Transformation pipeline can write output.
- Output profile can be generated.
- Lineage and transformation summary can be generated.
- Handover pack can be exported or assembled.
