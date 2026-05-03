import builtins

import pytest

from fabric_data_product_framework.ai import (
    build_dq_rule_candidate_prompt,
    build_governance_candidate_prompt,
    build_handover_summary_prompt,
    build_manual_dq_rule_prompt_package,
    build_manual_governance_prompt_package,
    build_manual_handover_prompt_package,
    check_fabric_ai_functions_available,
    configure_fabric_ai_functions,
    generate_dq_rule_candidates_with_fabric_ai,
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
    dq = build_dq_rule_candidate_prompt(business_context="ctx", dataset_name="orders")
    assert "{column_name}" in dq and "{{column_name}}" not in dq
    assert "Dataset name: orders" in dq and "Business context: ctx" in dq

    gov = build_governance_candidate_prompt(business_context="gctx", dataset_name="cust")
    assert "{column_name}" in gov and "{{column_name}}" not in gov
    assert "Dataset name: cust" in gov and "Business context: gctx" in gov

    ho = build_handover_summary_prompt(business_context="hctx")
    assert "{summary}" in ho and "{{summary}}" not in ho
    assert "Business context: hctx" in ho


def test_manual_prompt_packages_have_expected_keys():
    pkg = build_manual_dq_rule_prompt_package(sample_rows=[{"a": 1}], business_context="ctx", dataset_name="orders")
    assert {"mode", "target_use", "prompt", "expected_output_schema", "notes", "sample_rows"}.issubset(pkg)
    assert "orders" in pkg["prompt"]

    pkg2 = build_manual_governance_prompt_package(sample_rows=[{"c": "id"}], business_context="ctx", dataset_name="orders")
    assert {"mode", "target_use", "prompt", "expected_output_schema", "notes", "sample_rows"}.issubset(pkg2)

    pkg3 = build_manual_handover_prompt_package(sample_rows=[{"summary": "ok"}], business_context="ctx")
    assert {"mode", "target_use", "prompt", "expected_output_schema", "notes", "sample_rows"}.issubset(pkg3)


def test_generate_helpers_use_shared_prompt_and_supported_args_only():
    df = _DFMock()
    generate_dq_rule_candidates_with_fabric_ai(df, business_context="ctx", dataset_name="orders", output_col="o", error_col="e", concurrency=9)
    call = df.ai.calls[0]
    assert call["is_prompt_template"] is True
    assert call["output_col"] == "o" and call["error_col"] == "e"
    assert call["concurrency"] == 9
    assert "dataset_name" not in call and "business_context" not in call
    assert call["prompt"] == build_dq_rule_candidate_prompt("ctx", "orders")

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
