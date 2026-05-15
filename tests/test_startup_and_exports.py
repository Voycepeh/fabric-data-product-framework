import importlib
import sys
import types

import fabricops_kit
from fabricops_kit.config import setup_notebook


def test_all_exports_are_importable():
    for name in fabricops_kit.__all__:
        assert hasattr(fabricops_kit, name), f"Missing export: {name}"


def _sample_config():
    from fabricops_kit.config import AIPromptConfig, FrameworkConfig, GovernanceConfig, LineageConfig, NotebookRuntimeConfig, PathConfig, QualityConfig, ReviewWorkflowConfig
    from fabricops_kit.fabric_input_output import Housepath
    return FrameworkConfig(
        path_config=PathConfig({"Sandbox": {"Source": Housepath("w", "h", "s", "abfss://s"), "Unified": Housepath("w", "h2", "u", "abfss://u")}}),
        notebook_runtime_config=NotebookRuntimeConfig(("00_", "02_", "03_")),
        ai_prompt_config=AIPromptConfig("dq", "gov", "ho"),
        quality_config=QualityConfig(),
        governance_config=GovernanceConfig(),
        review_workflow_config=ReviewWorkflowConfig(),
        lineage_config=LineageConfig(),
    )


def test_setup_uses_current_run_id_and_user_fallback(monkeypatch):
    context = {
        "currentNotebookName": "03_pc_test_source_to_unified",
        "currentWorkspaceName": "ws",
        "currentWorkspaceId": "wid",
        "currentRunId": "fabric_run_1",
        "userName": "alice",
        "userId": "u1",
        "isForPipeline": True,
        "isForInteractive": False,
        "isReferenceRun": False,
    }
    runtime_mod = types.SimpleNamespace(context=context)
    monkeypatch.setitem(sys.modules, "notebookutils.runtime", runtime_mod)

    out = setup_notebook(config=_sample_config(), env="Sandbox", check_ai=False)
    assert out.run_id == "fabric_run_1"
    assert out.user_name == "alice"


def test_setup_user_falls_back_to_user_id(monkeypatch):
    context = {"currentNotebookName": "03_pc_test_source_to_unified", "currentRunId": "", "userId": "u2"}
    runtime_mod = types.SimpleNamespace(context=context)
    monkeypatch.setitem(sys.modules, "notebookutils.runtime", runtime_mod)
    out = setup_notebook(config=_sample_config(), env="Sandbox", check_ai=False)
    assert out.user_name == "u2"
    assert out.run_id
