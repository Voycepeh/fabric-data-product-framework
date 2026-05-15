import builtins

from fabricops_kit.config import _check_fabric_ai_functions_available, _configure_fabric_ai_functions


def test_check_and_configure_import_failure(monkeypatch):
    orig_import = builtins.__import__

    def _fake_import(name, *args, **kwargs):
        if name == "synapse.ml.spark.aifunc":
            raise ImportError("no module")
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _fake_import)
    assert _check_fabric_ai_functions_available()["available"] is False
    out = _configure_fabric_ai_functions()
    assert out["available"] is False and out["configured"] is False
