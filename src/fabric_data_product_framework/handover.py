"""Handover-oriented helpers for notebook workflow outputs."""



# --- merged from mvp_steps.py ---
"""Canonical 13-step MVP lifecycle registry and artifact validation helpers."""

from typing import Any


MVP_STEP_REGISTRY: list[dict[str, Any]] = [
    {
        "step_number": 1,
        "step_name": "Package and runtime setup",
        "owner_type": "framework",
        "canonical_modules": ["runtime.py", "fabric_io.py"],
        "expected_artifacts": ["runtime_context"],
        "description": "Initialize the notebook runtime and verify the framework package and execution context.",
    },
    {
        "step_number": 2,
        "step_name": "Fabric config and paths",
        "owner_type": "human",
        "canonical_modules": ["fabric_io.py", "config.py"],
        "expected_artifacts": ["fabric_config", "path_context"],
        "description": "Set project-specific Fabric configuration, source/target paths, and run identifiers.",
    },
    {
        "step_number": 3,
        "step_name": "Pull source data",
        "owner_type": "framework",
        "canonical_modules": ["fabric_io.py"],
        "expected_artifacts": ["source_dataframe"],
        "description": "Read source data from Fabric lakehouse, warehouse, or file path into the pipeline runtime.",
    },
    {"step_number": 4, "step_name": "Source profiling", "owner_type": "framework", "canonical_modules": ["profiling.py"], "expected_artifacts": ["source_profile"], "description": "Profile source structure and quality signals to establish baseline metadata."},
    {
        "step_number": 5,
        "step_name": "AI assisted DQ rule drafting",
        "owner_type": "ai_assisted",
        "canonical_modules": ["ai_quality_rules.py", "rule_compiler.py"],
        "expected_artifacts": ["draft_dq_rules"],
        "description": "Use AI support to draft candidate data quality rules from profiling outputs and business context.",
    },
    {
        "step_number": 6,
        "step_name": "Human review of rules and metadata",
        "owner_type": "human",
        "canonical_modules": ["rule_compiler.py", "metadata.py"],
        "expected_artifacts": ["approved_dq_rules", "approved_metadata_notes"],
        "description": "Review and approve drafted rules and key metadata assumptions before enforcement.",
    },
    {
        "step_number": 7,
        "step_name": "Compile and run DQ checks",
        "owner_type": "framework",
        "canonical_modules": ["quality.py", "rule_compiler.py"],
        "expected_artifacts": ["compiled_dq_rules", "dq_results"],
        "description": "Compile approved rules and execute data quality checks against the source dataframe.",
    },
    {
        "step_number": 8,
        "step_name": "Schema/profile/data drift checks",
        "owner_type": "framework",
        "canonical_modules": ["drift.py", "incremental.py"],
        "expected_artifacts": ["drift_results"],
        "description": "Compare current run metrics with baseline snapshots and flag schema/profile/data drift.",
    },
    {
        "step_number": 9,
        "step_name": "Core transformation",
        "owner_type": "mixed",
        "canonical_modules": ["fabric_io.py", "contracts.py"],
        "expected_artifacts": ["transformed_dataframe"],
        "description": "Apply business transformation logic using project code with framework-compatible conventions.",
    },
    {
        "step_number": 10,
        "step_name": "Standard technical columns",
        "owner_type": "framework",
        "canonical_modules": ["fabric_io.py", "technical_columns.py"],
        "expected_artifacts": ["output_with_technical_columns"],
        "description": "Apply required operational metadata columns to the transformed output dataframe.",
    },
    {
        "step_number": 11,
        "step_name": "Write output and profile output",
        "owner_type": "framework",
        "canonical_modules": ["fabric_io.py", "profiling.py", "metadata.py"],
        "expected_artifacts": ["target_write_result", "output_profile"],
        "description": "Write output data to target and capture output profiling metadata for traceability.",
    },
    {
        "step_number": 12,
        "step_name": "Governance classification and lineage",
        "owner_type": "mixed",
        "canonical_modules": ["governance.py", "lineage.py", "ai_lineage_summary.py"],
        "expected_artifacts": ["governance_labels", "lineage_records"],
        "description": "Classify governance tags and record lineage with human approval for AI-assisted suggestions.",
    },
    {
        "step_number": 13,
        "step_name": "Run summary and handover package",
        "owner_type": "framework",
        "canonical_modules": ["run_summary.py", "metadata.py"],
        "expected_artifacts": ["run_summary", "handover_package"],
        "description": "Publish run summary and handover artifacts for operational continuity and review.",
    },
]


_OWNER_TYPES = {"human", "ai_assisted", "framework", "mixed"}


def get_mvp_step_registry() -> list[dict[str, Any]]:
    """Return the canonical 13-step MVP lifecycle registry."""

    return [dict(step) for step in MVP_STEP_REGISTRY]


def get_mvp_step_names() -> list[str]:
    """Return ordered MVP step names."""

    return [step["step_name"] for step in MVP_STEP_REGISTRY]


def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Validate provided artifacts against the canonical MVP registry."""

    expected = sorted({name for step in MVP_STEP_REGISTRY for name in step["expected_artifacts"]})
    available = sorted([name for name in expected if artifacts.get(name) is not None])
    missing = [name for name in expected if name not in available]

    step_errors = []
    for step in MVP_STEP_REGISTRY:
        owner_type = step.get("owner_type")
        if owner_type not in _OWNER_TYPES:
            step_errors.append({"step_number": step["step_number"], "error": f"invalid owner_type: {owner_type}"})

    return {
        "valid": not missing and not step_errors,
        "expected_artifacts": expected,
        "available_artifacts": available,
        "missing_artifacts": missing,
        "step_errors": step_errors,
    }



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
    """Create pipeline notebook template.

    Run `create_pipeline_notebook_template`.

    Parameters
    ----------
    output_path : Any
        Parameter `output_path`.
    dataset_name : object, optional
        Parameter `dataset_name`.
    source_table : object, optional
        Parameter `source_table`.
    output_table : object, optional
        Parameter `output_table`.
    source_env : object, optional
        Parameter `source_env`.
    source_target : object, optional
        Parameter `source_target`.
    output_env : object, optional
        Parameter `output_env`.
    output_target : object, optional
        Parameter `output_target`.
    include_ai_prompts : object, optional
        Parameter `include_ai_prompts`.
    overwrite : object, optional
        Parameter `overwrite`.

    Returns
    -------
    result : object
        Return value from `create_pipeline_notebook_template`.

    Raises
    ------
    FileExistsError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> create_pipeline_notebook_template(output_path, dataset_name)
    """
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
from fabric_data_product_framework.fabric_io import (
    load_fabric_config,
    get_path,
    check_naming_convention,
    lakehouse_table_read,
    lakehouse_table_write,
    ODI_METADATA_LOGGER,
)
from fabric_data_product_framework.technical_columns import (
    add_audit_columns,
    add_datetime_features,
    add_hash_columns,
)

fabric_config = load_fabric_config(CONFIG)

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
    """Create actual data mvp template.

    Run `create_actual_data_mvp_template`.

    Parameters
    ----------
    output_path : str
        Parameter `output_path`.
    contract_path : str, optional
        Parameter `contract_path`.

    Returns
    -------
    result : str
        Return value from `create_actual_data_mvp_template`.

    Examples
    --------
    >>> create_actual_data_mvp_template(output_path, contract_path)
    """
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


# --- merged from mvp_steps.py ---
"""Canonical MVP workflow registry for the Fabric data product framework."""


from copy import deepcopy
from typing import Any

LEGACY_MVP_STEPS = [
    {"step_id": 1, "name": "Define data product", "actor": "Human led", "description": "Define purpose, grain, usage, and context.", "required_inputs": ["data product purpose", "expected grain", "approved usage"], "output_artifacts": ["data_product_context"], "fabric_test_hint": "Record context cell output or metadata row."},
    {"step_id": 2, "name": "Setup config and environment", "actor": "Framework led", "description": "Build runtime config and execution context.", "required_inputs": ["environment", "source/target placeholders"], "output_artifacts": ["runtime_config"], "fabric_test_hint": "Validate runtime context and notebook naming checks."},
    {"step_id": 3, "name": "Declare source and ingest data", "actor": "Framework led", "description": "Declare source table and read data.", "required_inputs": ["source declaration", "adapter reader"], "output_artifacts": ["source_declaration"], "fabric_test_hint": "Read synthetic source table in DRY_RUN mode."},
    {"step_id": 4, "name": "Profile source and capture metadata", "actor": "Framework led", "description": "Profile source and persist profile metadata.", "required_inputs": ["source dataframe"], "output_artifacts": ["source_profile"], "fabric_test_hint": "Persist source profile metadata rows."},
    {"step_id": 5, "name": "Explore data", "actor": "Human led", "description": "Review exploratory summaries and caveats.", "required_inputs": ["source_profile"], "output_artifacts": ["exploration_notes"], "fabric_test_hint": "Capture exploration markdown note cell."},
    {"step_id": 6, "name": "Explain transformation logic", "actor": "Human led", "description": "Document business rationale for transformations.", "required_inputs": ["business context", "exploration_notes"], "output_artifacts": ["transformation_rationale"], "fabric_test_hint": "Save rationale text/record."},
    {"step_id": 7, "name": "Build transformation pipeline", "actor": "Framework led", "description": "Run transformation and write output table.", "required_inputs": ["transformation logic", "runtime_config"], "output_artifacts": ["output_table"], "fabric_test_hint": "Write synthetic curated table or DRY_RUN equivalent."},
    {"step_id": 8, "name": "AI generate DQ rules from metadata, profile, and context", "actor": "AI assisted", "description": "Generate candidate rules using metadata evidence.", "required_inputs": ["source_profile", "column metadata", "data product context"], "output_artifacts": ["dq_candidate_rules"], "fabric_test_hint": "Generate candidates or stub candidate payload in dry run."},
    {"step_id": 9, "name": "Human review DQ rules", "actor": "Human led", "description": "Approve/edit/reject candidate DQ rules.", "required_inputs": ["dq_candidate_rules"], "output_artifacts": ["approved_dq_rules"], "fabric_test_hint": "Freeze approved rules artifact and run DQ gate."},
    {"step_id": 10, "name": "AI suggest sensitivity labels", "actor": "AI assisted", "description": "Suggest sensitivity labels from profile and context.", "required_inputs": ["source_profile", "column metadata", "approved usage"], "output_artifacts": ["sensitivity_suggestions"], "fabric_test_hint": "Generate or stub sensitivity suggestions in dry run."},
    {"step_id": 11, "name": "Human review and governance gate", "actor": "Human led", "description": "Approve governance labels and gate publication.", "required_inputs": ["sensitivity_suggestions"], "output_artifacts": ["approved_governance_labels"], "fabric_test_hint": "Record governance review artifact and gate decision."},
    {"step_id": 12, "name": "AI generated lineage and transformation summary", "actor": "AI assisted", "description": "Draft lineage and transformation summary.", "required_inputs": ["transformation_rationale", "source_profile", "output_table"], "output_artifacts": ["lineage_record"], "fabric_test_hint": "Generate lineage summary markdown/records."},
    {"step_id": 13, "name": "Handover framework pack", "actor": "Framework led", "description": "Assemble handover artifacts for transfer.", "required_inputs": ["approved_dq_rules", "approved_governance_labels", "lineage_record", "source_profile"], "output_artifacts": ["handover_pack"], "fabric_test_hint": "Export or assemble handover package with caveats and run summary."},
]

REQUIRED_HANDOVER_PACK_KEYS = ["profile", "dq", "governance", "lineage", "run_summary", "caveats"]


def _get_legacy_mvp_steps() -> list[dict[str, Any]]:
    """Get mvp step registry.

    Run `get_mvp_step_registry`.

    Parameters
    ----------
    None
        This callable does not require user-provided parameters.

    Returns
    -------
    result : list[dict[str, Any]]
        Return value from `get_mvp_step_registry`.

    Examples
    --------
    >>> get_mvp_step_registry()
    """
    return deepcopy(LEGACY_MVP_STEPS)


def validate_mvp_artifacts(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Validate mvp artifacts.

    Run `validate_mvp_artifacts`.

    Parameters
    ----------
    artifacts : dict[str, Any]
        Parameter `artifacts`.

    Returns
    -------
    result : dict[str, Any]
        Return value from `validate_mvp_artifacts`.

    Examples
    --------
    >>> validate_mvp_artifacts(artifacts)
    """
    expected_top_level = sorted({a for s in LEGACY_MVP_STEPS for a in s["output_artifacts"]})
    missing_top_level = [name for name in expected_top_level if name not in artifacts]
    invalid_fields: list[dict[str, str]] = []

    if "approved_dq_rules" in artifacts and not isinstance(artifacts["approved_dq_rules"], list):
        invalid_fields.append({"field": "approved_dq_rules", "issue": "must be a list"})

    if "approved_governance_labels" in artifacts and not isinstance(artifacts["approved_governance_labels"], list):
        invalid_fields.append({"field": "approved_governance_labels", "issue": "must be a list"})

    if "lineage_record" in artifacts and not isinstance(artifacts["lineage_record"], (dict, list)):
        invalid_fields.append({"field": "lineage_record", "issue": "must be a dict or list"})

    missing_handover_keys: list[str] = []
    if "handover_pack" in artifacts:
        if not isinstance(artifacts["handover_pack"], dict):
            invalid_fields.append({"field": "handover_pack", "issue": "must be a dict"})
        else:
            missing_handover_keys = [k for k in REQUIRED_HANDOVER_PACK_KEYS if k not in artifacts["handover_pack"]]

    valid = not missing_top_level and not invalid_fields and not missing_handover_keys
    return {
        "valid": valid,
        "is_valid": valid,
        "expected_top_level_artifacts": expected_top_level,
        "missing_top_level_artifacts": missing_top_level,
        "invalid_fields": invalid_fields,
        "required_handover_pack_keys": REQUIRED_HANDOVER_PACK_KEYS,
        "missing_handover_pack_keys": missing_handover_keys,
    }



# --- merged from ai_context.py ---
"""AI context export module scaffold."""
