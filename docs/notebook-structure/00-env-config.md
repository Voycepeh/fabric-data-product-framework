# 00_env_config

`00_env_config` is the shared runtime bootstrap for the full FabricOps notebook chain.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open template notebook</a>

## Purpose

`00_env_config` is the first notebook loaded by downstream notebooks and centralizes common setup so the rest of the flow stays clean, repeatable, and run-all-safe.

Downstream notebooks should start with:

```python
%run 00_env_config
```

After that, `01_dsa`, `02_ex`, and `03_pc` notebooks share the same runtime context, paths, prompts, classes, helper functions, and validation checks.

## How it fits the notebook lifecycle

The parent [Notebook Structure](../notebook-structure.md) page remains the high-level source of truth for notebook roles.

`00_env_config` implements **Step 2: Config** in the delivery flow and prepares runtime state for:

- ingestion
- exploration and profiling
- transformation
- standardization
- output publishing
- metadata capture
- lineage capture
- handover summaries

`02_ex` explains the **why** through profiling and evidence.
`03_pc` enforces the approved **what**.
`00_env_config` gives both notebooks the same shared runtime foundation.

## What belongs in 00_env_config

1. **Environment and path registry**
   - dev/prod or sandbox/prod environment setup
   - Source, Unified, Product, Metadata, and Warehouse targets
   - guardrails against accidental cross-environment leakage

2. **Shared classes and config objects**
   - `Housepath` or equivalent path object
   - environment and target registry objects
   - notebook naming rules
   - runtime context object
   - technical/audit column standards
   - metadata table name defaults

3. **Shared variables**
   - `ENV`
   - `AGREEMENT_ID`
   - `SOURCE_LAYER`
   - `TARGET_LAYER`
   - `RUN_ID`
   - `RUN_TIMESTAMP`
   - `AI_ENABLED`
   - `VALIDATION_MODE`
   - default metadata table names
   - default output naming conventions

4. **Shared utility functions**
   - `get_path`
   - lakehouse read/write helpers
   - warehouse read/write helpers
   - metadata logging helpers
   - datetime cleaning helpers
   - technical column helpers
   - transformation summary helpers
   - validation helpers

5. **AI prompt registry**
   - business context interpretation prompt
   - DQ rule suggestion prompt
   - DQ rule review prompt
   - governance/sensitivity classification prompt
   - metadata/profile explanation prompt
   - lineage summary prompt
   - handover summary prompt

6. **Startup validation / fail-fast tests**
   - required imports
   - Fabric runtime availability
   - `notebookutils` availability where used
   - required parameters/widgets
   - notebook naming convention
   - configured environment exists
   - configured source/unified/product/metadata targets exist
   - no cross-environment target mismatch
   - metadata table names are configured
   - Fabric AI function readiness when `AI_ENABLED=True`

## What does not belong in 00_env_config

- dataset-specific transformation logic
- one-off exploration cells
- business-rule enforcement that belongs in `03_pc`
- agreement approval content that belongs in `01_dsa`
- source-specific profiling commentary that belongs in `02_ex`

## Expected usage

```python
%run 00_env_config

get_path("source")
lakehouse_table_read("source", "sales.orders")
check_naming_convention("02_ex_customer_orders")
initialize_fabricops_runtime()
AI_PROMPTS["dq_rule_suggestion"]
```

## Maintenance rules

- Edit once per environment/workspace.
- Keep placeholders in public templates.
- Do not commit real workspace IDs, lakehouse IDs, warehouse IDs, or internal names.
- Keep dev/sandbox configuration separate from prod.
- If `00_env_config` passes startup validation, downstream notebooks can assume shared runtime setup is ready.
