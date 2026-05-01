# MVP Workflow (Canonical)

| Step | Actor | What the user does | What the framework does | What AI can help with | Fabric test evidence | Output artifact |
|---|---|---|---|---|---|---|
| 1. Define data product | Human led | Define purpose, grain, usage, caveats | Capture context structure | Draft context wording | Context artifact saved | `data_product_context` |
| 2. Setup config and environment | Framework led | Provide runtime inputs | Build runtime context and checks | N/A | Runtime config printed/validated | `runtime_config` |
| 3. Declare source and ingest data | Framework led | Select synthetic source | Read source via adapters | N/A | Source read succeeds | `source_declaration` |
| 4. Profile source and capture metadata | Framework led | Trigger profiling | Build and persist profile | Summarize profile findings | Metadata profile rows stored | `source_profile` |
| 5. Explore data | Human led | Review profile and anomalies | Store notes placeholder | Suggest exploration questions | Notes cell/log exists | `exploration_notes` |
| 6. Explain transformation logic | Human led | Document business rationale | Persist rationale note | Draft concise rationale | Rationale artifact exists | `transformation_rationale` |
| 7. Build transformation pipeline | Framework led | Execute transform | Apply helpers and write output | Suggest code improvements | Output write or DRY_RUN equivalent | `output_table` |
| 8. AI generate DQ rules from metadata, profile, and context | AI assisted | Request candidates | Validate/normalize candidates | Generate candidate rules | Candidate list generated or stubbed | `dq_candidate_rules` |
| 9. Human review DQ rules | Human led | Approve/edit/reject rules | Freeze approved rules and run gates | Explain rule intent | Approved rules + gate run record | `approved_dq_rules` |
| 10. AI suggest sensitivity labels | AI assisted | Request suggestions | Record suggestion artifact | Suggest label/action per column | Suggestion artifact generated/stubbed | `sensitivity_suggestions` |
| 11. Human review and governance gate | Human led | Approve labels and gate | Record governance decision | Explain tradeoffs | Governance review record exists | `approved_governance_labels` |
| 12. AI generated lineage and transformation summary | AI assisted | Review draft summary | Build lineage records | Draft summary/lineage text | Lineage record/summary generated | `lineage_record` |
| 13. Handover framework pack | Framework led | Review final pack | Assemble pack and caveats | Draft handover narrative | Handover export/assembly confirmed | `handover_pack` |

Source of truth in code: `src/fabric_data_product_framework/mvp_steps.py`.
