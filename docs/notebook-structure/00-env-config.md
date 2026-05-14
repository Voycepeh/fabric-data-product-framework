# 00_env_config

`00_env_config` is the single shared runtime bootstrap notebook for downstream FabricOps notebooks.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open template notebook</a>

## Purpose

`00_env_config` is loaded first and centralizes shared setup so downstream notebooks can stay run-all-safe and reusable.

```python
%run 00_env_config
```

After loading, `01_dsa`, `02_ex`, and `03_pc` notebooks can use the same runtime context, path registry, helper functions, prompts, and startup checks.

## How it fits the notebook lifecycle

The parent [Notebook Structure](../notebook-structure.md) page is the source of truth for notebook roles.

`00_env_config` implements the parent page **Environment runtime configuration role**:

- shared environment config
- shared paths
- runtime settings
- startup checks
- reusable config objects
- shared prompts
- shared helper functions

This shared runtime foundation is reused by exploration notebooks (`02_ex`) and pipeline contract notebooks (`03_pc`).

## What belongs in 00_env_config

1. **Environment and path registry**
   - dev/prod or sandbox/prod setup
   - Source, Unified, Product, Metadata, and Warehouse targets
   - cross-environment mismatch guardrails
2. **Shared classes and config objects**
   - `Housepath` and runtime context objects
   - environment and target registries
   - notebook naming rules
   - technical/audit standards
3. **Shared variables**
   - `ENV`, `AGREEMENT_ID`, `SOURCE_LAYER`, `TARGET_LAYER`
   - `RUN_ID`, `RUN_TIMESTAMP`, `AI_ENABLED`, `VALIDATION_MODE`
   - metadata table name defaults and output naming defaults
4. **Shared utility functions**
   - path resolution (`get_path`)
   - lakehouse helpers
   - metadata/event helpers
   - datetime and technical column helpers
   - validation helpers
5. **Shared AI prompt registry**
   - business context
   - DQ rule suggestion/review
   - governance classification
   - profile, lineage, and handover summaries
6. **Startup validation / fail-fast tests**
   - runtime import checks
   - optional Fabric runtime checks
   - naming convention checks
   - environment/target registry checks
   - metadata defaults checks
   - AI readiness checks when enabled

## What does not belong in 00_env_config

- dataset-specific transformation logic
- one-off exploration analysis cells
- pipeline business-rule enforcement that belongs in `03_pc`
- agreement approval content that belongs in `01_dsa`
- source-specific profiling commentary that belongs in `02_ex`

## Expected usage

```python
%run 00_env_config

get_path("source")
active_lakehouse_table_read("sales.orders")
check_naming_convention()
initialize_fabricops_runtime()
AI_PROMPTS["dq_rule_suggestion"]
```

## Maintenance rules

- Keep template values public-safe and placeholder-based.
- Do not commit real workspace IDs, lakehouse IDs, warehouse IDs, or internal names.
- Use `VALIDATION_MODE="warn"` in templates; use `"strict"` for production-ready `03_pc` notebooks.
- If startup validation passes, downstream notebooks can assume shared runtime setup is ready.
