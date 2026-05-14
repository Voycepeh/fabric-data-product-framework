import pytest

import fabricops_kit.business_context as bc
import fabricops_kit.notebook_registry as nr


def test_agreement_option_label_and_load_normalization():
    class Spark:
        def table(self, _):
            return [
                {"agreement_id": "A1", "agreement_name": "One", "approved_usage": "use", "updated_at": "2026-01-01"},
                {"agreement_id": "A1", "agreement_name": "One v2", "approved_usage": "use2", "updated_at": "2026-02-01"},
            ]

    rows = nr.load_agreements(Spark())
    assert rows[0]["agreement_name"] == "One v2"
    assert nr._agreement_option_label(rows[0]) == "One v2 | A1 | use2"


def test_get_selected_agreement_requires_selection(monkeypatch):
    monkeypatch.setattr(nr, "_SELECTED_AGREEMENT", None)
    with pytest.raises(RuntimeError, match="No agreement selected"):
        nr.get_selected_agreement()


def test_register_current_notebook_outside_fabric(monkeypatch):
    written = {}

    def fake_write(spark, rows, metadata_path, table_name, mode="append"):
        written["row"] = rows[0]

    monkeypatch.setattr(nr, "write_metadata_rows", fake_write)
    row = nr.register_current_notebook(
        spark=object(),
        metadata_path=object(),
        agreement_id="A1",
        notebook_type="02_ex",
        environment_name="Sandbox",
    )
    assert row["agreement_id"] == "A1"
    assert row["notebook_type"] == "02_ex"
    assert written["row"]["agreement_id"] == "A1"


def test_load_notebook_registry_filters_by_agreement_id():
    class Spark:
        def table(self, _):
            return [{"agreement_id": "A1", "notebook_type": "02_ex"}, {"agreement_id": "A2", "notebook_type": "03_pc"}]

    rows = nr.load_notebook_registry(Spark(), agreement_id="A1")
    assert len(rows) == 1
    assert rows[0]["agreement_id"] == "A1"


def test_business_context_widget_globals_update():
    approved = []
    rejected = []
    history = []

    def sync():
        bc.COLUMN_BUSINESS_CONTEXT_FROM_WIDGET.clear()
        bc.COLUMN_BUSINESS_CONTEXT_FROM_WIDGET.extend(approved)
        bc.REJECTED_COLUMN_BUSINESS_CONTEXT_FROM_WIDGET.clear()
        bc.REJECTED_COLUMN_BUSINESS_CONTEXT_FROM_WIDGET.extend(rejected)

    approved.append({"column_name": "a"})
    history.append("approve")
    sync()
    assert bc.COLUMN_BUSINESS_CONTEXT_FROM_WIDGET == [{"column_name": "a"}]

    rejected.append({"column_name": "b"})
    history.append("reject")
    sync()
    assert bc.REJECTED_COLUMN_BUSINESS_CONTEXT_FROM_WIDGET == [{"column_name": "b"}]

    last = history.pop()
    if last == "reject":
        rejected.pop()
    sync()
    assert bc.REJECTED_COLUMN_BUSINESS_CONTEXT_FROM_WIDGET == []
