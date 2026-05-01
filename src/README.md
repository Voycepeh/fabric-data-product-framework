# Callable Function Reference

This page is the workflow-first callable function map for `fabric_data_product_framework`.

> **Note:** Clickable links in this reference open the rendered GitHub Pages API docs (not raw repository Markdown).

> Click any function name to view its generated API documentation, including signature, parameters, returns, and examples.
> Links in this map point to one rendered GitHub Pages page per public callable.


## Notebook recipe map

Use these copy-paste runnable recipe docs to apply the callable groups end to end:

- [Recipe index](../docs/recipes/index.md)
- [Local-safe smoke](../docs/recipes/local-safe-smoke.md)
- [Fabric dry run](../docs/recipes/fabric-dry-run.md)
- [Contract-first one call](../docs/recipes/contract-first-one-call.md)
- [Full metadata chaining](../docs/recipes/profile-dq-governance-lineage-handover.md)

## Public callable surface source of truth

The public callable surface below is aligned to `src/fabric_data_product_framework/__init__.py` (`__all__`).

## Workflow-stage callable map

### 1) Fabric notebook runtime, IO, and metadata

API page: [`docs/api/fabric_notebook.md`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)

- [`Housepath`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/Housepath/)
- [`get_path`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/get_path/)
- [`load_fabric_config`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/load_fabric_config/)
- [`lakehouse_table_read`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/lakehouse_table_read/)
- [`lakehouse_table_write`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/lakehouse_table_write/)
- [`lakehouse_csv_read`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/lakehouse_csv_read/)
- [`lakehouse_parquet_read_as_spark`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/lakehouse_parquet_read_as_spark/)
- [`lakehouse_excel_read_as_spark`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/lakehouse_excel_read_as_spark/)
- [`warehouse_read`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/warehouse_read/)
- [`warehouse_write`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/warehouse_write/)
- [`check_naming_convention`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/check_naming_convention/)
- [`clean_datetime_columns`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/clean_datetime_columns/)
- [`add_system_technical_columns`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/add_system_technical_columns/)
- [`ODI_METADATA_LOGGER`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/ODI_METADATA_LOGGER/)
- [`transformation_summary`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/transformation_summary/)
- [`transformation_reasons`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/transformation_reasons/)
- [`pass_if_yes_else_run`](https://voycepeh.github.io/fabric-data-product-framework/reference/fabric_notebook/pass_if_yes_else_run/)

### 2) Template generation

API page: [`docs/api/template_generator.md`](https://voycepeh.github.io/fabric-data-product-framework/api/template_generator/)

- [`create_pipeline_notebook_template`](https://voycepeh.github.io/fabric-data-product-framework/reference/template_generator/create_pipeline_notebook_template/)
- [`create_actual_data_mvp_template`](https://voycepeh.github.io/fabric-data-product-framework/reference/template_generator/create_actual_data_mvp_template/)

### 3) Lineage and transformation summaries

API page: [`docs/api/lineage.md`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)

- [`validate_lineage_steps`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/validate_lineage_steps/)
- [`plot_lineage_networkx`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/plot_lineage_networkx/)
- [`get_fabric_copilot_lineage_prompt`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/get_fabric_copilot_lineage_prompt/)
- [`generate_mermaid_lineage`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/generate_mermaid_lineage/)
- [`build_transformation_summary_markdown`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/build_transformation_summary_markdown/)
- [`build_lineage_records`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/build_lineage_records/)
- [`build_lineage_record_from_steps`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/build_lineage_record_from_steps/)
- [`build_lineage_record`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/build_lineage_record/)
- [`build_lineage_prompt_context`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/build_lineage_prompt_context/)
- [`LineageRecorder`](https://voycepeh.github.io/fabric-data-product-framework/reference/lineage/LineageRecorder/)

### 4) Data quality workflow

API page: [`docs/api/dq.md`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)

- [`run_dq_workflow`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/run_dq_workflow/)
- [`run_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/run_dq_rules/)
- [`load_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/load_dq_rules/)
- [`store_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/store_dq_rules/)
- [`build_dq_rule_records`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/build_dq_rule_records/)
- [`normalize_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/normalize_dq_rules/)
- [`normalize_dq_rule`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/normalize_dq_rule/)
- [`generate_dq_rule_candidates`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/generate_dq_rule_candidates/)
- [`generate_dq_rule_candidates_with_fabric_ai`](https://voycepeh.github.io/fabric-data-product-framework/reference/dq/generate_dq_rule_candidates_with_fabric_ai/)

### 5) Governance classification

API page: [`docs/api/governance.md`](https://voycepeh.github.io/fabric-data-product-framework/api/governance/)

- [`classify_column`](https://voycepeh.github.io/fabric-data-product-framework/reference/governance/classify_column/)
- [`classify_columns`](https://voycepeh.github.io/fabric-data-product-framework/reference/governance/classify_columns/)
- [`build_governance_classification_records`](https://voycepeh.github.io/fabric-data-product-framework/reference/governance/build_governance_classification_records/)
- [`write_governance_classifications`](https://voycepeh.github.io/fabric-data-product-framework/reference/governance/write_governance_classifications/)
- [`summarize_governance_classifications`](https://voycepeh.github.io/fabric-data-product-framework/reference/governance/summarize_governance_classifications/)

### 6) Contract-first orchestration and contract models

API page: [`docs/api/contracts.md`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)

- [`SourceContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/SourceContract/)
- [`TargetContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/TargetContract/)
- [`QualityContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/QualityContract/)
- [`DriftContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/DriftContract/)
- [`GovernanceContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/GovernanceContract/)
- [`MetadataContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/MetadataContract/)
- [`RuntimeContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/RuntimeContract/)
- [`DataProductContract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/DataProductContract/)
- [`build_source_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_source_contract/)
- [`build_target_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_target_contract/)
- [`build_quality_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_quality_contract/)
- [`build_drift_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_drift_contract/)
- [`build_governance_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_governance_contract/)
- [`build_metadata_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_metadata_contract/)
- [`build_runtime_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_runtime_contract/)
- [`normalize_data_product_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/normalize_data_product_contract/)
- [`data_product_contract_to_dict`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/data_product_contract_to_dict/)
- [`assert_data_product_passed`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/assert_data_product_passed/)
- [`build_runtime_context_from_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/build_runtime_context_from_contract/)
- [`load_data_contract`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/load_data_contract/)
- [`run_data_product`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/run_data_product/)
- [`validate_data_contract_shape`](https://voycepeh.github.io/fabric-data-product-framework/reference/contracts/validate_data_contract_shape/)

### 7) Drift checks and snapshots

API page: [`docs/api/drift_checkers.md`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)

- [`check_schema_drift`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/check_schema_drift/)
- [`build_and_write_schema_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/build_and_write_schema_snapshot/)
- [`load_latest_schema_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/load_latest_schema_snapshot/)
- [`check_partition_drift`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/check_partition_drift/)
- [`build_and_write_partition_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/build_and_write_partition_snapshot/)
- [`load_latest_partition_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/load_latest_partition_snapshot/)
- [`check_profile_drift`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/check_profile_drift/)
- [`summarize_drift_results`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/summarize_drift_results/)

### 8) MVP step registry

API page: [`docs/api/mvp_steps.md`](https://voycepeh.github.io/fabric-data-product-framework/api/mvp_steps/)

- [`MVP_STEPS`](https://voycepeh.github.io/fabric-data-product-framework/reference/mvp_steps/MVP_STEPS/)
- [`get_mvp_step_registry`](https://voycepeh.github.io/fabric-data-product-framework/reference/mvp_steps/get_mvp_step_registry/)
- [`validate_mvp_artifacts`](https://voycepeh.github.io/fabric-data-product-framework/reference/mvp_steps/validate_mvp_artifacts/)
