import pytest

from fabricops_kit.fabric_io import (
    Housepath,
    ODI_METADATA_LOGGER,
    check_naming_convention,
    get_path,
    lakehouse_table_read,
    lakehouse_table_write,
)

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


def test_get_path_with_injected_config():
    cfg = {"Sandbox": {"Source": Housepath("w", "h", "n", "abfss://root")}}
    p = get_path("Sandbox", "Source", config=cfg)
    assert p.house_name == "n"


def test_get_path_invalid_raises():
    with pytest.raises(ValueError):
        get_path("Bad", "Source", config={})


def test_check_naming_convention_passes():
    result = check_naming_convention("dex_source_to_dex_unified_orders")
    assert result["compliant"] is True


def test_check_naming_convention_fails():
    with pytest.raises(ValueError):
        check_naming_convention("bad_name")


def test_lakehouse_table_write_repartition_partition_string():
    df = FakeDF()
    lh = Housepath("w", "h", "name", "abfss://root")
    lakehouse_table_write(
        df,
        lh,
        "EMAIL_LOGS",
        mode="overwrite",
        partition_by="p_bucket",
        repartition_by=("p_bucket"),
    )
    assert df.repartition_calls == [("p_bucket",)]
    assert df.write.partition_by == ("p_bucket",)


def test_lakehouse_table_write_repartition_with_int_and_column():
    df = FakeDF()
    lh = Housepath("w", "h", "name", "abfss://root")
    lakehouse_table_write(df, lh, "EMAIL_LOGS", repartition_by=(200, "p_bucket"))
    assert df.repartition_calls == [(200, "p_bucket")]


def test_lakehouse_table_read_builds_path():
    spark = FakeSpark()
    lh = Housepath("w", "h", "name", "abfss://root")
    lakehouse_table_read(lh, "MY_TABLE", spark_session=spark)
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
    assert callable(ODI_METADATA_LOGGER)
