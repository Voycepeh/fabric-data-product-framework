import json

from fabric_data_product_framework.metadata import (
    build_dataset_run_record,
    build_quality_result_records,
    build_schema_drift_records,
    build_schema_snapshot_records,
    write_metadata_records,
    write_multiple_metadata_outputs,
)


def test_build_dataset_run_record_expected_fields():
    row = build_dataset_run_record(
        run_id="run_1",
        dataset_name="synthetic_orders",
        environment="dev",
        source_table="raw.synthetic_orders",
        target_table="curated.synthetic_orders",
    )
    assert row["run_id"] == "run_1"
    assert row["status"] == "started"
    assert set(row) == {
        "run_id", "dataset_name", "environment", "source_table", "target_table", "status",
        "started_at_utc", "ended_at_utc", "row_count_source", "row_count_output", "notes",
    }


def test_build_schema_snapshot_records_flattens_columns():
    snapshot = {
        "dataset_name": "synthetic_orders",
        "table_name": "raw.synthetic_orders",
        "engine": "pandas",
        "generated_at": "2026-01-01T00:00:00Z",
        "columns": [{"column_name": "order_id", "ordinal_position": 0, "data_type": "int64", "nullable": False, "column_hash": "abc"}],
    }
    rows = build_schema_snapshot_records(snapshot, run_id="run_1", table_stage="source")
    assert len(rows) == 1
    assert rows[0]["column_name"] == "order_id"


def test_build_schema_drift_records_none_row_when_no_changes():
    result = build_schema_drift_records({"dataset_name": "d", "table_name": "t", "baseline_engine": "pandas", "current_engine": "pandas", "status": "passed", "can_continue": True, "changes": []}, run_id="run_1", table_stage="source")
    assert len(result) == 1
    assert result[0]["drift_type"] == "none"


def test_build_schema_drift_records_flattens_changes():
    drift_result = {
        "dataset_name": "d",
        "table_name": "t",
        "baseline_engine": "pandas",
        "current_engine": "pandas",
        "status": "warning",
        "can_continue": True,
        "changes": [{"drift_type": "column_added", "column_name": "new_col", "previous_value": None, "current_value": {"x": 1}, "severity": "warning", "action": "warn", "message": "added"}],
    }
    rows = build_schema_drift_records(drift_result, run_id="run_1", table_stage="target")
    assert len(rows) == 1
    assert rows[0]["column_name"] == "new_col"


def test_build_quality_result_records_list_input():
    rows = build_quality_result_records(
        [{"rule_id": "r1", "status": "passed", "failed_count": 0, "columns": ["order_id"]}],
        run_id="run_1",
        dataset_name="synthetic_orders",
        table_name="curated.synthetic_orders",
        table_stage="target",
    )
    assert len(rows) == 1
    assert rows[0]["rule_id"] == "r1"


def test_build_quality_result_records_dict_results_input():
    rows = build_quality_result_records(
        {"results": [{"rule_id": "r2", "status": "failed", "failed_count": 3}]},
        run_id="run_1",
        dataset_name="synthetic_orders",
        table_name="curated.synthetic_orders",
        table_stage="target",
    )
    assert len(rows) == 1
    assert rows[0]["rule_id"] == "r2"


def test_write_metadata_records_empty_returns_none():
    assert write_metadata_records([], "meta.dataset_runs", writer=lambda *_args, **_kwargs: "ignored") is None


def test_write_metadata_records_calls_injected_writer():
    calls = []

    def writer(records, table_identifier, mode="append", **options):
        calls.append((records, table_identifier, mode, options))
        return {"ok": True}

    result = write_metadata_records([{"run_id": "1"}], "meta.dataset_runs", writer=writer, mode="overwrite", merge_schema=True)
    assert result == {"ok": True}
    assert calls[0][1] == "meta.dataset_runs"
    assert calls[0][2] == "overwrite"


def test_write_metadata_records_raises_without_writer():
    try:
        write_metadata_records([{"run_id": "1"}], "meta.dataset_runs")
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        assert True


def test_write_multiple_metadata_outputs_writes_mapped_non_empty_outputs():
    calls = []

    def writer(records, table_identifier, mode="append", **options):
        calls.append((records, table_identifier, mode, options))
        return {"table": table_identifier, "count": len(records)}

    results = write_multiple_metadata_outputs(
        outputs={"dataset_runs": [{"run_id": "1"}], "schema_snapshots": [{"run_id": "1"}], "quality_results": []},
        table_mapping={"dataset_runs": "meta.dataset_runs", "schema_snapshots": "meta.schema_snapshots"},
        writer=writer,
    )
    assert set(results) == {"dataset_runs", "schema_snapshots"}
    assert len(calls) == 2


def test_write_multiple_metadata_outputs_raises_on_missing_mapping():
    try:
        write_multiple_metadata_outputs(outputs={"dataset_runs": [{"run_id": "1"}]}, table_mapping={}, writer=lambda *_args, **_kwargs: None)
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_all_produced_records_are_json_serializable():
    rows = []
    rows.append(build_dataset_run_record(run_id="run_1", dataset_name="d", environment="dev", source_table="s", target_table="t"))
    rows.extend(build_schema_snapshot_records({"dataset_name": "d", "table_name": "t", "engine": "pandas", "generated_at": "2026-01-01T00:00:00Z", "columns": [{"column_name": "x", "ordinal_position": 0, "data_type": "int64", "nullable": False, "column_hash": "h"}]}, run_id="run_1", table_stage="source"))
    rows.extend(build_schema_drift_records({"dataset_name": "d", "table_name": "t", "baseline_engine": "pandas", "current_engine": "pandas", "status": "passed", "can_continue": True, "changes": []}, run_id="run_1", table_stage="source"))
    rows.extend(build_quality_result_records([{"rule_id": "r1", "columns": ["x"]}], run_id="run_1", dataset_name="d", table_name="t", table_stage="target"))
    for row in rows:
        json.dumps(row)
