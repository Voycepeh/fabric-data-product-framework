# `00_env_config`

`00_env_config` is the shared environment bootstrap notebook for a FabricOps workspace or environment. Run it before agreement (`01_*`), exploration (`02_*`), or pipeline contract (`03_*`) notebooks. It prepares the shared `CONFIG` object and validates that required environment targets are available for downstream steps.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open template notebook</a>

## What this notebook does

This notebook performs environment setup, not business logic. It:

1. Imports reusable FabricOps package helpers and config classes.
2. Defines the active environment (for example, `dev`).
3. Sets notebook validation mode.
4. Defines allowed notebook naming prefixes.
5. Defines environment targets for `source`, `unified`, `product`, and `metadata`.
6. Defines the full operational prompt strings used by AI-assisted workflow steps.
7. Assembles `FrameworkConfig` and its sub-configs.
8. Runs `load_config` and `setup_notebook` startup validation.
9. Runs `check_naming_convention` for notebook naming policy.
10. Prints resolved bootstrap status for quick verification.

## Segment 1: Explain the shared environment role

The first segment establishes this notebook as the common runtime entry point. The imports and constants defined here make sure all downstream notebooks use one shared setup model instead of redefining environment behavior in each notebook.

### What gets imported

The notebook imports helper groups that are reused later in the template flow.

**I/O helpers**

- `FabricStore`
- `check_naming_convention`
- `read_lakehouse_csv`
- `read_lakehouse_table`
- `write_lakehouse_table`
- `read_warehouse_table`
- `write_warehouse_table`

**Config classes**

- `AIPromptConfig`
- `FrameworkConfig`
- `GovernanceConfig`
- `LineageConfig`
- `NotebookRuntimeConfig`
- `PathConfig`
- `QualityConfig`
- `ReviewWorkflowConfig`

**Bootstrap helpers**

- `load_config`
- `setup_notebook`

These imports are intentionally loaded in `00_env_config` so downstream notebooks can focus on their own stage tasks instead of repeating framework bootstrap code.

## Segment 2: Define environment targets and notebook policy

This segment defines environment selection, naming validation behavior, and logical Fabric targets.

### Environment and validation settings

- `ENV` controls which environment path group is active (for example, `dev`).
- `VALIDATION_MODE` controls whether naming checks warn or fail.
- `NOTEBOOK_PREFIXES` defines expected notebook naming prefixes.

`warn` mode allows testing and iteration to continue with visible warnings. `strict` mode is better when teams want naming violations to fail early.

### Fabric targets

The notebook defines four standard logical targets:

| Target | Meaning | Used by |
| --- | --- | --- |
| `source` | Source or raw lakehouse | Exploration and pipeline notebooks that read source data |
| `unified` | Standardized or transformed lakehouse | Notebooks that produce cleaned or intermediate outputs |
| `product` | Product or serving warehouse | Pipeline contracts that publish curated outputs |
| `metadata` | Metadata/evidence lakehouse | Governance, profiling, quality, lineage, and handover evidence |

The template includes placeholder Fabric item names and IDs. Replace these with real workspace values before production use.

## Segment 3: Set AI, quality, governance, and lineage defaults

This segment sets default prompt templates and framework policy defaults used by the rest of the notebook flow.

This notebook owns the full prompt strings used by the AI-assisted workflow. Those prompt strings are visible, auditable, and editable per workspace or environment in the notebook itself. Package functions consume prompt templates from `AIPromptConfig` (or explicit function arguments when provided), and should not rely on hidden package-level `DEFAULT_*` prompt constants at runtime.

`00_env_config` also does **not** check whether Fabric AI execution works. AI-assisted cells should handle AI availability locally when they run.

### AI prompt templates

`00_env_config` loads these standard templates into `AIPromptConfig`:

- `BUSINESS_CONTEXT_PROMPT_TEMPLATE` for business context extraction.
- `DQ_RULE_SUGGESTION_PROMPT_TEMPLATE` for AI-assisted DQ rule suggestion.
- `GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE` for personal identifier detection.
- `GOVERNANCE_CANDIDATE_PROMPT_TEMPLATE` for governance candidate classification.
- `GOVERNANCE_REVIEW_PROMPT_TEMPLATE` for governance review support.
- `HANDOVER_SUMMARY_PROMPT_TEMPLATE` for handover summary generation.

AI supports these tasks, but governance approvals and DQ rule validity remain human-controlled decisions.

## Segment 4: Assemble and validate framework config

This segment builds the typed config pieces and combines them into one shared framework object.

The notebook assembles:

- `PATH_CONFIG`
- `RUNTIME_CONFIG`
- `AI_PROMPT_CONFIG`
- `QUALITY_CONFIG`
- `GOVERNANCE_CONFIG`
- `REVIEW_WORKFLOW_CONFIG`
- `LINEAGE_CONFIG`

Then combines them into:

```python
CONFIG = FrameworkConfig(...)
```

`CONFIG` is the primary shared runtime object for downstream notebooks.

## Segment 5: Run startup checks and show resolved paths

This segment performs startup validation and emits a quick resolved-status printout.

### Startup checks

```python
CONFIG = load_config(CONFIG)

BOOTSTRAP = setup_notebook(
    config=CONFIG,
    env=ENV,
    required_targets=["source", "unified", "product", "metadata"],
    notebook_name="00_env_config",
)

check_naming_convention(...)
```

What each check proves:

- `load_config` validates and normalizes the supplied config object.
- `setup_notebook` verifies the selected environment exists and required targets are configured.
- `check_naming_convention` evaluates notebook naming policy.

### What is available after the notebook runs

Expected runtime state includes:

**Variables**

- `ENV`
- `VALIDATION_MODE`
- `NOTEBOOK_PREFIXES`
- `ENV_PATHS`
- `CONFIG`
- `BOOTSTRAP`

**Helpers**

- `read_lakehouse_csv`
- `read_lakehouse_table`
- `write_lakehouse_table`
- `read_warehouse_table`
- `write_warehouse_table`
- `check_naming_convention`
- `load_config`
- `setup_notebook`

**Prompt templates**

- `BUSINESS_CONTEXT_PROMPT_TEMPLATE`
- `DQ_RULE_SUGGESTION_PROMPT_TEMPLATE`
- `GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE`
- `GOVERNANCE_CANDIDATE_PROMPT_TEMPLATE`
- `GOVERNANCE_REVIEW_PROMPT_TEMPLATE`
- `HANDOVER_SUMMARY_PROMPT_TEMPLATE`

### How to interpret a successful run

If `00_env_config` runs successfully, the environment bootstrap has passed. That means the framework config can be built, required logical targets are present, and downstream notebooks can start from shared `CONFIG` and `BOOTSTRAP` state.

A successful run does **not** prove real Fabric item IDs are correct unless you replace placeholders and test real reads/writes in your workspace.
