"""Handover-oriented helpers for notebook workflow outputs."""



# --- merged from mvp_steps.py ---
"""Canonical 10-step lifecycle registry and artifact validation helpers."""

from typing import Any


MVP_STEP_REGISTRY: list[dict[str, Any]] = [
    {"step_number": 1, "step_name": "Define purpose, approved usage & governance ownership", "owner_type": "Governance", "canonical_modules": ["runtime.py"], "expected_artifacts": ["governance_context"]},
    {"step_number": 2, "step_name": "Configure runtime, environment & path rules", "owner_type": "Starter kit", "canonical_modules": ["config.py", "fabric_io.py"], "expected_artifacts": ["runtime_context", "fabric_config", "path_context"]},
    {"step_number": 3, "step_name": "Declare source contract & ingest source data", "owner_type": "Starter kit", "canonical_modules": ["quality.py", "fabric_io.py"], "expected_artifacts": ["source_contract", "source_dataframe"]},
    {"step_number": 4, "step_name": "Validate source against contract & capture metadata", "owner_type": "Starter kit", "canonical_modules": ["profiling.py", "drift.py", "metadata.py"], "expected_artifacts": ["source_profile", "drift_results"]},
    {"step_number": 5, "step_name": "Explore data & capture transformation / DQ rationale", "owner_type": "Analyst / Data scientist notebook", "canonical_modules": ["quality.py"], "expected_artifacts": ["exploration_notes", "transformation_rationale"]},
    {"step_number": 6, "step_name": "Build production transformation & write target output", "owner_type": "Data engineer notebook", "canonical_modules": ["quality.py", "technical_columns.py"], "expected_artifacts": ["transformed_dataframe", "target_write_result"]},
    {"step_number": 7, "step_name": "Validate output & persist target metadata", "owner_type": "Starter kit", "canonical_modules": ["fabric_io.py", "metadata.py"], "expected_artifacts": ["output_profile", "target_metadata"]},
    {"step_number": 8, "step_name": "Generate, review & configure DQ rules", "owner_type": "AI-assisted + human review", "canonical_modules": ["ai.py", "quality.py"], "expected_artifacts": ["draft_dq_rules", "approved_dq_rules", "dq_results"]},
    {"step_number": 9, "step_name": "Generate & review classification / sensitivity suggestions", "owner_type": "AI-assisted + human review", "canonical_modules": ["ai.py", "governance.py"], "expected_artifacts": ["classification_suggestions", "governance_labels"]},
    {"step_number": 10, "step_name": "Generate data lineage and handover documentation", "owner_type": "AI-assisted handover document generation", "canonical_modules": ["lineage.py", "ai.py", "run_summary.py"], "expected_artifacts": ["lineage_records", "handover_package"]},
]


def get_mvp_step_registry() -> list[dict[str, Any]]:
    """Return the canonical 10-step lifecycle registry."""
    return [dict(step) for step in MVP_STEP_REGISTRY]


def get_mvp_step_names() -> list[str]:
    """Return ordered lifecycle step names."""
    return [step["step_name"] for step in MVP_STEP_REGISTRY]


def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Validate provided artifacts against the canonical 10-step lifecycle registry."""
    expected = sorted({name for step in MVP_STEP_REGISTRY for name in step["expected_artifacts"]})
    available = sorted([name for name in expected if artifacts.get(name) is not None])
    missing = [name for name in expected if name not in available]
    return {"valid": not missing, "expected_artifacts": expected, "available_artifacts": available, "missing_artifacts": missing}


# --- merged from template_generator.py ---

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
    """Execute the `create_pipeline_notebook_template` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        output_path : Any
            Input parameter `output_path`.
        dataset_name : Any
            Input parameter `dataset_name`.
        source_table : Any
            Input parameter `source_table`.
        output_table : Any
            Input parameter `output_table`.
        source_env : Any
            Input parameter `source_env`.
        source_target : Any
            Input parameter `source_target`.
        output_env : Any
            Input parameter `output_env`.
        output_target : Any
            Input parameter `output_target`.
        include_ai_prompts : Any
            Input parameter `include_ai_prompts`.
        overwrite : Any
            Input parameter `overwrite`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> create_pipeline_notebook_template(..., ..., ..., ..., ..., ..., ..., ..., ..., ...)
        """
    path = Path(output_path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")

    content = f'''# %% [markdown]
# # 1. Purpose and governance ownership
# Notebook template for dataset: `{dataset_name}`.

# %% [markdown]
# # 2. Runtime, environment, and path setup
# - Describe business purpose.
# - List approved and non-approved usage.

# %% [markdown]
# # 3. Source contract and ingestion

# %%
import fabricops_kit as fw

# %%
from fabricops_kit.fabric_input_output import (
    load_fabric_config,
    get_path,
    check_naming_convention,
    lakehouse_table_read,
    lakehouse_table_write,
    generate_metadata_profile,
)
from fabricops_kit.technical_columns import (
    add_audit_columns,
    add_datetime_features,
    add_hash_columns,
)

fabric_config = load_fabric_config(CONFIG)

lh_in = get_path("{source_env}", "{source_target}", config=fabric_config)
lh_out = get_path("{output_env}", "{output_target}", config=fabric_config)
check_naming_convention()

# %% [markdown]
# # 3. Source contract declaration

# %%
source_table = "{source_table}"
output_table = "{output_table}"
dataset_name = "{dataset_name}"
run_id = None

# %% [markdown]
# # 3. Source data ingestion

# %%
df_source = lakehouse_table_read(lh_in, source_table)
print(df_source.count())

# %% [markdown]
# # 4. Source contract validation and metadata profiling

# %%
df_source_profile = generate_metadata_profile(
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
# # 5. Exploration and rationale
# Capture manual observations, anomalies, and assumptions.

# %% [markdown]
# # 6. Production transformation and target output
# Replace this section with the actual business transformation.

# %%
df_output = df_source

# %% [markdown]
# # 6. Production transformation and target output (technical columns)

# %%
# Example only. Change EVENT_START_DTM and BUSINESS_KEY to real columns.
# df_output = add_datetime_features(
#     df_output,
#     datetime_column="EVENT_START_DTM",
#     timezone="Asia/Singapore",
#     prefix="EVENT"
# )
# df_output = add_audit_columns(
#     df_output,
#     pipeline_name=dataset_name,
#     environment="Sandbox",
#     source_table=source_table,
#     bucket_column="BUSINESS_KEY",
# )
# df_output = add_hash_columns(
#     df_output,
#     business_keys=["BUSINESS_KEY"],
# )

# %% [markdown]
# # 8. AI-assisted DQ rule generation/review
# Add explicit must-fail and warning rules from evidence.

# %% [markdown]
# # 6. Production output write

# %%
lakehouse_table_write(
    df_output,
    lh_out,
    output_table,
    mode="overwrite"
)

# Optional for large tables after add_audit_columns creates _partition_bucket:
# lakehouse_table_write(
#     df_output,
#     lh_out,
#     output_table,
#     mode="overwrite",
#     partition_by="_partition_bucket",
#     repartition_by=("_partition_bucket",)
# )

# %% [markdown]
# # 7. Output validation and target metadata

# %%
df_output_read = lakehouse_table_read(lh_out, output_table)

df_output_profile = generate_metadata_profile(
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
# # 9. AI-assisted classification/sensitivity review
# Deterministic scanner extracts structure first; AI enrichment is optional; Copilot prompt is fallback only.

# %%
lineage_result = fw.build_lineage_from_notebook_code(__doc__ or "", use_ai=True)
lineage_steps = lineage_result.get("steps", [])
lineage_validation = lineage_result.get("validation", {{}})
display(lineage_validation)

# %%
if not lineage_result.get("ai_used") and lineage_result.get("fallback_prompt"):
    print(lineage_result["fallback_prompt"])

# %%
lineage_record = fw.build_lineage_record_from_steps(dataset_name=dataset_name, lineage_steps=lineage_steps, run_id=run_id)
display(lineage_record)

# %%
fw.plot_lineage_steps(lineage_record, title=f"{dataset_name} Notebook Lineage")

# %% [markdown]
# # 10. AI-assisted lineage and handover documentation
# Confirm assumptions, known gaps, and next-owner actions.
'''

    if include_ai_prompts:
        content += '''
# %% [markdown]
# # 10. AI-assisted lineage and handover prompts

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
# **AI prompt: Data lineage fallback**
# Only if AI helper is unavailable: use the printed fallback prompt to enrich reasons/notes for already-scanned lineage steps.

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
    """Execute the `create_actual_data_mvp_template` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        output_path : Any
            Input parameter `output_path`.
        contract_path : Any
            Input parameter `contract_path`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> create_actual_data_mvp_template(..., ...)
        """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f'''# %% [markdown]
# # 1. Purpose and governance ownership
# This notebook runs one data product contract end to end.
#
# Edit only the contract and `transform(df, ctx)` function.
# The framework handles profiling, DQ, drift, governance suggestions, quarantine,
# contract validation, lineage, run summary, metadata writes, and gated target writes.

# %% [markdown]
# # 2. Configure runtime, environment & path rules

# %%
import fabricops_kit as fw
from pyspark.sql import functions as F

# %% [markdown]
# # 3. Declare source contract & ingest source data

# %%
CONTRACT_PATH = "{contract_path}"
contract = fw.load_data_contract(CONTRACT_PATH)
if hasattr(fw, "data_product_contract_to_dict"):
    display(fw.data_product_contract_to_dict(contract))

# %% [markdown]
# # 4. Validate source against contract & capture metadata

# %%
source_df = spark.table(contract.source.table)
display(source_df.limit(10))

# %% [markdown]
# # 5. Explore data & capture transformation / DQ rationale

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
# # 6. Build production transformation & write target output

# %%
result = fw.run_data_product(
    spark=spark,
    contract=contract,
    transform=transform,
)

# %% [markdown]
# # 7. Validate output & persist target metadata

# %%
print(result.get("status"))
print(result.get("written"))
print(result.get("run_summary"))
print(result.get("dq_workflow"))
print((result.get("drift") or {{}}).get("summary"))
print((result.get("governance") or {{}}).get("summary"))
print(result.get("quarantine"))

# %% [markdown]
# # 8. Generate, review & configure DQ rules

# %%
fw.assert_data_product_passed(result)

# %% [markdown]
# # 10. Generate data lineage and handover documentation
# Deterministic scanner extracts lineage structure first. AI/Copilot is enrichment-only fallback.

# %%
lineage_result = fw.build_lineage_from_notebook_code(__doc__ or "", use_ai=True)
lineage_steps = lineage_result.get("steps", [])
lineage_validation = lineage_result.get("validation", {{}})
display(lineage_validation)

# %%
if not lineage_result.get("ai_used") and lineage_result.get("fallback_prompt"):
    print(lineage_result["fallback_prompt"])

# %%
lineage_record = fw.build_lineage_record_from_steps(
    dataset_name=contract.dataset.name,
    lineage_steps=lineage_steps,
    run_id=result.get("run_id"),
    notebook_name="actual_data_mvp_template",
)
display(lineage_record)

# %%
fw.plot_lineage_steps(
    lineage_record,
    title=f"{{contract.dataset.name}} Notebook Lineage",
)

# %% [markdown]
# Optional storage: write lineage_record with your metadata utility/table pattern after review.
# TODO: add table write call in your environment once metadata table conventions are finalized.
'''
    path.write_text(content, encoding="utf-8")
    return str(path)


# --- merged from mvp_steps.py ---
"""Canonical 10-step lifecycle registry for the Fabric data product framework."""

from copy import deepcopy
from typing import Any

MVP_STEP_REGISTRY: list[dict[str, Any]] = [
    {"step_number": 1, "step_name": "Define purpose, approved usage & governance ownership", "owner_type": "Governance", "expected_artifacts": ["governance_context"]},
    {"step_number": 2, "step_name": "Configure runtime, environment & path rules", "owner_type": "Starter kit", "expected_artifacts": ["runtime_context", "fabric_config", "path_context"]},
    {"step_number": 3, "step_name": "Declare source contract & ingest source data", "owner_type": "Starter kit", "expected_artifacts": ["source_contract", "source_dataframe"]},
    {"step_number": 4, "step_name": "Validate source against contract & capture metadata", "owner_type": "Starter kit", "expected_artifacts": ["source_profile", "drift_results"]},
    {"step_number": 5, "step_name": "Explore data & capture transformation / DQ rationale", "owner_type": "Analyst / Data scientist notebook", "expected_artifacts": ["exploration_notes", "transformation_rationale"]},
    {"step_number": 6, "step_name": "Build production transformation & write target output", "owner_type": "Data engineer notebook", "expected_artifacts": ["transformed_dataframe", "target_write_result"]},
    {"step_number": 7, "step_name": "Validate output & persist target metadata", "owner_type": "Starter kit", "expected_artifacts": ["output_profile", "target_metadata"]},
    {"step_number": 8, "step_name": "Generate, review & configure DQ rules", "owner_type": "AI-assisted + human review", "expected_artifacts": ["draft_dq_rules", "approved_dq_rules", "dq_results"]},
    {"step_number": 9, "step_name": "Generate & review classification / sensitivity suggestions", "owner_type": "AI-assisted + human review", "expected_artifacts": ["classification_suggestions", "governance_labels"]},
    {"step_number": 10, "step_name": "Generate data lineage and handover documentation", "owner_type": "AI-assisted handover document generation", "expected_artifacts": ["lineage_records", "handover_package"]},
]

def get_mvp_step_registry() -> list[dict[str, Any]]:
    """Return the canonical 10-step lifecycle registry."""
    return deepcopy(MVP_STEP_REGISTRY)

def get_mvp_step_names() -> list[str]:
    """Return ordered lifecycle step names."""
    return [step["step_name"] for step in MVP_STEP_REGISTRY]

def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Validate provided artifacts against the canonical 10-step lifecycle registry."""
    expected = sorted({name for step in MVP_STEP_REGISTRY for name in step["expected_artifacts"]})
    missing = [name for name in expected if artifacts.get(name) is None]
    return {"valid": not missing, "is_valid": not missing, "expected_artifacts": expected, "missing_artifacts": missing}

# --- merged from ai_context.py ---
"""AI context export module scaffold."""


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
    """Create a canonical 10-step lifecycle notebook template."""
    path = Path(output_path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")

    content = f'''# %% [markdown]
# # 1. Define purpose, approved usage & governance ownership
# Dataset: `{dataset_name}`

# %% [markdown]
# # 2. Configure runtime, environment & path rules

# %% [markdown]
# # 3. Declare source contract & ingest source data

# %% [markdown]
# # 4. Validate source against contract & capture metadata

# %% [markdown]
# # 5. Explore data & capture transformation / DQ rationale

# %% [markdown]
# # 6. Build production transformation & write target output

# %% [markdown]
# # 7. Validate output & persist target metadata

# %% [markdown]
# # 8. Generate, review & configure DQ rules

# %% [markdown]
# # 9. Generate & review classification / sensitivity suggestions

# %% [markdown]
# # 10. Generate data lineage and handover documentation
'''
    path.write_text(content, encoding="utf-8")
    return str(path)
