from pathlib import Path

from examples.mvp_fabric_smoke_test import build_smoke_artifacts
from fabric_data_product_framework.template_generator import MVP_STEPS, validate_mvp_artifacts


def test_mvp_steps_ordered_1_to_13():
    assert [s["step_id"] for s in MVP_STEPS] == list(range(1, 14))


def test_capability_status_references_all_mvp_steps():
    text = Path("docs/capability-status.md").read_text(encoding="utf-8")
    for i in range(1, 14):
        assert f"| {i}." in text


def test_incomplete_handover_pack_fails_validation():
    artifacts = build_smoke_artifacts()
    artifacts["handover_pack"] = {"status": "ready"}
    result = validate_mvp_artifacts(artifacts)
    assert result["valid"] is False
    assert "profile" in result["missing_handover_pack_keys"]


def test_missing_handover_nested_keys_fails_validation():
    artifacts = build_smoke_artifacts()
    del artifacts["handover_pack"]["lineage"]
    result = validate_mvp_artifacts(artifacts)
    assert result["valid"] is False
    assert "lineage" in result["missing_handover_pack_keys"]


def test_invalid_approved_dq_rule_type_fails_validation():
    artifacts = build_smoke_artifacts()
    artifacts["approved_dq_rules"] = {"rule_type": "not_null"}
    result = validate_mvp_artifacts(artifacts)
    assert result["valid"] is False
    assert any(x["field"] == "approved_dq_rules" for x in result["invalid_fields"])


def test_invalid_approved_governance_label_type_fails_validation():
    artifacts = build_smoke_artifacts()
    artifacts["approved_governance_labels"] = "approved"
    result = validate_mvp_artifacts(artifacts)
    assert result["valid"] is False
    assert any(x["field"] == "approved_governance_labels" for x in result["invalid_fields"])


def test_valid_full_mvp_artifact_set_passes_validation():
    artifacts = build_smoke_artifacts()
    result = validate_mvp_artifacts(artifacts)
    assert result["valid"] is True


def test_example_smoke_artifacts_pass_validation():
    artifacts = build_smoke_artifacts()
    result = validate_mvp_artifacts(artifacts)
    assert result["valid"] is True
