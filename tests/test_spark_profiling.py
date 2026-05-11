import pytest

from fabricops_kit.data_profiling import (
    generate_metadata_profile,
    profile_dataframe_to_metadata,
)


pyspark = pytest.importorskip("pyspark")
from pyspark.sql import SparkSession


@pytest.fixture(scope="module")
def spark_session():
    spark = SparkSession.builder.master("local[1]").appName("profiling-tests").getOrCreate()
    yield spark
    spark.stop()


def _make_spark_df(spark):
    return spark.createDataFrame(
        [
            {"id": 1, "status": "OPEN", "pipeline_ts": "2026-01-01"},
            {"id": 2, "status": None, "pipeline_ts": "2026-01-01"},
        ]
    )


def test_profile_dataframe_to_metadata_schema_and_exclusion(spark_session):
    df = _make_spark_df(spark_session)
    out = profile_dataframe_to_metadata(df, "orders_clean")
    expected = {
        "TABLE_NAME", "RUN_TIMESTAMP", "COLUMN_NAME", "DATA_TYPE", "ROW_COUNT", "NULL_COUNT",
        "NULL_PERCENT", "DISTINCT_COUNT", "DISTINCT_PERCENT", "MIN_VALUE", "MAX_VALUE"
    }
    assert set(out.columns) == expected
    profiled_columns = {r["COLUMN_NAME"] for r in out.collect()}
    assert "pipeline_ts" not in profiled_columns
    assert {"id", "status"}.issubset(profiled_columns)


def test_zero_row_dataframe_no_divide_by_zero(spark_session):
    schema = "id int, status string"
    empty_df = spark_session.createDataFrame([], schema=schema)
    out = profile_dataframe_to_metadata(empty_df, "orders_clean")
    rows = out.collect()
    assert all(r["ROW_COUNT"] == 0 for r in rows)
    assert all(r["NULL_COUNT"] == 0 for r in rows)
    assert all(r["NULL_PERCENT"] == 0.0 for r in rows)
    assert all(r["DISTINCT_COUNT"] == 0 for r in rows)
    assert all(r["DISTINCT_PERCENT"] == 0.0 for r in rows)
    assert all(r["MIN_VALUE"] is None for r in rows)
    assert all(r["MAX_VALUE"] is None for r in rows)


def test_odi_wrapper_matches_new_function_shape(spark_session):
    df = _make_spark_df(spark_session)
    out_new = profile_dataframe_to_metadata(df, "orders_clean")
    out_old = generate_metadata_profile(df, "orders_clean")
    assert out_new.columns == out_old.columns
    assert out_new.count() == out_old.count()
