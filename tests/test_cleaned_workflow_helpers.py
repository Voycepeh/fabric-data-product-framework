from fabricops_kit.business_context import (
    _parse_ai_dict_response,
    capture_column_business_context,
    prepare_business_context_profile_input,
)
from fabricops_kit.config import ReviewWorkflowConfig
from fabricops_kit.data_governance import prepare_governance_profile_input
from fabricops_kit.data_quality import attach_rule_metadata_keys, build_dq_review_rows, prepare_dq_profile_input, validate_dq_rules
from fabricops_kit.metadata import build_dq_rule_key, build_metadata_column_key, build_metadata_table_key


def test_deterministic_keys():
    assert build_metadata_table_key("dev", "sales", "orders") == build_metadata_table_key("dev", "sales", "orders")
    assert build_metadata_column_key("dev", "sales", "orders", "id")
    assert build_dq_rule_key("dev", "sales", "orders", "id_not_null")


def test_business_context_profile_and_parse():
    rows = prepare_business_context_profile_input([{"COLUMN_NAME": "id", "DATA_TYPE": "string", "OBSERVED_VALUES_SAMPLE": "1,2"}], "orders", "customer orders")
    assert rows[0]["column_name"] == "id"
    parsed = _parse_ai_dict_response("BUSINESS_CONTEXT = {'column_name': 'id', 'business_context': 'order identifier'}")
    assert parsed["column_name"] == "id"


def test_business_context_review_row_shape():
    rows = capture_column_business_context([
        {"column_name": "id", "business_context": "order id", "notes": "pk"}
    ], "dev", "sales", "orders")
    assert rows[0]["metadata_column_key"]
    assert rows[0]["approved_business_context"] == "order id"


def test_dq_prompt_input_uses_approved_context_and_keys():
    profile_rows = [{"column_name": "id", "data_type": "string"}, {"column_name": "status", "data_type": "string"}]
    contexts = [{"column_name": "id", "approved_business_context": "Order identifier"}]
    prepared = prepare_dq_profile_input(profile_rows, "orders", contexts)
    assert len(prepared) == 1 and prepared[0]["column_name"] == "id"
    keyed = attach_rule_metadata_keys([
        {"rule_id": "id_not_null", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "required"}
    ], "dev", "sales", "orders")
    assert keyed[0]["rule_key"]


def test_dq_value_range_uses_bounds():
    validate_dq_rules([
        {"rule_id": "amount_range", "rule_type": "value_range", "columns": ["amount"], "severity": "warning", "description": "range", "lower_bound": 0}
    ])


def test_governance_prompt_input_uses_approved_context():
    profile = [{"column_name": "email", "data_type": "string"}]
    contexts = [{"column_name": "email", "approved_business_context": "Customer contact email"}]
    prepared = prepare_governance_profile_input(profile, "orders", contexts)
    assert prepared[0]["approved_business_context"] == "Customer contact email"


def test_review_workflow_config_defaults_updated():
    cfg = ReviewWorkflowConfig()
    assert cfg.profile_table
    assert cfg.business_context_review_table


def test_dq_review_default_status():
    rows = build_dq_review_rows([
        {"rule_id": "id_not_null", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "required"}
    ], default_approval_status="queued")
    assert rows[0]["approval_status"] == "queued"
