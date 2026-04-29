import hashlib
import importlib
import json
import sys
import types

import pandas as pd
import pytest

from fabric_data_product_framework.engines import detect_dataframe_engine
from fabric_data_product_framework.technical_columns import (
    add_business_key_hash,
    add_datetime_parts,
    add_literal_column,
    add_loaded_at,
    add_pipeline_metadata,
    add_pipeline_run_id,
    add_row_hash,
    add_source_metadata,
    add_standard_technical_columns,
    add_watermark_value,
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

    def toPandas(self):
        raise AssertionError("Should not convert Spark DataFrame to pandas")


def _install_fake_pyspark():
    class _F:
        @staticmethod
        def lit(value):
            return ("lit", value)

        @staticmethod
        def col(name):
            return ("col", name)

    mod = types.ModuleType("pyspark")
    sql = types.ModuleType("pyspark.sql")
    sql.functions = _F
    mod.sql = sql
    sys.modules["pyspark"] = mod
    sys.modules["pyspark.sql"] = sql


def test_add_literal_column_returns_copy_and_does_not_mutate_original():
    df = pd.DataFrame({"id": [1, 2]})
    out = add_literal_column(df, "_pipeline_run_id", "run-1", engine="pandas")
    assert "_pipeline_run_id" not in df.columns
    assert out["_pipeline_run_id"].tolist() == ["run-1", "run-1"]


def test_add_pipeline_run_id_adds_expected_value():
    df = pd.DataFrame({"id": [1]})
    out = add_pipeline_run_id(df, run_id="run-42")
    assert out["_pipeline_run_id"].iloc[0] == "run-42"


def test_add_pipeline_metadata_adds_optional_fields():
    df = pd.DataFrame({"id": [1]})
    out = add_pipeline_metadata(df, run_id="r", pipeline_name="p", environment="dev")
    assert out["_pipeline_run_id"].iloc[0] == "r"
    assert out["_pipeline_name"].iloc[0] == "p"
    assert out["_pipeline_environment"].iloc[0] == "dev"


def test_add_source_metadata_adds_fields():
    df = pd.DataFrame({"id": [1]})
    out = add_source_metadata(df, source_system="synthetic", source_table="orders", source_extract_timestamp="2026-01-01T00:00:00Z")
    assert out["_source_system"].iloc[0] == "synthetic"
    assert out["_source_table"].iloc[0] == "orders"
    assert out["_source_extract_timestamp"].iloc[0] == "2026-01-01T00:00:00Z"


def test_add_loaded_at_uses_provided_timestamp():
    df = pd.DataFrame({"id": [1]})
    out = add_loaded_at(df, timestamp="2026-01-01T00:00:00Z")
    assert out["_record_loaded_timestamp"].iloc[0] == "2026-01-01T00:00:00Z"


def test_add_watermark_value_copies_values():
    df = pd.DataFrame({"updated_at": ["a", "b"]})
    out = add_watermark_value(df, watermark_column="updated_at")
    assert out["_watermark_value"].tolist() == ["a", "b"]


def test_add_row_hash_stable_and_excludes_technical_by_default():
    df = pd.DataFrame({"id": [1], "name": ["a"], "_pipeline_run_id": ["ignore"]})
    out = add_row_hash(df)
    expected = hashlib.sha256("1||a".encode("utf-8")).hexdigest()
    assert out["_row_hash"].iloc[0] == expected


def test_add_business_key_hash_stable():
    df = pd.DataFrame({"customer_id": [123]})
    out = add_business_key_hash(df, business_keys=["customer_id"])
    expected = hashlib.sha256("123".encode("utf-8")).hexdigest()
    assert out["_business_key_hash"].iloc[0] == expected


def test_add_datetime_parts_creates_expected_fields():
    df = pd.DataFrame({"updated_at": ["2026-01-01T00:45:00Z"]})
    out = add_datetime_parts(df, "updated_at", engine="pandas")
    assert out["updated_at_date"].iloc[0] == "2026-01-01"
    assert out["updated_at_time"].iloc[0] == "08:45:00"
    assert out["updated_at_hour"].iloc[0] == 8
    assert out["updated_at_time_block_30min"].iloc[0] == "08:30"


def test_add_standard_technical_columns_adds_expected_columns():
    df = pd.DataFrame({"customer_id": [1], "updated_at": ["2026-01-01T00:00:00Z"]})
    out = add_standard_technical_columns(df, run_id="run-1", environment="dev", source_table="orders", watermark_column="updated_at", business_keys=["customer_id"], engine="pandas")
    for col in ["_pipeline_run_id", "_pipeline_environment", "_source_table", "_record_loaded_timestamp", "_watermark_value", "_business_key_hash", "_row_hash"]:
        assert col in out.columns


def test_missing_watermark_column_raises_value_error():
    with pytest.raises(ValueError):
        add_watermark_value(pd.DataFrame({"a": [1]}), watermark_column="missing")


def test_missing_business_key_raises_value_error():
    with pytest.raises(ValueError):
        add_business_key_hash(pd.DataFrame({"a": [1]}), business_keys=["missing"])


def test_invalid_engine_raises_value_error():
    with pytest.raises(ValueError):
        add_pipeline_run_id(pd.DataFrame({"a": [1]}), run_id="x", engine="duckdb")


def test_output_is_json_and_pandas_friendly():
    df = pd.DataFrame({"customer_id": [1, 2]})
    out = add_business_key_hash(df, business_keys=["customer_id"])
    json.dumps(out.to_dict(orient="records"))


def test_fake_spark_detection_and_withcolumn_calls():
    _install_fake_pyspark()
    spark_df = FakeSparkDataFrame()
    assert detect_dataframe_engine(spark_df) == "spark"
    add_literal_column(spark_df, "_pipeline_run_id", "run-1", engine="spark")
    add_pipeline_run_id(spark_df, run_id="run-2", engine="spark")
    assert spark_df.calls[0][0] == "withColumn"
    assert spark_df.calls[1][0] == "withColumn"


def test_add_watermark_value_missing_column_raises_before_spark_execution():
    _install_fake_pyspark()
    spark_df = FakeSparkDataFrame(columns=["id"])
    with pytest.raises(ValueError):
        add_watermark_value(spark_df, watermark_column="updated_at", engine="spark")
    assert spark_df.calls == []


def test_no_pyspark_import_at_module_import_time():
    sys.modules.pop("pyspark", None)
    sys.modules.pop("pyspark.sql", None)
    module = importlib.reload(importlib.import_module("fabric_data_product_framework.technical_columns"))
    assert hasattr(module, "add_literal_column")
    assert "pyspark.sql" not in sys.modules
