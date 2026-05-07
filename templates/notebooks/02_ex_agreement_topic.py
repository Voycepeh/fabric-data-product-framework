"""Exploration notebook template (Step 3, 4, 5, 8, 9)."""

from fabricops_kit import (
    assert_notebook_name_valid,
    bootstrap_fabric_env,
    build_ai_quality_context,
    build_governance_classification_records,
    build_manual_dq_rule_prompt_package,
    build_manual_governance_prompt_package,
    build_runtime_context,
    classify_columns,
    generate_dq_rule_candidates_with_fabric_ai,
    generate_governance_candidates_with_fabric_ai,
    generate_metadata_profile,
    get_path,
    lakehouse_table_read,
    load_fabric_config,
    profile_dataframe_to_metadata,
    summarize_governance_classifications,
    validate_notebook_name,
    warehouse_read,
)

# 1) Purpose, data agreement, approved usage
print("Exploration notebook: advisory analysis only; no production enforcement.")
DATA_AGREEMENT = "TODO_replace_agreement_name"
APPROVED_USAGE = "TODO_replace_with_approved_usage_statement"

# 2) Runtime setup
NOTEBOOK_NAME = "02_ex_agreement_topic"
validate_notebook_name(NOTEBOOK_NAME)
assert_notebook_name_valid(NOTEBOOK_NAME)
CONFIG = load_fabric_config(CONFIG)  # Expects `%run 00_env_config` first.
runtime_context = build_runtime_context(
    dataset_name="topic_dataset",
    environment="dev",
    source_table="source.table_name",
    target_table="unified.topic_dataset",
    notebook_name=NOTEBOOK_NAME,
)
bootstrap_fabric_env(config=CONFIG, environment="dev")

# 3) Source declaration
SOURCE_LAYER = "source"  # source / unified
SOURCE_KIND = "lakehouse"  # lakehouse / warehouse
SOURCE_TABLE = "TODO_source_table"

# 4) Load source data
source_house = get_path("dev", SOURCE_LAYER, config=CONFIG)
if SOURCE_KIND == "lakehouse":
    df_source = lakehouse_table_read(source_house, SOURCE_TABLE)
else:
    df_source = warehouse_read(source_house, schema="dbo", table=SOURCE_TABLE)

# 5) Source schema and sample preview
print(df_source.schema)
display(df_source.limit(20))

# 6) Source metadata profiling
profile_rows = generate_metadata_profile(df_source, dataset_name="topic_dataset")
metadata_rows = profile_dataframe_to_metadata(df_source, dataset_name="topic_dataset")

# 7) Store or display source profile
display(profile_rows)
display(metadata_rows)

# 8) Exploration findings
print("TODO: capture profiling findings and risks observed during EDA.")

# 9) Transformation rationale
print("TODO: explain approved transformation rationale for pipeline handoff.")

# 10) AI-assisted DQ rule suggestions (advisory only)
ai_quality_context = build_ai_quality_context(profile_rows, dataset_name="topic_dataset")
manual_dq_prompt = build_manual_dq_rule_prompt_package(
    business_context="Data quality review for topic_dataset",
    dataset_name="topic_dataset",
    profile_context=ai_quality_context,
)
print("AI advisory only. Human approval required before pipeline use.")

try:
    dq_candidates = generate_dq_rule_candidates_with_fabric_ai(
        profile_rows,
        dataset_name="topic_dataset",
        business_context="Exploration-only draft rules",
    )
    display(dq_candidates)
except Exception:
    print("Fabric AI unavailable; use manual prompt package.")
    print(manual_dq_prompt["prompt"])

# 11) Human-reviewed DQ rule decisions
APPROVED_DQ_RULES = [
    # TODO: replace with human-approved deterministic rules.
]

# 12) AI-assisted classification suggestions (advisory only)
manual_gov_prompt = build_manual_governance_prompt_package(
    business_context="Exploration-only draft governance labels",
    dataset_name="topic_dataset",
    profile_context=ai_quality_context,
)
classification_candidates = classify_columns(profile_rows, business_context={"agreement": DATA_AGREEMENT})
summary = summarize_governance_classifications(classification_candidates)
print(summary)

try:
    ai_classification_candidates = generate_governance_candidates_with_fabric_ai(
        profile_rows,
        business_context="Exploration-only draft governance labels",
    )
    display(ai_classification_candidates)
except Exception:
    print("Fabric AI unavailable; use manual governance prompt package.")
    print(manual_gov_prompt["prompt"])

# 13) Human-reviewed classification decisions
APPROVED_CLASSIFICATIONS = [
    # TODO: replace with steward/governance-approved labels.
]
classification_records = build_governance_classification_records(
    dataset_name="topic_dataset",
    environment="dev",
    classifications=APPROVED_CLASSIFICATIONS,
    run_id=runtime_context["run_id"],
)

# 14) Draft output contract handoff
print("TODO: write contract draft for pipeline notebook based on approved decisions.")

# 15) Notes for pipeline notebook
print("Copy only approved rules/labels and transformation logic into 03_pc notebook.")
