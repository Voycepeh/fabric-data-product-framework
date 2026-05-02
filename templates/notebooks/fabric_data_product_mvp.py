"""Canonical 13-step MVP notebook template for onboarding and smoke tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd

import fabric_data_product_framework as fdpf
from fabric_data_product_framework import (
    build_lineage_records,
    classify_columns,
    profile_dataframe,
    run_quality_rules,
    summarize_profile,
)
from fabric_data_product_framework.mvp_steps import get_mvp_step_registry, validate_mvp_artifacts

# ==========================================================
# 1) Package and runtime setup [Framework]
# ==========================================================
print("framework module:", getattr(fdpf, "__file__", "unknown"))
print("framework version:", getattr(fdpf, "__version__", "unknown"))

DATASET_NAME = "orders"
SOURCE_TABLE = "raw_orders"
TARGET_TABLE = "clean_orders"

runtime_context = fdpf.build_runtime_context(
    dataset_name=DATASET_NAME,
    environment="Sandbox",
    source_table=SOURCE_TABLE,
    target_table=TARGET_TABLE,
    notebook_name="dex_source_to_dex_unified_orders",
)
RUN_ID = runtime_context["run_id"]

for step in get_mvp_step_registry():
    print(f"{step['step_number']}. {step['step_name']} [{step['owner_type']}]")

# ==========================================================
# 2) Fabric config and paths [Human]
# ==========================================================
try:
    config = fdpf.load_fabric_config(CONFIG)
    lh_source = fdpf.get_path("Sandbox", "Source", config=config)
    lh_unified = fdpf.get_path("Sandbox", "Unified", config=config)
except FileNotFoundError:
    config = None
    lh_source = fdpf.get_path("Sandbox", "Source", config=config)
    lh_unified = fdpf.get_path("Sandbox", "Unified", config=config)

USE_SAMPLE_DATA = True
ENABLE_FABRIC_WRITES = False

fabric_config = {"environment": "Sandbox"}
path_context = {"source_path": lh_source.root, "target_path": lh_unified.root}

# ==========================================================
# 3) Pull source data [Framework]
# ==========================================================
if USE_SAMPLE_DATA:
    source_dataframe = pd.DataFrame(
        [
            {"order_id": "O-1001", "customer_id": "C-001", "order_amount": 125.0, "order_status": "NEW", "updated_at": "2026-05-01T00:00:00Z"},
            {"order_id": "O-1002", "customer_id": "C-002", "order_amount": -5.0, "order_status": "BAD", "updated_at": "2026-05-01T00:05:00Z"},
        ]
    )
else:
    df_source = fdpf.lakehouse_table_read(lh_source, SOURCE_TABLE)
    display(df_source.limit(10))
    # Keep pandas conversion bounded for the current pandas-based MVP smoke path.
    source_dataframe = df_source.limit(1000).toPandas()

# Optional warehouse source example:
# df_wh = fdpf.warehouse_read(
#     env="DE",
#     target="Warehouse",
#     schema="dbo",
#     table="SomeTable",
#     config=config,
# )
# display(df_wh.limit(10))

# ==========================================================
# 4) Source profiling [Framework]
# ==========================================================
source_profile = profile_dataframe(source_dataframe, dataset_name=DATASET_NAME, engine="pandas")
print("Source profile:", json.dumps(summarize_profile(source_profile), indent=2, default=str))

# ==========================================================
# 5) AI assisted DQ rule drafting [AI Assisted]
# ==========================================================
draft_dq_rules = [
    {"rule_id": "order_id_required", "rule_type": "not_null", "column": "order_id", "severity": "critical"},
    {"rule_id": "order_amount_non_negative", "rule_type": "range_check", "column": "order_amount", "min_value": 0, "severity": "critical"},
]

# ==========================================================
# 6) Human review of rules and metadata [Human]
# ==========================================================
approved_dq_rules = draft_dq_rules
approved_metadata_notes = {"reviewer": "sample_reviewer", "notes": "Approved for smoke-test execution."}

# ==========================================================
# 7) Compile and run DQ checks [Framework]
# ==========================================================
compiled_dq_rules = approved_dq_rules
dq_results = run_quality_rules(source_dataframe, compiled_dq_rules, dataset_name=DATASET_NAME, table_name=SOURCE_TABLE, engine="pandas")
print("DQ summary:", dq_results.get("summary"))

# ==========================================================
# 8) Schema/profile/data drift checks [Framework]
# ==========================================================
drift_results = {"status": "todo_baseline_required", "critical_drift_detected": False}

# ==========================================================
# 9) Core transformation [Mixed]
# ==========================================================
transformed_dataframe = source_dataframe.copy()
transformed_dataframe["order_status"] = transformed_dataframe["order_status"].astype(str).str.upper()

# ==========================================================
# 10) Standard technical columns [Framework]
# ==========================================================
output_with_technical_columns = transformed_dataframe.copy()
output_with_technical_columns["_pipeline_run_id"] = RUN_ID
output_with_technical_columns["_record_loaded_timestamp"] = datetime.now(timezone.utc)

# ==========================================================
# 11) Write output and profile output [Framework]
# ==========================================================
if ENABLE_FABRIC_WRITES:
    raise NotImplementedError("TODO: implement target write for Fabric runtime.")
print(f"[SAFE MODE] Skip write to {TARGET_TABLE}; rows={len(output_with_technical_columns)}")
target_write_result = {"status": "safe_mode_skipped", "row_count": int(len(output_with_technical_columns))}
output_profile = profile_dataframe(output_with_technical_columns, dataset_name=f"{DATASET_NAME}_output", engine="pandas")

# ==========================================================
# 12) Governance classification and lineage [Mixed]
# ==========================================================
governance_labels = classify_columns(
    profile={"columns": [{"column_name": c, "data_type": str(output_with_technical_columns[c].dtype)} for c in output_with_technical_columns.columns]},
    business_context={"dataset_name": DATASET_NAME},
)
lineage_records = build_lineage_records(
    dataset_name=DATASET_NAME,
    run_id=RUN_ID,
    source_tables=[SOURCE_TABLE],
    target_table=TARGET_TABLE,
    transformation_steps=[{"step_id": "1", "step_name": "transform", "input_name": "source_dataframe", "output_name": "output_with_technical_columns", "transformation_type": "transform"}],
)

# ==========================================================
# 13) Run summary and handover package [Framework]
# ==========================================================
run_summary = {
    "dataset_name": DATASET_NAME,
    "run_id": RUN_ID,
    "dq_status": dq_results.get("status"),
    "drift_status": drift_results.get("status"),
    "target_write_status": target_write_result.get("status"),
}
handover_package = {
    "source_profile": source_profile,
    "dq_results": dq_results,
    "output_profile": output_profile,
    "governance_labels": governance_labels,
    "lineage_records": lineage_records,
    "run_summary": run_summary,
}

artifacts = {
    "runtime_context": runtime_context,
    "fabric_config": fabric_config,
    "path_context": path_context,
    "source_dataframe": source_dataframe,
    "source_profile": source_profile,
    "draft_dq_rules": draft_dq_rules,
    "approved_dq_rules": approved_dq_rules,
    "approved_metadata_notes": approved_metadata_notes,
    "compiled_dq_rules": compiled_dq_rules,
    "dq_results": dq_results,
    "drift_results": drift_results,
    "transformed_dataframe": transformed_dataframe,
    "output_with_technical_columns": output_with_technical_columns,
    "target_write_result": target_write_result,
    "output_profile": output_profile,
    "governance_labels": governance_labels,
    "lineage_records": lineage_records,
    "run_summary": run_summary,
    "handover_package": handover_package,
}

artifact_validation_result = validate_mvp_artifacts(artifacts)
print("MVP ARTIFACT VALIDATION")
print(json.dumps(artifact_validation_result, indent=2, default=str))
print("RUN SUMMARY")
print(json.dumps(run_summary, indent=2, default=str))
print("FINAL STATUS:", "READY_FOR_FABRIC_WRITE" if ENABLE_FABRIC_WRITES else "NOT_READY")
