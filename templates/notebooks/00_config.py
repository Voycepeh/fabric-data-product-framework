"""Sample Fabric configuration notebook for Fabric Data Product Framework.

Copy this content into a Microsoft Fabric notebook named ``00_config``.
In downstream notebooks:

    %run 00_config

    import fabric_data_product_framework as fdpf
    config = fdpf.load_fabric_config(CONFIG)
    lh_source = fdpf.get_path("Sandbox", "Source", config=config)
    lh_unified = fdpf.get_path("Sandbox", "Unified", config=config)
"""

from fabric_data_product_framework.fabric_io import Housepath

DEFAULT_ENV = "Sandbox"
DEFAULT_TARGET = "Source"

NOTEBOOK_PREFIX_LIST = ["00_", "01_", "02_", "03_"]

CONFIG = {
    "Sandbox": {
        "Source": Housepath(
            workspace_id="00000000-0000-0000-0000-000000000001",
            house_id="11111111-1111-1111-1111-111111111111",
            house_name="lh_source",
            root="abfss://workspace-sandbox@onelake.dfs.fabric.microsoft.com/lh_source.Lakehouse",
        ),
        "Unified": Housepath(
            workspace_id="00000000-0000-0000-0000-000000000001",
            house_id="11111111-1111-1111-1111-111111111112",
            house_name="lh_unified",
            root="abfss://workspace-sandbox@onelake.dfs.fabric.microsoft.com/lh_unified.Lakehouse",
        ),
        "Product": Housepath(
            workspace_id="00000000-0000-0000-0000-000000000001",
            house_id="11111111-1111-1111-1111-111111111113",
            house_name="lh_product",
            root="abfss://workspace-sandbox@onelake.dfs.fabric.microsoft.com/lh_product.Lakehouse",
        ),
        "Warehouse": Housepath(
            workspace_id="00000000-0000-0000-0000-000000000001",
            house_id="11111111-1111-1111-1111-111111111114",
            house_name="wh_product",
            root="abfss://workspace-sandbox@onelake.dfs.fabric.microsoft.com/wh_product.Warehouse",
        ),
    }
}
