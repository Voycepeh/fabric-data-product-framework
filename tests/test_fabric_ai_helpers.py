import builtins

import pytest

from fabricops_kit.config import (
    AIPromptConfig,
    FrameworkConfig,
    GovernanceConfig,
    LineageConfig,
    NotebookRuntimeConfig,
    PathConfig,
    QualityConfig,
    ReviewWorkflowConfig,
)
from fabricops_kit.ai import (
    build_governance_candidate_prompt,
    build_handover_summary_prompt,
    build_manual_governance_prompt_package,
    build_manual_handover_prompt_package,
    check_fabric_ai_functions_available,
    configure_fabric_ai_functions,
    generate_governance_candidates_with_fabric_ai,
    generate_handover_summary_with_fabric_ai,
    parse_manual_ai_json_response,
)


class _AIMock:
    def __init__(self):
        self.calls = []

    def generate_response(self, **kwargs):
        self.calls.append(kwargs)
        return {"ok": True}


class _DFMock:
    def __init__(self):
        self.ai = _AIMock()


def test_prompt_builders_contain_expected_placeholders_and_static_context():
    gov = build_governance_candidate_prompt(business_context="gctx", dataset_name="cust")
    assert "{column_name}" in gov and "{{column_name}}" not in gov
    assert "Dataset name: cust" in gov and "Business context: gctx" in gov

    ho = build_handover_summary_prompt(business_context="hctx")
    assert "{summary}" in ho and "{{summary}}" not in ho
    assert "Business context: hctx" in ho


def test_manual_prompt_packages_have_expected_keys():
    pkg2 = build_manual_governance_prompt_package(sample_rows=[{"c": "id"}], business_context="ctx", dataset_name="orders")
    assert {"mode", "target_use", "prompt", "expected_output_schema", "notes", "sample_rows"}.issubset(pkg2)

    pkg3 = build_manual_handover_prompt_package(sample_rows=[{"summary": "ok"}], business_context="ctx")
    assert {"mode", "target_use", "prompt", "expected_output_schema", "notes", "sample_rows"}.issubset(pkg3)


def test_generate_helpers_use_shared_prompt_and_supported_args_only():
    df2 = _DFMock()
    generate_governance_candidates_with_fabric_ai(df2, business_context="ctx", dataset_name="orders")
    assert df2.ai.calls[0]["prompt"] == build_governance_candidate_prompt("ctx", "orders")

    df3 = _DFMock()
    generate_handover_summary_with_fabric_ai(df3, business_context="ctx")
    assert df3.ai.calls[0]["prompt"] == build_handover_summary_prompt("ctx")


def test_check_and_configure_import_failure(monkeypatch):
    orig_import = builtins.__import__

    def _fake_import(name, *args, **kwargs):
        if name == "synapse.ml.spark.aifunc":
            raise ImportError("no module")
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _fake_import)
    assert check_fabric_ai_functions_available()["available"] is False
    out = configure_fabric_ai_functions()
    assert out["available"] is False and out["configured"] is False


def test_parse_manual_ai_json_response_success_and_failure():
    assert parse_manual_ai_json_response('{"a":1}')["a"] == 1
    with pytest.raises(ValueError):
        parse_manual_ai_json_response("not json")


def _build_config():
    return FrameworkConfig(
        path_config=PathConfig({"Sandbox": {"Source": type("H", (), {"workspace_id": "w", "house_id": "h", "house_name": "n", "root": "r"})()}}),
        notebook_runtime_config=NotebookRuntimeConfig(["00_"]),
        ai_prompt_config=AIPromptConfig(
            dq_rule_candidate_template="DQ {dataset_name} {business_context} {column_name}",
            governance_candidate_template="GOV {dataset_name} {business_context} {column_name}",
            handover_summary_template="HO {business_context} {summary}",
        ),
        quality_config=QualityConfig(),
        governance_config=GovernanceConfig(),
        review_workflow_config=ReviewWorkflowConfig(),
        lineage_config=LineageConfig(),
    )


def test_prompt_builders_use_config_templates_and_fallbacks():
    config = _build_config()
    assert build_governance_candidate_prompt("ctx", "orders", config=config).startswith("GOV orders ctx")
    assert build_handover_summary_prompt("ctx", config=config).startswith("HO ctx")


def test_generate_helpers_forward_config_to_prompt_builder():
    config = _build_config()
    df = _DFMock()
    generate_governance_candidates_with_fabric_ai(df, business_context="ctx", dataset_name="orders", config=config)
    assert df.ai.calls[0]["prompt"].startswith("GOV orders ctx")
