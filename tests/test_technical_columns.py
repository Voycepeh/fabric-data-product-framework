import hashlib
import importlib
import sys
import types

import pandas as pd
import pytest

from fabricops_kit.runtime import detect_dataframe_engine
from fabricops_kit.technical_columns import (
    _non_technical_columns,
    add_audit_columns,
    add_datetime_features,
    add_hash_columns,
    default_technical_columns,
)


class FakeSparkDataFrame:
    __module__ = "pyspark.sql.dataframe"

    def __init__(self, columns=None):
        self.columns = columns or ["id", "updated_at"]
        self.calls = []
        self.schema = {"fields": []}

    def withColumn(self, name, value):
        self.calls.append(("withColumn", name, value))
        if name not in self.columns:
            self.columns.append(name)
        return self


def _install_fake_pyspark():
    class _Expr:
        def __init__(self, value):
            self.value = value

        def __lt__(self, other):
            return ("lt", self.value, other)

        def cast(self, dtype):
            return ("cast", self.value, dtype)

    class _F:
        @staticmethod
        def lit(value):
            return ("lit", value)

        @staticmethod
        def col(name):
            return _Expr(("col", name))

        @staticmethod
        def from_utc_timestamp(c, tz):
            return ("from_utc_timestamp", c, tz)

        @staticmethod
        def to_date(c):
            return ("to_date", c)

        @staticmethod
        def date_format(c, p):
            return ("date_format", c, p)

        @staticmethod
        def hour(c):
            return ("hour", c)

        @staticmethod
        def minute(c):
            return _Expr(("minute", c))

        @staticmethod
        def when(cond, then):
            return types.SimpleNamespace(otherwise=lambda alt: ("when", cond, then, alt))

        @staticmethod
        def concat(*args):
            return ("concat", args)

        @staticmethod
        def current_timestamp():
            return ("current_timestamp",)

        @staticmethod
        def abs(v):
            return ("abs", v)

        @staticmethod
        def hash(v):
            return ("hash", v)

        @staticmethod
        def expr(v):
            return ("expr", v)

        @staticmethod
        def pmod(a, b):
            return ("pmod", a, b)

        @staticmethod
        def sha2(v, n):
            return ("sha2", v, n)

        @staticmethod
        def concat_ws(sep, *cols):
            return ("concat_ws", sep, cols)

        @staticmethod
        def coalesce(*v):
            return ("coalesce", v)

    mod = types.ModuleType("pyspark")
    sql = types.ModuleType("pyspark.sql")
    sql.functions = _F
    mod.sql = sql
    sys.modules["pyspark"] = mod
    sys.modules["pyspark.sql"] = sql


def test_default_technical_columns_include_new_standard_columns():
    cols = default_technical_columns()
    for col in [
        "_pipeline_run_id",
        "_pipeline_name",
        "_pipeline_environment",
        "_source_system",
        "_source_table",
        "_source_extract_timestamp",
        "_record_loaded_timestamp",
        "_notebook_name",
        "_loaded_by",
        "_watermark_value",
        "_partition_bucket",
        "_sample_bucket",
        "_row_ingest_id",
        "_business_key_hash",
        "_row_hash",
    ]:
        assert col in cols


def test_default_technical_columns_include_legacy_ignore_names():
    cols = default_technical_columns()
    for col in ["pipeline_ts", "notebook_name", "loaded_by", "p_bucket", "sample_bucket", "row_ingest_id", "ingest_run_id", "pipeline_run_id", "loaded_at", "run_ingest_id"]:
        assert col in cols


def test_non_technical_columns_excludes_technical_columns():
    df = pd.DataFrame({"id": [1], "amount": [10], "_pipeline_run_id": ["x"], "pipeline_ts": ["y"]})
    assert _non_technical_columns(df) == ["id", "amount"]


def test_add_datetime_features_pandas_creates_expected_columns():
    df = pd.DataFrame({"event_ts": ["2026-01-01T00:45:00Z"]})
    out = add_datetime_features(df, "event_ts", prefix="EVENT", engine="pandas")
    assert out["EVENT_DATE_UTC8"].iloc[0] == "2026-01-01"
    assert out["EVENT_TIME_UTC8"].iloc[0] == "08:45:00"
    assert out["EVENT_HOUR_UTC8"].iloc[0] == 8
    assert out["EVENT_TIME_BLOCK_30_MIN"].iloc[0] == "08:30"
    assert "EVENT_DTM_UTC8" in out.columns


def test_add_datetime_features_validates_missing_column():
    with pytest.raises(ValueError):
        add_datetime_features(pd.DataFrame({"a": [1]}), "missing")


def test_add_audit_columns_pandas_defaults_and_optional_metadata():
    df = pd.DataFrame({"id": [1], "updated_at": ["2026-01-01T00:00:00Z"]})
    out = add_audit_columns(
        df,
        pipeline_name="orders_pipeline",
        environment="dev",
        source_system="crm",
        source_table="orders",
        source_extract_timestamp="2026-01-01T00:00:00Z",
        watermark_column="updated_at",
        bucket_column="id",
        engine="pandas",
    )
    assert out["_pipeline_run_id"].iloc[0]
    assert out["_notebook_name"].iloc[0] == "local_notebook"
    assert out["_loaded_by"].iloc[0] == "local_user"
    assert out["_pipeline_name"].iloc[0] == "orders_pipeline"
    assert out["_watermark_value"].iloc[0] == "2026-01-01T00:00:00Z"
    assert "_partition_bucket" in out.columns and "_sample_bucket" in out.columns and "_row_ingest_id" in out.columns


def test_add_audit_columns_validations():
    with pytest.raises(ValueError):
        add_audit_columns(pd.DataFrame({"a": [1]}), watermark_column="missing", engine="pandas")
    with pytest.raises(ValueError):
        add_audit_columns(pd.DataFrame({"a": [1]}), bucket_column="missing", engine="pandas")
    with pytest.raises(ValueError):
        add_audit_columns(pd.DataFrame({"a": [1]}), bucket_column="a", bucket_size=999, engine="pandas")


def test_add_hash_columns_pandas_default_row_hash_and_nulls():
    df = pd.DataFrame({"id": [1], "name": [None], "_pipeline_run_id": ["ignore"]})
    out = add_hash_columns(df, business_keys=["id"], engine="pandas")
    assert out["_business_key_hash"].iloc[0] == hashlib.sha256("1".encode("utf-8")).hexdigest()
    assert out["_row_hash"].iloc[0] == hashlib.sha256("1||<NULL>".encode("utf-8")).hexdigest()


def test_add_hash_columns_validation_cases():
    with pytest.raises(ValueError):
        add_hash_columns(pd.DataFrame({"id": [1]}), include_business_key_hash=True, business_keys=None)
    with pytest.raises(ValueError):
        add_hash_columns(pd.DataFrame({"id": [1]}), business_keys=["missing"])


def test_fake_spark_paths_for_core_functions():
    _install_fake_pyspark()
    spark_df = FakeSparkDataFrame(columns=["id", "event_ts", "updated_at"])
    assert detect_dataframe_engine(spark_df) == "spark"
    add_datetime_features(spark_df, "event_ts", prefix="EVENT", engine="spark")
    add_audit_columns(spark_df, bucket_column="id", engine="spark")
    add_hash_columns(spark_df, business_keys=["id"], engine="spark")
    assert any(call[1] == "EVENT_DATE_UTC8" for call in spark_df.calls)
    assert any(call[1] == "_partition_bucket" for call in spark_df.calls)
    assert any(call[1] == "_row_hash" for call in spark_df.calls)


def test_module_imports_without_pyspark_installed():
    sys.modules.pop("pyspark", None)
    sys.modules.pop("pyspark.sql", None)
    module = importlib.reload(importlib.import_module("fabricops_kit.technical_columns"))
    assert hasattr(module, "add_audit_columns")
    assert "pyspark.sql" not in sys.modules
