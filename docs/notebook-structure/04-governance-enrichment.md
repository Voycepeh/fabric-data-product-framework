# `04_gov_<agreement>_<dataset>_<table>`

`04_gov_<agreement>_<dataset>_<table>` is the governance-workspace stage for table/column governance enrichment.
It is **not** part of execution workspaces.

This stage is documented as a planned operating stage when a dedicated project template is not yet available.

## Governance scope

- Review and approve per-column business context.
- Review and approve per-column classification / PII / confidentiality outcomes.
- Write approved business context rows to `METADATA_COLUMN_CONTEXT`.
- Write approved governance rows to `METADATA_COLUMN_GOVERNANCE`.

## Stage positioning

- Runs after evidence from `02_ex` and/or `03_pc` is available.
- Validates `agreement_id` against `METADATA_DATA_AGREEMENT`.
- Registers the notebook in `METADATA_NOTEBOOK_REGISTRY`.
- Reads metadata through configured routing (`read_lakehouse_table` / `write_lakehouse_table` with metadata target), not default-lakehouse access.

## Guardrails

- Keep human review checkpoints before metadata writes.
- Keep widget/review steps separate from persistence steps.
- Do not use direct metadata access patterns such as `spark.table("METADATA_...")` or metadata `spark.sql`.
- Do not treat this notebook as an execution-workspace stage.
