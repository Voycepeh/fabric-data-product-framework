import json

from fabricops_kit.config import ReviewWorkflowConfig
from fabricops_kit.data_governance import (
    build_approved_governance_records,
    build_governance_prompt_context,
    build_governance_review_rows,
)
from fabricops_kit.data_quality import approved_dq_rules_from_review_rows, build_dq_review_rows


def test_build_governance_prompt_context():
    ctx = build_governance_prompt_context("ops", "reporting", "orders")
    assert ctx["business_context"] == "ops"
    assert ctx["approved_usage"] == "reporting"


def test_build_governance_review_and_approved_records():
    rows = build_governance_review_rows([
        {"column_name": "email", "suggested_classification": "contact", "reason": "looks like email", "confidence": 0.9, "evidence": {"matched_terms": ["email"]}}
    ])
    rows[0]["approval_status"] = "approved"
    rows[0]["approved_label"] = "restricted"
    approved = build_approved_governance_records(rows, dataset_name="sales", table_name="customers", run_id="r1")
    assert approved[0]["approved_classification"] == "restricted"
    assert approved[0]["status"] == "approved"
    source = json.loads(approved[0]["source_suggestion_json"])
    assert source["suggested_classification"] == "contact"


def test_build_dq_review_and_approved_rules():
    rules = [{"rule_id": "id_not_null", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "id required"}]
    rows = build_dq_review_rows(rules)
    rows[0]["approval_status"] = "approved"
    out = approved_dq_rules_from_review_rows(rows)
    assert out[0]["rule_id"] == "id_not_null"


def test_default_approval_status_flows_to_review_rows():
    dq_rows = build_dq_review_rows(
        [{"rule_id": "id_not_null", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "id required"}],
        default_approval_status="needs_review",
    )
    assert dq_rows[0]["approval_status"] == "needs_review"

    gov_rows = build_governance_review_rows(
        [{"column_name": "email", "suggested_classification": "contact", "reason": "looks like email"}],
        default_approval_status="needs_review",
    )
    assert gov_rows[0]["approval_status"] == "needs_review"


def test_review_workflow_config_defaults():
    cfg = ReviewWorkflowConfig()
    assert cfg.default_approval_status == "pending"
    assert cfg.governance_approved_table
