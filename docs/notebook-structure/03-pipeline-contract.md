# `03_pc_<agreement>_<pipeline>`

Pipeline notebook flow for deterministic enforcement and controlled publishing.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb">Open template notebook</a>

`03_pc` is parameter-driven. The contract is represented by notebook parameters and approved metadata tables. This notebook enforces approved DQ rules and canonical technical/audit columns; it does not include AI suggestion flows, approval widgets, or governance classification generation.

## 1. Runtime setup and pipeline parameters

- Load `00_env_config` and import notebook-safe functions from `fabricops_kit`.
- Define canonical runtime parameters (`ENV_NAME`, source/target settings, `PIPELINE_NAME`, `RUN_ID`, `REQUIRED_SOURCE_COLUMNS`, `BUSINESS_KEYS`, `DRIFT_MODE`).
- Load Fabric config with `load_fabric_config`.
- Resolve `source_path`, `target_path`, and `metadata_path` with `get_path`.

## 2. Load agreement context and source data

- Select agreement context with `load_agreements`, `select_agreement`, `get_selected_agreement`.
- Register notebook run context with `register_current_notebook`.
- Read source data via `lakehouse_table_read` or `warehouse_read`.

## 3. Source evidence and guardrails

- Validate required source columns (fail-fast notebook code).
- Build source profile evidence via `profile_dataframe`.
- Run drift checks every run: `check_schema_drift`, `check_partition_drift`, `check_profile_drift`.
- Summarize drift via `summarize_drift_results`.
- Apply configurable drift action through `DRIFT_MODE` (`warn` or `fail`).

## 4. Deterministic transformation and technical columns

- Apply deterministic transformation logic in the editable transformation block.
- Apply canonical technical/audit enrichment with `standardize_output_columns`.

## 5. DQ enforcement and evidence materialization

- Load approved DQ metadata from `METADATA_DQ_RULES`.
- Enforce approved DQ rules with `enforce_dq_rules`.
- Split DQ output into `dq.valid_rows`, `dq.quarantine_rows`, `dq.failure_rows`, and `dq.rule_results`.
- Write DQ failure evidence and DQ rule results to `metadata_path`.
- Call `assert_dq_passed` only after DQ evidence is materialized.

## 6. Publish outputs

- Publish valid rows to target table.
- Publish quarantine rows to `${TARGET_TABLE}_QUARANTINE`.
- Use `lakehouse_table_write` or `warehouse_write` depending on target kind.

## 7. Lineage and run summary

- Build lineage evidence with `build_lineage_records` and `build_lineage_handover_markdown`.
- Build and render run summary with `build_run_summary` and `render_run_summary_markdown`.
- End with a compact handover summary.
