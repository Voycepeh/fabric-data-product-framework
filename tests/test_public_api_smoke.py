import fabric_data_product_framework as fdpf


def test_public_api_smoke_imports():
    assert callable(fdpf.profile_dataframe)
    assert callable(fdpf.run_quality_rules)
    assert callable(fdpf.check_schema_drift)
    assert callable(fdpf.classify_columns)


def test_mvp_step_registry_and_artifact_validation():
    from fabric_data_product_framework.mvp_steps import get_mvp_step_registry, validate_mvp_artifacts

    steps = get_mvp_step_registry()
    assert steps[0]["step_number"] == 1
    assert steps[0]["step_name"] == "Package and runtime setup"
    result = validate_mvp_artifacts({"runtime_context": {}, "source_profile": {}})
    assert result["valid"] is False
    assert "run_summary" in result["missing_artifacts"]


def test_technical_columns_entrypoints_on_root_package():
    import fabric_data_product_framework as fw

    assert hasattr(fw, "add_audit_columns")
    assert hasattr(fw, "add_datetime_features")
    assert hasattr(fw, "add_hash_columns")
    assert hasattr(fw, "default_technical_columns")
