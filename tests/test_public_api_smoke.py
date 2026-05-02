import fabric_data_product_framework as fdpf


def test_public_api_smoke_imports():
    assert callable(fdpf.profile_dataframe)
    assert callable(fdpf.run_quality_rules)
    assert callable(fdpf.check_schema_drift)
    assert callable(fdpf.classify_columns)


def test_mvp_step_registry_and_artifact_validation():
    from fabric_data_product_framework.mvp_steps import get_mvp_step_registry, validate_mvp_artifacts

    steps = get_mvp_step_registry()
    assert steps[0]["step"] == "configure runtime"
    result = validate_mvp_artifacts({"runtime_context": {}, "source_profile": {}})
    assert result["passed"] is False
    assert "run_summary" in result["missing"]
