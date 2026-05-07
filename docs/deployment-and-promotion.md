# Deployment and promotion

## Enterprise-friendly promotion model

FabricOps Starter Kit does not assume Git integration is always available in Microsoft Fabric enterprise environments.

- If Git integration is available, teams can use it for source control, review, and release workflows.
- If Git integration is blocked by policy or platform constraints, teams can still run a governed promotion model using Fabric deployment pipelines and controlled admin notebooks.

This keeps day-to-day engineering and governance operations viable in both Git-enabled and Git-restricted setups.

## What gets promoted

Fabric deployment pipelines can promote supported Fabric item definitions, including notebooks and other supported data engineering items.

In this model:

- Selected `03_pc` notebooks (and other supported items) are promoted from Dev to Test/Prod.
- Notebook deployment rules can rebind or map the target default lakehouse in each stage where supported.
- Lakehouse and Warehouse items may be deployed through pipelines or manually created per enterprise operating process.

## What does not get solved automatically

Deployment does not remove the need to provision and validate target environments. Teams still need explicit setup and validation for:

- target workspaces
- lakehouses / warehouses
- default lakehouse bindings
- Fabric environments / libraries
- permissions
- metadata tables
- contract records
- schedules / orchestration
- deployment rules

Promotion reliability depends on these dependencies being governed and validated per environment.

## Environment-local `00_env_config`

Normal lifecycle notebooks are designed to run as single-environment workloads.

- Each workspace should maintain its own `00_env_config` notebook.
- Dev `00_env_config` should point only to dev stores.
- Prod `00_env_config` should point only to prod stores.
- Avoid promoting `00_env_config` unchanged into prod unless the team has a controlled, audited config promotion process.

This prevents accidental cross-environment reads/writes and keeps runtime behavior explicit.

## Recommended promotion flow without Git

### Dev workspace

- Edit and test `02_ex` / `03_pc` notebooks.
- Approve source input contract records in dev metadata.
- Validate expected outputs.

### Deployment pipeline

- Promote selected `03_pc` notebooks and supported items to Test/Prod.
- Apply deployment rules for default lakehouse mapping where needed.

### Prod workspace

- Keep prod `00_env_config` in place.
- Run bootstrap smoke tests.
- Promote approved contract metadata into the prod metadata store.
- Run prod `03_pc` notebooks against prod config and prod metadata only.

## Contract and metadata promotion

Contract records are operational metadata, not just source code artifacts.

- Store contract and related operational metadata in each environment's metadata lakehouse or warehouse.
- Dev-approved contracts are not automatically prod-approved.
- Promote contracts through a controlled admin notebook or equivalent governed process.
- Prod pipelines must not read dev metadata at runtime.

Notebook code promotion and contract/metadata promotion should be treated as related but separate controls.

## Admin notebooks for cross-environment operations

Normal `03_pc` notebooks should remain single-environment.

When cross-environment operations are required, use explicit admin notebooks, for example:

- `90_admin_promote_contract_dev_to_prod`
- `90_admin_compare_contract_dev_prod`
- `90_admin_validate_prod_setup`

These admin notebooks provide intentional, auditable paths for environment-to-environment actions.
