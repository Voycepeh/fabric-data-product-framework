from __future__ import annotations

from pathlib import Path


def create_pipeline_notebook_template(
    output_path,
    dataset_name="sample_dataset",
    source_table="SOURCE_TABLE",
    output_table="OUTPUT_TABLE",
    source_env="Sandbox",
    source_target="Source",
    output_env="Sandbox",
    output_target="Unified",
    include_ai_prompts=True,
    overwrite=False,
):
    """Create a runnable Fabric notebook template for pipeline-style development."""
    path = Path(output_path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")

    content = f'''# %% [markdown]
# # 1. Introduction
# Notebook template for dataset: `{dataset_name}`.

# %% [markdown]
# # 2. Dataset purpose and approved usage
# - Describe business purpose.
# - List approved and non-approved usage.

# %% [markdown]
# # 3. Configuration and setup

# %%
import fabric_data_product_framework as fw

# %%
from fabric_data_product_framework.fabric_notebook import (
    load_fabric_config,
    get_path,
    check_naming_convention,
    lakehouse_table_read,
    lakehouse_table_write,
    clean_datetime_columns,
    add_system_technical_columns,
    ODI_METADATA_LOGGER,
)

fabric_config = load_fabric_config("Files/configs/fabric_houses.yaml")

lh_in = get_path("{source_env}", "{source_target}", config=fabric_config)
lh_out = get_path("{output_env}", "{output_target}", config=fabric_config)
check_naming_convention()

# %% [markdown]
# # 4. Source declaration

# %%
source_table = "{source_table}"
output_table = "{output_table}"
dataset_name = "{dataset_name}"
run_id = None

# %% [markdown]
# # 5. Source ingestion

# %%
df_source = lakehouse_table_read(lh_in, source_table)
print(df_source.count())

# %% [markdown]
# # 6. Source profiling metadata

# %%
df_source_profile = ODI_METADATA_LOGGER(
    df_source,
    f"{{lh_in.house_name}}|{{source_table}}"
)

lakehouse_table_write(
    df_source_profile,
    lh_in,
    "METADATA_SOURCE",
    mode="append"
)

# %% [markdown]
# # 7. Human EDA notes
# Capture manual observations, anomalies, and assumptions.

# %% [markdown]
# # 8. Core transformation
# Replace this section with the actual business transformation.

# %%
df_output = df_source

# %% [markdown]
# # 9. Standard datetime and technical columns

# %%
# Example only. Change EVENT_START_DTM and BUSINESS_KEY to real columns.
# df_output = clean_datetime_columns(
#     df_output,
#     datetime_col="EVENT_START_DTM",
#     tz_region="Asia/Singapore",
#     prefix="EVENT"
# )
# df_output = add_system_technical_columns(df_output, "BUSINESS_KEY")

# %% [markdown]
# # 10. Data quality rules placeholder
# Add explicit must-fail and warning rules from evidence.

# %% [markdown]
# # 11. Output write

# %%
lakehouse_table_write(
    df_output,
    lh_out,
    output_table,
    mode="overwrite"
)

# Optional for large tables after add_system_technical_columns creates p_bucket:
# lakehouse_table_write(
#     df_output,
#     lh_out,
#     output_table,
#     mode="overwrite",
#     partition_by="p_bucket",
#     repartition_by=("p_bucket",)
# )

# %% [markdown]
# # 12. Output profiling metadata

# %%
df_output_read = lakehouse_table_read(lh_out, output_table)

df_output_profile = ODI_METADATA_LOGGER(
    df_output_read,
    f"{{lh_out.house_name}}|{{output_table}}"
)

lakehouse_table_write(
    df_output_profile,
    lh_out,
    "METADATA_UNIFIED",
    mode="append"
)

# %% [markdown]
# # 13. AI-assisted notebook lineage
# Copilot scans the notebook and drafts lineage_steps. Framework validates and renders lineage.

# %%
prompt = fw.get_fabric_copilot_lineage_prompt()
print(prompt)

# %% [markdown]
# Paste the prompt into Fabric Copilot, then paste returned Python code in the next cell.

# %%
lineage_steps = [
    # Copilot generated steps go here.
]

# %%
lineage_validation = fw.validate_lineage_steps(lineage_steps)
display(lineage_validation)

# %%
lineage_record = fw.build_lineage_record_from_steps(dataset_name=dataset_name, lineage_steps=lineage_steps, run_id=run_id)
display(lineage_record)

# %%
fw.plot_lineage_networkx(lineage_record, title=f"{dataset_name} Notebook Lineage")

# %% [markdown]
# # 14. Run summary and handover notes
# Confirm assumptions, known gaps, and next-owner actions.
'''

    if include_ai_prompts:
        content += '''
# %% [markdown]
# # 15. AI Copilot prompt cells

# %% [markdown]
# **AI prompt: Transformation summary**
# Ask Copilot to inspect the transformation code above and produce a concise transformation summary with:
# - step name
# - input dataframe
# - output dataframe
# - business reason
# - important columns created or removed
# - data quality risk

# %% [markdown]
# **AI prompt: Data lineage**
# Ask Copilot to identify important dataframes in this notebook and draft lineage_steps using the framework schema. Avoid Mermaid and keep low-confidence items marked for human review.

# %% [markdown]
# **AI prompt: Data quality rules**
# Ask Copilot to review the source profile, output profile, and business purpose, then propose layman data quality rules.
# It must not invent rules without evidence. It should separate must fail rules from warning rules.

# %% [markdown]
# **AI prompt: Handover readiness**
# Ask Copilot to review whether the notebook is ready for another analyst or junior engineer to take over.
'''

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def create_actual_data_mvp_template(
    output_path: str,
    contract_path: str = "contracts/examples/actual_data_mvp_contract.yml",
) -> str:
    """Create the end-to-end "actual data MVP" notebook template."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f'''# %% [markdown]
# # 1. Introduction
# This notebook runs one data product contract end to end.
#
# Edit only the contract and `transform(df, ctx)` function.
# The framework handles profiling, DQ, drift, governance suggestions, quarantine,
# contract validation, lineage, run summary, metadata writes, and gated target writes.

# %% [markdown]
# # 2. Setup

# %%
import fabric_data_product_framework as fw
from pyspark.sql import functions as F

# %% [markdown]
# # 3. Load contract

# %%
CONTRACT_PATH = "{contract_path}"
contract = fw.load_data_contract(CONTRACT_PATH)
if hasattr(fw, "data_product_contract_to_dict"):
    display(fw.data_product_contract_to_dict(contract))

# %% [markdown]
# # 4. Optional source preview

# %%
source_df = spark.table(contract.source.table)
display(source_df.limit(10))

# %% [markdown]
# # 5. Business transformation

# %%
def transform(df, ctx):
    # return df.withColumn("ingest_date", F.current_date())
    # return df.select("col_a", "col_b")
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
print(result.get("status"))
print(result.get("written"))
print(result.get("run_summary"))
print(result.get("dq_workflow"))
print((result.get("drift") or {{}}).get("summary"))
print((result.get("governance") or {{}}).get("summary"))
print(result.get("quarantine"))

# %% [markdown]
# # 8. Assert gates

# %%
fw.assert_data_product_passed(result)

# %% [markdown]
# # 9. AI-assisted notebook lineage
# Copilot drafts lineage_steps by scanning this notebook; framework validates/renders;
# human reviews low-confidence or ambiguous items before storage.

# %%
prompt = fw.get_fabric_copilot_lineage_prompt()
print(prompt)

# %% [markdown]
# Paste the printed prompt into Fabric Copilot. It should return only Python code assigning
# lineage_steps = [...]. Paste that output into the next cell.

# %%
lineage_steps = [
    # Copilot generated steps go here.
]

# %%
lineage_validation = fw.validate_lineage_steps(lineage_steps)
display(lineage_validation)

# %%
lineage_record = fw.build_lineage_record_from_steps(
    dataset_name=contract.dataset.name,
    lineage_steps=lineage_steps,
    run_id=result.get("run_id"),
    notebook_name="actual_data_mvp_template",
)
display(lineage_record)

# %%
fw.plot_lineage_networkx(
    lineage_record,
    title=f"{{contract.dataset.name}} Notebook Lineage",
)

# %% [markdown]
# Optional storage: write lineage_record with your metadata utility/table pattern after review.
# TODO: add table write call in your environment once metadata table conventions are finalized.
'''
    path.write_text(content, encoding="utf-8")
    return str(path)
