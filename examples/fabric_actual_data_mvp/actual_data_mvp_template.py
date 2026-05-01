# %% [markdown]
# # 1. Introduction
#
# This notebook runs one data product contract end to end using the framework runner.
#
# You only need to edit:
# - Contract values in `contracts/examples/actual_data_mvp_contract.yml`
# - The `transform(df, ctx)` function in this notebook
#
# The framework automatically handles profiling, DQ, drift checks, governance suggestions,
# quarantine, contract validation, lineage, run summary, metadata writes, and gated target write.
#
# Placeholder metadata to complete for your dataset:
# - Data agreement ID: `REPLACE_WITH_DATA_AGREEMENT_ID`
# - Approved usage: `REPLACE_WITH_APPROVED_USAGE`
# - Dataset owner/steward: `REPLACE_WITH_OWNER`
# - Business purpose: `REPLACE_WITH_BUSINESS_PURPOSE`

# %% [markdown]
# # 2. Setup

# %%
import fabric_data_product_framework as fw
from pyspark.sql import functions as F

print(f"Framework package: {fw.__name__}")
if hasattr(fw, "__version__"):
    print(f"Framework version: {fw.__version__}")

# %% [markdown]
# # 3. Load contract

# %%
CONTRACT_PATH = "contracts/examples/actual_data_mvp_contract.yml"
contract = fw.load_data_contract(CONTRACT_PATH)

if hasattr(fw, "data_product_contract_to_dict"):
    display(fw.data_product_contract_to_dict(contract))
else:
    print(contract)

# %% [markdown]
# # 4. Optional source preview (development only)
#
# Optional: preview source rows while developing. Freeze/remove for production scheduling.

# %%
source_df = spark.table(contract.source.table)
display(source_df.limit(10))

# %% [markdown]
# # 5. Business transformation
#
# Only required user logic goes in `transform`.

# %%
def transform(df, ctx):
    # Minimal MVP: no-op passthrough.
    # return df.withColumn("ingest_date", F.current_date())
    # return df.select("col_a", "col_b", "col_c")
    # return df.withColumnRenamed("old_name", "new_name")
    # return df.filter(F.col("status") == F.lit("active"))
    # other_df = spark.table("REPLACE_WITH_OPTIONAL_JOIN_TABLE")
    # df = df.join(other_df, on="REPLACE_WITH_KEY_COLUMN", how="left")
    # df = df.withColumn("event_ts", F.to_timestamp("event_ts"))
    return df

# %% [markdown]
# # 6. Run full framework

# %%
result = fw.run_data_product(
    spark=spark,
    contract=contract,
    transform=transform,
)

# %% [markdown]
# # 7. Inspect result

# %%
print("status:", result.get("status"))
print("written:", result.get("written"))

run_summary = result.get("run_summary") or {}
if run_summary:
    print("run_summary:", run_summary)

for key in [
    "dq_workflow_summary",
    "drift_summary",
    "governance_summary",
    "quarantine_summary",
]:
    print(f"{key}:", result.get(key))

# %% [markdown]
# # 8. Assert gates
#
# Keep this assertion after inspection during development.
# In scheduled runs, keep it enabled so failed gates fail the pipeline.

# %%
fw.assert_data_product_passed(result)

# %% [markdown]
# # 9. Metadata tables (optional inspection)

# %%
metadata_tables = []
meta = getattr(contract, "metadata", None)
if meta:
    metadata_tables = [
        meta.source_profile_table,
        meta.output_profile_table,
        meta.schema_snapshot_table,
        meta.partition_snapshot_table,
        meta.quality_result_table,
        meta.classification_table,
        meta.contract_validation_table,
        meta.run_summary_table,
        meta.dataset_runs_table,
    ]

for table_name in metadata_tables:
    if not table_name:
        continue
    try:
        print(f"Preview metadata table: {table_name}")
        display(spark.table(table_name).limit(20))
    except Exception as ex:
        print(f"Skipping {table_name}: {ex}")

# %% [markdown]
# # 10. Notes for production scheduling
#
# - Freeze or remove exploratory preview cells before scheduling.
# - Keep `transform` deterministic.
# - Keep contract files in source control.
# - Use approved DQ rules for enforcement.
# - AI/profile-generated DQ candidates are reviewable and should not auto-block unless approved.
# - Governance classifications are review suggestions and not Purview labels.
