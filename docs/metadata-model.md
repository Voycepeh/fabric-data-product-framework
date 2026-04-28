# Metadata Model (Initial Proposal)

This proposal defines initial Lakehouse metadata tables for framework observability. Column names are suggestions and may evolve with contract validation in later PRs.

## 1) metadata_dataset_runs
- **Purpose:** One record per notebook run.
- **Suggested columns:** run_id, dataset_id, run_mode, run_start_ts, run_end_ts, status, triggered_by, notebook_name, contract_version.
- **Notes:** Anchor table for joining most metadata outputs.

## 2) metadata_source_profiles
- **Purpose:** Source-level profile summary captured before transformations.
- **Suggested columns:** run_id, source_name, row_count, column_count, null_cell_ratio, duplicate_key_ratio, profile_json, profiled_ts.
- **Notes:** Store compact summary plus JSON for extensibility.

## 3) metadata_column_profiles
- **Purpose:** Column-level profiling details.
- **Suggested columns:** run_id, source_name, column_name, data_type_observed, null_ratio, distinct_count, min_value, max_value, mean_value, stddev_value.
- **Notes:** Numeric stats may be null for non-numeric columns.

## 4) metadata_schema_snapshots
- **Purpose:** Capture observed schema per run.
- **Suggested columns:** run_id, source_name, schema_version_hash, schema_json, captured_ts.
- **Notes:** Used as baseline for schema drift comparisons.

## 5) metadata_schema_drift_results
- **Purpose:** Store schema drift detection outcomes.
- **Suggested columns:** run_id, source_name, baseline_run_id, drift_detected, added_columns, removed_columns, type_changes, policy_action, details_json.
- **Notes:** Supports warning/error policy handling.

## 6) metadata_partition_snapshots
- **Purpose:** Snapshot incremental partition/watermark state.
- **Suggested columns:** run_id, source_name, partition_column, watermark_column, min_watermark, max_watermark, partition_count, snapshot_ts.
- **Notes:** Enables incremental safety checks across runs.

## 7) metadata_data_drift_results
- **Purpose:** Store data drift metric comparisons.
- **Suggested columns:** run_id, source_name, baseline_run_id, metric_name, column_name, baseline_value, current_value, drift_score, threshold, breach_flag.
- **Notes:** Metric granularity can be row-level or column-level.

## 8) metadata_transformation_steps
- **Purpose:** Record transformation step trace.
- **Suggested columns:** run_id, step_order, step_name, step_type, input_refs, output_ref, row_count_before, row_count_after, step_notes.
- **Notes:** Supports explainability and debugging.

## 9) metadata_lineage
- **Purpose:** Capture upstream/downstream lineage links.
- **Suggested columns:** run_id, edge_id, upstream_asset, downstream_asset, operation_type, contract_ref, lineage_ts.
- **Notes:** Can later align with broader enterprise lineage models.

## 10) metadata_dq_results
- **Purpose:** Store data quality rule outcomes.
- **Suggested columns:** run_id, rule_id, rule_name, rule_scope, severity, pass_flag, failed_count, threshold, result_notes.
- **Notes:** Rule engine details are out of scope for this PR.

## 11) metadata_governance_labels
- **Purpose:** Persist governance classifications at dataset/column level.
- **Suggested columns:** run_id, asset_level, asset_name, label_key, label_value, assigned_by, assigned_ts.
- **Notes:** Labels may be human-defined or AI-suggested then approved.

## 12) metadata_contract_validation_results
- **Purpose:** Capture validation of upstream/downstream/data contract checks.
- **Suggested columns:** run_id, contract_id, contract_type, validation_status, violations_count, violation_details, checked_ts.
- **Notes:** Implementation comes in later PRs; this is schema scaffolding.
