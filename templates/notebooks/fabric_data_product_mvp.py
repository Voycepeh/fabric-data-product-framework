"""Canonical 10-step lifecycle notebook template for onboarding and smoke tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd

import fabricops_kit as fdpf
from fabricops_kit import (
    build_lineage_records,
    classify_columns,
    profile_dataframe,
    run_quality_rules,
    summarize_profile,
    check_fabric_ai_functions_available,
    configure_fabric_ai_functions,
    generate_dq_rule_candidates_with_fabric_ai,
    generate_governance_candidates_with_fabric_ai,
    build_manual_dq_rule_prompt_package,
)
from fabricops_kit.mvp_steps import get_mvp_step_registry, validate_mvp_artifacts

# ==========================================================
# 1) Define purpose, approved usage & governance ownership [Governance]
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
    notebook_name="03_pc_orders_source_to_unified",
)
RUN_ID = runtime_context["run_id"]

for step in get_mvp_step_registry():
    print(f"{step['step_number']}. {step['step_name']} [{step['owner_type']}]")

# ==========================================================
# 2) Configure runtime, environment & path rules [Starter kit]
# ==========================================================
# In Fabric notebooks, run `%run 00_config` before this template.
config = fdpf.load_fabric_config(CONFIG)
lh_source = fdpf.get_path("Sandbox", "Source", config=config)
lh_unified = fdpf.get_path("Sandbox", "Unified", config=config)

USE_SAMPLE_DATA = True
ENABLE_FABRIC_WRITES = False

fabric_config = {"environment": "Sandbox"}
path_context = {"source_path": lh_source.root, "target_path": lh_unified.root}

# ==========================================================
# 3) Declare source contract & ingest source data [Starter kit]
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
# 4) Validate source against contract & capture metadata [Starter kit]
# ==========================================================
source_profile = profile_dataframe(source_dataframe, dataset_name=DATASET_NAME, engine="pandas")
print("Source profile:", json.dumps(summarize_profile(source_profile), indent=2, default=str))

# ==========================================================
# 4A) Optional AI assisted rule and governance generation [AI Assisted]
# ==========================================================
# Run this during development or review.
# AI suggestions are not enforcement.
# Approved deterministic rules are what scheduled pipelines should run.
ai_functions_status = check_fabric_ai_functions_available()
print("Fabric AI Functions status:", ai_functions_status)
if ai_functions_status.get("available"):
    configure_fabric_ai_functions(temperature=0.0)
    # Example profile metadata DataFrame should include column profile fields.
    # profile_spark_df = spark.table("fw_metadata.source_profile_records")
    # dq_ai_df = generate_dq_rule_candidates_with_fabric_ai(
    #     profile_spark_df,
    #     business_context="Orders pipeline quality review",
    #     dataset_name=DATASET_NAME,
    # )
    # dq_ai_df.write.mode("append").saveAsTable("AI_DQ_RULE_CANDIDATES")
    # gov_ai_df = generate_governance_candidates_with_fabric_ai(
    #     profile_spark_df,
    #     business_context="Orders governance classification review",
    # )
    # gov_ai_df.write.mode("append").saveAsTable("AI_GOVERNANCE_CANDIDATES")

else:
    # Paste this into Copilot or another LLM if Fabric AI Functions are unavailable.
    # Review the response before storing approved rules.
    manual_dq_prompt = build_manual_dq_rule_prompt_package(
        business_context="Orders pipeline quality review",
        dataset_name=DATASET_NAME,
    )
    print(manual_dq_prompt["prompt"])

# ==========================================================
# 5) Explore data & capture transformation / DQ rationale [Analyst / Data scientist notebook]
# ==========================================================
draft_dq_rules = [
    {"rule_id": "order_id_required", "rule_type": "not_null", "column": "order_id", "severity": "critical"},
    {"rule_id": "order_amount_non_negative", "rule_type": "range_check", "column": "order_amount", "min_value": 0, "severity": "critical"},
]

# ==========================================================
# 6) Build production transformation & write target output [Data engineer notebook]
# ==========================================================
approved_dq_rules = draft_dq_rules
approved_metadata_notes = {"reviewer": "sample_reviewer", "notes": "Approved for smoke-test execution."}

# ==========================================================
# 7) Validate output & persist target metadata [Starter kit]
# ==========================================================
compiled_dq_rules = approved_dq_rules
dq_results = run_quality_rules(source_dataframe, compiled_dq_rules, dataset_name=DATASET_NAME, table_name=SOURCE_TABLE, engine="pandas")
print("DQ summary:", dq_results.get("summary"))

# ==========================================================
# 8) Generate, review & configure DQ rules [AI-assisted + human review]
# ==========================================================
drift_results = {"status": "todo_baseline_required", "critical_drift_detected": False}

# ==========================================================
# 9) Generate & review classification / sensitivity suggestions [AI-assisted + human review]
# ==========================================================
transformed_dataframe = source_dataframe.copy()
transformed_dataframe["order_status"] = transformed_dataframe["order_status"].astype(str).str.upper()

# ==========================================================
# 10) Generate data lineage and handover documentation [AI-assisted handover document generation]
# ==========================================================
output_with_technical_columns = transformed_dataframe.copy()
output_with_technical_columns["_pipeline_run_id"] = RUN_ID
output_with_technical_columns["_record_loaded_timestamp"] = datetime.now(timezone.utc)

# ==========================================================
# Supporting execution block: safe write/profile behavior
# ==========================================================
if ENABLE_FABRIC_WRITES:
    raise NotImplementedError("TODO: implement target write for Fabric runtime.")
print(f"[SAFE MODE] Skip write to {TARGET_TABLE}; rows={len(output_with_technical_columns)}")
target_write_result = {"status": "safe_mode_skipped", "row_count": int(len(output_with_technical_columns))}
output_profile = profile_dataframe(output_with_technical_columns, dataset_name=f"{DATASET_NAME}_output", engine="pandas")

# ==========================================================
# Supporting execution block: governance and lineage helpers
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
# Supporting execution block: lifecycle summary payload
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
print("LIFECYCLE ARTIFACT VALIDATION")
print(json.dumps(artifact_validation_result, indent=2, default=str))
print("RUN SUMMARY")
print(json.dumps(run_summary, indent=2, default=str))
print("FINAL STATUS:", "READY_FOR_FABRIC_WRITE" if ENABLE_FABRIC_WRITES else "NOT_READY")
