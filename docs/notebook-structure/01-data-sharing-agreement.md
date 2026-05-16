# `01_da_<agreement>`

`01_da_<agreement>` is the agreement-level approval notebook.

Its operational template remains:

- `templates/notebooks/01_data_agreement_template.ipynb`

When copying into a project workspace, keep the notebook naming convention as `01_da_<agreement>`.

It writes agreement evidence only and does **not** perform column-level governance enrichment.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/01_data_agreement_template.ipynb">Open template notebook</a>

## What this notebook does

1. **Runtime bootstrap**
   - Runs `%run 00_env_config` so all runtime settings and metadata routing come from shared `CONFIG`.
2. **Agreement metadata definition**
   - Defines agreement identity, approved usage context, stewardship/ownership details, and related agreement-level evidence.
3. **Controlled write behavior**
   - Uses `save_to_metadata=False` for dry runs/testing.
   - Uses `save_to_metadata=True` only when approval evidence is ready to persist.
4. **Agreement persistence**
   - Writes approved agreement rows to `METADATA_DATA_AGREEMENT`.
5. **Notebook registration**
   - Registers itself in `METADATA_NOTEBOOK_REGISTRY` under the `agreement_id` for traceability.
6. **Downstream reuse**
   - `02_ex` and `03_pc` select and reuse this approved `agreement_id` and associated agreement metadata.

## Required controls

- Keep `agreement_id` stable for the same real-world agreement.
- Route metadata reads/writes via configured metadata routing:
  - `read_lakehouse_table(..., config=CONFIG, env=env_name, target="metadata", ...)`
  - `write_lakehouse_table(..., config=CONFIG, env=env_name, target="metadata", ...)`
- Do not rely on `spark.table("METADATA_*")` or default lakehouse assumptions.

## Out of scope

These belong to `04_gov_<agreement>_<dataset>_<table>`:

- Per-column business context approval.
- Per-column classification / PII / confidentiality enrichment.
- Writes to `METADATA_COLUMN_CONTEXT` and `METADATA_COLUMN_GOVERNANCE`.

## Cross-notebook requirements

- Downstream notebooks (`02_ex`, `03_pc`, `04_gov`) must declare `agreement_id`.
- Downstream notebooks must validate `agreement_id` exists in `METADATA_DATA_AGREEMENT` before doing work.
- All notebooks must register in `METADATA_NOTEBOOK_REGISTRY` under `agreement_id` to avoid stray runs.
