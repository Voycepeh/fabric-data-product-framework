from fabricops_kit.business_context import extract_column_business_context_suggestions, prepare_business_context_profile_input
import fabricops_kit.business_context as business_context
from fabricops_kit.config import ReviewWorkflowConfig
from fabricops_kit.data_governance import extract_personal_identifier_suggestions, prepare_governance_profile_input
from fabricops_kit.data_quality import approved_dq_rules_from_review_rows, prepare_dq_profile_input


def test_business_context_profile_shaping_and_extraction():
    rows = prepare_business_context_profile_input([{"COLUMN_NAME": "id", "DATA_TYPE": "string"}], table_name="orders", table_context="sales")
    assert rows[0]["column_name"] == "id"
    out = extract_column_business_context_suggestions([{"ai_business_context_response": "{'column_name':'id','business_context':'identifier'}"}])
    assert out[0]["column_name"] == "id"


def test_dq_profile_prep_and_approved_extraction():
    profile_rows = [{"column_name": "id", "data_type": "string"}, {"column_name": "status", "data_type": "string"}]
    contexts = [{"column_name": "id", "approved_business_context": "Identifier"}]
    prepared = prepare_dq_profile_input(profile_rows, table_name="orders", column_contexts=contexts)
    assert len(prepared) == 1
    approved = approved_dq_rules_from_review_rows([{"approval_status": "approved", "proposed_rule_payload": "{'rule_id': 'id_not_null'}"}])
    assert approved[0]["rule_id"] == "id_not_null"


def test_governance_profile_prep_and_extraction():
    prepared = prepare_governance_profile_input([{"column_name": "email"}], table_name="orders", column_contexts=[{"column_name": "email", "approved_business_context": "Contact email"}])
    assert prepared[0]["approved_business_context"] == "Contact email"
    out = extract_personal_identifier_suggestions([{"ai_governance_response": '{"column_name":"email","ai_suggested_personal_identifier_classification":"direct_identifier"}'}])
    assert out[0]["column_name"] == "email"


def test_review_workflow_config_defaults():
    cfg = ReviewWorkflowConfig()
    assert cfg.default_approval_status == "pending"


def test_capture_column_business_context_requires_widgets(monkeypatch):
    def _raise(*args, **kwargs):
        raise ImportError("ipywidgets missing")

    monkeypatch.setattr(business_context.importlib, "import_module", _raise)
    try:
        business_context.capture_column_business_context([{"column_name": "id", "business_context": "Identifier"}], "dev", "sales", "orders")
        assert False, "expected ImportError"
    except ImportError:
        assert True


def test_capture_column_business_context_updates_globals_on_actions(monkeypatch):
    captured = {}

    class _Widget:
        def __init__(self, *args, **kwargs):
            self.value = kwargs.get("value", "")
            self.description = kwargs.get("description", "")
            self.layout = kwargs.get("layout")
            self.disabled = False

    class _Button(_Widget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._callback = None

        def on_click(self, cb):
            self._callback = cb

        def click(self):
            if self._callback:
                self._callback(None)

    class _Widgets:
        HTML = _Widget
        Textarea = _Widget
        Text = _Widget
        Layout = _Widget
        VBox = _Widget
        HBox = _Widget
        Button = _Button

    def _fake_display(_):
        return None

    def _fake_require():
        return _Widgets, _fake_display

    orig_button = _Widgets.Button

    def _capture_button(*args, **kwargs):
        btn = orig_button(*args, **kwargs)
        captured[btn.description] = btn
        return btn

    _Widgets.Button = _capture_button
    monkeypatch.setattr(business_context, "_require_ipywidgets", _fake_require)
    business_context.COLUMN_BUSINESS_CONTEXT_FROM_WIDGET.clear()
    business_context.REJECTED_COLUMN_BUSINESS_CONTEXT_FROM_WIDGET.clear()

    business_context.capture_column_business_context(
        [{"column_name": "id", "business_context": "Identifier"}],
        "dev",
        "sales",
        "orders",
    )

    captured["Approve"].click()
    assert len(business_context.COLUMN_BUSINESS_CONTEXT_FROM_WIDGET) == 1
    assert len(business_context.REJECTED_COLUMN_BUSINESS_CONTEXT_FROM_WIDGET) == 0

    captured["Undo"].click()
    assert len(business_context.COLUMN_BUSINESS_CONTEXT_FROM_WIDGET) == 0

    business_context.capture_column_business_context(
        [{"column_name": "status", "business_context": "Order status"}],
        "dev",
        "sales",
        "orders",
    )
    captured["Reject"].click()
    assert len(business_context.REJECTED_COLUMN_BUSINESS_CONTEXT_FROM_WIDGET) == 1
