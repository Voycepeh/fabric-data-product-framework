import pytest

from fabric_data_product_framework.fabric_notebook import (
    Housepath,
    get_path,
    load_fabric_config,
)


def test_load_fabric_config_valid(tmp_path):
    cfg = tmp_path / "fabric_houses.yaml"
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

    loaded = load_fabric_config(cfg)
    assert isinstance(loaded["Sandbox"]["Source"], Housepath)
    assert loaded["Sandbox"]["Source"].house_name == "SRC"


def test_load_fabric_config_missing_environments_raises(tmp_path):
    cfg = tmp_path / "fabric_houses.yaml"
    cfg.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        load_fabric_config(cfg)


def test_load_fabric_config_missing_required_field_raises(tmp_path):
    cfg = tmp_path / "fabric_houses.yaml"
    cfg.write_text(
        """
environments:
  Sandbox:
    Source:
      workspace_id: w1
      house_id: h1
      root: abfss://root1
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_fabric_config(cfg)


def test_get_path_without_config_uses_example_config():
    p = get_path("Sandbox", "Source")
    assert p.house_name == "SAMPLE_SOURCE"


def test_get_path_with_example_config():
    p = get_path("Sandbox", "Source", use_example_config=True)
    assert p.house_name == "SAMPLE_SOURCE"


def test_get_path_with_loaded_config(tmp_path):
    cfg = tmp_path / "fabric_houses.yaml"
    cfg.write_text(
        """
environments:
  Sandbox:
    Unified:
      workspace_id: w2
      house_id: h2
      house_name: UNIFIED
      root: abfss://root2
""",
        encoding="utf-8",
    )
    loaded = load_fabric_config(cfg)
    p = get_path("Sandbox", "Unified", config=loaded)
    assert p.root == "abfss://root2"
