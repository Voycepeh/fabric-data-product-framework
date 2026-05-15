import pytest

import fabricops_kit.data_agreement as da


def test_agreement_option_label_and_load_normalization():
    class Spark:
        def table(self, _):
            return [
                {"agreement_id": "A1", "agreement_name": "One", "approved_usage": "use", "updated_at": "2026-01-01"},
                {"agreement_id": "A1", "agreement_name": "One v2", "approved_usage": "use2", "updated_at": "2026-02-01"},
            ]

    rows = da.load_agreements(Spark())
    assert rows[0]["agreement_name"] == "One v2"
    assert da._agreement_option_label(rows[0]) == "One v2 | A1 | use2"


def test_get_selected_agreement_requires_selection(monkeypatch):
    monkeypatch.setattr(da, "_SELECTED_AGREEMENT", None)
    with pytest.raises(RuntimeError, match="No agreement selected"):
        da.get_selected_agreement()
