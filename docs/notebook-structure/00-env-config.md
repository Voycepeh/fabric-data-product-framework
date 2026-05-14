# 00_env_config

`00_env_config` is the shared environment bootstrap notebook for FabricOps Starter Kit.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open template notebook</a>

## Purpose

Use one `00_env_config` notebook per environment/workspace. It is loaded by downstream notebooks with `%run 00_env_config` and should contain environment-wide values and configuration wiring only.

Main principle:

- **Is**: environment bootstrap, package-default wiring, and environment-level AI prompt override review.
- **Is not**: agreement-specific, source/target-specific, helper-function implementation, or dataset-specific transformation/governance logic.

## What the template contains

### Package imports

The template imports reusable package behavior from:

- `fabricops_kit.fabric_input_output`
- `fabricops_kit.config`

Imported capabilities include:

- `Housepath`
- `lakehouse_table_read` / `lakehouse_table_write`
- `lakehouse_csv_read`
- `warehouse_read` / `warehouse_write`
- `check_naming_convention`
- `PathConfig`
- `NotebookRuntimeConfig`
- `AIPromptConfig`
- `FrameworkConfig`
- `load_fabric_config`
- `get_path`
- `setup_fabricops_notebook`

### Environment-level values

The template defines environment-level control values:

- `ENV`
- `VALIDATION_MODE`
- `AI_ENABLED`
- `NOTEBOOK_PREFIXES`

`VALIDATION_MODE` guidance:

- `"warn"` is safer for public templates and initial setup.
- `"strict"` should fail naming checks when you are ready for controlled production use.

### Environment path registry

`ENV_PATHS` registers per-environment targets and `Housepath` values. Expected target keys are:

- `source`
- `unified`
- `product`
- `metadata`
- `warehouse`

Replace placeholder `Housepath` IDs, item names, and roots with your own Fabric workspace/lakehouse/warehouse identifiers.

### AI prompt overrides

Prompt defaults come from package constants:

- `DEFAULT_BUSINESS_CONTEXT_PROMPT_TEMPLATE`
- `DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE`
- `DEFAULT_GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE`
- `DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE`
- `DEFAULT_GOVERNANCE_REVIEW_TEMPLATE`
- `DEFAULT_HANDOVER_SUMMARY_TEMPLATE`

`00_env_config` maps these into environment override variables:

- `BUSINESS_CONTEXT_PROMPT_TEMPLATE`
- `DQ_RULE_SUGGESTION_PROMPT_TEMPLATE`
- `GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE`
- `GOVERNANCE_CANDIDATE_PROMPT_TEMPLATE`
- `GOVERNANCE_REVIEW_PROMPT_TEMPLATE`
- `HANDOVER_SUMMARY_PROMPT_TEMPLATE`

Policy:

- The package is the source of truth for default prompt text.
- `00_env_config` exposes prompt override cells so a workspace can intentionally override defaults.
- Downstream notebooks should consume prompts from `CONFIG.ai_prompt_config`.

### Framework config assembly

The template assembles framework objects in order:

- `PATH_CONFIG = PathConfig(...)`
- `RUNTIME_CONFIG = NotebookRuntimeConfig(...)`
- `AI_PROMPT_CONFIG = AIPromptConfig(...)`
- `QUALITY_CONFIG = QualityConfig()`
- `GOVERNANCE_CONFIG = GovernanceConfig()`
- `REVIEW_WORKFLOW_CONFIG = ReviewWorkflowConfig()`
- `LINEAGE_CONFIG = LineageConfig()`
- `CONFIG = FrameworkConfig(...)`

`CONFIG` is the object downstream notebooks should rely on.

### Bootstrap checks

The template runs:

- `CONFIG = load_fabric_config(CONFIG)` to apply runtime-aware Fabric configuration updates.
- `BOOTSTRAP = setup_fabricops_notebook(...)` to validate required targets and optional AI dependencies.
- `check_naming_convention(..., fail_on_error=(VALIDATION_MODE == "strict"))` to enforce notebook naming policy.

### Downstream usage

```python
%run 00_env_config

source_hp = get_path(ENV, "source", CONFIG)
metadata_hp = get_path(ENV, "metadata", CONFIG)

# Downstream notebooks define their own scoped variables
AGREEMENT_ID = "..."
SOURCE_LAYER = "source"
TARGET_LAYER = "unified"
```

Keep those downstream variables in downstream notebooks; do not move them back into `00_env_config`.

## What belongs / what does not belong

### Belongs

- Imports from package modules
- Environment values
- Path registry
- Notebook prefix policy
- Prompt override variables
- Config object assembly
- Bootstrap checks

### Does not belong

- Reusable function definitions
- Dataclass definitions already in package
- `AGREEMENT_ID`
- `SOURCE_LAYER`
- `TARGET_LAYER`
- `SOURCE_TABLE` / `TARGET_TABLE`
- Transformation logic
- DQ enforcement logic
- Agreement approval content
- One-off exploration analysis

## Before using this template

- Install/import the `fabricops_kit` wheel in Fabric.
- Replace placeholder `Housepath` IDs and roots.
- Confirm `ENV` matches the active environment.
- Confirm target keys match downstream notebooks.
- Review AI prompt override cells.
- Keep `VALIDATION_MODE = "warn"` during setup.
- Switch to `"strict"` once naming and paths are stable.

## Common mistakes

- Defining helper functions inside `00_env_config` instead of package modules.
- Putting `AGREEMENT_ID` or source/target layer variables here.
- Editing package default prompts directly when only an environment override is needed.
- Using prompt names that do not exist in `AIPromptConfig`.
- Using target names in downstream notebooks that do not exist in `ENV_PATHS`.
