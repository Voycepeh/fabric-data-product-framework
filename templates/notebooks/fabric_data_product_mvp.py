"""Fabric MVP notebook starter aligned to the 13-step workflow.

Copy-paste into a Fabric notebook, run in DRY_RUN mode first, then
replace the marked transformation and Fabric adapter sections.
"""

from __future__ import annotations

import pandas as pd

from fabric_data_product_framework.governance_classifier import classify_columns
from fabric_data_product_framework.lineage import build_lineage_record
from fabric_data_product_framework.mvp_steps import get_mvp_step_registry
from fabric_data_product_framework.mvp_steps import validate_mvp_artifacts
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.quality import run_quality_rules

# ==========================================================
# PARAMETER BLOCK (edit this block first)
# ==========================================================
DRY_RUN = True  # Safe default: prevents production writes.
ENVIRONMENT = "dev"
RUN_ID = "dry_run_001" if DRY_RUN else "fabric_run_001"
SOURCE_TABLE = "sample_orders_source"
TARGET_TABLE = "sample_orders_product"
NOTEBOOK_NAME = "fabric_data_product_mvp"
APPROVED_USAGE = "analytics"


# ==========================================================
# Fabric adapter placeholders (replace when moving to Fabric IO)
# ==========================================================
def fabric_reader(table_name: str):
    """Fabric adapter placeholder (replace with spark.read.table in Fabric)."""
    raise NotImplementedError("Replace with Fabric table reader.")


def fabric_writer(df: pd.DataFrame, table_name: str) -> str:
    """Fabric adapter placeholder (replace with Fabric write implementation)."""
    raise NotImplementedError("Replace with Fabric table writer.")


# 1 Define data product
data_product_context = {
    "name": TARGET_TABLE,
    "purpose": "Synthetic sample for MVP testing",
    "expected_grain": "order_id",
    "approved_usage": APPROVED_USAGE,
    "refresh_pattern": "daily",
}

# 2 Setup config and environment
runtime_config = {
    "environment": ENVIRONMENT,
    "dry_run": DRY_RUN,
    "run_id": RUN_ID,
}
mvp_registry = get_mvp_step_registry()

# 3 Declare source and ingest data
source_declaration = {"source_table": SOURCE_TABLE}
if DRY_RUN:
    # Local/Fabric-safe sample branch: no external dependencies, no writes.
    df_source = pd.DataFrame(
        [
            {
                "order_id": 1,
                "customer_email": "alice@example.com",
                "amount": 10.0,
            },
            {
                "order_id": 2,
                "customer_email": "bob@example.com",
                "amount": 20.5,
            },
        ]
    )
else:
    # Fabric branch: replace adapter with production-safe source read.
    df_source = fabric_reader(source_declaration["source_table"])

# 4 Profile source and capture metadata
source_profile = profile_dataframe(
    df_source,
    dataset_name=data_product_context["name"],
    engine="auto",
)

# 5 Explore data
exploration_notes = "Checked nulls, schema, and row counts in dry run before Fabric write path."

# 6 Explain transformation logic
transformation_rationale = "Standardize amount precision and preserve all rows for MVP smoke path."

# 7 Build transformation pipeline
# ------------------------------------------------------------------
# REPLACE THIS TRANSFORMATION SECTION WITH DOMAIN-SPECIFIC LOGIC.
# Keep output schema and business grain explicit before production runs.
# ------------------------------------------------------------------
df_output = df_source.copy()
df_output["amount"] = df_output["amount"].round(2)

if DRY_RUN:
    output_table = df_output.to_dict(orient="records")
else:
    output_table = fabric_writer(df_output, TARGET_TABLE)

# 8 AI generate DQ rules
# Copilot prompt (use as-is, then review output):
# "Given columns {columns} and business grain {expected_grain}, generate 5-8
# deterministic data quality rules with severity and rationale. Include at
# least one not_null, uniqueness, and numeric range rule. Return JSON list."
dq_candidate_rules = [
    {
        "rule_type": "not_null",
        "column": "order_id",
        "severity": "critical",
        "reason": "Primary key",
    },
    {
        "rule_type": "range_check",
        "column": "amount",
        "min_value": 0,
        "severity": "warning",
        "reason": "No negative amounts",
    },
]

# 9 Human review DQ rules
approved_dq_rules = [dict(rule, review_status="approved") for rule in dq_candidate_rules]
quality_rules = [
    {
        "rule_type": "not_null",
        "column": "order_id",
        "severity": "critical",
    },
    {
        "rule_type": "range_check",
        "column": "amount",
        "min_value": 0,
        "severity": "warning",
    },
]
dq_result = run_quality_rules(
    df_output,
    quality_rules,
    dataset_name=data_product_context["name"],
    table_name=TARGET_TABLE,
    engine="auto",
)

# 10 AI suggest sensitivity labels
# Copilot prompt (use as-is, then review output):
# "Classify each column by sensitivity (public/internal/confidential/restricted)
# using approved usage '{approved_usage}'. Return JSON with column, label,
# rationale, and confidence."
columns_profile = [
    {
        "column_name": column,
        "data_type": str(df_source[column].dtype),
    }
    for column in df_source.columns
]
sensitivity_suggestions = classify_columns(
    profile={"columns": columns_profile},
    business_context={"approved_usage": data_product_context["approved_usage"]},
)

# 11 Human review and governance gate
approved_governance_labels = [
    dict(suggestion, approved=True) for suggestion in sensitivity_suggestions
]

# 12 AI generated lineage and transformation summary
# Copilot prompt (use as-is, then review output):
# "Summarize lineage from source '{source_table}' to target '{target_table}',
# include transformation intent, key fields changed, and confidence level.
# Return JSON object aligned to framework lineage schema."
lineage_record = build_lineage_record(
    dataset_name=data_product_context["name"],
    run_id=RUN_ID,
    lineage_steps=[
        {
            "source": SOURCE_TABLE,
            "target": TARGET_TABLE,
            "transformation": "round(amount, 2)",
            "reason": transformation_rationale,
            "source_type": "dataframe",
            "target_type": "dataframe",
            "confidence": "high",
        }
    ],
    notebook_name=NOTEBOOK_NAME,
)

# Output profile for handover
output_profile = profile_dataframe(
    df_output,
    dataset_name=f"{data_product_context['name']}_output",
    engine="auto",
)

# 13 Handover framework pack
# Copilot prompt (use as-is, then review output):
# "Draft a handover summary with: run status, key assumptions, unresolved risks,
# and next actions for productionization. Keep it concise and checklist-ready."
handover_pack = {
    "profile": {
        "source": source_profile,
        "output": output_profile,
    },
    "dq": {
        "candidates": dq_candidate_rules,
        "approved": approved_dq_rules,
        "result": dq_result,
    },
    "governance": {
        "suggestions": sensitivity_suggestions,
        "approved": approved_governance_labels,
    },
    "lineage": lineage_record,
    "run_summary": {
        "status": "dry_run" if DRY_RUN else "completed",
        "mvp_steps": len(mvp_registry),
    },
    "caveats": [
        "Synthetic data only when DRY_RUN=True",
        "AI suggestions require human approval",
    ],
}

artifacts = {
    "data_product_context": data_product_context,
    "runtime_config": runtime_config,
    "source_declaration": source_declaration,
    "source_profile": source_profile,
    "exploration_notes": exploration_notes,
    "transformation_rationale": transformation_rationale,
    "output_table": output_table,
    "dq_candidate_rules": dq_candidate_rules,
    "approved_dq_rules": approved_dq_rules,
    "sensitivity_suggestions": sensitivity_suggestions,
    "approved_governance_labels": approved_governance_labels,
    "lineage_record": lineage_record,
    "handover_pack": handover_pack,
}

validation = validate_mvp_artifacts(artifacts)
if not validation["valid"]:
    raise ValueError(f"MVP artifact validation failed: {validation}")

# ==========================================================
# FINAL RUN SUMMARY CELL
# ==========================================================
print("Run ID:", RUN_ID)
print("MVP steps:", len(mvp_registry))
print("Validation:", validation)
print("Mode:", "DRY_RUN (no production write)" if DRY_RUN else "FABRIC_WRITE")
print("Output target:", TARGET_TABLE)

# ==========================================================
# HUMAN FILLS THIS IN vs FRAMEWORK GENERATES THIS
# ==========================================================
# Human fills this in:
# - data_product_context.purpose, expected_grain, approved_usage
# - source_declaration and Fabric adapters
# - transformation logic section
# - DQ/governance approvals
#
# Framework generates this:
# - profiling outputs
# - DQ execution result
# - governance suggestions (pre-review)
# - lineage record and validation checks
