import pytest

from fabricops_kit.config import (
    ConfigSmokeCheckResult,
    bootstrap_fabric_env,
    create_ai_prompt_config,
    create_framework_config,
    create_governance_config,
    create_lineage_config,
    create_notebook_runtime_config,
    create_path_config,
    create_quality_config,
    run_config_smoke_tests,
)
from fabricops_kit.fabric_io import Housepath


def _cfg():
    return create_framework_config(
        path_config=create_path_config(
            {
                "Sandbox": {
                    "Source": Housepath("w1", "h1", "source", "abfss://root1"),
                    "Unified": Housepath("w2", "h2", "unified", "abfss://root2"),
                }
            }
        ),
        notebook_runtime_config=create_notebook_runtime_config(["00_", "01_"]),
        ai_prompt_config=create_ai_prompt_config("dq", "gov", "handover"),
        quality_config=create_quality_config(),
        governance_config=create_governance_config(),
        lineage_config=create_lineage_config(),
    )


def test_valid_env_target_path_resolution():
    ctx = bootstrap_fabric_env(config=_cfg(), check_ai=False, smoke_test=False)
    assert ctx.paths["Source"].house_name == "source"


def test_invalid_env_target_raises_useful_error():
    with pytest.raises(ValueError, match="Environment 'Prod'"):
        bootstrap_fabric_env(env="Prod", config=_cfg(), smoke_test=False, check_ai=False)


def test_config_validation_catches_missing_fields():
    broken = _cfg()
    broken.path_config.paths["Sandbox"]["Source"] = Housepath("", "", "", "")  # type: ignore[index]
    results = run_config_smoke_tests(config=broken, check_ai=False)
    assert any(r.status == "fail" for r in results)


def test_smoke_result_formatting_statuses():
    results = run_config_smoke_tests(config=_cfg(), check_ai=False, check_io=True, notebook_name="00_env_config")
    assert all(isinstance(r, ConfigSmokeCheckResult) for r in results)
    assert {r.status for r in results}.issubset({"pass", "fail", "warn", "skipped"})


def test_bootstrap_ai_and_smoke_disabled():
    ctx = bootstrap_fabric_env(config=_cfg(), check_ai=False, smoke_test=False)
    assert ctx.ai_availability["available"] is None
    assert ctx.smoke_test_results == []


def test_bootstrap_with_mocked_ai_true_false(monkeypatch):
    monkeypatch.setattr("fabricops_kit.config.check_fabric_ai_functions_available", lambda: {"available": True, "message": "ok"})
    ctx_true = bootstrap_fabric_env(config=_cfg(), check_ai=True, smoke_test=False)
    assert ctx_true.ai_availability["available"] is True

    monkeypatch.setattr("fabricops_kit.config.check_fabric_ai_functions_available", lambda: {"available": False, "message": "no"})
    ctx_false = bootstrap_fabric_env(config=_cfg(), check_ai=True, smoke_test=False)
    assert ctx_false.ai_availability["available"] is False
