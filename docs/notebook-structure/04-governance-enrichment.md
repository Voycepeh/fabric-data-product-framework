# `04_gov_<agreement>_<dataset>_<table>`

Governance enrichment notebook flow that runs after profiling evidence exists from `02_ex` or `03_pc`.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/04_gov_agreement_dataset_table.ipynb">Open template notebook</a>

## Segment flow

1. Load `00_env_config`.
2. Use public FabricOps APIs only.
3. Declare agreement and table-scoped runtime variables.
4. Validate `agreement_id` against `METADATA_DATA_AGREEMENT`.
5. Register this notebook in `METADATA_NOTEBOOK_REGISTRY`.
6. Read profile evidence from `METADATA_PROFILE_ROWS` via `read_lakehouse_table` against `CONFIG` metadata target.
7. Filter rows by `environment_name`, `agreement_id` (if present), `dataset_name`, and `table_name`.
8. Draft business context suggestions and launch `review_business_context`.
9. Save approved business context in a separate cell into `METADATA_COLUMN_CONTEXT`.
10. Draft governance suggestions from approved business context + profile rows and launch `review_governance`.
11. Save approved governance in a separate cell into `METADATA_COLUMN_GOVERNANCE`.
12. Optionally read `METADATA_DQ_RULES` for read-only visibility.

## Guardrails

- Keep widget launch and metadata save in separate cells.
- Do not use private imports.
- Do not use `notebookutils.widgets`.
- Do not use direct metadata access patterns such as `spark.table("METADATA_...")` or metadata `spark.sql`.
- Do not introduce new metadata tables in this notebook.
