# Notebook Structure

Use a notebook split that is easy to teach, review, and hand over.

| Notebook | Purpose | Main actor |
| --- | --- | --- |
| 00_governance_setup | Purpose, steward, usage, business metadata, labels, contract draft | Functional + Technical People |
| 01_source_profiling | Source declaration, source profile, metadata logging | Framework + Technical People |
| 02_eda_notes | Data quirks, caveats, assumptions, transformation rationale | Technical People, AI assisted |
| 03_pipeline_transform | Parameters, transformation logic, technical columns, write pattern, output profiling | Technical People + Framework |
| 04_checks_and_gates | Drift checks, incremental safety, DQ rules, contract validation | Framework + Technical People |
| 05_handover_export | Lineage, run summary, AI context export, final business metadata summary | Framework + AI, reviewed by Technical and Functional People |

## Usage guidance

- EDA notes should be a separate notebook.
- Profiling, output profiling, metadata logging, and lineage capture are code-run framework steps.
- AI can be used inside Fabric / Copilot / ChatGPT-style workflows to generate summaries, DQ rule candidates, label suggestions, and lineage diagrams.
- Human approval is still required.
