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

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)


### 2) Template generation

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)

- [`create_pipeline_notebook_template`](https://voycepeh.github.io/fabric-data-product-framework/reference/template_generator/create_pipeline_notebook_template/)
- [`create_actual_data_mvp_template`](https://voycepeh.github.io/fabric-data-product-framework/reference/template_generator/create_actual_data_mvp_template/)

### 3) Lineage and transformation summaries

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)

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

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)

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

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)


### 6) Contract-first orchestration and contract models

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)


### 7) Drift checks and snapshots

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)

- [`check_schema_drift`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/check_schema_drift/)
- [`build_and_write_schema_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/build_and_write_schema_snapshot/)
- [`load_latest_schema_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/load_latest_schema_snapshot/)
- [`check_partition_drift`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/check_partition_drift/)
- [`build_and_write_partition_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/build_and_write_partition_snapshot/)
- [`load_latest_partition_snapshot`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/load_latest_partition_snapshot/)
- [`check_profile_drift`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/check_profile_drift/)
- [`summarize_drift_results`](https://voycepeh.github.io/fabric-data-product-framework/reference/drift_checkers/summarize_drift_results/)

### 8) MVP step registry

Function reference: [`/reference/`](https://voycepeh.github.io/fabric-data-product-framework/reference/)

- [`MVP_STEPS`](https://voycepeh.github.io/fabric-data-product-framework/reference/mvp_steps/MVP_STEPS/)
- [`get_mvp_step_registry`](https://voycepeh.github.io/fabric-data-product-framework/reference/mvp_steps/get_mvp_step_registry/)
- [`validate_mvp_artifacts`](https://voycepeh.github.io/fabric-data-product-framework/reference/mvp_steps/validate_mvp_artifacts/)
