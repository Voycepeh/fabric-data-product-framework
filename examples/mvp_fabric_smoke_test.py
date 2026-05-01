"""Synthetic MVP smoke example for Fabric import."""

from fabric_data_product_framework.mvp_steps import get_mvp_step_registry, validate_mvp_artifacts

artifacts = {
    "data_product_context": {"name": "sample_orders_product"},
    "runtime_config": {"workspace": "WORKSPACE_ID", "dry_run": True},
    "source_declaration": {"source_table": "sample_orders_source"},
    "source_profile": {"row_count": 2},
    "exploration_notes": "Synthetic-only exploration complete",
    "transformation_rationale": "Keep positive amounts",
    "output_table": [{"order_id": 1, "amount": 10}],
    "dq_candidate_rules": [{"rule": "amount_non_negative"}],
    "approved_dq_rules": [{"rule": "amount_non_negative", "review_status": "approved"}],
    "sensitivity_suggestions": [{"column": "country", "suggested_label": "public"}],
    "approved_governance_labels": [{"column": "country", "approved_label": "public"}],
    "lineage_record": {"from": "sample_orders_source", "to": "sample_orders_product"},
    "handover_pack": {"status": "ready"},
}

print("MVP steps:", [s["name"] for s in get_mvp_step_registry()])
print("Artifact validation:", validate_mvp_artifacts(artifacts))
