import json

import pandas as pd
import pytest

from fabric_data_product_framework.drift import (
    SchemaDriftError,
    UnsupportedDataFrameEngineError,
    assert_no_blocking_schema_drift,
    build_schema_snapshot,
    compare_schema_snapshots,
    default_schema_drift_policy,
    detect_dataframe_engine,
)


class FakeSparkType:
    def __str__(self):
        return "StringType()"


class FakeSparkField:
    def __init__(self, name, data_type, nullable):
        self.name = name
        self.dataType = data_type
        self.nullable = nullable


class FakeSparkSchema:
    def __init__(self, fields):
        self.fields = fields


class FakeSparkDataFrame:
    __module__ = "pyspark.sql.dataframe"

    def __init__(self):
        self.columns = ["customer_id", "status"]
        self.schema = FakeSparkSchema(
            [
                FakeSparkField("customer_id", FakeSparkType(), False),
                FakeSparkField("status", FakeSparkType(), True),
            ]
        )
        self.scan_calls = 0

    def collect(self):
        self.scan_calls += 1
        raise AssertionError("collect must not be called")


def test_detect_dataframe_engine_returns_pandas() -> None:
    assert detect_dataframe_engine(pd.DataFrame({"a": [1]})) == "pandas"


def test_build_schema_snapshot_auto_works_for_pandas() -> None:
    snapshot = build_schema_snapshot(pd.DataFrame({"a": [1]}), engine="auto")
    assert snapshot["engine"] == "pandas"


def test_build_schema_snapshot_pandas_explicit() -> None:
    snapshot = build_schema_snapshot(pd.DataFrame({"a": [1]}), engine="pandas")
    assert snapshot["engine"] == "pandas"


def test_unsupported_input_raises_error() -> None:
    with pytest.raises(UnsupportedDataFrameEngineError):
        build_schema_snapshot({"not": "a_dataframe"}, engine="auto")


def test_invalid_engine_raises_value_error() -> None:
    with pytest.raises(ValueError):
        build_schema_snapshot(pd.DataFrame({"a": [1]}), engine="duckdb")


def test_fake_spark_dataframe_detected() -> None:
    assert detect_dataframe_engine(FakeSparkDataFrame()) == "spark"


def test_fake_spark_snapshot_uses_schema_without_scan() -> None:
    fake_df = FakeSparkDataFrame()
    snapshot = build_schema_snapshot(fake_df, engine="spark")

    assert fake_df.scan_calls == 0
    assert snapshot["columns"][0]["column_name"] == "customer_id"
    assert snapshot["columns"][0]["data_type"] == "StringType()"
    assert snapshot["columns"][0]["nullable"] is False


def test_spark_snapshot_contains_engine() -> None:
    snapshot = build_schema_snapshot(FakeSparkDataFrame(), engine="spark")
    assert snapshot["engine"] == "spark"


def test_pandas_snapshot_contains_engine() -> None:
    snapshot = build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]}))
    assert snapshot["engine"] == "pandas"


def test_build_schema_snapshot_includes_dataset_and_table_name() -> None:
    df = pd.DataFrame({"customer_id": [1, 2]})
    snapshot = build_schema_snapshot(df, dataset_name="synthetic_orders", table_name="source_orders")
    assert snapshot["dataset_name"] == "synthetic_orders"
    assert snapshot["table_name"] == "source_orders"
    assert "generated_at" in snapshot


def test_snapshot_includes_ordinal_position_and_dtype() -> None:
    df = pd.DataFrame({"customer_id": [1, 2], "order_amount": [10.0, 20.0]})
    snapshot = build_schema_snapshot(df)
    assert snapshot["columns"][0]["ordinal_position"] == 0
    assert snapshot["columns"][0]["data_type"] == "int64"


def test_identical_snapshots_pass() -> None:
    df = pd.DataFrame({"customer_id": [1, 2], "order_amount": [10.0, 20.0]})
    result = compare_schema_snapshots(build_schema_snapshot(df), build_schema_snapshot(df))
    assert result["status"] == "passed"
    assert result["can_continue"] is True


def test_added_column_is_detected() -> None:
    result = compare_schema_snapshots(
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]})),
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2], "new_status": ["paid", "pending"]})),
    )
    assert any(change["drift_type"] == "column_added" for change in result["changes"])


def test_removed_column_blocks_by_default() -> None:
    result = compare_schema_snapshots(
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2], "old_col": ["x", "y"]})),
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]})),
    )
    assert result["status"] == "failed"


def test_data_type_change_blocks_by_default() -> None:
    result = compare_schema_snapshots(
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]})),
        build_schema_snapshot(pd.DataFrame({"customer_id": ["1", "2"]})),
    )
    assert any(c["drift_type"] == "data_type_changed" and c["action"] == "block" for c in result["changes"])


def test_nullable_change_warning_by_default() -> None:
    result = compare_schema_snapshots(
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]})),
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, None]})),
    )
    change = next(c for c in result["changes"] if c["drift_type"] == "nullable_changed")
    assert change["action"] == "warn"


def test_ordinal_change_is_detectable() -> None:
    result = compare_schema_snapshots(
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2], "order_amount": [10.0, 20.0]})),
        build_schema_snapshot(pd.DataFrame({"order_amount": [10.0, 20.0], "customer_id": [1, 2]})),
    )
    assert any(change["drift_type"] == "ordinal_changed" for change in result["changes"])


def test_policy_can_allow_added_columns() -> None:
    policy = default_schema_drift_policy()
    policy["warn_on_added_column"] = False
    policy["require_approval_for_new_columns"] = False
    result = compare_schema_snapshots(
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]})),
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2], "new_status": ["paid", "pending"]})),
        policy=policy,
    )
    assert next(c for c in result["changes"] if c["drift_type"] == "column_added")["action"] == "allow"


def test_assert_no_blocking_schema_drift_raises() -> None:
    result = compare_schema_snapshots(
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2], "old_col": ["x", "y"]})),
        build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]})),
    )
    with pytest.raises(SchemaDriftError):
        assert_no_blocking_schema_drift(result)


def test_compare_schema_includes_engines() -> None:
    baseline = build_schema_snapshot(pd.DataFrame({"a": [1]}), engine="pandas")
    current = build_schema_snapshot(FakeSparkDataFrame(), engine="spark")
    result = compare_schema_snapshots(baseline, current)
    assert result["baseline_engine"] == "pandas"
    assert result["current_engine"] == "spark"


def test_schema_drift_output_is_json_serializable() -> None:
    baseline = build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2]}))
    current = build_schema_snapshot(pd.DataFrame({"customer_id": [1, 2], "new_status": ["paid", "pending"]}))
    result = compare_schema_snapshots(baseline, current)
    json.dumps(baseline)
    json.dumps(current)
    json.dumps(result)


def test_empty_dataframe_does_not_crash() -> None:
    snapshot = build_schema_snapshot(pd.DataFrame(), dataset_name="synthetic_orders", table_name="empty_table")
    result = compare_schema_snapshots(snapshot, snapshot)
    assert snapshot["columns"] == []
    assert result["status"] == "passed"
