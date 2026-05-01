"""Fabric MVP notebook template aligned to the 13-step workflow.

Safe default is local DRY_RUN with synthetic pandas data.
Replace adapter functions when running in Fabric.
"""

from __future__ import annotations

import pandas as pd

from fabric_data_product_framework.governance_classifier import classify_columns
from fabric_data_product_framework.lineage import build_lineage_record
from fabric_data_product_framework.mvp_steps import get_mvp_step_registry, validate_mvp_artifacts
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.quality import run_quality_rules

DRY_RUN = True


def fabric_reader(table_name: str):
    """Fabric adapter placeholder (replace with spark.read.table in Fabric)."""
    raise NotImplementedError("Replace with Fabric table reader.")


# 1 Define data product
data_product_context = {
    "name": "sample_orders_product",
    "purpose": "Synthetic sample for MVP testing",
    "expected_grain": "order_id",
    "approved_usage": "analytics",
    "refresh_pattern": "daily",
}

# 2 Setup config and environment
runtime_config = {"environment": "dev", "dry_run": DRY_RUN}
mvp_registry = get_mvp_step_registry()

# 3 Declare source and ingest data
source_declaration = {"source_table": "sample_orders_source"}
if DRY_RUN:
    df_source = pd.DataFrame(
        [
            {"order_id": 1, "customer_email": "alice@example.com", "amount": 10.0},
            {"order_id": 2, "customer_email": "bob@example.com", "amount": 20.5},
        ]
    )
else:
    df_source = fabric_reader(source_declaration["source_table"])

# 4 Profile source and capture metadata
source_profile = profile_dataframe(df_source, dataset_name=data_product_context["name"], engine="auto")

# 5 Explore data
exploration_notes = "Checked nulls/shape in synthetic dry run."

# 6 Explain transformation logic
transformation_rationale = "Keep all rows and standardize amount precision for MVP smoke path."

# 7 Build transformation pipeline
df_output = df_source.copy()
df_output["amount"] = df_output["amount"].round(2)
output_table = df_output.to_dict(orient="records") if DRY_RUN else "written_in_fabric"

# 8 AI generate DQ rules (deterministic fallback for local run)
dq_candidate_rules = [
    {"rule_type": "not_null", "column": "order_id", "severity": "critical", "reason": "Primary key"},
    {"rule_type": "range_check", "column": "amount", "min_value": 0, "severity": "warning", "reason": "No negative amounts"},
]

# 9 Human review DQ rules
approved_dq_rules = [dict(r, review_status="approved") for r in dq_candidate_rules]
quality_rules = [{"rule_type": "not_null", "column": "order_id", "severity": "critical"}, {"rule_type": "range_check", "column": "amount", "min_value": 0, "severity": "warning"}]
dq_result = run_quality_rules(df_output, quality_rules, dataset_name=data_product_context["name"], table_name="sample_orders_product", engine="auto")

# 10 AI suggest sensitivity labels (local heuristic via governance classifier)
sensitivity_suggestions = classify_columns(
    profile={"columns": [{"column_name": c, "data_type": str(df_source[c].dtype)} for c in df_source.columns]},
    business_context={"approved_usage": data_product_context["approved_usage"]},
)

# 11 Human review and governance gate
approved_governance_labels = [dict(item, approved=True) for item in sensitivity_suggestions]

# 12 AI generated lineage and transformation summary
lineage_record = build_lineage_record(
    dataset_name=data_product_context["name"],
    run_id="dry_run",
    lineage_steps=[
        {"source": source_declaration["source_table"], "target": "sample_orders_product", "transformation": "round(amount, 2)", "reason": transformation_rationale, "source_type": "dataframe", "target_type": "dataframe", "confidence": "high"}
    ],
    notebook_name="mvp_template",
)

# Output profile for handover
output_profile = profile_dataframe(df_output, dataset_name=f"{data_product_context['name']}_output", engine="auto")

# 13 Handover framework pack
handover_pack = {
    "profile": {"source": source_profile, "output": output_profile},
    "dq": {"candidates": dq_candidate_rules, "approved": approved_dq_rules, "result": dq_result},
    "governance": {"suggestions": sensitivity_suggestions, "approved": approved_governance_labels},
    "lineage": lineage_record,
    "run_summary": {"status": "dry_run" if DRY_RUN else "completed", "mvp_steps": len(mvp_registry)},
    "caveats": ["Synthetic data only", "AI suggestions require human approval"],
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

print("MVP steps:", len(mvp_registry))
print("Validation:", validation)
