# Function Reference

Use this page as an API lookup after you understand the notebook flow. Start with the three notebook templates, then use the callable map by workflow step for implementation details.

## Start from the templates

| Notebook | User goal | Main functions | Full template |
|---|---|---|---|
| `00_env_config` | Configure Fabric paths, runtime checks, AI config, naming rules, quality defaults, governance defaults, and lineage defaults. | `create_framework_config`, `load_fabric_config`, `get_path`, `run_config_smoke_tests`, `bootstrap_fabric_env` | [00_env_config.ipynb](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb) |
| `02_ex_&lt;agreement&gt;_&lt;topic&gt;` | Read and profile source data, build AI-ready context, suggest DQ and classification, and capture human-reviewed contract decisions. | `lakehouse_table_read`, `generate_metadata_profile`, `build_ai_quality_context`, `build_manual_dq_rule_prompt_package`, `classify_columns`, `build_contract_summary` | [02_ex_agreement_topic.ipynb](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb) |
| `03_pc_&lt;agreement&gt;_&lt;pipeline&gt;` | Load approved contract, read source, transform, enforce DQ, quarantine failures, write output, persist metadata, and produce lineage and handover evidence. | `load_latest_approved_contract`, `get_executable_quality_rules`, `run_dq_rules`, `split_valid_and_quarantine`, `assert_dq_passed`, `lakehouse_table_write`, `write_metadata_records` | [03_pc_agreement_source_to_target.ipynb](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb) |

## What runs where

- `00_env_config` equals shared setup.
- `02_ex` equals AI-assisted exploration and human review.
- `03_pc` equals deterministic pipeline enforcement.

AI functions are advisory. Approved contracts and pipeline notebooks are the enforcement point.

## Callable map by workflow step

## Step 1: Governance context

This step captures the governance context: approved usage, owner, and data agreement. The agreement may live outside Fabric, such as in SharePoint documents. Functions in this step mainly link notebooks back to that agreement so the technical work stays tied to the approved business context.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`assert_notebook_name_valid`](./step-01-governance-context/assert_notebook_name_valid/) | [`runtime_context`](../api/modules/runtime_context/) | Essential | Raise :class:`NotebookNamingError` when a notebook name is invalid. |
| [`build_runtime_context`](./step-01-governance-context/build_runtime_context/) | [`runtime_context`](../api/modules/runtime_context/) | Essential | Build a standard runtime context dictionary for Fabric notebooks. |
| [`configure_fabric_ai_functions`](./step-01-governance-context/configure_fabric_ai_functions/) | [`environment_config`](../api/modules/environment_config/) | Essential | Apply optional default Fabric AI Function configuration. |
| [`generate_run_id`](./step-01-governance-context/generate_run_id/) | [`runtime_context`](../api/modules/runtime_context/) | Essential | Generate a notebook-safe run identifier. |
| [`validate_notebook_name`](./step-01-governance-context/validate_notebook_name/) | [`runtime_context`](../api/modules/runtime_context/) | Essential | Validate notebook names against the framework workspace notebook model. |

## Step 2A: Create shared runtime config

This step creates the shared config that other notebooks depend on, including environment paths, workspace targets, AI availability, and standard naming rules. The goal is to define the project setup once so exploration and pipeline notebooks do not repeat hidden manual configuration.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`check_fabric_ai_functions_available`](./step-02a-shared-runtime-config/check_fabric_ai_functions_available/) | [`environment_config`](../api/modules/environment_config/) | Essential | Check whether Fabric AI Functions are available in the current runtime. |
| [`create_ai_prompt_config`](./step-02a-shared-runtime-config/create_ai_prompt_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Create the AI prompt-template configuration used by FabricOps. |
| [`create_framework_config`](./step-02a-shared-runtime-config/create_framework_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Create the top-level FabricOps framework configuration contract. |
| [`create_governance_config`](./step-02a-shared-runtime-config/create_governance_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Create governance policy defaults for FabricOps runtime checks. |
| [`create_lineage_config`](./step-02a-shared-runtime-config/create_lineage_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Create lineage capture defaults for FabricOps handover traceability. |
| [`create_notebook_runtime_config`](./step-02a-shared-runtime-config/create_notebook_runtime_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Create notebook naming-policy configuration for runtime guards. |
| [`create_path_config`](./step-02a-shared-runtime-config/create_path_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Create environment-to-target routing used by Fabric IO helpers. |
| [`create_quality_config`](./step-02a-shared-runtime-config/create_quality_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Create the default quality policy used during FabricOps checks. |
| [`get_path`](./step-02a-shared-runtime-config/get_path/) | [`environment_config`](../api/modules/environment_config/) | Essential | Resolve a configured Fabric path for an environment and target. |
| [`Housepath`](./step-02a-shared-runtime-config/Housepath/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Fabric lakehouse or warehouse connection details. |
| [`load_fabric_config`](./step-02a-shared-runtime-config/load_fabric_config/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Validate and return a user-supplied framework configuration. |
| [`validate_framework_config`](./step-02a-shared-runtime-config/validate_framework_config/) | [`environment_config`](../api/modules/environment_config/) | Essential | Validate and normalize framework configuration input. |

## Step 2B: Run notebook startup checks

This step runs the startup utility or smoke test at the beginning of every exploration and pipeline notebook. The goal is to confirm the notebook is running in the expected environment, follows naming rules, and has the required Fabric or AI capabilities before any data work begins.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`bootstrap_fabric_env`](./step-02b-notebook-startup-checks/bootstrap_fabric_env/) | [`environment_config`](../api/modules/environment_config/) | Essential | Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results. |
| [`run_config_smoke_tests`](./step-02b-notebook-startup-checks/run_config_smoke_tests/) | [`environment_config`](../api/modules/environment_config/) | Essential | Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports. |

## Step 3: Define source contract & ingestion pattern

This step defines the contract between the upstream source and this notebook. It captures what data is expected, including schema, data types, update frequency, update method, watermark column, and whether the source is append only, overwritten, or slowly changing. Functions in this step help the pipeline decide how to ingest, validate, snapshot, or incrementally process the source data.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`extract_business_keys`](./step-03-source-contract-ingestion-pattern/extract_business_keys/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Extract business-key column names from a normalized contract. |
| [`extract_classifications`](./step-03-source-contract-ingestion-pattern/extract_classifications/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Extract column classification mappings from a normalized contract. |
| [`extract_optional_columns`](./step-03-source-contract-ingestion-pattern/extract_optional_columns/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Extract optional column names from a normalized contract. |
| [`extract_quality_rules`](./step-03-source-contract-ingestion-pattern/extract_quality_rules/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Extract raw quality-rule definitions from a normalized contract. |
| [`extract_required_columns`](./step-03-source-contract-ingestion-pattern/extract_required_columns/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Extract required column names from a normalized contract. |
| [`lakehouse_csv_read`](./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Read a CSV file from a Fabric lakehouse Files path. |
| [`lakehouse_excel_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Read an Excel file from a Fabric lakehouse Files path. |
| [`lakehouse_parquet_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Read a Parquet file from a Fabric lakehouse Files path. |
| [`lakehouse_table_read`](./step-03-source-contract-ingestion-pattern/lakehouse_table_read/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Read a Delta table from a Fabric lakehouse. |
| [`load_contract_from_lakehouse`](./step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Load one contract by ID/version from Fabric metadata storage. |
| [`load_data_contract`](./step-03-source-contract-ingestion-pattern/load_data_contract/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Load and normalize a data product contract from file path or dictionary. |
| [`load_latest_approved_contract`](./step-03-source-contract-ingestion-pattern/load_latest_approved_contract/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Load the latest approved contract for a dataset/object pair. |
| [`normalize_contract_dict`](./step-03-source-contract-ingestion-pattern/normalize_contract_dict/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Normalize a notebook-authored contract dictionary to a stable shape. |
| [`validate_contract_dict`](./step-03-source-contract-ingestion-pattern/validate_contract_dict/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Validate a contract dictionary and return error strings without raising. |
| [`warehouse_read`](./step-03-source-contract-ingestion-pattern/warehouse_read/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Read a table from a Microsoft Fabric warehouse. |

## Step 4: Ingest, profile & store source data

This step brings the source data into the framework, profiles it, and stores it for later use. Functions in this step focus on reading the data, capturing basic profiling results, and saving the raw or source-aligned version before business transformation begins.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`build_ai_quality_context`](./step-04-ingest-profile-store/build_ai_quality_context/) | [`data_profiling`](../api/modules/data_profiling/) | Essential | Build deterministic AI-ready context from standard metadata profile rows. |
| [`build_schema_drift_records`](./step-04-ingest-profile-store/build_schema_drift_records/) | [`data_product_metadata`](../api/modules/data_product_metadata/) | Essential | Convert schema drift results into metadata records for audit trails. |
| [`build_schema_snapshot_records`](./step-04-ingest-profile-store/build_schema_snapshot_records/) | [`data_product_metadata`](../api/modules/data_product_metadata/) | Essential | Convert a schema snapshot into row-wise metadata records. |
| [`check_partition_drift`](./step-04-ingest-profile-store/check_partition_drift/) | [`data_drift`](../api/modules/data_drift/) | Essential | Check partition-level drift using keys, partitions, and optional watermark baselines. |
| [`check_profile_drift`](./step-04-ingest-profile-store/check_profile_drift/) | [`data_drift`](../api/modules/data_drift/) | Essential | Compare profile metrics against a baseline profile and drift thresholds. |
| [`check_schema_drift`](./step-04-ingest-profile-store/check_schema_drift/) | [`data_drift`](../api/modules/data_drift/) | Essential | Compare a current dataframe schema against a baseline schema snapshot. |
| [`generate_metadata_profile`](./step-04-ingest-profile-store/generate_metadata_profile/) | [`data_profiling`](../api/modules/data_profiling/) | Essential | Generate standard metadata profile rows for a Spark/Fabric DataFrame. |
| [`profile_dataframe`](./step-04-ingest-profile-store/profile_dataframe/) | [`data_profiling`](../api/modules/data_profiling/) | Essential | Build a lightweight profile for pandas or Spark-like DataFrames. |
| [`profile_dataframe_to_metadata`](./step-04-ingest-profile-store/profile_dataframe_to_metadata/) | [`data_profiling`](../api/modules/data_profiling/) | Essential | Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows. |
| [`profile_metadata_to_records`](./step-04-ingest-profile-store/profile_metadata_to_records/) | [`data_profiling`](../api/modules/data_profiling/) | Essential | Convert Spark metadata profile rows into JSON-friendly dictionaries. |
| [`summarize_drift_results`](./step-04-ingest-profile-store/summarize_drift_results/) | [`data_drift`](../api/modules/data_drift/) | Essential | Summarize schema, partition, and profile drift outcomes into one decision. |

## Step 5: Explore data & explain transformation logic

This step is where the analyst studies the profiled source data and explains why transformation is needed. There may not be many helper functions here today, but future functions could support standard EDA, AI assisted analysis, and documentation of business assumptions before the logic becomes part of the repeatable pipeline.

No public callable is currently mapped to this step. Use exploration notebook prompts to capture transformation rationale before pipeline enforcement.

## Step 6A: Write transformation logic

This step contains the main transformation logic that converts source-aligned data into the target output. Functions here support reusable pipeline code so the same logic can run consistently during development, testing, and scheduled refresh.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`run_data_product`](./step-06a-transformation-logic/run_data_product/) | [`data_quality`](../api/modules/data_quality/) | Essential | Run the starter kit workflow end-to-end for a data product outcome. |

## Step 6B: Apply runtime standards

This step applies standard runtime requirements such as technical columns, run IDs, timestamps, partition keys, and other repeatable conventions. Functions here make outputs easier to audit, troubleshoot, join back to pipeline runs, and operate at scale.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`add_audit_columns`](./step-06b-runtime-standards/add_audit_columns/) | [`technical_audit_columns`](../api/modules/technical_audit_columns/) | Essential | Add run tracking and audit columns for ingestion workflows. |
| [`add_datetime_features`](./step-06b-runtime-standards/add_datetime_features/) | [`technical_audit_columns`](../api/modules/technical_audit_columns/) | Essential | Add localized datetime feature columns derived from a UTC datetime column. |
| [`add_hash_columns`](./step-06b-runtime-standards/add_hash_columns/) | [`technical_audit_columns`](../api/modules/technical_audit_columns/) | Essential | Add business key and row-level SHA256 hash columns. |
| [`default_technical_columns`](./step-06b-runtime-standards/default_technical_columns/) | [`technical_audit_columns`](../api/modules/technical_audit_columns/) | Essential | Return framework-generated and legacy technical column names to ignore. |

## Step 6C: Enforce pipeline controls

This step enforces the controls that decide whether the pipeline output should be trusted. Functions here support data quality rules, schema checks, classification checks, and other contract validations before data is released downstream.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`get_executable_quality_rules`](./step-06c-pipeline-controls/get_executable_quality_rules/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Return normalized quality rules ready for pipeline enforcement. |
| [`run_dq_rules`](./step-06c-pipeline-controls/run_dq_rules/) | [`data_quality`](../api/modules/data_quality/) | Essential | Run notebook-facing DQ rules and return a Spark DataFrame result. |
| [`run_quality_rules`](./step-06c-pipeline-controls/run_quality_rules/) | [`data_quality`](../api/modules/data_quality/) | Essential | Execute quality rules against a dataframe and return structured results. |
| [`split_valid_and_quarantine`](./step-06c-pipeline-controls/split_valid_and_quarantine/) | [`data_quality`](../api/modules/data_quality/) | Optional | Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules. |
| [`validate_dq_rules`](./step-06c-pipeline-controls/validate_dq_rules/) | [`data_quality`](../api/modules/data_quality/) | Essential | Validate notebook-facing DQ rules. |

## Step 6D: Write controlled outputs

This step writes the transformed output to the correct lakehouse, warehouse, or product layer. Functions here make the write pattern explicit, repeatable, and aligned to the intended environment instead of relying on ad hoc exports.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`assert_dq_passed`](./step-06d-controlled-outputs/assert_dq_passed/) | [`data_quality`](../api/modules/data_quality/) | Essential | Raise when any error-severity DQ rule failed after results are logged. |
| [`lakehouse_table_write`](./step-06d-controlled-outputs/lakehouse_table_write/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Write a Spark DataFrame to a Fabric lakehouse Delta table. |
| [`warehouse_write`](./step-06d-controlled-outputs/warehouse_write/) | [`fabric_input_output`](../api/modules/fabric_input_output/) | Essential | Write a Spark DataFrame to a Microsoft Fabric warehouse table. |

## Step 7: Profile output & publish product contract

This step profiles the created output, stores its metadata, and creates the data contract for the next notebook, pipeline, or consumer. Functions here help record what was produced, write the evidence to metadata tables or catalogues, and make the output understandable and reusable downstream.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`build_contract_column_records`](./step-07-output-profile-product-contract/build_contract_column_records/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Build normalized contract-column metadata records for persistence. |
| [`build_contract_header_record`](./step-07-output-profile-product-contract/build_contract_header_record/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Build one header row for FABRICOPS_CONTRACTS. |
| [`build_contract_records`](./step-07-output-profile-product-contract/build_contract_records/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Build grouped contract header, column, and rule metadata payloads. |
| [`build_contract_rule_records`](./step-07-output-profile-product-contract/build_contract_rule_records/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Build quality-rule metadata records from a validated contract. |
| [`build_contract_summary`](./step-07-output-profile-product-contract/build_contract_summary/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Build a concise contract summary for reviews and handover. |
| [`build_dataset_run_record`](./step-07-output-profile-product-contract/build_dataset_run_record/) | [`data_product_metadata`](../api/modules/data_product_metadata/) | Essential | Build a dataset-run metadata record for operational tracking. |
| [`build_quality_result_records`](./step-07-output-profile-product-contract/build_quality_result_records/) | [`data_product_metadata`](../api/modules/data_product_metadata/) | Essential | Convert quality-rule execution output into metadata evidence records. |
| [`contract_records_to_spark`](./step-07-output-profile-product-contract/contract_records_to_spark/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Convert record dictionaries into a Spark DataFrame when Spark is available. |
| [`write_contract_to_lakehouse`](./step-07-output-profile-product-contract/write_contract_to_lakehouse/) | [`data_contracts`](../api/modules/data_contracts/) | Essential | Validate and persist contract records into Fabric metadata tables. |
| [`write_metadata_records`](./step-07-output-profile-product-contract/write_metadata_records/) | [`data_product_metadata`](../api/modules/data_product_metadata/) | Essential | Write metadata records to a configured metadata sink. |
| [`write_multiple_metadata_outputs`](./step-07-output-profile-product-contract/write_multiple_metadata_outputs/) | [`data_product_metadata`](../api/modules/data_product_metadata/) | Essential | Write multiple metadata payloads to their configured destinations. |

## Step 8: Suggest AI assisted data quality rules

This step uses AI in exploration notebooks to suggest possible data quality rules from profiling results, business context, and source knowledge. These AI functions are only advisory. The actual rule creation, approval, and enforcement must still be done by the human engineer in the pipeline notebook.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`build_dq_rule_candidate_prompt`](./step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt/) | [`data_quality`](../api/modules/data_quality/) | Optional | Build the DQ-candidate prompt used in AI-assisted quality drafting. |
| [`build_manual_dq_rule_prompt_package`](./step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package/) | [`data_quality`](../api/modules/data_quality/) | Optional | Build copy/paste prompt package for manual DQ candidate generation. |
| [`DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE`](./step-08-ai-assisted-dq-suggestions/DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE/) | [`data_quality`](../api/modules/data_quality/) | Optional | Default prompt template used to draft candidate DQ rules. |
| [`generate_dq_rule_candidates_with_fabric_ai`](./step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai/) | [`data_quality`](../api/modules/data_quality/) | Optional | Append AI-suggested DQ rule candidates to a profiling DataFrame. |
| [`get_default_dq_rule_templates`](./step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates/) | [`data_quality`](../api/modules/data_quality/) | Optional | Return editable example data quality rules. |
| [`suggest_accepted_value_mapping_prompt`](./step-08-ai-assisted-dq-suggestions/suggest_accepted_value_mapping_prompt/) | [`data_quality`](../api/modules/data_quality/) | Optional | Build a constrained prompt for accepted-value mapping suggestions. |
| [`suggest_closest_accepted_value`](./step-08-ai-assisted-dq-suggestions/suggest_closest_accepted_value/) | [`data_quality`](../api/modules/data_quality/) | Optional | Suggest a deterministic closest accepted value using ``difflib``. |
| [`suggest_dq_rules_prompt`](./step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt/) | [`data_quality`](../api/modules/data_quality/) | Optional | Build a prompt for candidate DQ rule suggestions. |

## Step 9: Suggest AI assisted column classification

This step uses AI in exploration notebooks to suggest column classifications such as PII, sensitivity level, and governance labels for the planned output. These AI functions are only advisory. The actual label assignment must be approved by governance or data stewards and enforced by the human engineer in the pipeline notebook.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`build_governance_candidate_prompt`](./step-09-ai-assisted-classification/build_governance_candidate_prompt/) | [`data_governance`](../api/modules/data_governance/) | Optional | Build the governance-candidate prompt for AI-assisted classification drafts. |
| [`build_governance_classification_records`](./step-09-ai-assisted-classification/build_governance_classification_records/) | [`data_governance`](../api/modules/data_governance/) | Optional | Build metadata-ready governance classification records from column suggestions. |
| [`build_manual_governance_prompt_package`](./step-09-ai-assisted-classification/build_manual_governance_prompt_package/) | [`data_governance`](../api/modules/data_governance/) | Optional | Build copy/paste prompt package for manual governance suggestion generation. |
| [`classify_column`](./step-09-ai-assisted-classification/classify_column/) | [`data_governance`](../api/modules/data_governance/) | Optional | Classify one column using term matching, metadata cues, and business context. |
| [`classify_columns`](./step-09-ai-assisted-classification/classify_columns/) | [`data_governance`](../api/modules/data_governance/) | Optional | Classify multiple columns and return normalized governance suggestions. |
| [`generate_governance_candidates_with_fabric_ai`](./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/) | [`data_governance`](../api/modules/data_governance/) | Optional | Execute Fabric AI Functions to append governance suggestions to a DataFrame. |
| [`summarize_governance_classifications`](./step-09-ai-assisted-classification/summarize_governance_classifications/) | [`data_governance`](../api/modules/data_governance/) | Optional | Summarize governance classification outputs into review-friendly counts. |
| [`write_governance_classifications`](./step-09-ai-assisted-classification/write_governance_classifications/) | [`data_governance`](../api/modules/data_governance/) | Optional | Persist governance classifications to a metadata destination. |

## Step 10: Generate lineage & handover documentation

This step creates the final documentation needed for review, handover, and future maintenance. Functions here support lineage, transformation summaries, and handover notes so another analyst or engineer can understand what was built, why it was built, and how to operate it.

| Function / class | Module | Importance | Purpose |
|---|---|---|---|
| [`build_handover_summary_prompt`](./step-10-lineage-handover-documentation/build_handover_summary_prompt/) | [`handover_documentation`](../api/modules/handover_documentation/) | Optional | Build the handover-summary prompt for AI-assisted run handoff drafting. |
| [`build_lineage_from_notebook_code`](./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Scan, optionally enrich, and validate lineage from notebook source code. |
| [`build_lineage_handover_markdown`](./step-10-lineage-handover-documentation/build_lineage_handover_markdown/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Create a concise markdown handover summary from lineage execution results. |
| [`build_lineage_record_from_steps`](./step-10-lineage-handover-documentation/build_lineage_record_from_steps/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Create metadata-ready lineage records from validated lineage steps. |
| [`build_lineage_records`](./step-10-lineage-handover-documentation/build_lineage_records/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Build compact lineage records for downstream metadata sinks. |
| [`build_manual_handover_prompt_package`](./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/) | [`handover_documentation`](../api/modules/handover_documentation/) | Optional | Build copy/paste prompt package for manual handover summary generation. |
| [`build_run_summary`](./step-10-lineage-handover-documentation/build_run_summary/) | [`handover_documentation`](../api/modules/handover_documentation/) | Optional | Build a handover-friendly summary for one data product run. |
| [`enrich_lineage_steps_with_ai`](./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Optionally enrich deterministic lineage steps using an AI helper callable. |
| [`fallback_copilot_lineage_prompt`](./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Build a fallback Copilot prompt for manual lineage enrichment. |
| [`generate_handover_summary_with_fabric_ai`](./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/) | [`handover_documentation`](../api/modules/handover_documentation/) | Optional | Execute Fabric AI Functions to append handover summary suggestions. |
| [`parse_manual_ai_json_response`](./step-10-lineage-handover-documentation/parse_manual_ai_json_response/) | [`handover_documentation`](../api/modules/handover_documentation/) | Optional | Parse manual AI JSON output into Python objects. |
| [`plot_lineage_steps`](./step-10-lineage-handover-documentation/plot_lineage_steps/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Render lineage steps as a directed graph figure. |
| [`render_run_summary_markdown`](./step-10-lineage-handover-documentation/render_run_summary_markdown/) | [`handover_documentation`](../api/modules/handover_documentation/) | Optional | Render a run summary dictionary into Markdown for handover notes. |
| [`scan_notebook_cells`](./step-10-lineage-handover-documentation/scan_notebook_cells/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Scan multiple notebook cells and append cell references to lineage steps. |
| [`scan_notebook_lineage`](./step-10-lineage-handover-documentation/scan_notebook_lineage/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Extract deterministic lineage steps from notebook code using AST parsing. |
| [`validate_lineage_steps`](./step-10-lineage-handover-documentation/validate_lineage_steps/) | [`data_lineage`](../api/modules/data_lineage/) | Optional | Validate lineage step structure and flag records requiring human review. |

## Other exported callables

These callables are exported by `fabricops_kit.__all__` but are not currently mapped to a lifecycle step. They are listed here so the public reference remains complete.

No unmapped exported callables.

