import pytest

from fabricops_kit.fabric_input_output import (
    FabricStore,
    build_table_identifier,
    _get_store,
    read_lakehouse_csv,
    read_lakehouse_table,
    load_config,
    read_warehouse_table,
)


def test_load_config_and__get_store(tmp_path):
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
    parsed = load_config(cfg)
    p = _get_store("Sandbox", "Source", config=parsed)
    assert isinstance(p, FabricStore)
    assert p.house_name == "SRC"


def test__get_store_missing_env_and_target_errors():
    cfg = {"Sandbox": {"Source": FabricStore("Sandbox", "w", "h", "n", "lakehouse")}}
    with pytest.raises(ValueError, match="Environment 'Prod' was not found"):
        _get_store("Prod", "Source", config=cfg)
    with pytest.raises(ValueError, match="Target 'Unified' was not found"):
        _get_store("Sandbox", "Unified", config=cfg)


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
    lh = FabricStore("Sandbox", "w", "h", "n", "lakehouse")
    spark = _FakeSpark()
    read_lakehouse_table(lh, "orders", spark_session=spark)
    read_lakehouse_csv(lh, "Files/orders.csv", spark_session=spark)
    assert spark.read.loaded_path.endswith("/Tables/orders")
    assert spark.read.csv_path.endswith("/Files/orders.csv")


def test_read_warehouse_table_missing_fabric_connector_message():
    lh = FabricStore("Sandbox", "w", "h", "wh", "warehouse")
    cfg = {"DE": {"Warehouse": lh}}
    with pytest.raises(RuntimeError, match="must run inside Microsoft Fabric Spark"):
        read_warehouse_table("DE", "Warehouse", "dbo", "t", config=cfg, spark_session=_FakeSpark())
