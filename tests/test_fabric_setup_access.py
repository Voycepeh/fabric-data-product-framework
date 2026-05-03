import pytest

from fabricops_kit.fabric_io import (
    Housepath,
    build_table_identifier,
    get_path,
    lakehouse_csv_read,
    lakehouse_table_read,
    load_fabric_config,
    warehouse_read,
)


def test_load_fabric_config_and_get_path(tmp_path):
    cfg = tmp_path / "fabric_config.yml"
    cfg.write_text(
        """
environments:
  Sandbox:
    Source:
      workspace_id: w1
      house_id: h1
      house_name: SRC
      root: abfss://root1
""",
        encoding="utf-8",
    )
    parsed = load_fabric_config(cfg)
    p = get_path("Sandbox", "Source", config=parsed)
    assert isinstance(p, Housepath)
    assert p.house_name == "SRC"


def test_get_path_missing_env_and_target_errors():
    cfg = {"Sandbox": {"Source": Housepath("w", "h", "n", "abfss://root")}}
    with pytest.raises(ValueError, match="Environment 'Prod' was not found"):
        get_path("Prod", "Source", config=cfg)
    with pytest.raises(ValueError, match="Target 'Unified' was not found"):
        get_path("Sandbox", "Unified", config=cfg)


def test_build_table_identifier_variants():
    assert build_table_identifier(table="table") == "table"
    assert build_table_identifier(schema="dbo", table="table") == "dbo.table"
    assert build_table_identifier(lakehouse="lh", schema="dbo", table="table") == "lh.dbo.table"


class _FakeRead:
    def __init__(self):
        self.loaded_path = None
        self.csv_path = None
        self.header = None

    def format(self, _):
        return self

    def load(self, path):
        self.loaded_path = path
        return {"path": path}

    def option(self, key, value):
        if key == "header":
            self.header = value
        return self

    def csv(self, path):
        self.csv_path = path
        return {"path": path}


class _FakeSpark:
    def __init__(self):
        self.read = _FakeRead()


def test_lakehouse_read_helpers_with_fake_spark():
    lh = Housepath("w", "h", "n", "abfss://root")
    spark = _FakeSpark()
    lakehouse_table_read(lh, "orders", spark_session=spark)
    lakehouse_csv_read(lh, "Files/orders.csv", spark_session=spark)
    assert spark.read.loaded_path.endswith("/Tables/orders")
    assert spark.read.csv_path.endswith("/Files/orders.csv")


def test_warehouse_read_missing_fabric_connector_message():
    lh = Housepath("w", "h", "wh", "abfss://root")
    cfg = {"DE": {"Warehouse": lh}}
    with pytest.raises(RuntimeError, match="must run inside Microsoft Fabric Spark"):
        warehouse_read("DE", "Warehouse", "dbo", "t", config=cfg, spark_session=_FakeSpark())
