import json

import pytest

from fabricops_kit.data_lineage import build_lineage_record_from_steps
from fabricops_kit.drift import (
    UnsupportedDataFrameEngineError,
    build_drift_evidence_record,
    build_schema_snapshot,
)
from fabricops_kit.metadata import EVIDENCE_DRIFT_RESULT, EVIDENCE_LINEAGE, build_evidence_row, default_evidence_types


# Notebook templates should read Fabric identity directly, for example:
# from notebookutils import runtime
# ctx = runtime.context
# if callable(ctx):
#     ctx = ctx()
# workspace_id = ctx.get("workspaceId") or ctx.get("currentWorkspaceId")
# notebook_id = ctx.get("notebookId") or ctx.get("currentNotebookId") or ctx.get("artifactId") or ctx.get("itemId")
# notebook_name = ctx.get("notebookName") or ctx.get("currentNotebookName") or ctx.get("artifactName") or ctx.get("itemName")
# run_id = ctx.get("runId") or ctx.get("activityRunId") or ctx.get("livyId") or ctx.get("sessionId")


def test_top_level_does_not_export_internal_drift_helpers() -> None:
    import fabricops_kit as fk

    assert callable(fk.build_drift_evidence_record)
    assert not hasattr(fk, "UnsupportedDataFrameEngineError")
    assert not hasattr(fk, "detect_dataframe_engine")


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


def test_lineage_record_includes_workspace_and_notebook_ids() -> None:
    steps = [{"source": "a", "target": "b", "transformation": "join", "reason": "x", "source_type": "dataframe", "target_type": "dataframe", "confidence": "high"}]
    rows = build_lineage_record_from_steps("ds", steps, workspace_id="ws-1", notebook_id="nb-1")
    assert rows[0]["workspace_id"] == "ws-1"
    assert rows[0]["notebook_id"] == "nb-1"
