"""MVP Fabric notebook template (Python script form).

Copy into a Fabric notebook and wire the adapter functions below.
"""

# 1. Imports
from fabric_data_product_framework.config import load_and_validate_dataset_contract
from fabric_data_product_framework.contracts import assert_contracts_valid, build_contract_validation_records, validate_runtime_contracts
from fabric_data_product_framework.drift import (
    assert_no_blocking_schema_drift,
    build_schema_snapshot,
    compare_schema_snapshots,
)
from fabric_data_product_framework.fabric import build_table_identifier, read_table, write_table
from fabric_data_product_framework.incremental import assert_incremental_safe, build_partition_snapshot, compare_partition_snapshots
from fabric_data_product_framework.lineage import LineageRecorder, build_lineage_records, build_transformation_summary_markdown
from fabric_data_product_framework.metadata import (
    build_dataset_run_record,
    build_schema_drift_records,
    build_schema_snapshot_records,
    write_multiple_metadata_outputs,
)
from fabric_data_product_framework.profiling import (
    flatten_profile_for_metadata,
    profile_and_write_metadata,
    profile_dataframe,
)
from fabric_data_product_framework.quality import assert_quality_gate, build_quality_result_records, run_quality_rules
from fabric_data_product_framework.run_summary import build_run_summary, build_run_summary_record, render_run_summary_markdown
from fabric_data_product_framework.runtime import assert_notebook_name_valid, build_runtime_context
from fabric_data_product_framework.technical_columns import add_loaded_at, add_pipeline_run_id, default_technical_columns


# Adapter placeholders: replace with your Fabric patterns.
def fabric_reader(table_identifier):
    # Replace with spark.read.table(table_identifier) in Fabric.
    raise NotImplementedError("Wire this to your Fabric read pattern.")


def fabric_table_writer(df, table_identifier, mode="append", **options):
    # Replace with df.write.mode(mode).saveAsTable(table_identifier) in Fabric.
    raise NotImplementedError("Wire this to your Fabric table write pattern.")


def metadata_writer(records, table_identifier, mode="append", **options):
    # Replace with your metadata write pattern.
    raise NotImplementedError("Wire this to your metadata table write pattern.")


# 2. Notebook parameters
DATASET_CONTRACT_PATH = "REPLACE_WITH_CONTRACT_PATH"
NOTEBOOK_NAME = "source_to_product_synthetic_dataset"
WORKSPACE = "workspace_placeholder"
LAKEHOUSE = "lakehouse_placeholder"
SOURCE_TABLE = "source_table_placeholder"
TARGET_TABLE = "target_table_placeholder"
ENVIRONMENT = "dev"
DRY_RUN = False
PROFILE_ONLY = False

# 3. Load and validate dataset contract
contract, errors = load_and_validate_dataset_contract(DATASET_CONTRACT_PATH)
if errors:
    raise ValueError(f"Dataset contract is invalid: {errors}")

# 4. Build runtime context
ctx = build_runtime_context(
    dataset_name=contract.get("dataset_name", "synthetic_dataset"),
    environment=ENVIRONMENT,
    source_table=SOURCE_TABLE,
    target_table=TARGET_TABLE,
    notebook_name=NOTEBOOK_NAME,
)

# 5. Validate notebook naming
assert_notebook_name_valid(ctx["notebook_name"], ["source_to_product_", "bronze_to_silver_", "silver_to_gold_"])

# 6. Declare source and target table identifiers
source_table_identifier = build_table_identifier(WORKSPACE, LAKEHOUSE, ctx["source_table"])
target_table_identifier = build_table_identifier(WORKSPACE, LAKEHOUSE, ctx["target_table"])

# 7. Read source
df_source = read_table(source_table_identifier, reader=fabric_reader)

# 8. Source schema snapshot
source_snapshot = build_schema_snapshot(df_source, dataset_name=ctx["dataset_name"], table_name=source_table_identifier)

# 9. Source profiling
source_profile = profile_dataframe(df_source, dataset_name=ctx["dataset_name"], engine="auto")
source_profile_rows = flatten_profile_for_metadata(
    source_profile,
    table_name=source_table_identifier,
    run_id=ctx["run_id"],
    table_stage="source",
    exclude_columns=default_technical_columns(),
)
# Optional one-call Fabric helper:
# profile_and_write_metadata(
#     spark=spark,
#     df=df_source,
#     dataset_name=ctx["dataset_name"],
#     table_name=source_table_identifier,
#     metadata_table="fw_metadata.source_profile_records",
#     run_id=ctx["run_id"],
#     table_stage="source",
#     mode="append",
# )

# 10. Optional schema drift comparison
# Replace baseline snapshot retrieval with your own metadata table read.
baseline_snapshot = None
schema_drift_result = None
if baseline_snapshot:
    schema_drift_result = compare_schema_snapshots(baseline_snapshot, source_snapshot)
    assert_no_blocking_schema_drift(schema_drift_result)

# 11. Optional incremental safety check
# previous_partition_snapshots = ...  # Load from metadata table
# current_partition_snapshots = build_partition_snapshot(
#     df_source,
#     dataset_name=ctx["dataset_name"],
#     table_name=source_table_identifier,
#     partition_column="business_date",
#     business_keys=["customer_id", "order_id"],
#     watermark_column="updated_at",
#     run_id=ctx["run_id"],
#     engine="auto",
# )
# incremental_result = compare_partition_snapshots(previous_partition_snapshots, current_partition_snapshots)
# assert_incremental_safe(incremental_result)

# 11. EDA notes placeholder
# Keep EDA/debug cells in development only. Freeze or remove them before scheduled runs.

# 12. Initialize optional lineage recorder
lineage = LineageRecorder(
    dataset_name=ctx["dataset_name"],
    run_id=ctx["run_id"],
    source_tables=[source_table_identifier],
    target_table=target_table_identifier,
)

# 13. Transformation section
# USER TRANSFORMATION START
df_output = df_source
# Optional lineage example:
# lineage.add_step(
#     step_id="T001",
#     step_name="Apply business filter",
#     input_name="df_source",
#     output_name="df_output",
#     description="Filter to records needed for reporting.",
#     reason="The product table should only contain approved reporting records.",
#     transformation_type="filter",
# )
# USER TRANSFORMATION END

if PROFILE_ONLY:
    df_output = df_source

# 14. Add technical columns
df_output = add_pipeline_run_id(df_output, ctx["run_id"], engine="auto")
df_output = add_loaded_at(df_output, engine="auto")

# 15. Run data quality rules before publish
quality_result = run_quality_rules(
    df_output,
    contract.get("quality_rules", []),
    dataset_name=ctx["dataset_name"],
    table_name=target_table_identifier,
    engine="auto",
)
quality_records = build_quality_result_records(quality_result, run_id=ctx["run_id"])

# Optional failure metadata pattern:
# If the quality gate fails, you can persist `quality_records` and a failed
# dataset run row before re-raising DataQualityError.
# try:
#     assert_quality_gate(quality_result)
# except Exception:
#     failed_dataset_run_row = build_dataset_run_record(
#         run_id=ctx["run_id"],
#         dataset_name=ctx["dataset_name"],
#         environment=ctx["environment"],
#         source_table=source_table_identifier,
#         target_table=target_table_identifier,
#         status="failed",
#         started_at_utc=ctx["started_at_utc"],
#         row_count_source=source_profile.get("row_count"),
#         row_count_output=None,
#         notes="Data quality gate failed before publish.",
#     )
#     write_multiple_metadata_outputs(...)
#     raise
assert_quality_gate(quality_result)



# 16. Runtime contract enforcement
contract_result = validate_runtime_contracts(
    source_df=df_source,
    output_df=df_output,
    contract=contract,
    engine="auto",
)
assert_contracts_valid(contract_result)
contract_validation_records = build_contract_validation_records(contract_result, run_id=ctx["run_id"])

# 17. Write target only after gate passes
if not DRY_RUN and not PROFILE_ONLY:
    write_table(df_output, target_table_identifier, writer=fabric_table_writer, mode="overwrite")

# 18. Read/profile output
if DRY_RUN:
    df_written = df_output
else:
    df_written = read_table(target_table_identifier, reader=fabric_reader)

output_profile = profile_dataframe(df_written, dataset_name=ctx["dataset_name"], engine="auto")
output_profile_rows = flatten_profile_for_metadata(
    output_profile,
    table_name=target_table_identifier,
    run_id=ctx["run_id"],
    table_stage="target",
    exclude_columns=default_technical_columns(),
)

# 19. Build metadata records
dataset_run_row = build_dataset_run_record(
    run_id=ctx["run_id"],
    dataset_name=ctx["dataset_name"],
    environment=ctx["environment"],
    source_table=source_table_identifier,
    target_table=target_table_identifier,
    status="completed",
    started_at_utc=ctx["started_at_utc"],
    row_count_source=source_profile.get("row_count"),
    row_count_output=output_profile.get("row_count"),
    notes="MVP notebook template run.",
)
schema_snapshot_rows = build_schema_snapshot_records(source_snapshot, run_id=ctx["run_id"], table_stage="source")
schema_drift_rows = build_schema_drift_records(
    schema_drift_result or {"dataset_name": ctx["dataset_name"], "table_name": source_table_identifier, "baseline_engine": source_snapshot.get("engine"), "current_engine": source_snapshot.get("engine"), "status": "passed", "can_continue": True, "changes": []},
    run_id=ctx["run_id"],
    table_stage="source",
)

# 20. Build final run summary

lineage_summary = lineage.build_summary()
lineage_summary_markdown = build_transformation_summary_markdown(lineage_summary)
print(lineage_summary_markdown)
lineage_records = build_lineage_records(
    dataset_name=ctx["dataset_name"],
    run_id=ctx["run_id"],
    source_tables=[source_table_identifier],
    target_table=target_table_identifier,
    transformation_steps=lineage.to_records(),
)

run_summary = build_run_summary(
    runtime_context=ctx,
    contract=contract,
    source_profile=source_profile,
    output_profile=output_profile,
    schema_drift_result=schema_drift_result,
    quality_result=quality_result,
    contract_validation_result=contract_result,
    lineage_summary=lineage_summary,
    notes=["MVP notebook template run."],
)
summary_markdown = render_run_summary_markdown(run_summary)
print(summary_markdown)
run_summary_record = build_run_summary_record(run_summary)

# 21. Write metadata records
metadata_outputs = {
    "dataset_runs": [dataset_run_row],
    "column_profiles": source_profile_rows + output_profile_rows,
    "schema_snapshots": schema_snapshot_rows,
    "schema_drift_results": schema_drift_rows,
    "quality_results": quality_records,
    "contract_validation_results": contract_validation_records,
    "lineage": lineage_records,
    "run_summaries": [run_summary_record],
}
metadata_table_mapping = {
    "dataset_runs": "metadata.dataset_runs",
    "column_profiles": "metadata.column_profiles",
    "schema_snapshots": "metadata.schema_snapshots",
    "schema_drift_results": "metadata.schema_drift_results",
    "quality_results": "metadata.quality_results",
    "contract_validation_results": "metadata.contract_validation_results",
    "lineage": "metadata.lineage",
    "run_summaries": "metadata.run_summaries",
}
if not DRY_RUN:
    write_multiple_metadata_outputs(
        outputs=metadata_outputs,
        table_mapping=metadata_table_mapping,
        writer=metadata_writer,
        mode="append",
    )
