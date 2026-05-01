# Callable Function Reference

This page is the workflow-first callable function map for `fabric_data_product_framework`.

> Click any function name to view its generated API documentation, including signature, parameters, returns, and examples.
> Links in this map intentionally point to module-level API pages (not per-function anchors) to avoid broken-anchor maintenance.

## Public callable surface source of truth

The public callable surface below is aligned to `src/fabric_data_product_framework/__init__.py` (`__all__`).

## Workflow-stage callable map

### 1) Fabric notebook runtime, IO, and metadata

API page: [`docs/api/fabric_notebook.md`](../docs/api/fabric_notebook.md)

- [`Housepath`](../docs/api/fabric_notebook.md)
- [`get_path`](../docs/api/fabric_notebook.md)
- [`load_fabric_config`](../docs/api/fabric_notebook.md)
- [`lakehouse_table_read`](../docs/api/fabric_notebook.md)
- [`lakehouse_table_write`](../docs/api/fabric_notebook.md)
- [`lakehouse_csv_read`](../docs/api/fabric_notebook.md)
- [`lakehouse_parquet_read_as_spark`](../docs/api/fabric_notebook.md)
- [`lakehouse_excel_read_as_spark`](../docs/api/fabric_notebook.md)
- [`warehouse_read`](../docs/api/fabric_notebook.md)
- [`warehouse_write`](../docs/api/fabric_notebook.md)
- [`check_naming_convention`](../docs/api/fabric_notebook.md)
- [`clean_datetime_columns`](../docs/api/fabric_notebook.md)
- [`add_system_technical_columns`](../docs/api/fabric_notebook.md)
- [`ODI_METADATA_LOGGER`](../docs/api/fabric_notebook.md)
- [`transformation_summary`](../docs/api/fabric_notebook.md)
- [`transformation_reasons`](../docs/api/fabric_notebook.md)
- [`pass_if_yes_else_run`](../docs/api/fabric_notebook.md)

### 2) Template generation

API page: [`docs/api/template_generator.md`](../docs/api/template_generator.md)

- [`create_pipeline_notebook_template`](../docs/api/template_generator.md)
- [`create_actual_data_mvp_template`](../docs/api/template_generator.md)

### 3) Lineage and transformation summaries

API page: [`docs/api/lineage.md`](../docs/api/lineage.md)

- [`validate_lineage_steps`](../docs/api/lineage.md)
- [`plot_lineage_networkx`](../docs/api/lineage.md)
- [`get_fabric_copilot_lineage_prompt`](../docs/api/lineage.md)
- [`generate_mermaid_lineage`](../docs/api/lineage.md)
- [`build_transformation_summary_markdown`](../docs/api/lineage.md)
- [`build_lineage_records`](../docs/api/lineage.md)
- [`build_lineage_record_from_steps`](../docs/api/lineage.md)
- [`build_lineage_record`](../docs/api/lineage.md)
- [`build_lineage_prompt_context`](../docs/api/lineage.md)
- [`LineageRecorder`](../docs/api/lineage.md)

### 4) Data quality workflow

API page: [`docs/api/dq.md`](../docs/api/dq.md)

- [`run_dq_workflow`](../docs/api/dq.md)
- [`run_dq_rules`](../docs/api/dq.md)
- [`load_dq_rules`](../docs/api/dq.md)
- [`store_dq_rules`](../docs/api/dq.md)
- [`build_dq_rule_records`](../docs/api/dq.md)
- [`normalize_dq_rules`](../docs/api/dq.md)
- [`normalize_dq_rule`](../docs/api/dq.md)
- [`generate_dq_rule_candidates`](../docs/api/dq.md)
- [`generate_dq_rule_candidates_with_fabric_ai`](../docs/api/dq.md)

### 5) Governance classification

API page: [`docs/api/governance.md`](../docs/api/governance.md)

- [`classify_column`](../docs/api/governance.md)
- [`classify_columns`](../docs/api/governance.md)
- [`build_governance_classification_records`](../docs/api/governance.md)
- [`write_governance_classifications`](../docs/api/governance.md)
- [`summarize_governance_classifications`](../docs/api/governance.md)

### 6) Contract-first orchestration and contract models

API page: [`docs/api/contracts.md`](../docs/api/contracts.md)

- [`SourceContract`](../docs/api/contracts.md)
- [`TargetContract`](../docs/api/contracts.md)
- [`QualityContract`](../docs/api/contracts.md)
- [`DriftContract`](../docs/api/contracts.md)
- [`GovernanceContract`](../docs/api/contracts.md)
- [`MetadataContract`](../docs/api/contracts.md)
- [`RuntimeContract`](../docs/api/contracts.md)
- [`DataProductContract`](../docs/api/contracts.md)
- [`build_source_contract`](../docs/api/contracts.md)
- [`build_target_contract`](../docs/api/contracts.md)
- [`build_quality_contract`](../docs/api/contracts.md)
- [`build_drift_contract`](../docs/api/contracts.md)
- [`build_governance_contract`](../docs/api/contracts.md)
- [`build_metadata_contract`](../docs/api/contracts.md)
- [`build_runtime_contract`](../docs/api/contracts.md)
- [`normalize_data_product_contract`](../docs/api/contracts.md)
- [`data_product_contract_to_dict`](../docs/api/contracts.md)
- [`assert_data_product_passed`](../docs/api/contracts.md)
- [`build_runtime_context_from_contract`](../docs/api/contracts.md)
- [`load_data_contract`](../docs/api/contracts.md)
- [`run_data_product`](../docs/api/contracts.md)
- [`validate_data_contract_shape`](../docs/api/contracts.md)

### 7) Drift checks and snapshots

API page: [`docs/api/drift_checkers.md`](../docs/api/drift_checkers.md)

- [`check_schema_drift`](../docs/api/drift_checkers.md)
- [`build_and_write_schema_snapshot`](../docs/api/drift_checkers.md)
- [`load_latest_schema_snapshot`](../docs/api/drift_checkers.md)
- [`check_partition_drift`](../docs/api/drift_checkers.md)
- [`build_and_write_partition_snapshot`](../docs/api/drift_checkers.md)
- [`load_latest_partition_snapshot`](../docs/api/drift_checkers.md)
- [`check_profile_drift`](../docs/api/drift_checkers.md)
- [`summarize_drift_results`](../docs/api/drift_checkers.md)

### 8) MVP step registry

API page: [`docs/api/mvp_steps.md`](../docs/api/mvp_steps.md)

- [`MVP_STEPS`](../docs/api/mvp_steps.md)
- [`get_mvp_step_registry`](../docs/api/mvp_steps.md)
- [`validate_mvp_artifacts`](../docs/api/mvp_steps.md)
