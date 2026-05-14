# `03_pc_<agreement>_<pipeline>`

Pipeline notebook flow for deterministic enforcement and controlled publishing.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb">Open template notebook</a>

`03_pc` is parameter-driven. The contract is represented by notebook parameters and approved metadata tables. No AI suggestion flows, approval widgets, or governance classification generation belong in this notebook.

## 1. Runtime setup and pipeline parameters
- Load `00_env_config` and import notebook-safe `fabricops_kit` functions.
- Define pipeline parameters including `RUN_ID`, `BUSINESS_KEYS`, `DRIFT_MODE`, and `DQ_PUBLISH_MODE`.
- Supported `DQ_PUBLISH_MODE` values:
  - `same_table_with_flags`
  - `split_valid_quarantine` (default)
  - `fail_on_invalid`
- Load config via `load_fabric_config` and resolve source/target/metadata paths with `get_path`.

## 2. Load agreement context and source data
- Load and select agreement context with `load_agreements`, `select_agreement`, `get_selected_agreement`.
- Register run context via `register_current_notebook`.
- Read source from lakehouse or warehouse.

## 3. Source evidence and guardrails
- Validate required source columns using fail-fast notebook code.
- Build source profile evidence with `profile_dataframe`.
- Run drift checks every execution with `check_schema_drift`, `check_partition_drift`, `check_profile_drift`.
- Summarize drift with `summarize_drift_results` and apply `DRIFT_MODE` behavior.

## 4. Deterministic transformation and technical columns
- Apply deterministic transformation logic in the editable block.
- Apply canonical technical/audit enrichment using `standardize_output_columns`.

## 5. DQ enforcement and evidence materialization
- Load approved DQ metadata from `METADATA_DQ_RULES`.
- Enforce rules with `enforce_dq_rules`.
- Split DQ outputs (`dq.valid_rows`, `dq.quarantine_rows`, `dq.failure_rows`, `dq.rule_results`).
- Always write DQ failure evidence and DQ rule results to `metadata_path` before any failure is raised.
- Run `assert_dq_passed` after DQ evidence materialization.

## 6. Publish strategy
- Publish behavior is controlled by `DQ_PUBLISH_MODE`:
  - `same_table_with_flags`: write the DQ-annotated/full result to target and keep all rows; recommended mainly when DQ rules are warnings/advisory.
  - `split_valid_quarantine`: write valid rows to target and quarantine rows to `${TARGET_TABLE}_QUARANTINE`.
  - `fail_on_invalid`: if invalid rows exist, raise before any target publish; do not publish partial target output.

## 7. Post-write profile, lineage, and run summary
- Reload the actual published target table.
- Profile the published table with `profile_dataframe`, append run metadata columns via Spark DataFrame operations, and write published profile evidence to `metadata_path`.
- Build lineage records and lineage handover markdown.
- Build run summary, render final run summary markdown, and display final execution summary.
