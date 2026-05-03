import importlib
import json
import sys

import pandas as pd
import pytest

from fabric_data_product_framework.drift import (
    IncrementalSafetyError,
    assert_incremental_safe,
    build_incremental_safety_records,
    build_partition_snapshot,
    compare_partition_snapshots,
)


def _df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "business_date": ["2026-04-25", "2026-04-25", "2026-04-26"],
            "customer_id": [1, 1, 2],
            "order_id": [100, 101, 200],
            "updated_at": ["2026-04-25T10:00:00", "2026-04-25T10:30:00", "2026-04-26T11:00:00"],
        }
    )


def test_build_partition_snapshot_returns_one_row_per_partition() -> None:
    rows = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    assert len(rows) == 2


def test_snapshot_includes_counts_and_watermarks() -> None:
    rows = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"], watermark_column="updated_at")
    row = next(r for r in rows if r["partition_value"] == "2026-04-25")
    assert row["row_count"] == 2
    assert row["business_key_count"] == 2
    assert row["max_watermark"] == "2026-04-25T10:30:00"


def test_missing_partition_column_raises_value_error() -> None:
    with pytest.raises(ValueError):
        build_partition_snapshot(_df(), partition_column="bad", business_keys=["customer_id"])


def test_missing_business_key_raises_value_error() -> None:
    with pytest.raises(ValueError):
        build_partition_snapshot(_df(), partition_column="business_date", business_keys=["bad_key"])


def test_identical_snapshots_pass() -> None:
    a = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(a, a)
    assert result["status"] == "passed"


def test_new_partition_is_allowed() -> None:
    baseline = build_partition_snapshot(_df().query("business_date == '2026-04-25'"), partition_column="business_date", business_keys=["customer_id", "order_id"])
    current = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(baseline, current)
    assert any(c["drift_type"] == "partition_added" and c["action"] == "allow" for c in result["changes"])


def test_removed_partition_blocks_by_default() -> None:
    baseline = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    current = build_partition_snapshot(_df().query("business_date == '2026-04-25'"), partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(baseline, current, policy={"closed_partition_grace_days": 0})
    assert result["status"] == "failed"


def test_row_count_change_blocks_by_default() -> None:
    baseline = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    mutated = _df().drop(index=[1])
    current = build_partition_snapshot(mutated, partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(baseline, current, policy={"closed_partition_grace_days": 0})
    assert any(c["drift_type"] == "row_count_changed" and c["action"] == "block" for c in result["changes"])


def test_business_key_hash_change_blocks_by_default() -> None:
    baseline = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    mutated = _df().copy(); mutated.loc[0, "order_id"] = 999
    current = build_partition_snapshot(mutated, partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(baseline, current, policy={"closed_partition_grace_days": 0})
    assert any(c["drift_type"] == "business_key_hash_changed" and c["action"] == "block" for c in result["changes"])


def test_partition_hash_change_blocks_by_default() -> None:
    baseline = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    mutated = _df().copy(); mutated.loc[0, "updated_at"] = "2026-04-25T20:00:00"
    current = build_partition_snapshot(mutated, partition_column="business_date", business_keys=["customer_id", "order_id"], watermark_column="updated_at")
    baseline_w = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"], watermark_column="updated_at")
    result = compare_partition_snapshots(baseline_w, current, policy={"closed_partition_grace_days": 0})
    assert any(c["drift_type"] == "partition_hash_changed" and c["action"] == "block" for c in result["changes"])


def test_backfill_mode_allows_historical_changes() -> None:
    baseline = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    current = build_partition_snapshot(_df().drop(index=[1]), partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(baseline, current, policy={"closed_partition_grace_days": 0, "run_mode": "backfill"})
    assert result["can_continue"] is True
    assert result["status"] == "warning"


def test_allow_historical_changes_with_approval_allows() -> None:
    baseline = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    current = build_partition_snapshot(_df().drop(index=[1]), partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(baseline, current, policy={"closed_partition_grace_days": 0, "allow_historical_changes": True, "approval_reference": "CHG-100"})
    assert result["can_continue"] is True


def test_allow_historical_changes_without_required_approval_blocks() -> None:
    baseline = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"])
    current = build_partition_snapshot(_df().drop(index=[1]), partition_column="business_date", business_keys=["customer_id", "order_id"])
    result = compare_partition_snapshots(baseline, current, policy={"closed_partition_grace_days": 0, "allow_historical_changes": True, "approval_reference": None})
    assert result["can_continue"] is False


def test_assert_incremental_safe_raises() -> None:
    with pytest.raises(IncrementalSafetyError):
        assert_incremental_safe({"can_continue": False})


def test_build_incremental_safety_records_none_row_when_no_changes() -> None:
    rows = build_incremental_safety_records({"status": "passed", "can_continue": True, "changes": []}, run_id="r1", dataset_name="d", table_name="t")
    assert rows[0]["drift_type"] == "none"


def test_build_incremental_safety_records_flattens_changes() -> None:
    rows = build_incremental_safety_records({"status": "warning", "can_continue": True, "changes": [{"drift_type": "partition_added", "partition_value": "2026-04-26", "previous_value": None, "current_value": 1, "severity": "info", "action": "allow", "message": "x"}]}, run_id="r1", dataset_name="d", table_name="t")
    assert rows[0]["run_id"] == "r1"
    assert rows[0]["drift_type"] == "partition_added"


def test_incremental_outputs_are_json_serializable() -> None:
    snap = build_partition_snapshot(_df(), partition_column="business_date", business_keys=["customer_id", "order_id"], watermark_column="updated_at")
    result = compare_partition_snapshots(snap, snap)
    records = build_incremental_safety_records(result, run_id="r1", dataset_name="d", table_name="t")
    json.dumps(snap)
    json.dumps(result)
    json.dumps(records)


def test_no_pyspark_import_at_module_import_time() -> None:
    sys.modules.pop("fabric_data_product_framework.drift", None)
    before = set(sys.modules)
    importlib.import_module("fabric_data_product_framework.drift")
    assert "pyspark" not in (set(sys.modules) - before)


def test_spark_path_code_exists_without_topandas_usage() -> None:
    import fabric_data_product_framework.drift as incremental

    source = open(incremental.__file__, encoding="utf-8").read()
    assert "_build_spark_partition_snapshot" in source
    assert "toPandas(" not in source
