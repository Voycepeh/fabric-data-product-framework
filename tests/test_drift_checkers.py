import json

import pandas as pd

from fabric_data_product_framework import drift_checkers


class _FakeWriter:
    def __init__(self, parent, spark):
        self._parent = parent
        self._spark = spark
        self._mode = None

    def mode(self, mode):
        self._mode = mode
        return self

    def saveAsTable(self, table):
        self._spark.saved = {"table": table, "mode": self._mode, "records": self._parent.records}


class _FakeSparkDF:
    def __init__(self, records, spark):
        self.records = records
        self.write = _FakeWriter(self, spark)


class _FakeSpark:
    def __init__(self, table_rows=None, raise_on_table=False):
        self._table_rows = table_rows or []
        self._raise_on_table = raise_on_table
        self.saved = None

    def createDataFrame(self, records):
        return _FakeSparkDF(records, self)

    def table(self, _):
        if self._raise_on_table:
            raise Exception("missing")

        class T:
            def __init__(self, rows):
                self._rows = rows

            def collect(self):
                return self._rows

        return T(self._table_rows)


def test_check_schema_drift_no_baseline():
    df = pd.DataFrame({"a": [1]})
    result = drift_checkers.check_schema_drift(df, "ds", "tbl", baseline_snapshot=None, engine="pandas")
    assert result["status"] == "no_baseline"
    assert result["can_continue"] is True


def test_check_schema_drift_uses_existing_helpers(monkeypatch):
    calls = {"build": 0, "compare": 0}
    monkeypatch.setattr(drift_checkers, "build_schema_snapshot", lambda *args, **kwargs: calls.__setitem__("build", calls["build"] + 1) or {"columns": []})
    monkeypatch.setattr(drift_checkers, "compare_schema_snapshots", lambda *args, **kwargs: calls.__setitem__("compare", calls["compare"] + 1) or {"can_continue": True})
    out = drift_checkers.check_schema_drift(object(), "ds", "tbl", baseline_snapshot={"columns": []}, engine="spark")
    assert out["status"] == "passed"
    assert calls == {"build": 1, "compare": 1}


def test_build_and_write_schema_snapshot_json_safe():
    spark = _FakeSpark()
    df = pd.DataFrame({"a": [1]})
    out = drift_checkers.build_and_write_schema_snapshot(spark, df, "ds", "tbl", "fw_metadata.schema", run_id="r1", engine="pandas")
    assert out["written"] is True
    assert spark.saved["table"] == "fw_metadata.schema"
    assert isinstance(out["records"][0]["schema_snapshot_json"], str)
    json.loads(out["records"][0]["schema_snapshot_json"])


def test_load_latest_schema_snapshot_none_when_missing_table_or_rows():
    assert drift_checkers.load_latest_schema_snapshot(_FakeSpark(raise_on_table=True), "m", "ds", "tbl") is None
    assert drift_checkers.load_latest_schema_snapshot(_FakeSpark([]), "m", "ds", "tbl") is None


def test_check_partition_drift_no_baseline(monkeypatch):
    monkeypatch.setattr(drift_checkers, "build_partition_snapshot", lambda *args, **kwargs: [{"partition_value": "2026-01-01"}])
    out = drift_checkers.check_partition_drift(object(), "ds", "tbl", partition_column="p", business_keys=["id"], baseline_snapshot=None)
    assert out["status"] == "no_baseline"


def test_check_partition_drift_uses_existing_helpers(monkeypatch):
    calls = {"build": 0, "compare": 0}
    monkeypatch.setattr(drift_checkers, "build_partition_snapshot", lambda *args, **kwargs: calls.__setitem__("build", calls["build"] + 1) or [{"partition_value": "2026-01-01"}])
    monkeypatch.setattr(drift_checkers, "compare_partition_snapshots", lambda *args, **kwargs: calls.__setitem__("compare", calls["compare"] + 1) or {"can_continue": True})
    out = drift_checkers.check_partition_drift(object(), "ds", "tbl", partition_column="p", business_keys=["id"], baseline_snapshot=[{"partition_value": "2026-01-01"}])
    assert out["status"] == "passed"
    assert calls == {"build": 1, "compare": 1}


def test_build_and_write_partition_snapshot_json_safe(monkeypatch):
    monkeypatch.setattr(drift_checkers, "build_partition_snapshot", lambda *args, **kwargs: [{"partition_value": "2026-01-01"}])
    spark = _FakeSpark()
    out = drift_checkers.build_and_write_partition_snapshot(spark, object(), "ds", "tbl", "fw_metadata.partition", partition_column="business_date", business_keys=["order_id"])
    assert out["written"] is True
    assert isinstance(out["records"][0]["partition_snapshot_json"], str)
    json.loads(out["records"][0]["partition_snapshot_json"])


def test_check_profile_drift_no_baseline():
    out = drift_checkers.check_profile_drift({"row_count": 10}, baseline_profile=None)
    assert out["status"] == "no_baseline"


def test_check_profile_drift_detects_row_count_drift():
    base = {"row_count": 100, "columns": []}
    curr = {"row_count": 1000, "columns": []}
    out = drift_checkers.check_profile_drift(curr, base)
    assert out["status"] == "failed"


def test_check_profile_drift_detects_null_percent_drift():
    base = {"row_count": 100, "columns": [{"column_name": "a", "null_pct": 0}]}
    curr = {"row_count": 100, "columns": [{"column_name": "a", "null_pct": 50}]}
    out = drift_checkers.check_profile_drift(curr, base)
    assert out["status"] == "failed"


def test_summarize_drift_results_failed_and_cannot_continue():
    out = drift_checkers.summarize_drift_results(
        schema_drift_result={"status": "passed", "can_continue": True},
        partition_drift_result={"status": "failed", "can_continue": False},
        profile_drift_result={"status": "passed", "can_continue": True},
    )
    assert out["status"] == "failed"
    assert out["can_continue"] is False
