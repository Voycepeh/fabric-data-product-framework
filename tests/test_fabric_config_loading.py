import pytest

from fabricops_kit.config import (
    FrameworkConfig,
    create_ai_prompt_config,
    create_framework_config,
    create_governance_config,
    create_lineage_config,
    create_notebook_runtime_config,
    create_path_config,
    create_quality_config,
)
from fabricops_kit.fabric_io import Housepath, get_path, load_fabric_config


def _sample_framework_config() -> FrameworkConfig:
    path_config = create_path_config(
        {
            "Sandbox": {
                "Source": Housepath("w1", "h1", "SRC", "abfss://src"),
                "Unified": Housepath("w1", "h2", "UNI", "abfss://uni"),
            }
        }
    )
    return create_framework_config(
        path_config=path_config,
        notebook_runtime_config=create_notebook_runtime_config(["00_", "03_"]),
        ai_prompt_config=create_ai_prompt_config(dq_rule_candidate_template="quality {profile}", governance_candidate_template="lineage {steps}", handover_summary_template="handover {context}"),
        quality_config=create_quality_config(),
        governance_config=create_governance_config(),
        lineage_config=create_lineage_config(),
    )


def test_load_fabric_config_accepts_framework_config():
    config = _sample_framework_config()
    loaded = load_fabric_config(config)
    assert isinstance(loaded, FrameworkConfig)
    assert loaded.path_config.paths["Sandbox"]["Source"].house_name == "SRC"


def test_load_fabric_config_accepts_structured_dict():
    config = _sample_framework_config()
    loaded = load_fabric_config(
        {
            "path_config": config.path_config,
            "notebook_runtime_config": config.notebook_runtime_config,
            "ai_prompt_config": config.ai_prompt_config,
            "quality_config": config.quality_config,
            "governance_config": config.governance_config,
            "lineage_config": config.lineage_config,
        }
    )
    assert isinstance(loaded, FrameworkConfig)


def test_get_path_works_with_framework_config():
    config = _sample_framework_config()
    p = get_path("Sandbox", "Unified", config=config)
    assert p.root == "abfss://uni"


def test_get_path_works_with_path_config():
    config = _sample_framework_config()
    p = get_path("Sandbox", "Source", config=config.path_config)
    assert p.house_id == "h1"


def test_get_path_missing_values_raise_clean_errors():
    config = _sample_framework_config()
    with pytest.raises(ValueError, match="Environment 'Prod' was not found"):
        get_path("Prod", "Source", config=config)
    with pytest.raises(ValueError, match="Target 'Warehouse' was not found"):
        get_path("Sandbox", "Warehouse", config=config.path_config)


def test_create_ai_prompt_config_requires_explicit_templates():
    with pytest.raises(ValueError, match="dq_rule_candidate_template"):
        create_ai_prompt_config("", "g", "h")
    with pytest.raises(TypeError):
        create_ai_prompt_config(dq_rule_candidate_template="dq", governance_candidate_template="g")
