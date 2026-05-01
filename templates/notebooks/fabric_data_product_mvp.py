"""Fabric MVP notebook template aligned to 13-step workflow."""

DRY_RUN = True

# 1 Define data product
DATA_PRODUCT_CONTEXT = {
    "name": "sample_orders_product",
    "purpose": "Synthetic MVP demo",
    "approved_usage": "Demo and framework validation",
    "expected_grain": "one row per order",
}

# 2 Setup config and environment
RUNTIME_CONFIG = {"workspace": "WORKSPACE_ID", "source_lakehouse": "SOURCE_LAKEHOUSE", "product_lakehouse": "PRODUCT_LAKEHOUSE", "dry_run": DRY_RUN}

# 3 Declare source and ingest data
SOURCE_DECLARATION = {"source_table": "sample_orders_source", "refresh_pattern": "daily"}
SOURCE_ROWS = [{"order_id": 1, "amount": 100.0, "country": "SG"}, {"order_id": 2, "amount": 50.0, "country": "US"}]

# 4 Profile source and capture metadata
SOURCE_PROFILE = {"row_count": len(SOURCE_ROWS), "columns": ["order_id", "amount", "country"]}

# 5 Explore data
EXPLORATION_NOTES = "TODO: review nulls/outliers and capture assumptions"

# 6 Explain transformation logic
TRANSFORMATION_RATIONALE = "Normalize country codes and keep positive amounts only."

# 7 Build transformation pipeline
OUTPUT_TABLE = [row for row in SOURCE_ROWS if row["amount"] > 0]

# 8 AI generate DQ rules
DQ_CANDIDATE_RULES = [{"rule": "amount_non_negative", "reason": "monetary amount should be >= 0", "severity": "high"}] if DRY_RUN else []

# 9 Human review DQ rules
APPROVED_DQ_RULES = [{**DQ_CANDIDATE_RULES[0], "review_status": "approved"}] if DQ_CANDIDATE_RULES else []

# 10 AI suggest sensitivity labels
SENSITIVITY_SUGGESTIONS = [{"column": "country", "suggested_label": "public"}] if DRY_RUN else []

# 11 Human review and governance gate
APPROVED_GOVERNANCE_LABELS = [{"column": "country", "approved_label": "public", "gate_status": "approved"}]

# 12 AI generated lineage and transformation summary
LINEAGE_RECORD = {"from": SOURCE_DECLARATION["source_table"], "to": "sample_orders_product", "summary": TRANSFORMATION_RATIONALE}

# 13 Handover framework pack
HANDOVER_PACK = {
    "profile": SOURCE_PROFILE,
    "dq": APPROVED_DQ_RULES,
    "governance": APPROVED_GOVERNANCE_LABELS,
    "lineage": LINEAGE_RECORD,
    "run_summary": {"status": "completed", "dry_run": DRY_RUN},
    "caveats": ["Synthetic data only"],
}

print("MVP handover pack ready", HANDOVER_PACK)
