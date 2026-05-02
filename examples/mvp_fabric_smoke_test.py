"""Synthetic MVP 13-step smoke example for local/Fabric-safe execution."""

from __future__ import annotations

import pandas as pd

from fabric_data_product_framework.governance import classify_columns
from fabric_data_product_framework.lineage import build_lineage_record
from fabric_data_product_framework.template_generator import get_mvp_step_registry, validate_mvp_artifacts
from fabric_data_product_framework.profiling import profile_dataframe


def build_smoke_artifacts() -> dict:
    data_product_context = {
        "name": "sample_orders_product",
        "purpose": "MVP smoke validation",
        "expected_grain": "order_id",
        "approved_usage": "analytics",
    }
    runtime_config = {"environment": "dev", "dry_run": True}
    source_declaration = {"source_table": "sample_orders_source"}

    source_df = pd.DataFrame([
        {"order_id": 1, "customer_email": "a@example.com", "amount": 12.0},
        {"order_id": 2, "customer_email": "b@example.com", "amount": 18.5},
    ])
    source_profile = profile_dataframe(source_df, dataset_name="sample_orders", engine="auto")
    exploration_notes = "Synthetic rows reviewed."
    transformation_rationale = "Round amount and keep all records."

    output_df = source_df.copy()
    output_df["amount"] = output_df["amount"].round(2)
    output_profile = profile_dataframe(output_df, dataset_name="sample_orders_output", engine="auto")

    dq_candidate_rules = [{"rule_type": "not_null", "column": "order_id", "reason": "key", "severity": "high"}]
    approved_dq_rules = [dict(dq_candidate_rules[0], review_status="approved")]

    sensitivity_suggestions = classify_columns(
        profile={"columns": [{"column_name": c, "data_type": str(source_df[c].dtype)} for c in source_df.columns]},
        business_context={"approved_usage": "analytics"},
    )
    approved_governance_labels = [dict(item, approved=True) for item in sensitivity_suggestions]

    lineage_record = build_lineage_record(
        dataset_name="sample_orders",
        run_id="smoke",
        lineage_steps=[
            {"source": source_declaration["source_table"], "target": "sample_orders_product", "transformation": "round(amount, 2)", "reason": transformation_rationale, "source_type": "dataframe", "target_type": "dataframe", "confidence": "high"}
        ],
        notebook_name="mvp_smoke",
    )

    handover_pack = {
        "profile": {"source": source_profile, "output": output_profile},
        "dq": {"candidates": dq_candidate_rules, "approved": approved_dq_rules},
        "governance": {"suggestions": sensitivity_suggestions, "approved": approved_governance_labels},
        "lineage": lineage_record,
        "run_summary": {"status": "completed", "steps": len(get_mvp_step_registry())},
        "caveats": ["Synthetic data only"],
    }

    return {
        "data_product_context": data_product_context,
        "runtime_config": runtime_config,
        "source_declaration": source_declaration,
        "source_profile": source_profile,
        "exploration_notes": exploration_notes,
        "transformation_rationale": transformation_rationale,
        "output_table": output_df.to_dict(orient="records"),
        "dq_candidate_rules": dq_candidate_rules,
        "approved_dq_rules": approved_dq_rules,
        "sensitivity_suggestions": sensitivity_suggestions,
        "approved_governance_labels": approved_governance_labels,
        "lineage_record": lineage_record,
        "handover_pack": handover_pack,
    }


if __name__ == "__main__":
    artifacts = build_smoke_artifacts()
    validation = validate_mvp_artifacts(artifacts)
    if not validation["valid"]:
        raise RuntimeError(f"Smoke artifacts failed MVP validation: {validation}")
    print("MVP artifact validation passed.")
