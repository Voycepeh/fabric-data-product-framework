from pathlib import Path

import pandas as pd
import pytest

from fabricops_kit.quality import (
    assert_data_product_passed,
    build_runtime_context_from_contract,
    load_data_contract,
    normalize_data_product_contract,
    data_product_contract_to_dict,
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


def _contract(refresh_mode=None):
    c = {
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
    if refresh_mode is not None:
        c["refresh"] = {"mode": refresh_mode}
    return c


def _source_df():
    return pd.DataFrame([{"order_id": 1, "updated_at": "2026-01-01T00:00:00Z", "order_date": "2026-01-01", "amount": 10.0}, {"order_id": 2, "updated_at": "2026-01-01T00:00:00Z", "order_date": "2026-01-01", "amount": 20.0}])


def test_validate_contract_full_no_partition_column_passes():
    c = _contract("full")
    del c["keys"]["partition_column"]
    assert validate_data_contract_shape(c) == []


def test_validate_contract_missing_mode_defaults_full():
    c = _contract(None)
    del c["keys"]["partition_column"]
    assert validate_data_contract_shape(c) == []


def test_incremental_missing_partition_fails_validation():
    c = _contract("incremental")
    del c["keys"]["partition_column"]
    assert any("partition_column" in e for e in validate_data_contract_shape(c))


def test_load_data_contract_accepts_dict_and_path(tmp_path: Path):
    assert load_data_contract(_contract()).dataset["name"] == "orders"
    assert load_data_contract(_contract())["dataset"]["name"] == "orders"
    f = tmp_path / "contract.yml"
    f.write_text(
        "dataset:\n"
        "  name: orders\n"
        "source:\n"
        "  table: raw.orders\n"
        "target:\n"
        "  table: curated.orders\n"
        "metadata:\n"
        "  source_profile_table: m.source_profile\n"
        "  output_profile_table: m.output_profile\n"
        "  schema_snapshot_table: m.schema_snapshot\n"
        "  partition_snapshot_table: m.partition_snapshot\n"
        "  quality_result_table: m.quality_result\n"
        "  quarantine_table: m.quarantine\n"
        "  contract_validation_table: m.contract_validation\n"
        "  lineage_table: m.lineage\n"
        "  run_summary_table: m.run_summary\n"
        "  dataset_runs_table: m.dataset_runs\n",
        encoding="utf-8",
    )
    assert load_data_contract(f).dataset["name"] == "orders"


def test_build_runtime_context_from_contract_uses_contract_fields():
    ctx = build_runtime_context_from_contract(_contract(), overrides={"run_id": "run_123"})
    assert (ctx["dataset_name"], ctx["environment"], ctx["run_id"]) == ("orders", "dev", "run_123")


def test_assert_data_product_passed_raises_for_failed_status():
    with pytest.raises(RuntimeError):
        assert_data_product_passed({"status": "failed"})


def test_incremental_invalid_partition_column_fails_runner_and_no_target_write():
    spark = _FakeSpark(_source_df())
    c = _contract("incremental")
    c["keys"]["partition_column"] = "missing_partition"
    result = run_data_product(spark=spark, contract=c, source_df=_source_df())
    assert result["can_continue"] is False
    assert "silver.orders" not in [t for t, _, _ in spark.writes]


def test_legacy_write_false_disables_target_and_metadata():
    spark = _FakeSpark(_source_df())
    run_data_product(spark=spark, contract=_contract("full"), source_df=_source_df(), write=False)
    assert spark.writes == []


def test_write_flags_disable_quarantine_write_truthfully():
    spark = _FakeSpark(_source_df())
    bad = _source_df(); bad.loc[0, "order_id"] = None
    result = run_data_product(spark=spark, contract=_contract("full"), source_df=bad, write_target=False, write_metadata=False)
    assert result["quarantine_written"] is False


def test_quality_metadata_rows_include_run_id():
    spark = _FakeSpark(_source_df())
    result = run_data_product(spark=spark, contract=_contract("full"), source_df=_source_df())
    quality_writes = [df for table, _, df in spark.writes if table == "meta.quality_result"]
    assert quality_writes
    assert "run_id" in quality_writes[0].columns
    assert result["quarantine_row_count"] >= 0


def test_normalize_minimal_contract_defaults_applied():
    normalized = normalize_data_product_contract({"dataset": {"name": "orders"}, "source": {"table": "raw.orders"}, "target": {"table": "curated.orders"}})
    assert normalized.runtime.dataset_name == "orders"
    assert normalized.source.format == "delta"
    assert normalized.target.mode == "append"


def test_backward_compatibility_upstream_downstream_mapping():
    normalized = normalize_data_product_contract({
        "dataset": {"name": "orders"},
        "source": {},
        "target": {},
        "upstream_contract": {"table_name": "raw.orders", "business_keys": ["order_id"], "required_columns": ["order_id"], "watermark_column": "updated_at"},
        "downstream_contract": {"table_name": "curated.orders", "required_columns": ["order_id"]},
        "metadata": _contract()["metadata"],
    })
    assert normalized.source.table == "raw.orders"
    assert normalized.target.table == "curated.orders"
    assert normalized.source.business_keys == ["order_id"]


def test_data_product_contract_to_dict_is_plain_dict():
    normalized = normalize_data_product_contract(_contract())
    as_dict = data_product_contract_to_dict(normalized)
    assert isinstance(as_dict, dict)
    assert as_dict["source"]["table"] == "bronze.orders"


def test_run_data_product_accepts_normalized_contract_object():
    spark = _FakeSpark(_source_df())
    normalized = normalize_data_product_contract(_contract("full"))
    result = run_data_product(spark=spark, contract=normalized, source_df=_source_df())
    assert result["status"] in {"passed", "failed"}


def test_runtime_contract_uses_target_required_columns():
    c = _contract("full")
    c["target"]["required_columns"] = ["order_id", "updated_at", "missing_col"]
    spark = _FakeSpark(_source_df())
    result = run_data_product(spark=spark, contract=c, source_df=_source_df())
    assert result["status"] == "failed"


def test_data_product_contract_without_raw_builds_effective_contract():
    normalized = normalize_data_product_contract(_contract("full"))
    normalized.raw = {}
    assert normalized["schema"]["required_output_columns"] == ["order_id", "updated_at"]
    assert normalized["keys"]["business_keys"] == ["order_id"]


def test_transform_receives_effective_normalized_contract():
    seen = {}

    def _transform(df, _ctx, contract):
        seen["contract"] = contract
        return df

    spark = _FakeSpark(_source_df())
    run_data_product(spark=spark, contract=_contract("full"), source_df=_source_df(), transform=_transform)
    assert seen["contract"]["source"]["table"] == "bronze.orders"
    assert "schema" in seen["contract"]


def test_incremental_validation_messages_reference_source_fields():
    c = _contract("incremental")
    del c["keys"]["partition_column"]
    c["keys"]["business_keys"] = []
    errors = validate_data_contract_shape(c)
    assert "source.partition_column" in " | ".join(errors)
    assert "source.business_keys" in " | ".join(errors)


def test_run_data_product_includes_dq_workflow_result():
    spark = _FakeSpark(_source_df())
    result = run_data_product(spark=spark, contract=_contract("full"), source_df=_source_df())
    assert "dq_workflow" in result
    assert "quality_result" in result["dq_workflow"]


def test_run_data_product_calls_schema_drift_wrappers(monkeypatch):
    spark = _FakeSpark(_source_df())
    seen = {"check": 0}

    monkeypatch.setattr("fabricops_kit.quality.load_latest_schema_snapshot", lambda *args, **kwargs: None)

    def _check_schema_drift(**kwargs):
        seen["check"] += 1
        return {"status": "no_baseline", "can_continue": True}

    monkeypatch.setattr("fabricops_kit.quality.check_schema_drift", _check_schema_drift)
    monkeypatch.setattr("fabricops_kit.quality.build_and_write_schema_snapshot", lambda **kwargs: {"written": True})

    c = _contract("full")
    c["drift"]["schema_enabled"] = True
    result = run_data_product(spark=spark, contract=c, source_df=_source_df())
    assert seen["check"] == 1
    assert result["drift"]["schema"]["status"] == "no_baseline"


def test_data_drift_second_run_uses_written_baseline(monkeypatch):
    spark = _FakeSpark(_source_df())
    c = _contract("full")
    c["drift"]["data_enabled"] = True
    c["drift"]["data_policy"] = {"partition_column": "order_date", "business_keys": ["order_id"], "watermark_column": "updated_at"}
    state = {"baseline": None}

    def _load_latest_partition_snapshot(_spark, _table, dataset_name, table_name):
        assert table_name == "silver.orders"
        return state["baseline"]

    def _build_and_write_partition_snapshot(**kwargs):
        state["baseline"] = [{"partition_value": "2026-01-01", "row_count": 2}]
        return {"written": True, "snapshot": state["baseline"]}

    def _check_partition_drift(**kwargs):
        return {"status": "no_baseline" if kwargs.get("baseline_snapshot") is None else "passed", "can_continue": True}

    monkeypatch.setattr("fabricops_kit.quality.load_latest_partition_snapshot", _load_latest_partition_snapshot)
    monkeypatch.setattr("fabricops_kit.quality.build_and_write_partition_snapshot", _build_and_write_partition_snapshot)
    monkeypatch.setattr("fabricops_kit.quality.check_partition_drift", _check_partition_drift)

    first = run_data_product(spark=spark, contract=c, source_df=_source_df())
    second = run_data_product(spark=spark, contract=c, source_df=_source_df())
    assert first["drift"]["data"]["status"] == "no_baseline"
    assert second["drift"]["data"]["status"] == "passed"


def test_data_drift_missing_column_fails_cleanly():
    spark = _FakeSpark(_source_df())
    c = _contract("full")
    c["drift"]["data_enabled"] = True
    c["drift"]["data_policy"] = {"partition_column": "order_date", "business_keys": ["order_id"], "watermark_column": "updated_at"}

    def _drop_partition(df, _ctx, _contract):
        return df.drop(columns=["order_date"])

    result = run_data_product(spark=spark, contract=c, source_df=_source_df(), transform=_drop_partition)
    assert result["status"] == "failed"
    assert result["can_continue"] is False
    assert "errors" in result
    assert "runtime_context" in result
