"""Simplified Fabric smoke test flow based on the MVP template."""

from fabric_data_product_framework.config import load_dataset_contract, validate_dataset_contract
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.profiling import profile_dataframe

from templates.fabric_adapters import (
    fabric_reader,
    fabric_table_writer,
    metadata_writer_with_schema_hint,
)

DATASET_CONTRACT_PATH = "examples/fabric_smoke_test/synthetic_orders_contract.yaml"
SOURCE_TABLE = "source.synthetic_orders"
TARGET_TABLE = "product.synthetic_orders_curated"
METADATA_TABLE = "metadata.dataset_runs"
DRY_RUN = True

contract = load_dataset_contract(DATASET_CONTRACT_PATH)
validate_dataset_contract(contract)
context = build_runtime_context(dataset_name=contract["dataset_name"], environment="dev", dry_run=DRY_RUN)

source_df = fabric_reader(SOURCE_TABLE)
source_profile = profile_dataframe(source_df)

if not DRY_RUN:
    fabric_table_writer(source_df, TARGET_TABLE, mode="overwrite")

metadata_writer_with_schema_hint(
    records=[
        {
            "run_id": context.run_id,
            "dataset_name": contract["dataset_name"],
            "status": "dry_run" if DRY_RUN else "completed",
            "details": {"source_table": SOURCE_TABLE, "target_table": TARGET_TABLE, "profile": source_profile},
        }
    ],
    table_identifier=METADATA_TABLE,
)
