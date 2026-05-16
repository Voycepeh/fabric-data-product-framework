# `01_da_<agreement>`

`01_da_agreement_template.ipynb` defines the **source/agreement-level permission boundary** for one agreement.

- Keep `agreement_id` stable for the same agreement.
- Keep `save_to_metadata=False` while testing.
- Set `save_to_metadata=True` only when ready to write metadata.
- Set `register_notebook_to_metadata=True` to register the notebook run to metadata.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/01_da_agreement_template.ipynb">Open template notebook</a>

## 01 Runtime bootstrap and imports

- `%run 00_env_config` stays in its own cell.
- Import only public APIs from `fabricops_kit`.
- The notebook remains lightweight and avoids private/internal helpers.

## 02 Agreement parameters (source/agreement-level only)

The notebook captures source/agreement-level approval evidence fields:

- `agreement_id`
- `agreement_requested_source`
- `agreement_source_data_classification`
- `agreement_source_contains_pii_flag`
- `agreement_source_tables`
- `agreement_source_stewarding_data_manager_name`
- `agreement_purpose`
- `agreement_permitted_uses`
- `agreement_approval_duration`
- `agreement_approval_date`
- `agreement_requester_name`
- `agreement_requesting_department`
- `agreement_stewarding_approver_name`
- `agreement_stewarding_department`
- `agreement_renewal_procedure`
- `agreement_status`
- `agreement_notes`
- `environment_name`
- `created_at`

## 03 Build agreement record

The notebook builds one agreement metadata record only and appends it to `METADATA_DATA_AGREEMENT` through config-routed metadata IO.

## 04 Save agreement metadata

When metadata writes are enabled, the notebook appends to `METADATA_DATA_AGREEMENT` using `write_lakehouse_table`.

No extra agreement mapping tables are introduced in this step.

## 05 Register notebook

The notebook optionally registers itself via `register_current_notebook` into `METADATA_NOTEBOOK_REGISTRY`.

Registration links notebook evidence to `agreement_id` and environment.

## 06 What happens next

- `01` captures source/agreement-level permission boundary evidence only.
- `02` and `03` produce and enforce evidence under `agreement_id`.
- `04` (future) performs table/column governance enrichment under `agreement_id + dataset_name + table_name`.
