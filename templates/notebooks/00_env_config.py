"""Shared Fabric notebook runtime configuration template (Step 1, 2A, 2B)."""

from fabricops_kit import (
    Housepath,
    bootstrap_fabric_env,
    check_fabric_ai_functions_available,
    configure_fabric_ai_functions,
    create_ai_prompt_config,
    create_framework_config,
    create_governance_config,
    create_lineage_config,
    create_notebook_runtime_config,
    create_path_config,
    create_quality_config,
    get_path,
    load_fabric_config,
    run_config_smoke_tests,
    validate_framework_config,
)

# 1) Purpose of this config notebook
print("00_env_config: build once, reuse in exploration and pipeline notebooks.")

# 2) User-editable project constants
# TODO: Replace sample IDs/names with your own Fabric workspace and house values.
ENV_NAME = "dev"  # Example values: dev, prod
NOTEBOOK_PREFIXES = ["00_", "02_ex_", "03_pc_"]

# 3) Environment path configuration
PATH_CONFIG = create_path_config(
    {
        ENV_NAME: {
            "source": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000001",
                house_id="11111111-1111-1111-1111-111111111111",
                house_name="lh_source",
                root="abfss://REPLACE-WORKSPACE@onelake.dfs.fabric.microsoft.com/REPLACE-HOUSE",
            ),
            "unified": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000001",
                house_id="11111111-1111-1111-1111-111111111112",
                house_name="lh_unified",
                root="abfss://REPLACE-WORKSPACE@onelake.dfs.fabric.microsoft.com/REPLACE-HOUSE",
            ),
            "product": Housepath(
                workspace_id="00000000-0000-0000-0000-000000000001",
                house_id="11111111-1111-1111-1111-111111111113",
                house_name="lh_product",
                root="abfss://REPLACE-WORKSPACE@onelake.dfs.fabric.microsoft.com/REPLACE-HOUSE",
            ),
        }
    }
)

# 4) Notebook naming policy
NOTEBOOK_RUNTIME_CONFIG = create_notebook_runtime_config(valid_prefixes=NOTEBOOK_PREFIXES)

# 5) AI prompt configuration
AI_PROMPT_CONFIG = create_ai_prompt_config(
    quality_rule_generation_template=(
        "Suggest deterministic quality rules from profile/context. "
        "Output JSON only. Profile: {profile}"
    ),
    governance_candidate_template=(
        "Suggest governance labels from metadata/context. "
        "Output JSON only. Profile: {profile}"
    ),
)

# 6) Governance defaults
GOVERNANCE_CONFIG = create_governance_config(required_classification=True)

# 7) Quality defaults
QUALITY_CONFIG = create_quality_config(default_severity="warning", fail_on_critical=True)

# 8) Lineage / handover defaults
LINEAGE_CONFIG = create_lineage_config(capture_transformation_steps=True, capture_ai_summaries=False)

# 9) Build framework config
CONFIG = create_framework_config(
    path_config=PATH_CONFIG,
    notebook_runtime_config=NOTEBOOK_RUNTIME_CONFIG,
    ai_prompt_config=AI_PROMPT_CONFIG,
    governance_config=GOVERNANCE_CONFIG,
    quality_config=QUALITY_CONFIG,
    lineage_config=LINEAGE_CONFIG,
)

# 10) Validate config
CONFIG = validate_framework_config(CONFIG)
FABRIC_CONFIG = load_fabric_config(CONFIG)

# 11) Startup smoke test
smoke = run_config_smoke_tests(config=FABRIC_CONFIG, environment=ENV_NAME)
print("Smoke check status:", smoke.get("status", "unknown"))
bootstrap = bootstrap_fabric_env(config=FABRIC_CONFIG, environment=ENV_NAME)
print("Bootstrap status:", bootstrap.get("status", "unknown"))

ai_status = check_fabric_ai_functions_available()
print("Fabric AI Functions available:", ai_status.get("available", False))
if ai_status.get("available"):
    configure_fabric_ai_functions(temperature=0.0)

# 12) Example: resolve source, unified, and product paths
source_path = get_path(ENV_NAME, "source", config=FABRIC_CONFIG)
unified_path = get_path(ENV_NAME, "unified", config=FABRIC_CONFIG)
product_path = get_path(ENV_NAME, "product", config=FABRIC_CONFIG)

print("source house:", source_path.house_name)
print("unified house:", unified_path.house_name)
print("product house:", product_path.house_name)
