import json

import pandas as pd
import pytest

from fabric_data_product_framework.drift import (
    SchemaDriftError,
    assert_no_blocking_schema_drift,
    build_schema_snapshot,
    compare_schema_snapshots,
    default_schema_drift_policy,
)


def test_build_schema_snapshot_includes_dataset_and_table_name() -> None:
    df = pd.DataFrame({"customer_id": [1, 2]})

    snapshot = build_schema_snapshot(df, dataset_name="synthetic_orders", table_name="source_orders")

    assert snapshot["dataset_name"] == "synthetic_orders"
    assert snapshot["table_name"] == "source_orders"
    assert "generated_at" in snapshot


def test_snapshot_includes_ordinal_position_and_dtype() -> None:
    df = pd.DataFrame({"customer_id": [1, 2], "order_amount": [10.0, 20.0]})

    snapshot = build_schema_snapshot(df)

    assert snapshot["columns"][0]["column_name"] == "customer_id"
    assert snapshot["columns"][0]["ordinal_position"] == 0
    assert snapshot["columns"][0]["data_type"] == "int64"
    assert snapshot["columns"][1]["column_name"] == "order_amount"
    assert snapshot["columns"][1]["ordinal_position"] == 1
    assert snapshot["columns"][1]["data_type"] == "float64"


def test_identical_snapshots_pass() -> None:
    df = pd.DataFrame({"customer_id": [1, 2], "order_amount": [10.0, 20.0]})
    baseline = build_schema_snapshot(df)
    current = build_schema_snapshot(df)

    result = compare_schema_snapshots(baseline, current)

    assert result["status"] == "passed"
    assert result["can_continue"] is True
    assert result["changes"] == []


def test_added_column_is_detected() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2]})
    current_df = pd.DataFrame({"customer_id": [1, 2], "new_status": ["paid", "pending"]})

    result = compare_schema_snapshots(build_schema_snapshot(baseline_df), build_schema_snapshot(current_df))

    assert any(change["drift_type"] == "column_added" for change in result["changes"])


def test_removed_column_blocks_by_default() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2], "old_col": ["x", "y"]})
    current_df = pd.DataFrame({"customer_id": [1, 2]})

    result = compare_schema_snapshots(build_schema_snapshot(baseline_df), build_schema_snapshot(current_df))

    assert result["status"] == "failed"
    assert result["can_continue"] is False
    assert result["summary"]["blocking_change_count"] >= 1


def test_data_type_change_blocks_by_default() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2]})
    current_df = pd.DataFrame({"customer_id": ["1", "2"]})

    result = compare_schema_snapshots(build_schema_snapshot(baseline_df), build_schema_snapshot(current_df))

    assert any(change["drift_type"] == "data_type_changed" and change["action"] == "block" for change in result["changes"])
    assert result["status"] == "failed"


def test_nullable_change_warning_by_default() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2]})
    current_df = pd.DataFrame({"customer_id": [1, None]})

    result = compare_schema_snapshots(build_schema_snapshot(baseline_df), build_schema_snapshot(current_df))

    nullable_change = next(change for change in result["changes"] if change["drift_type"] == "nullable_changed")
    assert nullable_change["severity"] == "warning"
    assert nullable_change["action"] == "warn"


def test_ordinal_change_is_detectable() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2], "order_amount": [10.0, 20.0]})
    current_df = pd.DataFrame({"order_amount": [10.0, 20.0], "customer_id": [1, 2]})

    result = compare_schema_snapshots(build_schema_snapshot(baseline_df), build_schema_snapshot(current_df))

    assert any(change["drift_type"] == "ordinal_changed" for change in result["changes"])


def test_policy_can_allow_added_columns() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2]})
    current_df = pd.DataFrame({"customer_id": [1, 2], "new_status": ["paid", "pending"]})
    policy = default_schema_drift_policy()
    policy["warn_on_added_column"] = False
    policy["require_approval_for_new_columns"] = False

    result = compare_schema_snapshots(build_schema_snapshot(baseline_df), build_schema_snapshot(current_df), policy=policy)

    added_change = next(change for change in result["changes"] if change["drift_type"] == "column_added")
    assert added_change["severity"] == "info"
    assert added_change["action"] == "allow"
    assert result["status"] == "passed"


def test_assert_no_blocking_schema_drift_raises() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2], "old_col": ["x", "y"]})
    current_df = pd.DataFrame({"customer_id": [1, 2]})
    result = compare_schema_snapshots(build_schema_snapshot(baseline_df), build_schema_snapshot(current_df))

    with pytest.raises(SchemaDriftError):
        assert_no_blocking_schema_drift(result)


def test_schema_drift_output_is_json_serializable() -> None:
    baseline_df = pd.DataFrame({"customer_id": [1, 2]})
    current_df = pd.DataFrame({"customer_id": [1, 2], "new_status": ["paid", "pending"]})
    baseline = build_schema_snapshot(baseline_df)
    current = build_schema_snapshot(current_df)
    result = compare_schema_snapshots(baseline, current)

    json.dumps(baseline)
    json.dumps(current)
    json.dumps(result)


def test_empty_dataframe_does_not_crash() -> None:
    empty_df = pd.DataFrame()
    snapshot = build_schema_snapshot(empty_df, dataset_name="synthetic_orders", table_name="empty_table")
    result = compare_schema_snapshots(snapshot, snapshot)

    assert snapshot["columns"] == []
    assert result["status"] == "passed"
