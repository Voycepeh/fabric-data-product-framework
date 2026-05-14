# `03_pc_<agreement>_<pipeline>`

Pipeline notebook flow for deterministic enforcement and controlled publishing.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb">Open template notebook</a>

`03_pc` is currently **parameter-driven**. The pipeline "contract" is represented by notebook parameters plus approved metadata tables (especially approved DQ metadata). This notebook does not run AI suggestion or human approval widgets.

## Segment 1: Load shared config and runtime context

- Load `00_env_config`.
- Import notebook-safe FabricOps functions from `fabricops_kit`.
- Define pipeline parameters:
  - `ENV_NAME`, `SOURCE_KIND`, `TARGET_KIND`
  - `SOURCE_LAYER`, `TARGET_LAYER`
  - `SOURCE_TABLE`, `TARGET_TABLE`, `DQ_TABLE_NAME`
  - `DATASET_NAME`, `PIPELINE_NAME`, `WRITE_MODE`
  - `REQUIRED_SOURCE_COLUMNS`, `BUSINESS_KEYS`, `RUN_ID`
- Load Fabric config with `load_fabric_config`.
- Resolve source/target/metadata paths with `get_path`.

## Segment 2: Load source data and run schema fail-fast

- Read source using `lakehouse_table_read` or `warehouse_read`.
- Validate required source columns with simple notebook code.

## Segment 3: Load approved active DQ rules from metadata

- Load approved DQ metadata using the metadata table pattern (`METADATA_DQ_RULES`).
- Keep enforcement deterministic and metadata-driven.

## Segment 4: Apply deterministic transformation (editable)

- Apply deterministic transformation logic in one clearly marked editable cell.
- No AI-generated rules, labels, or governance suggestions are proposed here.

## Segment 5: Standardize technical/audit columns, run DQ, publish evidence, then assert

- Apply canonical technical/audit enrichment with `standardize_output_columns`.
- Enforce approved DQ rules with `enforce_dq_rules`.
- Split output from DQ result:
  - `dq.valid_rows`
  - `dq.quarantine_rows`
  - `dq.failure_rows`
  - `dq.rule_results`
- Materialize evidence before pass/fail assertion:
  - write valid rows
  - write quarantine rows
  - write DQ failure evidence
  - write DQ rule results
- Call `assert_dq_passed` **only after** evidence writes complete.

## Optional evidence sections

- Optional drift/profile/lineage/run summary sections can appear at the end and should use existing FabricOps functions only.
- End with a compact final run summary.

## Scope guardrails for `03_pc`

- Enforce approved metadata and approved DQ rules only.
- Do not invent new contract-loading helpers.
- Do not add `load_pipeline_contract`, `validate_output_contract`, or equivalent new abstractions.
- AI suggestion and approval flows belong in `02_ex` or `01` agreement notebooks, not `03_pc`.
