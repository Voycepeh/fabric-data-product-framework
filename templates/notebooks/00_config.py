"""Sample Fabric configuration notebook for Fabric Data Product Framework.

Copy this content into a Microsoft Fabric notebook named ``00_config``.
Then, in downstream notebooks, run:

    %run 00_config

and use:

    import fabric_data_product_framework as fdpf
    config = fdpf.load_fabric_config(CONFIG)
    lh_source = fdpf.get_path("Sandbox", "Source", config=config)

Replace all placeholder IDs, names, and ABFSS paths with your own environment values.
"""

from fabric_data_product_framework.fabric_io import Housepath

DEFAULT_ENV = "Sandbox"
DEFAULT_TARGET = "Source"

NOTEBOOK_PREFIX_LIST = [
    "00_",
    "01_",
    "02_",
    "03_",
]

CONFIG = {
    "houses": {
        "Sandbox": {
            "Source": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000001",
                workspace_name="workspace-sandbox",
                warehouse_id="11111111-1111-1111-1111-111111111111",
                warehouse_name="warehouse_source",
                lakehouse_id="22222222-2222-2222-2222-222222222221",
                lakehouse_name="lh_source",
                lakehouse_abfss="abfss://workspace-sandbox@onelake.dfs.fabric.microsoft.com/lh_source.Lakehouse",
            ),
            "Unified": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000001",
                workspace_name="workspace-sandbox",
                warehouse_id="11111111-1111-1111-1111-111111111112",
                warehouse_name="warehouse_unified",
                lakehouse_id="22222222-2222-2222-2222-222222222222",
                lakehouse_name="lh_unified",
                lakehouse_abfss="abfss://workspace-sandbox@onelake.dfs.fabric.microsoft.com/lh_unified.Lakehouse",
            ),
        },
        "Prod": {
            "Source": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000002",
                workspace_name="workspace-prod",
                warehouse_id="11111111-1111-1111-1111-111111111121",
                warehouse_name="warehouse_source_prod",
                lakehouse_id="22222222-2222-2222-2222-222222222231",
                lakehouse_name="lh_source_prod",
                lakehouse_abfss="abfss://workspace-prod@onelake.dfs.fabric.microsoft.com/lh_source_prod.Lakehouse",
            )
        },
    }
}
