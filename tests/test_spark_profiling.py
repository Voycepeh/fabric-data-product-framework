import json
import sys
import types

import pandas as pd

from fabric_data_product_framework.profiling import (
    default_technical_columns,
    flatten_profile_for_metadata,
    profile_and_write_metadata,
    profile_dataframe,
    profile_table_and_write_metadata,
    write_profile_metadata_rows,
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
        self.last_writer = None

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

    @property
    def write(self):
        self.last_writer = FakeWrite()
        return self.last_writer


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


class FakeWrite:
    def __init__(self):
        self._mode = None
        self.saved_table = None

    def mode(self, mode):
        self._mode = mode
        return self

    def saveAsTable(self, table):
        self.saved_table = table
        return None


class FakeSparkSession:
    def __init__(self):
        self.sparkContext = self
        self.last_table = None
        self.last_json_input = None

    def parallelize(self, rows):
        return rows

    class _Reader:
        def __init__(self, parent):
            self.parent = parent

        def json(self, rows):
            self.parent.last_json_input = rows
            return FakeSparkDataFrame()

    @property
    def read(self):
        return self._Reader(self)

    def table(self, table_name):
        self.last_table = table_name
        return FakeSparkDataFrame()


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


def test_write_profile_metadata_rows_uses_json_reader():
    spark = FakeSparkSession()
    rows = [{"column_name": "id", "sample_values": [1], "top_values": [{"value": 1, "count": 2}]}]
    out = write_profile_metadata_rows(spark=spark, metadata_rows=rows, metadata_table="fw.meta", mode="overwrite")
    assert out is not None
    assert spark.last_json_input is not None
    assert out.last_writer is not None
    assert out.last_writer._mode == "overwrite"
    assert out.last_writer.saved_table == "fw.meta"


def test_write_profile_metadata_rows_drops_nested_sample_and_top_values():
    spark = FakeSparkSession()
    rows = [
        {"column_name": "id", "sample_values": [1, "two"], "top_values": [{"value": 1, "count": 2}]},
        {"column_name": "status", "sample_values": ["open", 3], "top_values": [{"value": "open", "count": 1}]},
    ]
    write_profile_metadata_rows(spark=spark, metadata_rows=rows, metadata_table="fw.meta")
    assert spark.last_json_input is not None
    for payload in spark.last_json_input:
        record = json.loads(payload)
        assert "sample_values" not in record
        assert "top_values" not in record
        assert "sample_values_json" in record
        assert "top_values_json" in record


def test_profile_and_write_metadata_one_call():
    _install_fake_pyspark()
    spark = FakeSparkSession()
    result = profile_and_write_metadata(
        spark=spark,
        df=FakeSparkDataFrame(),
        dataset_name="framework_smoke_orders",
        table_name="fw_smoke_source_orders",
        metadata_table="fw_metadata.source_profile_records",
        run_id="run-1",
        table_stage="source",
        mode="overwrite",
    )
    assert result["profile"]["engine"] == "spark"
    assert len(result["metadata_rows"]) == 1


def test_profile_table_and_write_metadata_reads_table_then_writes():
    _install_fake_pyspark()
    spark = FakeSparkSession()
    result = profile_table_and_write_metadata(
        spark=spark,
        table_name="fw_smoke_source_orders",
        dataset_name="framework_smoke_orders",
        metadata_table="fw_metadata.source_profile_records",
        run_id="run-1",
        table_stage="source",
        mode="overwrite",
    )
    assert spark.last_table == "fw_smoke_source_orders"
    assert result["profile"]["dataset_name"] == "framework_smoke_orders"
