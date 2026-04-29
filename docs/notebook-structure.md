# Notebook Structure

Use a notebook split that is easy to teach, review, and hand over.

| Notebook | Purpose | Lane |
| --- | --- | --- |
| 00_governance_setup | Purpose, steward, usage, business metadata, labels, contract draft | Outside Fabric + Inside Fabric: Human-guided |
| 01_source_profiling | Source declaration, source profile, metadata logging | Inside Fabric: Framework-run + Human-guided |
| 02_eda_notes | Data quirks, caveats, assumptions, transformation rationale | Inside Fabric: Human-guided (AI-assisted optional) |
| 03_pipeline_transform | Parameters, transformation logic, technical columns, write pattern, output profiling | Inside Fabric: Human-guided + Framework-run |
| 04_checks_and_gates | Drift checks, incremental safety, DQ rules, contract validation | Inside Fabric: Framework-run + Human-guided |
| 05_handover_export | Lineage, run summary, AI context export, final business metadata summary | Inside Fabric: Framework-run + Human-guided |

## Usage guidance

- EDA notes should be a separate notebook.
- Profiling, output profiling, metadata logging, and lineage capture are framework-run steps.
- AI can assist with summaries, DQ rule candidates, label suggestions, and lineage drafts.
- AI output must be reviewed before acceptance.
