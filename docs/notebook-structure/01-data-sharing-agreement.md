# `01_data_sharing_agreement_<agreement>`

`01_data_agreement_template.ipynb` defines the **agreement-level usage boundary** for one agreement.

It captures who approved usage, what usage is approved, why it is approved, and until when it remains valid.

- Keep `agreement_id` stable for the same agreement.
- Keep `save_to_metadata=False` while testing.
- Set `save_to_metadata=True` only when ready to write metadata.
- Set `register_notebook_to_metadata=True` to register the notebook run to metadata.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/01_data_agreement_template.ipynb">Open template notebook</a>

## 01 Runtime bootstrap and imports

- `%run 00_env_config` stays in its own cell.
- Import only public APIs from `fabricops_kit`.
- The notebook remains lightweight and avoids private/internal helpers.

## 02 Agreement parameters (agreement-level only)

The agreement input section is intentionally small:

- `agreement_id`
- `agreement_name`
- `agreement_context`
- `approved_usage`
- `owner`
- `expiry_date`
- `notes`

Optional context values such as `dataset_name` and `table_name` may be used for local testing, but they are not required agreement inputs.

## 03 Build agreement record

The notebook builds one agreement metadata record with agreement-level fields (plus `created_at`).

Do **not** require table/column governance fields here.

## 04 Save agreement metadata

When metadata writes are enabled, the notebook appends to `METADATA_DATA_AGREEMENT` using `write_lakehouse_table`.

No extra agreement mapping tables are introduced in this step.

## 05 Register notebook

The notebook optionally registers itself via `register_current_notebook` into `METADATA_NOTEBOOK_REGISTRY`.

Registration links notebook evidence to `agreement_id` and environment without requiring dataset/table fields.

## 06 What happens next

- `01` sets agreement-level boundaries.
- `02` exploration profiles real table/column evidence.
- Table/column classification, sensitivity, and PII review happen later in governance-focused steps.
- `03` pipeline contract enforces approved outputs and rules using agreement context.
