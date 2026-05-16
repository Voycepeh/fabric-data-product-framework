# `01_da_<agreement>`

This is the agreement notebook. Its purpose is agreement-level approval evidence only.

It captures source/agreement-level approvals, writes `METADATA_DATA_AGREEMENT`, and registers itself in `METADATA_NOTEBOOK_REGISTRY` under the agreement.

It does **not** perform table/column governance review.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/01_data_agreement_template.ipynb">Open template notebook</a>

## Responsibilities

- Define agreement identity and approved usage context.
- Keep `agreement_id` stable for the same agreement.
- Write agreement-level evidence to `METADATA_DATA_AGREEMENT`.
- Register notebook traceability in `METADATA_NOTEBOOK_REGISTRY`.
- Route metadata I/O through configured metadata targets.

## Out of scope

- Column business context review.
- Classification / sensitivity / PII approval.
- Per-dataset, per-table governance enrichment.

Those activities belong in `04_gov_<agreement>_<dataset>_<table>`.

## Required metadata routing

Do not read/write metadata via `spark.table("METADATA_*")` or default lakehouse assumptions.

Use configured routing with FabricOps helpers:

- `read_lakehouse_table(..., config=CONFIG, env=env_name, target="metadata", ...)`
- `write_lakehouse_table(..., config=CONFIG, env=env_name, target="metadata", ...)`

## Agreement and registration requirements

- Downstream notebooks (`02_ex`, `03_pc`, `04_gov`) must declare `agreement_id`.
- Downstream notebooks must validate that `agreement_id` exists in `METADATA_DATA_AGREEMENT` before work starts.
- All notebooks must register in `METADATA_NOTEBOOK_REGISTRY` under `agreement_id` to prevent stray notebook runs.
