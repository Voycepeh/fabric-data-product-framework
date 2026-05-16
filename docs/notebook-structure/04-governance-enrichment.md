# `04_gov_<agreement>_<dataset>_<table>`

This notebook performs governance enrichment after profile/pipeline evidence exists.

It is scoped per agreement + dataset + table.

> Run this notebook only after evidence from `02_ex` and/or `03_pc` is available.

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
