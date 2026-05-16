# `04_gov_<agreement>_<dataset>_<table>`

This is a documented **planned operating stage** for governance enrichment after profile/pipeline evidence exists.

It is scoped per agreement + dataset + table.

> Template status: a dedicated `templates/notebooks/04_gov_agreement_dataset_table.ipynb` notebook is **not yet included** in this repo. Use this page as operating guidance until that template is added.

## Purpose

`04_gov` reviews column-level evidence and records approved governance outcomes.

It reads profiling and related evidence, then performs:

- Per-column business context review.
- Per-column classification / PII / confidentiality review.

It writes:

- `METADATA_COLUMN_CONTEXT`
- `METADATA_COLUMN_GOVERNANCE`

## Required prerequisites

- `agreement_id` is declared.
- `agreement_id` exists in `METADATA_DATA_AGREEMENT`.
- Notebook run is registered in `METADATA_NOTEBOOK_REGISTRY` under `agreement_id`.

## Required metadata routing

Do not use `spark.table("METADATA_*")` or implicit default lakehouse routing.

Use:

- `read_lakehouse_table(..., config=CONFIG, env=env_name, target="metadata", ...)`
- `write_lakehouse_table(..., config=CONFIG, env=env_name, target="metadata", ...)`
