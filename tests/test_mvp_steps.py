from fabric_data_product_framework.mvp_steps import (
    get_mvp_step_names,
    get_mvp_step_registry,
    validate_mvp_artifacts,
)


def test_registry_has_exactly_13_steps():
    registry = get_mvp_step_registry()
    assert len(registry) == 13


def test_step_numbers_are_1_to_13():
    registry = get_mvp_step_registry()
    assert [s["step_number"] for s in registry] == list(range(1, 14))


def test_each_step_has_required_fields():
    registry = get_mvp_step_registry()
    for step in registry:
        assert step.get("owner_type")
        assert isinstance(step.get("canonical_modules"), list)
        assert isinstance(step.get("expected_artifacts"), list)
        assert step.get("description")


def test_get_mvp_step_names_ordered():
    names = get_mvp_step_names()
    assert len(names) == 13
    assert names[0] == "Package and runtime setup"
    assert names[-1] == "Run summary and handover package"


def test_validate_mvp_artifacts_reports_missing():
    result = validate_mvp_artifacts({"runtime_context": {}})
    assert result["valid"] is False
    assert "source_dataframe" in result["missing_artifacts"]
    assert "runtime_context" in result["available_artifacts"]
