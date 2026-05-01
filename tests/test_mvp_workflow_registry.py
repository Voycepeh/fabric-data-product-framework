from fabric_data_product_framework.mvp_steps import MVP_STEPS, get_mvp_step_registry, validate_mvp_artifacts


def test_mvp_steps_are_ordered_1_to_13():
    assert [s["step_id"] for s in MVP_STEPS] == list(range(1, 14))


def test_registry_has_actor_artifact_and_test_evidence():
    registry = get_mvp_step_registry()
    assert len(registry) == 13
    for step in registry:
        assert step["actor"]
        assert step["output_artifacts"]
        assert step["fabric_test_hint"]


def test_validate_mvp_artifacts_reports_missing():
    artifacts = {"data_product_context": {}}
    result = validate_mvp_artifacts(artifacts)
    assert result["is_valid"] is False
    assert "handover_pack" in result["missing_artifacts"]


def test_handover_pack_expectations_present():
    handover_step = [s for s in MVP_STEPS if s["step_id"] == 13][0]
    assert "handover_pack" in handover_step["output_artifacts"]
    assert "profile" in handover_step["fabric_test_hint"].lower()
    assert "dq" in handover_step["fabric_test_hint"].lower()
    assert "governance" in handover_step["fabric_test_hint"].lower()
    assert "lineage" in handover_step["fabric_test_hint"].lower()
    assert "run summary" in handover_step["fabric_test_hint"].lower()
