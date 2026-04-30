from pathlib import Path

import pandas as pd
import pytest

from fabric_data_product_framework.data_contract import (
    assert_data_product_passed,
    build_runtime_context_from_contract,
    load_data_contract,
    run_data_product,
    validate_data_contract_shape,
)


class _FakeWriter:
    def __init__(self, spark, df):
        self.spark = spark
        self.df = df
        self._mode = "append"

    def mode(self, mode):
        self._mode = mode
        return self

    def saveAsTable(self, table):
        self.spark.writes.append((table, self._mode, self.df.copy()))


class _FakeSparkDF:
    def __init__(self, spark, df):
        self.spark = spark
        self._df = df

    @property
    def write(self):
        return _FakeWriter(self.spark, self._df)


class _FakeSpark:
    def __init__(self, source_df):
        self.source_df = source_df
        self.writes = []

    def table(self, _):
        return self.source_df.copy()

    def createDataFrame(self, rows):
        return _FakeSparkDF(self, pd.DataFrame(rows))


def _valid_contract():
    return {
        "dataset": {"name": "orders", "description": "desc", "owner": "owner", "approved_usage": "analytics"},
        "environment": {"name": "dev", "metadata_schema": "meta"},
        "source": {"table": "bronze.orders", "format": "delta"},
        "target": {"table": "silver.orders", "mode": "append", "format": "delta"},
        "keys": {"business_keys": ["order_id"], "watermark_column": "updated_at", "partition_column": "order_date"},
        "schema": {"required_source_columns": ["order_id", "updated_at"], "required_output_columns": ["order_id", "updated_at"]},
        "quality": {"rules": [{"rule_id": "DQ001", "rule_type": "not_null", "column": "order_id", "severity": "critical"}]},
        "drift": {"schema_policy": {}, "incremental_policy": {}},
        "metadata": {"source_profile_table": "meta.source_profile", "output_profile_table": "meta.output_profile", "schema_snapshot_table": "meta.schema_snapshot", "partition_snapshot_table": "meta.partition_snapshot", "quality_result_table": "meta.quality_result", "quarantine_table": "meta.quarantine", "contract_validation_table": "meta.contract_validation", "lineage_table": "meta.lineage", "run_summary_table": "meta.run_summary", "dataset_runs_table": "meta.dataset_runs"},
    }


def _source_df():
    return pd.DataFrame(
        [
            {"order_id": 1, "updated_at": "2026-01-01T00:00:00Z", "order_date": "2026-01-01", "amount": 10.0},
            {"order_id": 2, "updated_at": "2026-01-01T00:00:00Z", "order_date": "2026-01-01", "amount": 20.0},
        ]
    )


def test_validate_data_contract_shape_passes_for_complete_contract():
    assert validate_data_contract_shape(_valid_contract()) == []


def test_validate_data_contract_shape_reports_missing_sections():
    contract = _valid_contract(); del contract["metadata"]
    assert "Missing required section: metadata" in validate_data_contract_shape(contract)


def test_load_data_contract_accepts_dict_and_path(tmp_path: Path):
    loaded_dict = load_data_contract(_valid_contract())
    assert loaded_dict["dataset"]["name"] == "orders"
    contract_file = tmp_path / "contract.yml"
    contract_file.write_text("dataset:\n  name: orders\n", encoding="utf-8")
    assert load_data_contract(contract_file)["dataset"]["name"] == "orders"


def test_build_runtime_context_from_contract_uses_contract_fields():
    ctx = build_runtime_context_from_contract(_valid_contract(), overrides={"run_id": "run_123"})
    assert (ctx["dataset_name"], ctx["environment"], ctx["run_id"]) == ("orders", "dev", "run_123")


def test_assert_data_product_passed_raises_for_failed_status():
    with pytest.raises(RuntimeError):
        assert_data_product_passed({"status": "failed"})


def test_run_data_product_happy_path_writes_target_and_metadata():
    spark = _FakeSpark(_source_df())
    result = run_data_product(spark=spark, contract=_valid_contract(), source_df=_source_df())
    assert result["status"] == "passed"
    tables = [t for t, _, _ in spark.writes]
    assert "silver.orders" in tables
    assert "meta.source_profile" in tables and "meta.output_profile" in tables


def test_run_data_product_quarantine_rules_wiring_no_type_error():
    spark = _FakeSpark(_source_df())
    bad = _source_df(); bad.loc[0, "order_id"] = None
    result = run_data_product(spark=spark, contract=_valid_contract(), source_df=bad)
    assert result["status"] == "failed"


def test_run_data_product_enforces_schema_required_columns():
    spark = _FakeSpark(_source_df())
    bad = _source_df().drop(columns=["updated_at"])
    result = run_data_product(spark=spark, contract=_valid_contract(), source_df=bad)
    assert result["contract_validation_result"]["can_continue"] is False


def test_quality_fail_blocks_target_write():
    spark = _FakeSpark(_source_df())
    bad = _source_df(); bad.loc[0, "order_id"] = None
    run_data_product(spark=spark, contract=_valid_contract(), source_df=bad)
    assert "silver.orders" not in [t for t, _, _ in spark.writes]


def test_dry_run_disables_target_and_metadata_writes():
    spark = _FakeSpark(_source_df())
    run_data_product(spark=spark, contract=_valid_contract(), source_df=_source_df(), write_target=False, write_metadata=False)
    assert spark.writes == []
