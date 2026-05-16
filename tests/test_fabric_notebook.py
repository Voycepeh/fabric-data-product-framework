import pytest

from fabricops_kit.config import PathConfig
from fabricops_kit.fabric_input_output import (
    FabricStore,
    check_naming_convention,
    _get_store,
    read_lakehouse_table,
    write_lakehouse_table,
)

from fabricops_kit.data_profiling import generate_metadata_profile
from fabricops_kit.technical_columns import add_audit_columns, add_datetime_features

class FakeWriter:
    def __init__(self):
        self.mode_value = None
        self.format_value = None
        self.partition_by = None
        self.options = {}
        self.saved_path = None

    def mode(self, mode):
        self.mode_value = mode
        return self

    def format(self, fmt):
        self.format_value = fmt
        return self

    def partitionBy(self, *args):
        self.partition_by = args
        return self

    def option(self, key, value):
        self.options[key] = value
        return self

    def save(self, path):
        self.saved_path = path


class FakeDF:
    def __init__(self):
        self.repartition_calls = []
        self.write = FakeWriter()

    def repartition(self, *args):
        self.repartition_calls.append(args)
        return self


class FakeRead:
    def __init__(self):
        self.format_value = None
        self.loaded_path = None

    def format(self, fmt):
        self.format_value = fmt
        return self

    def load(self, path):
        self.loaded_path = path
        return {"path": path}


class FakeSpark:
    def __init__(self):
        self.read = FakeRead()


def test__get_store_with_injected_config():
    cfg = PathConfig(paths={"Sandbox": {"Source": FabricStore("Sandbox", "w", "h", "n", "lakehouse")}})
    p = _get_store("Sandbox", "Source", config=cfg)
    assert p.name == "n"


def test__get_store_invalid_raises():
    with pytest.raises(ValueError):
        _get_store("Bad", "Source", config={})


def test_check_naming_convention_passes():
    result = check_naming_convention("dex_source_to_dex_unified_orders", allowed_prefixes=["dex_"], fail_on_error=False)
    assert result["compliant"] is True


def test_check_naming_convention_fails():
    with pytest.raises(ValueError):
        check_naming_convention("bad_name")


def test_write_lakehouse_table_repartition_partition_string():
    df = FakeDF()
    lh = FabricStore("Sandbox", "w", "h", "name", "lakehouse")
    write_lakehouse_table(
        df,
        PathConfig(paths={"Sandbox": {"source": lh}}),
        "Sandbox",
        "source",
        "EMAIL_LOGS",
        mode="overwrite",
        partition_by="p_bucket",
        repartition_by=("p_bucket"),
    )
    assert df.repartition_calls == [("p_bucket",)]
    assert df.write.partition_by == ("p_bucket",)


def test_write_lakehouse_table_repartition_with_int_and_column():
    df = FakeDF()
    lh = FabricStore("Sandbox", "w", "h", "name", "lakehouse")
    write_lakehouse_table(df, PathConfig(paths={"Sandbox": {"source": lh}}), "Sandbox", "source", "EMAIL_LOGS", repartition_by=(200, "p_bucket"))
    assert df.repartition_calls == [(200, "p_bucket")]


def test_read_lakehouse_table_builds_path():
    spark = FakeSpark()
    lh = FabricStore("Sandbox", "w", "h", "name", "lakehouse")
    read_lakehouse_table(PathConfig(paths={"Sandbox": {"source": lh}}), "Sandbox", "source", "MY_TABLE", spark_session=spark)
    assert spark.read.loaded_path.endswith("/Tables/MY_TABLE")


def test_add_audit_columns_validates_missing_bucket_col_early():
    class DF:
        columns = ["x"]

    with pytest.raises(ValueError):
        add_audit_columns(DF(), bucket_column="missing", engine="pandas")


def test_add_datetime_features_validates_missing_col_early():
    class DF:
        columns = ["x"]

    with pytest.raises(ValueError):
        add_datetime_features(DF(), datetime_column="missing", prefix="EVENT", engine="pandas")


def test_odi_metadata_logger_importable():
    assert callable(generate_metadata_profile)
