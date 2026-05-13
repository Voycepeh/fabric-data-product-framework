import fabricops_kit.data_governance as dg
from fabricops_kit.data_governance import _approved_widget_rows, _coerce_row_dicts, load_governance


class RowLike:
    def __init__(self, data):
        self._data = data

    def asDict(self, recursive=True):
        return dict(self._data)


class CollectLike:
    def __init__(self, rows):
        self._rows = rows

    def collect(self):
        return self._rows


def test_coerce_row_dicts_none_and_list():
    assert _coerce_row_dicts(None) == []
    assert _coerce_row_dicts([{"a": 1}, {"b": 2}]) == [{"a": 1}, {"b": 2}]


def test_coerce_row_dicts_collect_like_rows():
    rows = CollectLike([RowLike({"a": 1}), RowLike({"b": 2})])
    assert _coerce_row_dicts(rows) == [{"a": 1}, {"b": 2}]


def test_load_governance_filters_and_latest_agreement():
    governance_rows = [
        {"agreement_id": "A1", "dataset_name": "D", "table_name": "T", "column_name": "c1", "status": "approved", "approved_at": "2025-01-01T00:00:00Z"},
        {"agreement_id": "A1", "dataset_name": "D", "table_name": "T", "column_name": "c2", "status": "rejected", "approved_at": "2025-01-02T00:00:00Z"},
        {"agreement_id": "A1", "dataset_name": "D", "table_name": "T", "column_name": "c3", "status": "approved", "approved_at": "2025-01-03T00:00:00Z"},
        {"agreement_id": "A2", "dataset_name": "D", "table_name": "T", "column_name": "c4", "status": "approved", "approved_at": "2025-01-04T00:00:00Z"},
    ]
    agreement_rows = [
        {"agreement_id": "A1", "dataset_name": "D", "table_name": "T", "approved_usage": "old", "approved_at": "2025-01-01T00:00:00Z"},
        {"agreement_id": "A1", "dataset_name": "D", "table_name": "T", "approved_usage": "latest", "approved_at": "2025-01-05T00:00:00Z"},
    ]

    out = load_governance(
        governance_rows,
        agreement_rows=agreement_rows,
        agreement_id="A1",
        dataset_name="D",
        table_name="T",
    )

    assert [r["column_name"] for r in out["columns"]] == ["c1", "c3"]
    assert out["agreement_context"]["approved_usage"] == "latest"


def test_approved_widget_rows_merges_context_and_status():
    dg._WIDGET_APPROVED_ROWS.clear()
    dg._WIDGET_APPROVED_ROWS.extend([{"column_name": "email"}])

    rows = _approved_widget_rows(agreement_context={"agreement_id": "A1"}, action_by="tester")

    assert rows[0]["column_name"] == "email"
    assert rows[0]["agreement_id"] == "A1"
    assert rows[0]["status"] == "approved"
    assert rows[0]["approved_by"] == "tester"
