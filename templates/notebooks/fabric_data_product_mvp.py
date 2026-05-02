"""
Fabric Data Product MVP notebook starter.

Run this in Microsoft Fabric *after* attaching an Environment that already has
``fabric_data_product_framework`` installed from wheel.

Default settings are safe for sample-only execution and do not write to Fabric.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd

import fabric_data_product_framework as fdpf
from fabric_data_product_framework.governance import classify_columns
from fabric_data_product_framework.lineage import (
    build_lineage_records,
    build_transformation_summary_markdown,
    generate_mermaid_lineage,
)
from fabric_data_product_framework.profiling import profile_dataframe, summarize_profile
from fabric_data_product_framework.quality import run_quality_rules

# ==========================================================
# 0) Package and environment verification
# ==========================================================
print("fabric_data_product_framework version:", getattr(fdpf, "__version__", "unknown"))
print("fabric_data_product_framework module:", getattr(fdpf, "__file__", "unknown"))
print("Assumption: framework wheel is installed through your Fabric Environment.")

# ==========================================================
# 1) Runtime parameters (safe defaults)
# ==========================================================
DATASET_NAME = "orders"
RUN_ID = f"orders_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
ENVIRONMENT = "sandbox"
SOURCE_TABLE = "source_lakehouse.sales.orders"
TARGET_TABLE = "unified_lakehouse.curated.orders"
SOURCE_STAGE = "bronze"
TARGET_STAGE = "silver"
METADATA_TABLE = "metadata_profile"
DQ_RULE_TABLE = "metadata_dq_rules"
DQ_RESULT_TABLE = "metadata_dq_results"
GOVERNANCE_TABLE = "metadata_governance"
LINEAGE_TABLE = "metadata_lineage"
RUN_SUMMARY_TABLE = "metadata_run_summary"

USE_SAMPLE_DATA = True
ENABLE_FABRIC_WRITES = False
ENABLE_AI_ASSISTED_DQ = False
ENABLE_AI_ASSISTED_GOVERNANCE = False
ENABLE_AI_ASSISTED_LINEAGE = False

APPROVED_ORDER_STATUS = ["NEW", "PROCESSING", "COMPLETED", "CANCELLED"]


# ==========================================================
# 2) Source declaration
# ==========================================================
def load_source_dataframe() -> pd.DataFrame:
    if USE_SAMPLE_DATA:
        return pd.DataFrame(
            [
                {
                    "order_id": "ORD-1001",
                    "customer_id": "CUST-001",
                    "customer_email": "alice@example.com",
                    "order_amount": 120.50,
                    "order_status": "NEW",
                    "business_date": "2026-04-28",
                    "updated_at": "2026-04-28T08:00:00Z",
                },
                {
                    "order_id": "ORD-1002",
                    "customer_id": "CUST-002",
                    "customer_email": None,  # DQ issue: null email
                    "order_amount": 55.00,
                    "order_status": "PROCESSING",
                    "business_date": "2026-04-28",
                    "updated_at": "2026-04-28T08:05:00Z",
                },
                {
                    "order_id": "ORD-1003",
                    "customer_id": "CUST-003",
                    "customer_email": "chris@example.com",
                    "order_amount": -15.00,  # DQ issue: negative amount
                    "order_status": "COMPLETED",
                    "business_date": "2026-04-28",
                    "updated_at": "2026-04-28T08:10:00Z",
                },
                {
                    "order_id": "ORD-1003",  # DQ issue: duplicate order_id
                    "customer_id": "CUST-004",
                    "customer_email": "dee@example.com",
                    "order_amount": 88.00,
                    "order_status": "UNKNOWN",  # DQ issue: invalid status
                    "business_date": "2026-04-28",
                    "updated_at": "2026-04-28T08:20:00Z",
                },
            ]
        )

    # Replace this block with your Fabric/Spark read path when running real data.
    # Example (Fabric notebook):
    #   source_spark_df = spark.table(SOURCE_TABLE)
    #   return source_spark_df.toPandas()
    # or keep data in Spark and adapt downstream calls to Spark engine helpers.
    raise NotImplementedError(
        "USE_SAMPLE_DATA=False requires project-specific Fabric read logic (for example, spark.table(SOURCE_TABLE))."
    )



def write_metadata_artifact(table_name: str, artifact_name: str, payload: object) -> None:
    if ENABLE_FABRIC_WRITES:
        raise NotImplementedError(
            f"ENABLE_FABRIC_WRITES=True but no Fabric writer configured for {artifact_name} -> {table_name}."
        )
    print(f"[SAFE MODE] {artifact_name} preview only; no write to {table_name}.")
    print(str(payload)[:1200])


def write_target_dataframe(table_name: str, df: pd.DataFrame) -> None:
    if ENABLE_FABRIC_WRITES:
        raise NotImplementedError(
            f"ENABLE_FABRIC_WRITES=True but no Fabric target writer configured for {table_name}."
        )
    print(f"[SAFE MODE] Target preview only; no write to {table_name}. row_count={len(df)}")
    print(df.head(10))


source_df = load_source_dataframe()
print("Source rows:", len(source_df))

# ==========================================================
# 3) Source profiling
# ==========================================================
source_profile = profile_dataframe(source_df, dataset_name=DATASET_NAME, engine="pandas")
source_profile_summary = summarize_profile(source_profile)
print("Source profile summary:", json.dumps(source_profile_summary, indent=2, default=str))

write_metadata_artifact(METADATA_TABLE, "source_profile", source_profile)

# ==========================================================
# 4) AI-assisted DQ rule candidate generation
# AI suggests rules from profile + metadata + context.
# Human must approve thresholds and meaning before enforcement.
# ==========================================================
if ENABLE_AI_ASSISTED_DQ:
    print("[AI DQ] Use your AI assistant to draft candidate rules from profile/context, then paste reviewed rules here.")

# Deterministic fallback so this notebook always runs:
dq_rules = [
    {"rule_id": "order_id_required", "rule_type": "not_null", "column": "order_id", "severity": "critical"},
    {"rule_id": "order_id_unique", "rule_type": "unique", "column": "order_id", "severity": "critical"},
    {"rule_id": "customer_id_required", "rule_type": "not_null", "column": "customer_id", "severity": "critical"},
    {"rule_id": "customer_email_required", "rule_type": "not_null", "column": "customer_email", "severity": "warning"},
    {
        "rule_id": "order_status_valid",
        "rule_type": "accepted_values",
        "column": "order_status",
        "accepted_values": APPROVED_ORDER_STATUS,
        "severity": "critical",
    },
    {
        "rule_id": "order_amount_non_negative",
        "rule_type": "range_check",
        "column": "order_amount",
        "min_value": 0,
        "severity": "critical",
    },
    {"rule_id": "business_date_required", "rule_type": "not_null", "column": "business_date", "severity": "warning"},
]

# ==========================================================
# 5) Human approval checkpoint for DQ
# ==========================================================
APPROVED_DQ_RULES = dq_rules  # In production, functional + technical owners must review first.

# ==========================================================
# 6) DQ validation
# ==========================================================
dq_result = run_quality_rules(
    source_df,
    APPROVED_DQ_RULES,
    dataset_name=DATASET_NAME,
    table_name=SOURCE_TABLE,
    engine="pandas",
)
print("DQ status:", dq_result["status"])
print("DQ summary:", dq_result["summary"])
failed_rules = [r for r in dq_result["results"] if r.get("status") == "failed"]
print("Failed rule count:", len(failed_rules))
print("Failed rule preview:", json.dumps(failed_rules[:3], indent=2, default=str))

write_metadata_artifact(DQ_RULE_TABLE, "dq_rules", APPROVED_DQ_RULES)
write_metadata_artifact(DQ_RESULT_TABLE, "dq_result", dq_result)

# ==========================================================
# 7) Drift guard placeholders (explicit lifecycle behavior)
# - First approved run creates baseline snapshot.
# - Later runs compare current profile/schema/partition state against latest approved baseline.
# - Critical drift stops pipeline before target write.
# ==========================================================
drift_status = "warning_needs_baseline" if USE_SAMPLE_DATA else "pending_runtime_comparison"
critical_drift_detected = False
print("Drift status:", drift_status)

# ==========================================================
# 8) Transformation
# ==========================================================
working_df = source_df.copy()
working_df["order_status"] = working_df["order_status"].astype(str).str.upper()
working_df["business_date"] = pd.to_datetime(working_df["business_date"], errors="coerce").dt.date
working_df["updated_at"] = pd.to_datetime(working_df["updated_at"], errors="coerce", utc=True)

valid_df = working_df[
    working_df["order_id"].notna()
    & working_df["customer_id"].notna()
    & working_df["order_amount"].ge(0)
    & working_df["order_status"].isin(APPROVED_ORDER_STATUS)
].drop_duplicates(subset=["order_id"], keep="first")

valid_df["order_value_band"] = pd.cut(
    valid_df["order_amount"],
    bins=[-0.01, 50, 100, 10_000_000],
    labels=["LOW", "MEDIUM", "HIGH"],
)

# ==========================================================
# 9) Technical columns / run metadata
# ==========================================================
valid_df["_pipeline_run_id"] = RUN_ID
valid_df["_pipeline_environment"] = ENVIRONMENT
valid_df["_record_loaded_timestamp"] = datetime.now(timezone.utc)

# ==========================================================
# 10) Output profiling
# ==========================================================
output_profile = profile_dataframe(valid_df, dataset_name=f"{DATASET_NAME}_output", engine="pandas")
output_profile_summary = summarize_profile(output_profile)
print("Output rows:", len(valid_df))
print("Output profile summary:", output_profile_summary)

# ==========================================================
# 11) Governance classification (AI visible, human approval explicit)
# ==========================================================
columns_profile = [{"column_name": c, "data_type": str(valid_df[c].dtype)} for c in valid_df.columns]
governance_suggestions = classify_columns(
    profile={"columns": columns_profile},
    business_context={"approved_usage": "analytics", "dataset_name": DATASET_NAME},
)
print("Governance suggestions preview:", json.dumps(governance_suggestions[:5], indent=2, default=str))
if ENABLE_AI_ASSISTED_GOVERNANCE:
    print("[AI GOV] AI may suggest labels; human governance owner must approve final labels.")

GOVERNANCE_APPROVED = False  # Set to True only after human governance review.

# ==========================================================
# 12) Lineage and transformation summary
# ==========================================================
lineage_steps = [
    {"step_id": "1", "step_name": "source_read", "input_name": SOURCE_TABLE, "output_name": "source_df", "transformation_type": "ingest"},
    {"step_id": "2", "step_name": "quality_validation", "input_name": "source_df", "output_name": "dq_result", "transformation_type": "quality_gate"},
    {"step_id": "3", "step_name": "business_transform", "input_name": "source_df", "output_name": "valid_df", "transformation_type": "transform"},
]
lineage_records = build_lineage_records(
    dataset_name=DATASET_NAME,
    run_id=RUN_ID,
    source_tables=[SOURCE_TABLE],
    target_table=TARGET_TABLE,
    transformation_steps=lineage_steps,
)
lineage_mermaid = generate_mermaid_lineage(source_tables=[SOURCE_TABLE], target_table=TARGET_TABLE, transformation_steps=lineage_steps)
lineage_summary_md = build_transformation_summary_markdown(
    {
        "dataset_name": DATASET_NAME,
        "run_id": RUN_ID,
        "source_tables": [SOURCE_TABLE],
        "target_table": TARGET_TABLE,
        "step_count": len(lineage_steps),
        "steps": lineage_steps,
        "columns_used": ["order_id", "customer_id", "customer_email", "order_amount", "order_status", "business_date", "updated_at"],
        "columns_created": ["order_value_band", "_pipeline_run_id", "_pipeline_environment", "_record_loaded_timestamp"],
    }
)
if ENABLE_AI_ASSISTED_LINEAGE:
    print("[AI LINEAGE] AI can scan notebook and propose lineage; approved lineage is what gets stored.")

LINEAGE_RECORDED = True
write_metadata_artifact(LINEAGE_TABLE, "lineage_records", lineage_records)

# ==========================================================
# 13) Target write (safe by default)
# ==========================================================
write_target_dataframe(TARGET_TABLE, valid_df)

# ==========================================================
# 14) Run summary and AI handoff export
# ==========================================================
number_of_dq_failures = sum(int(r.get("failed_count", 0)) for r in failed_rules)
release_readiness = (
    dq_result.get("can_continue", False)
    and not critical_drift_detected
    and GOVERNANCE_APPROVED
    and LINEAGE_RECORDED
)

run_summary = {
    "dataset_name": DATASET_NAME,
    "run_id": RUN_ID,
    "source_table": SOURCE_TABLE,
    "target_table": TARGET_TABLE,
    "source_row_count": int(len(source_df)),
    "output_row_count": int(len(valid_df)),
    "dq_status": dq_result.get("status"),
    "number_of_dq_failures": int(number_of_dq_failures),
    "drift_status": drift_status,
    "governance_review_status": "approved" if GOVERNANCE_APPROVED else "pending_human_review",
    "lineage_status": "recorded" if LINEAGE_RECORDED else "missing",
    "release_readiness": "ready" if release_readiness else "not_ready",
}

ai_handoff_context = {
    "business_context": {
        "dataset_name": DATASET_NAME,
        "source_stage": SOURCE_STAGE,
        "target_stage": TARGET_STAGE,
        "environment": ENVIRONMENT,
    },
    "source_profile_summary": source_profile_summary,
    "approved_dq_rules": APPROVED_DQ_RULES,
    "dq_results_summary": dq_result.get("summary", {}),
    "drift_summary": {"status": drift_status, "critical_drift_detected": critical_drift_detected},
    "governance_classification_summary": governance_suggestions,
    "lineage_summary": {"lineage_records": lineage_records, "lineage_mermaid": lineage_mermaid, "summary_markdown": lineage_summary_md},
    "known_limitations": [
        "Sample mode uses in-notebook synthetic data.",
        "Governance approval is intentionally manual and currently set to False.",
    ],
}

print("RUN SUMMARY")
print(json.dumps(run_summary, indent=2, default=str))
print("AI HANDOFF CONTEXT")
print(json.dumps(ai_handoff_context, indent=2, default=str)[:6000])

write_metadata_artifact(RUN_SUMMARY_TABLE, "run_summary", run_summary)

# ==========================================================
# 15) Final release gate
# ==========================================================
dq_ok = dq_result.get("status") in {"passed", "warning"}
no_critical_drift = not critical_drift_detected
governance_reviewed = GOVERNANCE_APPROVED
lineage_recorded = LINEAGE_RECORDED
write_approved = ENABLE_FABRIC_WRITES and governance_reviewed and dq_ok and no_critical_drift and lineage_recorded

reasons = []
if not dq_ok:
    reasons.append("DQ gate failed")
if not no_critical_drift:
    reasons.append("critical drift detected")
if not governance_reviewed:
    reasons.append("governance not approved by human reviewer")
if not lineage_recorded:
    reasons.append("lineage not recorded")
if not ENABLE_FABRIC_WRITES:
    reasons.append("target write intentionally disabled (safe default)")

if write_approved:
    print("FINAL STATUS: READY_FOR_FABRIC_WRITE")
else:
    print("FINAL STATUS: NOT_READY")
    print("REASONS:", reasons)
