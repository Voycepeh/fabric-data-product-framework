import json
import sys
import types

import pandas as pd

from fabric_data_product_framework.profiling import (
    default_technical_columns,
    flatten_profile_for_metadata,
    profile_dataframe,
)


class FakeRow(dict):
    def asDict(self):
        return dict(self)


class FakeField:
    def __init__(self, name, data_type):
        self.name = name
        self.dataType = data_type


class FakeSchema:
    def __init__(self, fields):
        self.fields = fields


class FakeSparkDataFrame:
    __module__ = "pyspark.sql.dataframe"

    def __init__(self):
        self.columns = ["id", "_pipeline_run_id"]
        self.schema = FakeSchema([FakeField("id", "int"), FakeField("_pipeline_run_id", "string")])

    def count(self):
        return 3

    def agg(self, *exprs):
        col = exprs[0].col_name
        if col == "id":
            return FakeCollect([FakeRow(non_null_count=3, distinct_count=2, min_value=1, max_value=2, mean_value=1.3333, std_value=0.5773)])
        return FakeCollect([FakeRow(non_null_count=2, distinct_count=2, min_value="run1", max_value="run2")])

    def select(self, col):
        values = [1, 2, 1] if col == "id" else ["run1", None, "run2"]
        return FakeSelect(col, values)

    def groupBy(self, col):
        values = [{col: 1, "count": 2}, {col: 2, "count": 1}] if col == "id" else [{col: "run1", "count": 1}, {col: "run2", "count": 1}]
        return FakeGroup(values)


class FakeCollect:
    def __init__(self, rows):
        self._rows = rows

    def collect(self):
        return self._rows


class FakeSelect:
    def __init__(self, col, values):
        self.col = col
        self.values = [v for v in values if v is not None]

    def where(self, *_):
        return self

    def limit(self, n):
        return FakeCollect([FakeRow({self.col: v}) for v in self.values[:n]])


class FakeGroup:
    def __init__(self, rows):
        self.rows = rows

    def count(self):
        return self

    def orderBy(self, *_):
        return self

    def limit(self, n):
        return FakeCollect([FakeRow(r) for r in self.rows[:n]])


class _FakeColExpr:
    def __init__(self, col_name):
        self.col_name = col_name

    def alias(self, _):
        return self

    def isNotNull(self):
        return self


class _FakeF:
    @staticmethod
    def col(col_name):
        return _FakeColExpr(col_name)

    @staticmethod
    def count(expr):
        return expr

    @staticmethod
    def countDistinct(expr):
        return expr

    @staticmethod
    def min(expr):
        return expr

    @staticmethod
    def max(expr):
        return expr

    @staticmethod
    def mean(expr):
        return expr

    @staticmethod
    def stddev(expr):
        return expr

    @staticmethod
    def desc(_):
        return None


def _install_fake_pyspark():
    mod = types.ModuleType("pyspark")
    sql = types.ModuleType("pyspark.sql")
    sql.functions = _FakeF
    mod.sql = sql
    sys.modules["pyspark"] = mod
    sys.modules["pyspark.sql"] = sql


def test_pandas_paths_still_work():
    df = pd.DataFrame({"a": [1, 2]})
    assert profile_dataframe(df, engine="pandas")["engine"] == "pandas"
    assert profile_dataframe(df, engine="auto")["engine"] == "pandas"


def test_flatten_profile_for_metadata_and_exclusions_jsonable():
    profile = {
        "dataset_name": "synthetic_orders",
        "engine": "spark",
        "row_count": 3,
        "generated_at": "2026-01-01T00:00:00Z",
        "columns": [
            {"column_name": "id", "data_type": "int", "non_null_count": 3, "null_count": 0, "null_pct": 0.0, "distinct_count": 2, "distinct_pct": 66.6, "min_value": 1, "max_value": 2, "mean_value": 1.5, "median_value": None, "std_value": 0.5, "sample_values": [1, 2], "top_values": [{"value": 1, "count": 2}], "inferred_semantic_type": "identifier"},
            {"column_name": "_pipeline_run_id", "data_type": "string", "non_null_count": 3, "null_count": 0, "null_pct": 0.0, "distinct_count": 2, "distinct_pct": 66.6, "min_value": "a", "max_value": "b", "mean_value": None, "median_value": None, "std_value": None, "sample_values": ["a"], "top_values": [{"value": "a", "count": 2}], "inferred_semantic_type": "unknown"},
        ],
    }
    rows = flatten_profile_for_metadata(profile, "source.synthetic_orders", "run-1", "source", exclude_columns=default_technical_columns())
    assert len(rows) == 1
    assert rows[0]["column_name"] == "id"
    json.dumps(rows)


def test_spark_lazy_import_and_fake_profile_caps():
    assert "pyspark.sql" not in sys.modules
    _install_fake_pyspark()
    prof = profile_dataframe(FakeSparkDataFrame(), engine="spark", sample_size=1, top_n=1)
    assert prof["engine"] == "spark"
    assert prof["row_count"] == 3
    assert prof["column_count"] == 2
    assert len(prof["columns"][0]["sample_values"]) == 1
    assert len(prof["columns"][0]["top_values"]) == 1
