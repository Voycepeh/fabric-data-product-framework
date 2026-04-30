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
from fabric_data_product_framework.fabric_notebook import (
    get_path,
    check_naming_convention,
    lakehouse_table_read,
    lakehouse_table_write,
    clean_datetime_columns,
    add_system_technical_columns,
    ODI_METADATA_LOGGER,
)

lh_in = get_path("{source_env}", "{source_target}")
lh_out = get_path("{output_env}", "{output_target}")
check_naming_convention()

# %% [markdown]
# # 4. Source declaration

# %%
source_table = "{source_table}"
output_table = "{output_table}"

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
    mode="overwrite",
    partition_by="p_bucket",
    repartition_by=("p_bucket",)
)

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
# # 13. Lineage and transformation summary
# Document key steps and business reasons.

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
# Ask Copilot to identify important dataframes in this notebook and create a Mermaid lineage diagram.

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
