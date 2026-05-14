# 00_env_config

`00_env_config` is the single shared environment bootstrap notebook for FabricOps Starter Kit templates.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open template notebook</a>

## Purpose

`00_env_config` loads first and defines only environment-wide configuration values plus framework wiring.
Reusable behavior is imported from `src/fabricops_kit/` package modules.

## What belongs in 00_env_config

- Environment-wide values such as `ENV`, `VALIDATION_MODE`, and `AI_ENABLED`
- Notebook naming policy (allowed prefixes)
- Environment path registry values (as `Housepath` placeholders)
- Framework config assembly (`PathConfig`, `NotebookRuntimeConfig`, `AIPromptConfig`, `FrameworkConfig`)
- Startup bootstrap and smoke checks (`load_fabric_config`, `setup_fabricops_notebook`)

## What does not belong in 00_env_config

- Reusable helper function implementations (these belong in `src/fabricops_kit/*.py`)
- `AGREEMENT_ID`, `SOURCE_LAYER`, `TARGET_LAYER`
- Dataset-, contract-, or run-specific parameters

## Downstream ownership

Downstream notebooks define their own scoped parameters:

- `01_dsa_*`: agreement scope and agreement identifiers
- `02_ex_*`: exploration source/topic parameters
- `03_pc_*`: source layer, target layer, and input/output table parameters

## Usage pattern

```python
%run 00_env_config

# Package helpers imported by 00_env_config are available for downstream notebooks.
source_hp = get_path(ENV, "source", CONFIG)
```

## Maintenance rules

- Keep template defaults public-safe and placeholder-based.
- Do not commit production identifiers or internal URLs.
- Keep `00_env_config` singular per environment/workspace.
