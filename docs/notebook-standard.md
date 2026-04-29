# Notebook Standard

This standard defines a consistent notebook lifecycle for framework-aligned data products.

## 1) Dataset purpose and steward agreement
- **Purpose:** Define business intent, boundaries, and accountable ownership.
- **Practitioner writes:** Dataset objective, intended consumers, owner/steward placeholders, usage constraints.
- **Framework automates:** Template structure and required field checks.
- **Example notes/pseudocode:**
  - `dataset_purpose = "Synthetic customer retention mart"`
  - `steward = "data.steward@example.org"`

## 2) Parameters and environment setup
- **Purpose:** Configure run-time values and environment metadata.
- **Practitioner writes:** Run date, source/target aliases, mode (full/incremental), parameter overrides.
- **Framework automates:** Parameter parsing defaults and run identifier generation.
- **Example notes/pseudocode:**
  - `run_mode = params.get("run_mode", "incremental")`

## 3) Source declaration
- **Purpose:** Declare what is being read and why.
- **Practitioner writes:** Source table names, expected schema intent, extraction scope.
- **Framework automates:** Source declaration logging and metadata capture.
- **Example notes/pseudocode:**
  - `source_table = "lakehouse_ops.sales_orders_synthetic"`

## 4) Source profiling
- **Purpose:** Capture baseline shape and quality indicators before transformation.
- **Practitioner writes:** Optional domain interpretations of profile metrics.
- **Framework automates:** Row counts, null rates, uniqueness checks, distribution summaries.
- **Example notes/pseudocode:**
  - `profile_source(df_source)`

## 5) Drift and incremental safety checks
- **Purpose:** Detect schema/data changes and validate incremental boundaries.
- **Practitioner writes:** Policy thresholds and escalation notes.
- **Framework automates:** Schema drift compare, data drift metrics, partition/watermark safety checks.
- **Example notes/pseudocode:**
  - `assert_incremental_window(df_source, watermark_col, prior_max)`

## 6) EDA and data nuance notes
- **Purpose:** Preserve analyst insight and caveats.
- **Practitioner writes:** Observed anomalies, domain explanations, assumptions.
- **Framework automates:** Structured note capture for run metadata.
- **Example notes/pseudocode:**
  - `eda_notes.append("Synthetic campaign spike around month-end batches")`

## 7) Transformation logic
- **Purpose:** Apply business logic to produce model-ready outputs.
- **Practitioner writes:** Core transformation code and rationale.
- **Framework automates:** Transformation step logging wrappers.
- **Example notes/pseudocode:**
  - `df_out = build_customer_metrics(df_source)`

## 8) Technical columns
- **Purpose:** Add traceability and operational metadata columns.
- **Practitioner writes:** Any dataset-specific technical additions.
- **Framework automates:** Standard columns such as run ID, load timestamp, and hash keys.
- **Example notes/pseudocode:**
  - `df_out = add_technical_columns(df_out, run_id=run_id)`

## 9) Output write
- **Purpose:** Persist curated output with safe write strategy.
- **Practitioner writes:** Target mode and partition intent.
- **Framework automates:** Standard write wrappers and write-result logging.
- **Example notes/pseudocode:**
  - `write_output(df_out, target_table, mode=run_mode)`

## 10) Output profiling
- **Purpose:** Validate resulting dataset shape after write.
- **Practitioner writes:** Interpretation of major profile changes.
- **Framework automates:** Post-write profile metrics and comparison against source/previous run.
- **Example notes/pseudocode:**
  - `profile_output(df_out)`

## 11) Data quality rules
- **Purpose:** Ensure contractual data expectations are met.
- **Practitioner writes:** Rule definitions and severity classes.
- **Framework automates:** Rule execution scaffold and standardized result logging.
- **Example notes/pseudocode:**
  - `rules = [{"rule": "order_id_not_null", "severity": "error"}]`

## 12) Governance labels
- **Purpose:** Tag datasets/columns for policy and stewardship.
- **Practitioner writes:** Required classifications and rationale.
- **Framework automates:** Governance label output records.
- **Example notes/pseudocode:**
  - `labels = ["internal", "contains_synthetic_pii"]`

## 13) Upstream and downstream data contracts
- **Purpose:** Clarify dependencies and delivery guarantees.
- **Practitioner writes:** Upstream assumptions and downstream service expectations.
- **Framework automates:** Contract validation result capture.
- **Example notes/pseudocode:**
  - `validate_contracts(contract_config, df_out)`

## 14) Lineage and transformation summary
- **Purpose:** Document data movement and major transformation steps.
- **Practitioner writes:** Human-readable summary of joins, filters, enrichments.
- **Framework automates:** Lineage graph records and step metadata.
- **Example notes/pseudocode:**
  - `log_lineage(upstream=[...], downstream=[...], steps=[...])`

## 15) Run summary
- **Purpose:** Produce operational run narrative for maintainers.
- **Practitioner writes:** Exceptions, manual overrides, and approval notes.
- **Framework automates:** Summary assembly from collected metadata.
- **Example notes/pseudocode:**
  - `generate_run_summary(run_id)`

## 16) AI context export
- **Purpose:** Export structured context for AI-assisted documentation and review.
- **Practitioner writes:** Guardrails and review decisions.
- **Framework automates:** Prompt/context payload generation from run metadata.
- **Example notes/pseudocode:**
  - `export_ai_context(run_id, include_sections=["eda", "quality", "lineage"])`

> AI-generated suggestions must always be reviewed and approved by humans before adoption.


## Engine-aware guidance

- Use pandas for small/local synthetic data, CSV/Excel prototyping, and unit tests.
- Use Spark for Fabric lakehouse-scale production workloads.
- Public dataframe APIs should accept `engine="auto" | "pandas" | "spark"`.
- Do not auto-convert Spark DataFrames to pandas.
