from fabricops_kit.data_governance import _coerce_row_dicts, load_governance_context


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


def test_load_governance_context_filters_and_latest_agreement():
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

    out = load_governance_context(
        governance_rows,
        agreement_rows=agreement_rows,
        agreement_id="A1",
        dataset_name="D",
        table_name="T",
    )

    assert [r["column_name"] for r in out["columns"]] == ["c1", "c3"]
    assert out["agreement_context"]["approved_usage"] == "latest"
