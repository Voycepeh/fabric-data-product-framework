# Callable Map

This page maps public FabricOps callables to the internal helpers they use. It is generated from src/fabricops_kit/*.py using Python AST parsing.

## Public callable chains

<input id="callable-map-search" type="search" placeholder="Search callable map" aria-label="Search callable map">

<article data-callable-map-row="true" data-callable-name="draft_business_context" data-callable-module="business_context" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `draft_business_context`
- module: `business_context`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="review_business_context" data-callable-module="business_context" data-callable-role="essential" data-callable-helpers="_require_ipywidgets" data-callable-cross-module="build_metadata_column_key build_metadata_table_key">
### `review_business_context`
- module: `business_context`
- role: `essential`
- direct internal helpers used: `_require_ipywidgets`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: `fabricops_kit.metadata.build_metadata_column_key`, `fabricops_kit.metadata.build_metadata_table_key`
</article>

<article data-callable-map-row="true" data-callable-name="write_business_context" data-callable-module="business_context" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="write_column_business_context">
### `write_business_context`
- module: `business_context`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: `fabricops_kit.metadata.write_column_business_context`
</article>

<article data-callable-map-row="true" data-callable-name="get_path" data-callable-module="config" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `get_path`
- module: `config`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="load_config" data-callable-module="config" data-callable-role="essential" data-callable-helpers="_validate_framework_config" data-callable-cross-module="">
### `load_config`
- module: `config`
- role: `essential`
- direct internal helpers used: `_validate_framework_config`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="setup_notebook" data-callable-module="config" data-callable-role="essential" data-callable-helpers="_check_fabric_ai_functions_available _configure_fabric_ai_functions _run_config_smoke_tests" data-callable-cross-module="">
### `setup_notebook`
- module: `config`
- role: `essential`
- direct internal helpers used: `_check_fabric_ai_functions_available`, `_configure_fabric_ai_functions`, `_run_config_smoke_tests`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="get_selected_agreement" data-callable-module="data_agreement" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `get_selected_agreement`
- module: `data_agreement`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="load_agreements" data-callable-module="data_agreement" data-callable-role="essential" data-callable-helpers="_coerce_row_dicts _latest_distinct_agreements" data-callable-cross-module="">
### `load_agreements`
- module: `data_agreement`
- role: `essential`
- direct internal helpers used: `_coerce_row_dicts`, `_latest_distinct_agreements`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="select_agreement" data-callable-module="data_agreement" data-callable-role="essential" data-callable-helpers="_agreement_option_label _coerce_row_dicts" data-callable-cross-module="">
### `select_agreement`
- module: `data_agreement`
- role: `essential`
- direct internal helpers used: `_agreement_option_label`, `_coerce_row_dicts`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="draft_governance" data-callable-module="data_governance" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `draft_governance`
- module: `data_governance`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="load_governance" data-callable-module="data_governance" data-callable-role="essential" data-callable-helpers="_coerce_row_dicts" data-callable-cross-module="">
### `load_governance`
- module: `data_governance`
- role: `essential`
- direct internal helpers used: `_coerce_row_dicts`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="review_governance" data-callable-module="data_governance" data-callable-role="essential" data-callable-helpers="_undo_last_action" data-callable-cross-module="_now_utc_iso build_metadata_column_key build_metadata_table_key">
### `review_governance`
- module: `data_governance`
- role: `essential`
- direct internal helpers used: `_undo_last_action`
- direct cross-module public calls: —
- direct cross-module private helper calls: `fabricops_kit.metadata._now_utc_iso`
- direct cross-module internal calls: `fabricops_kit.metadata.build_metadata_column_key`, `fabricops_kit.metadata.build_metadata_table_key`
</article>

<article data-callable-map-row="true" data-callable-name="write_governance" data-callable-module="data_governance" data-callable-role="essential" data-callable-helpers="_approved_widget_rows" data-callable-cross-module="">
### `write_governance`
- module: `data_governance`
- role: `essential`
- direct internal helpers used: `_approved_widget_rows`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="build_lineage_handover_markdown" data-callable-module="data_lineage" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `build_lineage_handover_markdown`
- module: `data_lineage`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="build_lineage_records" data-callable-module="data_lineage" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `build_lineage_records`
- module: `data_lineage`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="profile_dataframe" data-callable-module="data_profiling" data-callable-role="essential" data-callable-helpers="_get_profiled_columns _is_min_max_supported_type" data-callable-cross-module="">
### `profile_dataframe`
- module: `data_profiling`
- role: `essential`
- direct internal helpers used: `_get_profiled_columns`, `_is_min_max_supported_type`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="assert_dq_passed" data-callable-module="data_quality" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `assert_dq_passed`
- module: `data_quality`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="draft_dq_rules" data-callable-module="data_quality" data-callable-role="essential" data-callable-helpers="__prepare_dq_profile_input_rows _extract_dq_rules _suggest_dq_rules" data-callable-cross-module="">
### `draft_dq_rules`
- module: `data_quality`
- role: `essential`
- direct internal helpers used: `__prepare_dq_profile_input_rows`, `_extract_dq_rules`, `_suggest_dq_rules`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="enforce_dq" data-callable-module="data_quality" data-callable-role="essential" data-callable-helpers="_load_active_dq_rules _run_dq_rules _split_dq_rows" data-callable-cross-module="">
### `enforce_dq`
- module: `data_quality`
- role: `essential`
- direct internal helpers used: `_load_active_dq_rules`, `_run_dq_rules`, `_split_dq_rows`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="get_dq_review_results" data-callable-module="data_quality" data-callable-role="essential" data-callable-helpers="_attach_rule_metadata_keys" data-callable-cross-module="">
### `get_dq_review_results`
- module: `data_quality`
- role: `essential`
- direct internal helpers used: `_attach_rule_metadata_keys`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="load_dq_rules" data-callable-module="data_quality" data-callable-role="essential" data-callable-helpers="_load_active_dq_rules" data-callable-cross-module="">
### `load_dq_rules`
- module: `data_quality`
- role: `essential`
- direct internal helpers used: `_load_active_dq_rules`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="review_dq_rule_deactivations" data-callable-module="data_quality" data-callable-role="optional" data-callable-helpers="_require_ipywidgets" data-callable-cross-module="">
### `review_dq_rule_deactivations`
- module: `data_quality`
- role: `optional`
- direct internal helpers used: `_require_ipywidgets`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="review_dq_rules" data-callable-module="data_quality" data-callable-role="essential" data-callable-helpers="_require_ipywidgets" data-callable-cross-module="">
### `review_dq_rules`
- module: `data_quality`
- role: `essential`
- direct internal helpers used: `_require_ipywidgets`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="validate_dq_rules" data-callable-module="data_quality" data-callable-role="optional" data-callable-helpers="" data-callable-cross-module="">
### `validate_dq_rules`
- module: `data_quality`
- role: `optional`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="write_dq_rules" data-callable-module="data_quality" data-callable-role="essential" data-callable-helpers="_build_dq_rule_history" data-callable-cross-module="write_lakehouse_table">
### `write_dq_rules`
- module: `data_quality`
- role: `essential`
- direct internal helpers used: `_build_dq_rule_history`
- direct cross-module public calls: `fabricops_kit.fabric_input_output.write_lakehouse_table`
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="check_partition_drift" data-callable-module="drift" data-callable-role="optional" data-callable-helpers="" data-callable-cross-module="">
### `check_partition_drift`
- module: `drift`
- role: `optional`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="check_profile_drift" data-callable-module="drift" data-callable-role="optional" data-callable-helpers="" data-callable-cross-module="">
### `check_profile_drift`
- module: `drift`
- role: `optional`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="check_schema_drift" data-callable-module="drift" data-callable-role="optional" data-callable-helpers="" data-callable-cross-module="">
### `check_schema_drift`
- module: `drift`
- role: `optional`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="summarize_drift_results" data-callable-module="drift" data-callable-role="optional" data-callable-helpers="" data-callable-cross-module="">
### `summarize_drift_results`
- module: `drift`
- role: `optional`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="Housepath" data-callable-module="fabric_input_output" data-callable-role="optional" data-callable-helpers="" data-callable-cross-module="">
### `Housepath`
- module: `fabric_input_output`
- role: `optional`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="read_lakehouse_csv" data-callable-module="fabric_input_output" data-callable-role="optional" data-callable-helpers="_get_spark" data-callable-cross-module="">
### `read_lakehouse_csv`
- module: `fabric_input_output`
- role: `optional`
- direct internal helpers used: `_get_spark`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="read_lakehouse_excel" data-callable-module="fabric_input_output" data-callable-role="optional" data-callable-helpers="_get_spark" data-callable-cross-module="">
### `read_lakehouse_excel`
- module: `fabric_input_output`
- role: `optional`
- direct internal helpers used: `_get_spark`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="read_lakehouse_parquet" data-callable-module="fabric_input_output" data-callable-role="optional" data-callable-helpers="_convert_single_parquet_ns_to_us _get_spark" data-callable-cross-module="">
### `read_lakehouse_parquet`
- module: `fabric_input_output`
- role: `optional`
- direct internal helpers used: `_convert_single_parquet_ns_to_us`, `_get_spark`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="read_lakehouse_table" data-callable-module="fabric_input_output" data-callable-role="essential" data-callable-helpers="_get_spark" data-callable-cross-module="">
### `read_lakehouse_table`
- module: `fabric_input_output`
- role: `essential`
- direct internal helpers used: `_get_spark`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="read_warehouse_table" data-callable-module="fabric_input_output" data-callable-role="essential" data-callable-helpers="_get_spark" data-callable-cross-module="get_path">
### `read_warehouse_table`
- module: `fabric_input_output`
- role: `essential`
- direct internal helpers used: `_get_spark`
- direct cross-module public calls: `fabricops_kit.config.get_path`
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="write_lakehouse_table" data-callable-module="fabric_input_output" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `write_lakehouse_table`
- module: `fabric_input_output`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="write_warehouse_table" data-callable-module="fabric_input_output" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="get_path">
### `write_warehouse_table`
- module: `fabric_input_output`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: `fabricops_kit.config.get_path`
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="build_handover" data-callable-module="handover" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `build_handover`
- module: `handover`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="render_handover_markdown" data-callable-module="handover" data-callable-role="essential" data-callable-helpers="_status_of" data-callable-cross-module="">
### `render_handover_markdown`
- module: `handover`
- role: `essential`
- direct internal helpers used: `_status_of`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="load_notebook_registry" data-callable-module="metadata" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `load_notebook_registry`
- module: `metadata`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="register_current_notebook" data-callable-module="metadata" data-callable-role="essential" data-callable-helpers="_runtime_context" data-callable-cross-module="">
### `register_current_notebook`
- module: `metadata`
- role: `essential`
- direct internal helpers used: `_runtime_context`
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

<article data-callable-map-row="true" data-callable-name="standardize_columns" data-callable-module="technical_columns" data-callable-role="essential" data-callable-helpers="" data-callable-cross-module="">
### `standardize_columns`
- module: `technical_columns`
- role: `essential`
- direct internal helpers used: —
- direct cross-module public calls: —
- direct cross-module private helper calls: —
- direct cross-module internal calls: —
</article>

## Internal helper index

| helper | module | used by public callables | used by internal helpers |
|---|---|---|---|
| `_to_jsonable` | `_utils` | — | `_build_pandas_partition_snapshot`, `_build_spark_partition_snapshot`, `_json_dumps`, `_to_jsonable`, `build_incremental_safety_records`, `compare_partition_snapshots` |
| `_extract_column_business_context_suggestions` | `business_context` | — | — |
| `_parse_ai_dict_response` | `business_context` | — | `_extract_column_business_context_suggestions` |
| `_prepare_business_context_profile_input` | `business_context` | — | — |
| `_require_ipywidgets` | `business_context` | `review_business_context` | — |
| `_bootstrap_fabric_env` | `config` | — | — |
| `_check_fabric_ai_functions_available` | `config` | `setup_notebook` | `_bootstrap_fabric_env`, `_run_config_smoke_tests` |
| `_check_spark_session` | `config` | — | `_run_config_smoke_tests` |
| `_configure_fabric_ai_functions` | `config` | `setup_notebook` | — |
| `_default_schema_text` | `config` | — | `_load_schema` |
| `_format_error_path` | `config` | — | `validate_dataset_contract` |
| `_get_fabric_runtime_metadata` | `config` | — | `_bootstrap_fabric_env`, `_run_config_smoke_tests` |
| `_load_schema` | `config` | — | `validate_dataset_contract` |
| `_normalize_name` | `config` | — | `_validate_notebook_name` |
| `_run_config_smoke_tests` | `config` | `setup_notebook` | `_bootstrap_fabric_env` |
| `_validate_framework_config` | `config` | `load_config` | — |
| `_validate_notebook_name` | `config` | — | `_run_config_smoke_tests` |
| `_agreement_option_label` | `data_agreement` | `select_agreement` | — |
| `_coerce_row_dicts` | `data_agreement` | `load_agreements`, `select_agreement` | — |
| `_latest_distinct_agreements` | `data_agreement` | `load_agreements` | — |
| `_approved_widget_rows` | `data_governance` | `write_governance` | — |
| `_build_governance_context` | `data_governance` | — | — |
| `_coerce_row_dicts` | `data_governance` | `load_governance` | — |
| `_extract_pii_suggestions` | `data_governance` | — | — |
| `_prepare_governance_input` | `data_governance` | — | — |
| `_undo_last_action` | `data_governance` | `review_governance` | — |
| `_build_lineage_record_from_steps` | `data_lineage` | — | `_build_lineage_records` |
| `_build_lineage_records` | `data_lineage` | — | — |
| `_call_name` | `data_lineage` | — | `_scan_notebook_lineage` |
| `_enrich_lineage_steps_with_ai` | `data_lineage` | — | — |
| `_fallback_copilot_lineage_prompt` | `data_lineage` | — | `_enrich_lineage_steps_with_ai` |
| `_flatten_chain` | `data_lineage` | — | `_scan_notebook_lineage` |
| `_literal` | `data_lineage` | — | `_resolve_write_target` |
| `_name` | `data_lineage` | — | `_flatten_chain`, `_scan_notebook_lineage` |
| `_resolve_write_target` | `data_lineage` | — | `_scan_notebook_lineage` |
| `_scan_notebook_cells` | `data_lineage` | — | — |
| `_scan_notebook_lineage` | `data_lineage` | — | `_scan_notebook_cells` |
| `_step` | `data_lineage` | — | `_scan_notebook_lineage` |
| `_validate_lineage_steps` | `data_lineage` | — | `_build_lineage_record_from_steps` |
| `_get_profiled_columns` | `data_profiling` | `profile_dataframe` | — |
| `_is_min_max_supported_type` | `data_profiling` | `profile_dataframe` | — |
| `__parse_dq_rules_dict_from_text` | `data_quality` | — | `_extract_candidate_rules_from_responses`, `_extract_dq_rules` |
| `__prepare_dq_profile_input_rows` | `data_quality` | `draft_dq_rules` | — |
| `_approved_dq_rules_from_review_rows` | `data_quality` | — | — |
| `_attach_rule_metadata_keys` | `data_quality` | `get_dq_review_results` | — |
| `_build_dq_rule_deactivation_metadata_df` | `data_quality` | — | — |
| `_build_dq_rule_deactivations` | `data_quality` | — | — |
| `_build_dq_rule_history` | `data_quality` | `write_dq_rules` | — |
| `_build_dq_rules_metadata_df` | `data_quality` | — | — |
| `_extract_candidate_rules_from_responses` | `data_quality` | — | — |
| `_extract_dq_rules` | `data_quality` | `draft_dq_rules` | `_extract_candidate_rules_from_responses` |
| `_latest_dq_rule_versions` | `data_quality` | — | `_load_active_dq_rule_metadata`, `_load_active_dq_rules` |
| `_load_active_dq_rule_metadata` | `data_quality` | — | — |
| `_load_active_dq_rules` | `data_quality` | `enforce_dq`, `load_dq_rules` | — |
| `_prepare_dq_profile_input_rows` | `data_quality` | — | — |
| `_profile_for_dq` | `data_quality` | — | — |
| `_require_ipywidgets` | `data_quality` | `review_dq_rule_deactivations`, `review_dq_rules` | — |
| `_run_dq_rules` | `data_quality` | `enforce_dq` | — |
| `_split_dq_rows` | `data_quality` | `enforce_dq` | `_run_dq_rules` |
| `_suggest_dq_rules` | `data_quality` | `draft_dq_rules` | — |
| `_suggest_dq_rules_with_fabric_ai` | `data_quality` | — | — |
| `_build_pandas_partition_snapshot` | `drift` | — | `build_partition_snapshot` |
| `_build_pandas_schema_snapshot` | `drift` | — | `build_schema_snapshot` |
| `_build_partition_hash` | `drift` | — | `_build_pandas_partition_snapshot`, `_build_spark_partition_snapshot` |
| `_build_spark_partition_snapshot` | `drift` | — | `build_partition_snapshot` |
| `_build_spark_schema_snapshot` | `drift` | — | `build_schema_snapshot` |
| `_column_hash` | `drift` | — | `_build_pandas_schema_snapshot`, `_build_spark_schema_snapshot` |
| `_hash` | `drift` | — | `_build_pandas_partition_snapshot`, `_build_partition_hash` |
| `_is_closed_partition` | `drift` | — | `compare_partition_snapshots` |
| `_is_missing_table_error` | `drift` | — | `load_latest_partition_snapshot`, `load_latest_schema_snapshot` |
| `_json_dumps` | `drift` | — | `build_and_write_partition_snapshot`, `build_and_write_schema_snapshot`, `build_drift_evidence_record` |
| `_resolve_change_behavior` | `drift` | — | `compare_schema_snapshots` |
| `_safe_spark_collect` | `drift` | — | `load_latest_partition_snapshot`, `load_latest_schema_snapshot` |
| `_utc_now_iso` | `drift` | — | `build_and_write_partition_snapshot`, `build_and_write_schema_snapshot`, `build_drift_evidence_record` |
| `_write_metadata_rows` | `drift` | — | `build_and_write_partition_snapshot`, `build_and_write_schema_snapshot` |
| `_convert_single_parquet_ns_to_us` | `fabric_input_output` | `read_lakehouse_parquet` | — |
| `_get_fabric_runtime_context` | `fabric_input_output` | — | `check_naming_convention` |
| `_get_spark` | `fabric_input_output` | `read_lakehouse_csv`, `read_lakehouse_excel`, `read_lakehouse_parquet`, `read_lakehouse_table`, `read_warehouse_table` | `seed_minimal_sample_source_table` |
| `_status_of` | `handover` | `render_handover_markdown` | `build_handover_record` |
| `_extract_columns_from_profile` | `metadata` | — | — |
| `_key_part` | `metadata` | — | `_sha256_key` |
| `_now_utc_iso` | `metadata` | `review_governance` | `_build_dq_rule_deactivation_metadata_df`, `_build_dq_rules_metadata_df`, `build_evidence_row` |
| `_resolve_action_by` | `metadata` | — | `_approved_widget_rows`, `_build_dq_rule_deactivation_metadata_df`, `_build_dq_rule_deactivations`, `_build_dq_rule_history`, `_build_dq_rules_metadata_df` |
| `_runtime_context` | `metadata` | `register_current_notebook` | — |
| `_sha256_key` | `metadata` | — | `build_dq_rule_key`, `build_metadata_column_key`, `build_metadata_table_key` |
| `__add_audit_columns` | `technical_columns` | — | — |
| `__add_datetime_features` | `technical_columns` | — | — |
| `__add_hash_columns` | `technical_columns` | — | — |
| `__default_technical_columns` | `technical_columns` | — | — |
| `_assert_columns_exist` | `technical_columns` | — | `__add_audit_columns`, `__add_datetime_features`, `__add_hash_columns` |
| `_bucket_values_pandas` | `technical_columns` | — | `__add_audit_columns` |
| `_get_fabric_runtime_context` | `technical_columns` | — | `__add_audit_columns` |
| `_hash_row` | `technical_columns` | — | `__add_hash_columns` |
| `_non_technical_columns` | `technical_columns` | — | `__add_hash_columns` |
| `_safe_string` | `technical_columns` | — | `_bucket_values_pandas`, `_hash_row` |

## Cross-module FabricOps calls

| caller module | caller function | callee module | callee function |
|---|---|---|---|
| `data_quality` | `_attach_rule_metadata_keys` | `metadata` | `build_metadata_table_key` |
| `data_quality` | `_attach_rule_metadata_keys` | `metadata` | `build_dq_rule_key` |
| `data_quality` | `_attach_rule_metadata_keys` | `metadata` | `build_metadata_column_key` |
| `data_quality` | `_build_dq_rule_history` | `metadata` | `_resolve_action_by` |
| `data_quality` | `_build_dq_rule_deactivations` | `metadata` | `_resolve_action_by` |
| `data_quality` | `__prepare_dq_profile_input_rows` | `data_profiling` | `profile_dataframe` |
| `data_quality` | `write_dq_rules` | `fabric_input_output` | `write_lakehouse_table` |
| `data_quality` | `_build_dq_rules_metadata_df` | `metadata` | `_now_utc_iso` |
| `data_quality` | `_build_dq_rules_metadata_df` | `metadata` | `_resolve_action_by` |
| `data_quality` | `_build_dq_rule_deactivation_metadata_df` | `metadata` | `_now_utc_iso` |
| `data_quality` | `_build_dq_rule_deactivation_metadata_df` | `metadata` | `_resolve_action_by` |
| `drift` | `_json_dumps` | `_utils` | `_to_jsonable` |
| `drift` | `_build_pandas_partition_snapshot` | `_utils` | `_to_jsonable` |
| `drift` | `_build_pandas_partition_snapshot` | `_utils` | `_to_jsonable` |
| `drift` | `_build_pandas_partition_snapshot` | `_utils` | `_to_jsonable` |
| `drift` | `_build_spark_partition_snapshot` | `_utils` | `_to_jsonable` |
| `drift` | `_build_spark_partition_snapshot` | `_utils` | `_to_jsonable` |
| `drift` | `_build_spark_partition_snapshot` | `_utils` | `_to_jsonable` |
| `drift` | `compare_partition_snapshots` | `_utils` | `_to_jsonable` |
| `drift` | `compare_partition_snapshots` | `_utils` | `_to_jsonable` |
| `drift` | `build_incremental_safety_records` | `_utils` | `_to_jsonable` |
| `business_context` | `review_business_context` | `metadata` | `build_metadata_table_key` |
| `business_context` | `review_business_context` | `metadata` | `build_metadata_column_key` |
| `business_context` | `write_business_context` | `metadata` | `write_column_business_context` |
| `data_governance` | `review_governance` | `metadata` | `build_metadata_table_key` |
| `data_governance` | `review_governance` | `metadata` | `build_metadata_column_key` |
| `data_governance` | `review_governance` | `metadata` | `_now_utc_iso` |
| `data_governance` | `_approved_widget_rows` | `metadata` | `_resolve_action_by` |
| `data_profiling` | `_get_profiled_columns` | `technical_columns` | `_default_technical_columns` |
| `metadata` | `write_metadata_rows` | `fabric_input_output` | `write_lakehouse_table` |
| `fabric_input_output` | `load_config` | `config` | `load_config` |
| `fabric_input_output` | `read_warehouse_table` | `config` | `get_path` |
| `fabric_input_output` | `write_warehouse_table` | `config` | `get_path` |

## Module dependency summary

| module | calls modules | called by modules | public callable count | internal helper count |
|---|---|---|---:|---:|
| `_utils` | — | `drift` | 0 | 1 |
| `business_context` | `metadata` | — | 3 | 4 |
| `config` | — | `fabric_input_output` | 3 | 12 |
| `data_agreement` | — | — | 3 | 3 |
| `data_governance` | `metadata` | — | 4 | 6 |
| `data_lineage` | — | — | 2 | 13 |
| `data_profiling` | `technical_columns` | `data_quality` | 1 | 2 |
| `data_quality` | `data_profiling`, `fabric_input_output`, `metadata` | — | 9 | 20 |
| `docs_metadata` | — | — | 0 | 0 |
| `drift` | `_utils` | — | 4 | 14 |
| `fabric_input_output` | `config` | `data_quality`, `metadata` | 8 | 3 |
| `handover` | — | — | 2 | 1 |
| `metadata` | `fabric_input_output` | `business_context`, `data_governance`, `data_quality` | 2 | 6 |
| `technical_columns` | — | — | 1 | 10 |
