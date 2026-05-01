# MVP workflow (canonical)

This page is the detailed source of truth for the MVP workflow image.

| Step | Actor | What the user does | What the framework does | What AI can help with | Fabric test evidence | Output artifact |
|---|---|---|---|---|---|---|
| 1. Define data product | Human led | Defines purpose, usage, grain, and scope. | Captures context structure. | Suggests wording only. | Context section completed in notebook. | `data_product_context` |
| 2. Setup config and environment | Framework led | Provides environment and paths. | Builds runtime config and guards. | N/A | Runtime config cell executes. | `runtime_config` |
| 3. Declare source and ingest data | Framework led | Declares source table and expectations. | Reads declared source table. | N/A | Synthetic source table read succeeds. | `source_declaration` |
| 4. Profile source and capture metadata | Framework led | Runs source profile step. | Generates profile and metadata logs. | Summarizes profile highlights. | Source profile stored/printed. | `source_profile` |
| 5. Explore data | Human led | Reviews shape and anomalies. | Provides placeholder section. | Suggests exploratory checks. | Exploration notes recorded. | `exploration_notes` |
| 6. Explain transformation logic | Human led | Documents transformation reasons. | Stores rationale artifact. | Drafts rationale text. | Rationale artifact captured. | `transformation_rationale` |
| 7. Build transformation pipeline | Framework led | Executes transform logic. | Applies helpers and writes output. | Suggests code snippets. | Output table written or dry-run simulated. | `output_table` |
| 8. AI generate DQ rules from metadata, profile, and context | AI assisted | Runs AI DQ draft prompt. | Parses candidate rules. | Generates candidate rules. | DQ candidates generated or stubbed. | `dq_candidate_rules` |
| 9. Human review DQ rules | Human led | Approves/edits/rejects rules. | Freezes approved rules record. | Reformats rule explanations. | Approved rules artifact saved. | `approved_dq_rules` |
| 10. AI suggest sensitivity labels | AI assisted | Runs sensitivity suggestion prompt. | Records suggestions. | Suggests candidate labels. | Sensitivity suggestions generated or stubbed. | `sensitivity_suggestions` |
| 11. Human review and governance gate | Human led | Approves labels and governance gate decision. | Records governance approval. | Summarizes label rationale. | Governance review artifact recorded. | `approved_governance_labels` |
| 12. AI generated lineage and transformation summary | AI assisted | Runs lineage/summary draft prompt. | Collects transformation logs. | Drafts lineage + business summary. | Lineage and summary artifact generated. | `lineage_record` |
| 13. Handover framework pack | Framework led | Reviews final pack for release. | Assembles handover package. | Drafts caveat wording. | Handover pack exported or assembled. | `handover_pack` |
