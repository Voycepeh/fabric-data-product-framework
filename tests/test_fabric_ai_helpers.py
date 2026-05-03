import builtins

import pytest

from fabric_data_product_framework.ai import (
    check_fabric_ai_functions_available,
    configure_fabric_ai_functions,
    generate_dq_rule_candidates_with_fabric_ai,
    generate_governance_candidates_with_fabric_ai,
    generate_handover_summary_with_fabric_ai,
)


class _AIMock:
    def __init__(self):
        self.calls = []

    def generate_response(self, **kwargs):
        self.calls.append(kwargs)
        return {"ok": True, "kwargs": kwargs}


class _DFMock:
    def __init__(self):
        self.ai = _AIMock()


def test_generate_dq_candidates_calls_generate_response_with_expected_params():
    df = _DFMock()
    out = generate_dq_rule_candidates_with_fabric_ai(df, business_context="ctx", dataset_name="orders", output_col="o", error_col="e", response_format="json_object", concurrency=9)
    call = df.ai.calls[0]
    assert out["ok"] is True
    assert call["is_prompt_template"] is True
    assert call["output_col"] == "o"
    assert call["error_col"] == "e"
    assert call["response_format"] == "json_object"
    assert call["concurrency"] == 9
    assert "prompt" in call
    assert "{column_name}" in call["prompt"]
    assert "{{column_name}}" not in call["prompt"]
    assert "dataset_name" not in call
    assert "business_context" not in call


def test_generate_governance_candidates_calls_generate_response_with_expected_params():
    df = _DFMock()
    generate_governance_candidates_with_fabric_ai(df, output_col="go", error_col="ge", concurrency=3)
    call = df.ai.calls[0]
    assert call["is_prompt_template"] is True
    assert call["output_col"] == "go"
    assert call["error_col"] == "ge"
    assert call["response_format"] == "json_object"
    assert call["concurrency"] == 3
    assert "candidate_label" in call["prompt"]
    assert "{column_name}" in call["prompt"]
    assert "{{column_name}}" not in call["prompt"]
    assert "business_context" not in call


def test_generate_handover_summary_calls_generate_response_with_expected_params():
    df = _DFMock()
    generate_handover_summary_with_fabric_ai(df, output_col="ho", error_col="he", concurrency=4)
    call = df.ai.calls[0]
    assert call["is_prompt_template"] is True
    assert call["output_col"] == "ho"
    assert call["error_col"] == "he"
    assert call["response_format"] == "json_object"
    assert call["concurrency"] == 4
    assert "{summary}" in call["prompt"]
    assert "{{summary}}" not in call["prompt"]
    assert "business_context" not in call


def test_check_fabric_ai_functions_available_returns_false_when_import_fails(monkeypatch):
    orig_import = builtins.__import__

    def _fake_import(name, *args, **kwargs):
        if name == "synapse.ml.spark.aifunc":
            raise ImportError("no module")
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _fake_import)
    out = check_fabric_ai_functions_available()
    assert out["available"] is False
    assert "Fabric PySpark runtime" in out["message"]


def test_configure_fabric_ai_functions_handles_import_failure(monkeypatch):
    orig_import = builtins.__import__

    def _fake_import(name, *args, **kwargs):
        if name == "synapse.ml.spark.aifunc":
            raise ImportError("no module")
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _fake_import)
    out = configure_fabric_ai_functions()
    assert out["available"] is False
    assert out["configured"] is False


def test_generate_helpers_raise_clear_error_without_dataframe_ai():
    class NoAI:
        pass

    with pytest.raises(RuntimeError):
        generate_dq_rule_candidates_with_fabric_ai(NoAI())
