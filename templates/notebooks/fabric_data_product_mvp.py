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
from fabric_data_product_framework.mvp_steps import get_mvp_step_registry

# ==========================================================
# 1) Package and runtime setup [Framework]
# Verify package availability and lifecycle order.
# ==========================================================
print("framework version:", getattr(fdpf, "__version__", "unknown"))
print("framework module:", getattr(fdpf, "__file__", "unknown"))
for step in get_mvp_step_registry():
    print(f"{step['step_number']}. {step['step_name']} [{step['owner_type']}]")

# ==========================================================
# 2) Fabric config and paths [Human]
# User sets runtime parameters and Fabric source/target paths.
# ==========================================================
DATASET_NAME = "orders"
RUN_ID = f"orders_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
SOURCE_TABLE = "source_lakehouse.sales.orders"
TARGET_TABLE = "unified_lakehouse.curated.orders"
USE_SAMPLE_DATA = True
ENABLE_FABRIC_WRITES = False

# TODO: Replace with load_fabric_config(...) and get_path(...) in production notebooks.

# ==========================================================
# 3) Pull source data [Framework]
# Framework reads source. Sample mode keeps template runnable.
# ==========================================================
if USE_SAMPLE_DATA:
    source_df = pd.DataFrame(
        [
            {"order_id": "O1", "customer_id": "C1", "order_amount": 120.0, "order_status": "NEW", "updated_at": "2026-05-01T00:00:00Z"},
            {"order_id": "O2", "customer_id": "C2", "order_amount": -2.0, "order_status": "BAD", "updated_at": "2026-05-01T00:05:00Z"},
        ]
    )
else:
    raise NotImplementedError("TODO: implement Fabric source read (for example spark.table(SOURCE_TABLE)).")

# ==========================================================
# 4) Source profiling [Framework]
# ==========================================================
source_profile = profile_dataframe(source_df, dataset_name=DATASET_NAME, engine="pandas")
print("Source profile:", json.dumps(summarize_profile(source_profile), indent=2, default=str))

# ==========================================================
# 5) AI assisted DQ rule drafting [AI Assisted]
# AI drafts candidates; this template keeps a deterministic starter set.
# ==========================================================
draft_dq_rules = [
    {"rule_id": "order_id_required", "rule_type": "not_null", "column": "order_id", "severity": "critical"},
    {"rule_id": "order_amount_non_negative", "rule_type": "range_check", "column": "order_amount", "min_value": 0, "severity": "critical"},
]
# TODO: replace with ai_quality_rules helper when your project enables AI rule generation.

# ==========================================================
# 6) Human review of rules and metadata [Human]
# Human reviewer approves what will be enforced.
# ==========================================================
approved_dq_rules = draft_dq_rules
approved_metadata_notes = {"reviewer": "TODO", "notes": "TODO human review decision"}

# ==========================================================
# 7) Compile and run DQ checks [Framework]
# ==========================================================
dq_results = run_quality_rules(source_df, approved_dq_rules, dataset_name=DATASET_NAME, table_name=SOURCE_TABLE, engine="pandas")
print("DQ summary:", dq_results.get("summary"))
compiled_dq_rules = approved_dq_rules  # TODO: replace with explicit compile step if used in your project.

# ==========================================================
# 8) Schema/profile/data drift checks [Framework]
# ==========================================================
drift_results = {"status": "todo_baseline_required"}
# TODO: integrate drift.py/incremental.py checks after baseline design is finalized.

# ==========================================================
# 9) Core transformation [Mixed]
# Human owns logic; framework executes the notebook.
# ==========================================================
transformed_dataframe = source_df.copy()
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
output_profile = profile_dataframe(output_with_technical_columns, dataset_name=f"{DATASET_NAME}_output", engine="pandas")
target_write_result = {"status": "safe_mode_skipped"}

# ==========================================================
# 12) Governance classification and lineage [Mixed]
# AI/Framework can suggest, human approves.
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
    transformation_steps=[{"step_id": "1", "step_name": "transform", "input_name": "source_df", "output_name": "output_df", "transformation_type": "transform"}],
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

print("RUN SUMMARY")
print(json.dumps(run_summary, indent=2, default=str))
print("FINAL STATUS:", "READY_FOR_FABRIC_WRITE" if ENABLE_FABRIC_WRITES else "NOT_READY")
