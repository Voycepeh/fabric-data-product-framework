import importlib

from fabricops_kit.business_context import suggest_column_business_contexts, capture_column_business_context, extract_column_business_context_suggestions
from fabricops_kit.data_governance import suggest_personal_identifier_classifications, extract_personal_identifier_suggestions


class _AI:
    def __init__(self):
        self.called = False
        self.kw = None

    def generate_response(self, **kwargs):
        self.called = True
        self.kw = kwargs
        return {"ok": True}


class _DF:
    def __init__(self):
        self.ai = _AI()


def test_import_fabricops_kit_and_all_symbols_importable():
    pkg = importlib.import_module("fabricops_kit")
    for n in pkg.__all__:
        assert hasattr(pkg, n)


def test_business_context_suggestion_calls_ai_generate_response():
    df = _DF()
    out = suggest_column_business_contexts(df)
    assert out["ok"] is True
    assert df.ai.called is True


def test_governance_suggestion_calls_ai_generate_response():
    df = _DF()
    out = suggest_personal_identifier_classifications(df)
    assert out["ok"] is True
    assert df.ai.called is True


def test_capture_column_business_context_requires_ipywidgets(monkeypatch):
    def fail(name, *a, **k):
        raise ImportError("missing")

    monkeypatch.setattr("importlib.import_module", fail)
    try:
        capture_column_business_context([{"column_name": "id", "business_context": "id"}], "dev", "sales", "orders")
        assert False, "expected import error"
    except ImportError:
        pass


def test_business_context_extraction_reads_ai_business_context_response():
    rows = [{"ai_business_context_response": "{'column_name':'id','business_context':'identifier'}"}]
    out = extract_column_business_context_suggestions(rows)
    assert out[0]["column_name"] == "id"


def test_governance_extraction_reads_ai_governance_response():
    rows = [{"ai_governance_response": "{\"column_name\":\"email\",\"ai_suggested_personal_identifier_classification\":\"direct_identifier\"}"}]
    out = extract_personal_identifier_suggestions(rows)
    assert out[0]["column_name"] == "email"
