# Callable Function Reference

This page is the workflow-first callable function map for `fabric_data_product_framework`.

> **Note:** Clickable links in this reference open the rendered GitHub Pages API docs (not raw repository Markdown).

> Click any function name to view its generated API documentation, including signature, parameters, returns, and examples.
> Links in this map intentionally point to module-level API pages (not per-function anchors) to avoid broken-anchor maintenance.

## Public callable surface source of truth

The public callable surface below is aligned to `src/fabric_data_product_framework/__init__.py` (`__all__`).

## Workflow-stage callable map

### 1) Fabric notebook runtime, IO, and metadata

API page: [`docs/api/fabric_notebook.md`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)

- [`Housepath`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`get_path`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`load_fabric_config`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`lakehouse_table_read`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`lakehouse_table_write`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`lakehouse_csv_read`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`lakehouse_parquet_read_as_spark`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`lakehouse_excel_read_as_spark`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`warehouse_read`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`warehouse_write`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`check_naming_convention`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`clean_datetime_columns`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`add_system_technical_columns`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`ODI_METADATA_LOGGER`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`transformation_summary`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`transformation_reasons`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)
- [`pass_if_yes_else_run`](https://voycepeh.github.io/fabric-data-product-framework/api/fabric_notebook/)

### 2) Template generation

API page: [`docs/api/template_generator.md`](https://voycepeh.github.io/fabric-data-product-framework/api/template_generator/)

- [`create_pipeline_notebook_template`](https://voycepeh.github.io/fabric-data-product-framework/api/template_generator/)
- [`create_actual_data_mvp_template`](https://voycepeh.github.io/fabric-data-product-framework/api/template_generator/)

### 3) Lineage and transformation summaries

API page: [`docs/api/lineage.md`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)

- [`validate_lineage_steps`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`plot_lineage_networkx`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`get_fabric_copilot_lineage_prompt`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`generate_mermaid_lineage`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`build_transformation_summary_markdown`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`build_lineage_records`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`build_lineage_record_from_steps`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`build_lineage_record`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`build_lineage_prompt_context`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)
- [`LineageRecorder`](https://voycepeh.github.io/fabric-data-product-framework/api/lineage/)

### 4) Data quality workflow

API page: [`docs/api/dq.md`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)

- [`run_dq_workflow`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`run_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`load_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`store_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`build_dq_rule_records`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`normalize_dq_rules`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`normalize_dq_rule`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`generate_dq_rule_candidates`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)
- [`generate_dq_rule_candidates_with_fabric_ai`](https://voycepeh.github.io/fabric-data-product-framework/api/dq/)

### 5) Governance classification

API page: [`docs/api/governance.md`](https://voycepeh.github.io/fabric-data-product-framework/api/governance/)

- [`classify_column`](https://voycepeh.github.io/fabric-data-product-framework/api/governance/)
- [`classify_columns`](https://voycepeh.github.io/fabric-data-product-framework/api/governance/)
- [`build_governance_classification_records`](https://voycepeh.github.io/fabric-data-product-framework/api/governance/)
- [`write_governance_classifications`](https://voycepeh.github.io/fabric-data-product-framework/api/governance/)
- [`summarize_governance_classifications`](https://voycepeh.github.io/fabric-data-product-framework/api/governance/)

### 6) Contract-first orchestration and contract models

API page: [`docs/api/contracts.md`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)

- [`SourceContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`TargetContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`QualityContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`DriftContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`GovernanceContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`MetadataContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`RuntimeContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`DataProductContract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_source_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_target_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_quality_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_drift_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_governance_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_metadata_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_runtime_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`normalize_data_product_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`data_product_contract_to_dict`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`assert_data_product_passed`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`build_runtime_context_from_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`load_data_contract`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`run_data_product`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)
- [`validate_data_contract_shape`](https://voycepeh.github.io/fabric-data-product-framework/api/contracts/)

### 7) Drift checks and snapshots

API page: [`docs/api/drift_checkers.md`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)

- [`check_schema_drift`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)
- [`build_and_write_schema_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)
- [`load_latest_schema_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)
- [`check_partition_drift`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)
- [`build_and_write_partition_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)
- [`load_latest_partition_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)
- [`check_profile_drift`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)
- [`summarize_drift_results`](https://voycepeh.github.io/fabric-data-product-framework/api/drift_checkers/)

### 8) MVP step registry

API page: [`docs/api/mvp_steps.md`](https://voycepeh.github.io/fabric-data-product-framework/api/mvp_steps/)

- [`MVP_STEPS`](https://voycepeh.github.io/fabric-data-product-framework/api/mvp_steps/)
- [`get_mvp_step_registry`](https://voycepeh.github.io/fabric-data-product-framework/api/mvp_steps/)
- [`validate_mvp_artifacts`](https://voycepeh.github.io/fabric-data-product-framework/api/mvp_steps/)
