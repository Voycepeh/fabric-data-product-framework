import fabricops_kit.business_context as bc
import fabricops_kit.metadata as nr


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
