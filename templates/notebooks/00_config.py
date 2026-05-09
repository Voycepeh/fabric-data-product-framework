"""Sample reusable framework config notebook for FabricOps Starter Kit."""

# EDIT THESE VALUES BEFORE USE:
# 1) Replace all sample workspace_id / house_id / house_name / root values.
# 2) Add your real environments and targets under PATH_CONFIG.
# 3) Tune notebook prefixes and default AI/quality/governance/lineage behavior.
# 4) Keep this notebook reusable and run `%run 00_config` from operational notebooks.

from fabricops_kit import (
    Housepath,
    create_ai_prompt_config,
    create_framework_config,
    create_governance_config,
    create_lineage_config,
    create_notebook_runtime_config,
    create_path_config,
    create_quality_config,
    get_default_dq_rule_templates,
)

PATH_CONFIG = create_path_config(
    {
        "Sandbox": {
            "Source": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000001",
                house_id="11111111-1111-1111-1111-111111111111",
                house_name="lh_source",
                root="abfss://00000000-0000-0000-0000-000000000001@onelake.dfs.fabric.microsoft.com/11111111-1111-1111-1111-111111111111",
            ),
            "Unified": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000001",
                house_id="11111111-1111-1111-1111-111111111112",
                house_name="lh_unified",
                root="abfss://00000000-0000-0000-0000-000000000001@onelake.dfs.fabric.microsoft.com/11111111-1111-1111-1111-111111111112",
            ),
        }
    }
)

NOTEBOOK_RUNTIME_CONFIG = create_notebook_runtime_config(["00_", "01_", "02_", "03_"])
AI_PROMPT_CONFIG = create_ai_prompt_config(
    lineage_summary_template="Summarize these transformation steps for lineage handover: {steps}",
    handover_summary_template="Generate a concise handover summary for dataset {dataset_name}: {context}",
    quality_rule_generation_template="Generate deterministic quality-rule candidates using this profile: {profile}",
)
QUALITY_CONFIG = create_quality_config(default_severity="warning", fail_on_critical=True, quarantine_on_failure=False)
GOVERNANCE_CONFIG = create_governance_config(required_classification=True, sensitivity_rules={"email": "sensitive"})
LINEAGE_CONFIG = create_lineage_config(capture_ai_summaries=True, capture_transformation_steps=True)

CONFIG = create_framework_config(
    path_config=PATH_CONFIG,
    notebook_runtime_config=NOTEBOOK_RUNTIME_CONFIG,
    ai_prompt_config=AI_PROMPT_CONFIG,
    quality_config=QUALITY_CONFIG,
    governance_config=GOVERNANCE_CONFIG,
    lineage_config=LINEAGE_CONFIG,
)


# Data Quality Rules
# Copy and edit these rules per output table after profiling and business review.
DQ_RULES = get_default_dq_rule_templates()

# Editable AI suggestion prompt template for notebook users.
DQ_RULE_SUGGESTION_PROMPT_TEMPLATE = """Suggest candidate DQ rules for table '{table_name}'.
AI output is advisory only; human review and approval is required before adding rules to DQ_RULES.
Use only: not_null, unique_key, accepted_values, accepted_values_ref, value_range, regex_format, string_length_between. Schema drift, data drift, row count, and freshness checks are out of scope and belong to drift/contract modules.
Return only Python dictionary output named DQ_RULES in {output_format} format.
Business context:
{business_context}
Profile metadata:
{profile_json}
"""

