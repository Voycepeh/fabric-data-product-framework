import sys
import types

sys.modules.setdefault("yaml", types.SimpleNamespace(safe_load=lambda *_a, **_k: {}))

import json

import pytest

from fabricops_kit.drift import (
    UnsupportedDataFrameEngineError,
    build_drift_evidence_record,
    build_schema_snapshot,
)
from fabricops_kit.metadata import (
    EVIDENCE_DRIFT_RESULT,
    EVIDENCE_LINEAGE,
    build_evidence_row,
    default_evidence_types,
)


def test_lineage_wrappers_importable_from_package(monkeypatch) -> None:
    import importlib
    import types
    import sys

    monkeypatch.setitem(sys.modules, "yaml", types.SimpleNamespace(safe_load=lambda *_a, **_k: {}))
    pkg = importlib.import_module("fabricops_kit")
    assert callable(pkg.enrich_lineage_steps_with_ai)
    assert callable(pkg.build_lineage_record_from_steps)


def test_top_down_layout_is_stable() -> None:
    steps = [{"source": "raw", "target": "clean"}, {"source": "clean", "target": "published"}]
    from fabricops_kit.data_lineage import build_top_down_lineage_layout
    pos = build_top_down_lineage_layout(steps)
    assert pos["raw"][1] > pos["clean"][1] > pos["published"][1]
    assert pos == build_top_down_lineage_layout(steps)


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
        drift_type="schema",
        result={"status": "warning", "can_continue": True, "summary": {"warning_change_count": 1}},
    )
    assert row["dataset_name"] == "ds"
    assert row["drift_type"] == "schema"
    assert "created_at" in row
    json.loads(row["summary_json"])
    json.loads(row["result_json"])


def test_metadata_evidence_constants_and_helpers() -> None:
    evidence_types = default_evidence_types()
    assert evidence_types["lineage"] == EVIDENCE_LINEAGE
    assert evidence_types["drift_result"] == EVIDENCE_DRIFT_RESULT
    row = build_evidence_row(dataset_name="ds", table_name="tbl", run_id="r2", evidence_type=EVIDENCE_LINEAGE, payload_json="{}")
    assert row["evidence_type"] == EVIDENCE_LINEAGE
