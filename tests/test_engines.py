import pandas as pd
import pytest

from fabricops_kit.runtime import (
    UnsupportedDataFrameEngineError,
    detect_dataframe_engine,
    validate_engine,
)


class FakeSparkDataFrame:
    __module__ = "pyspark.sql.dataframe"

    def __init__(self):
        self.schema = {"fields": []}


def test_detect_dataframe_engine_pandas():
    df = pd.DataFrame({"a": [1]})
    assert detect_dataframe_engine(df) == "pandas"


def test_detect_dataframe_engine_fake_spark():
    assert detect_dataframe_engine(FakeSparkDataFrame()) == "spark"


def test_detect_dataframe_engine_unsupported_input_raises():
    with pytest.raises(UnsupportedDataFrameEngineError):
        detect_dataframe_engine({"a": [1]})


def test_validate_engine_rejects_invalid_values():
    with pytest.raises(ValueError):
        validate_engine("duckdb")
