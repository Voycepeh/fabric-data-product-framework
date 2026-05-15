from importlib.resources import files
from pathlib import Path

import pytest

from fabricops_kit.config import (
    DatasetContractValidationError,
    assert_valid_dataset_contract,
    load_and_validate_dataset_contract,
    load_dataset_contract,
    validate_dataset_contract,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures"
VALID_FIXTURE = FIXTURES_DIR / "valid_dataset_contract.yaml"
MISSING_REQUIRED_FIXTURE = FIXTURES_DIR / "invalid_dataset_contract_missing_required.yaml"
BAD_POLICY_FIXTURE = FIXTURES_DIR / "invalid_dataset_contract_bad_policy.yaml"


def test_load_dataset_contract_loads_yaml_correctly() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)

    assert contract["dataset"]["name"] == "synthetic_customer_orders_product"
    assert contract["target"]["write_mode"] == "merge"


def test_valid_contract_returns_no_errors() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)

    errors = validate_dataset_contract(contract)

    assert errors == []


def test_missing_required_section_returns_errors() -> None:
    contract = load_dataset_contract(MISSING_REQUIRED_FIXTURE)

    errors = validate_dataset_contract(contract)

    assert errors
    assert any("source" in error and "required property" in error for error in errors)


def test_invalid_refresh_mode_returns_validation_error() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["refresh"]["mode"] = "daily_incremental"

    errors = validate_dataset_contract(contract)

    assert any("refresh.mode" in error and "not one of" in error for error in errors)


def test_invalid_write_mode_returns_validation_error() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["target"]["write_mode"] = "upsert"

    errors = validate_dataset_contract(contract)

    assert any("target.write_mode" in error and "not one of" in error for error in errors)


def test_invalid_policy_fixture_returns_readable_errors() -> None:
    contract = load_dataset_contract(BAD_POLICY_FIXTURE)

    errors = validate_dataset_contract(contract)

    assert errors
    assert any(
        "policies.incremental_safety.closed_partition_grace_days" in error for error in errors
    )


def test_load_and_validate_dataset_contract_returns_contract_and_errors() -> None:
    contract, errors = load_and_validate_dataset_contract(MISSING_REQUIRED_FIXTURE)

    assert isinstance(contract, dict)
    assert errors


def test_default_schema_loading_from_package_resource_path() -> None:
    schema_resource = files("fabricops_kit.schemas").joinpath(
        "dataset_contract.schema.json"
    )

    assert schema_resource.is_file()

    _, errors = load_and_validate_dataset_contract(VALID_FIXTURE)
    assert errors == []


def test_unknown_typo_fields_are_rejected() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["dataset"]["owenr"] = "typo_field"

    errors = validate_dataset_contract(contract)

    assert any("dataset" in error and "Additional properties are not allowed" in error for error in errors)


def test_full_refresh_contract_does_not_require_watermark_or_partition() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["refresh"]["mode"] = "full_refresh"
    contract["refresh"].pop("watermark_column")
    contract["refresh"].pop("partition_column")

    errors = validate_dataset_contract(contract)

    assert errors == []


def test_incremental_contract_requires_watermark_and_partition() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["refresh"]["mode"] = "incremental"
    contract["refresh"].pop("watermark_column")
    contract["refresh"].pop("partition_column")

    errors = validate_dataset_contract(contract)

    assert any("refresh.watermark_column" in error for error in errors)
    assert any("refresh.partition_column" in error for error in errors)


def test_assert_valid_dataset_contract_raises_on_invalid_contract() -> None:
    contract = load_dataset_contract(MISSING_REQUIRED_FIXTURE)

    with pytest.raises(DatasetContractValidationError):
        assert_valid_dataset_contract(contract)


def test_assert_valid_dataset_contract_does_not_raise_on_valid_contract() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)

    assert_valid_dataset_contract(contract)


import sys
import types

from fabricops_kit.config import (
    ConfigSmokeCheckResult,
    bootstrap_fabric_env,
    AIPromptConfig,
    FrameworkConfig,
    GovernanceConfig,
    LineageConfig,
    NotebookRuntimeConfig,
    PathConfig,
    QualityConfig,
    ReviewWorkflowConfig,
    get_path,
    run_config_smoke_tests,
)
from fabricops_kit.fabric_input_output import Housepath, load_config


def _sample_framework_config():
    path_config = PathConfig(
        {
            "Sandbox": {
                "Source": Housepath("w1", "h1", "SRC", "abfss://src"),
                "Unified": Housepath("w1", "h2", "UNI", "abfss://uni"),
            }
        }
    )
    return FrameworkConfig(
        path_config=path_config,
        notebook_runtime_config=NotebookRuntimeConfig(["00_", "03_"]),
        ai_prompt_config=AIPromptConfig("quality {profile}", "lineage {steps}", "handover {context}"),
        quality_config=QualityConfig(),
        governance_config=GovernanceConfig(),
        review_workflow_config=ReviewWorkflowConfig(),
        lineage_config=LineageConfig(),
    )


def test_load_config_accepts_framework_config():
    config = _sample_framework_config()
    loaded = load_config(config)
    assert loaded.path_config.paths["Sandbox"]["Source"].house_name == "SRC"


def test_get_path_missing_values_raise_clean_errors():
    config = _sample_framework_config()
    with pytest.raises(ValueError, match="Environment 'Prod' was not found"):
        get_path("Prod", "Source", config=config)


def test_bootstrap_env_and_smoke_behavior(monkeypatch):
    config = _sample_framework_config()
    ctx = bootstrap_fabric_env(config=config, check_ai=False, smoke_test=False)
    assert ctx.paths["Source"].house_name == "SRC"
    assert ctx.smoke_test_results == []

    runtime_mod = types.SimpleNamespace(context={"currentNotebookName": "00_env_config"})
    monkeypatch.setitem(sys.modules, "notebookutils", types.SimpleNamespace(runtime=runtime_mod))
    monkeypatch.setitem(sys.modules, "notebookutils.runtime", runtime_mod)
    monkeypatch.setattr("fabricops_kit.config.spark", object(), raising=False)
    results = run_config_smoke_tests(config=config, check_ai=False)
    assert all(isinstance(r, ConfigSmokeCheckResult) for r in results)


def test_bootstrap_invalid_env_raises_useful_error():
    with pytest.raises(ValueError, match="Environment 'Prod'"):
        bootstrap_fabric_env(env="Prod", config=_sample_framework_config(), smoke_test=False, check_ai=False)


def test_config_dataclass_validation_guards() -> None:
    with pytest.raises(ValueError, match="paths must be a non-empty mapping"):
        PathConfig(paths={})
    with pytest.raises(ValueError, match="allowed_notebook_prefixes"):
        NotebookRuntimeConfig(allowed_notebook_prefixes=("   ",))
    with pytest.raises(ValueError, match="dq_rule_candidate_template"):
        AIPromptConfig(" ", "x", "y")
    with pytest.raises(ValueError, match="default_severity"):
        QualityConfig(default_severity="urgent")


def test_config_dataclasses_normalize_values() -> None:
    runtime = NotebookRuntimeConfig(allowed_notebook_prefixes=(" 00_ ", "", "03_ "))
    assert runtime.allowed_notebook_prefixes == ("00_", "03_")
    quality = QualityConfig(default_severity=" WARNING ")
    assert quality.default_severity == "warning"
    governance = GovernanceConfig(required_classification=1, sensitivity_rules=None)
    assert governance.required_classification is True and governance.sensitivity_rules == {}
    lineage = LineageConfig(capture_ai_summaries=0, capture_transformation_steps=1)
    assert lineage.capture_ai_summaries is False and lineage.capture_transformation_steps is True
