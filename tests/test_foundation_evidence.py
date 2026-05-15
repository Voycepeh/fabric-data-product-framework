import json

import pytest

from fabricops_kit import build_notebook_lineage
from fabricops_kit.drift import UnsupportedDataFrameEngineError, build_drift_evidence_record, build_schema_snapshot
from fabricops_kit.metadata import EVIDENCE_DRIFT_RESULT, EVIDENCE_LINEAGE, build_evidence_row, default_evidence_types


def test_build_notebook_lineage_returns_expected_sections() -> None:
    code = """
df = read_lakehouse_table('orders')
clean = df.select('id')
write_lakehouse_table(clean, lh_out, 'orders_clean')
"""
    out = build_notebook_lineage(
        notebook_code=code,
        dataset_name="ds",
        table_name="orders_clean",
        run_id="r1",
        workspace_id="ws-1",
        notebook_id="nb-1",
    )
    assert out["steps"]
    assert "validation" in out
    assert "records" in out
    assert "summary_markdown" in out
    assert "figure" not in out


def test_helpers_not_top_level_exports() -> None:
    import fabricops_kit as fk

    assert callable(fk.build_notebook_lineage)
    assert not hasattr(fk, "scan_notebook_lineage")
    assert not hasattr(fk, "validate_lineage_steps")
    assert not hasattr(fk, "build_lineage_record_from_steps")
    assert not hasattr(fk, "build_lineage_from_notebook_code")


def test_build_schema_snapshot_pandas_engine() -> None:
    pd = pytest.importorskip("pandas")
    snap = build_schema_snapshot(pd.DataFrame({"a": [1]}), engine="pandas")
    assert snap["engine"] == "pandas"


def test_unsupported_dataframe_engine_raises() -> None:
    with pytest.raises(UnsupportedDataFrameEngineError):
        build_schema_snapshot(object(), engine="auto")


def test_drift_evidence_builder_fields() -> None:
    row = build_drift_evidence_record(
        dataset_name="ds",
        table_name="tbl",
        run_id="r1",
        workspace_id="ws-1",
        workspace_name="workspace",
        notebook_id="nb-1",
        notebook_name="Notebook",
        drift_type="schema",
        result={"status": "warning", "can_continue": True, "summary": {"warning_change_count": 1}},
    )
    assert row["workspace_id"] == "ws-1"
    assert row["notebook_id"] == "nb-1"
    json.loads(row["summary_json"])
    json.loads(row["result_json"])


def test_metadata_evidence_constants_and_helpers() -> None:
    evidence_types = default_evidence_types()
    assert evidence_types["lineage"] == EVIDENCE_LINEAGE
    assert evidence_types["drift_result"] == EVIDENCE_DRIFT_RESULT
    row = build_evidence_row(
        dataset_name="ds",
        table_name="tbl",
        run_id="r2",
        workspace_id="ws-1",
        notebook_id="nb-1",
        evidence_type=EVIDENCE_LINEAGE,
        payload_json="{}",
    )
    assert row["workspace_id"] == "ws-1"
    assert row["notebook_id"] == "nb-1"
