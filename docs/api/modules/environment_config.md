# `environment_config` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`bootstrap_fabric_env`](../../reference/step-02b-notebook-startup-checks/bootstrap_fabric_env.md) | function | Bootstrap 00_env_config environment readiness for FabricOps notebooks. | [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) (internal) |
| [`check_fabric_ai_functions_available`](../../reference/step-02a-shared-runtime-config/check_fabric_ai_functions_available.md) | function | Check whether Fabric AI Functions are available in the current runtime. | — |
| [`configure_fabric_ai_functions`](../../reference/step-01-governance-context/configure_fabric_ai_functions.md) | function | Apply optional default Fabric AI Function configuration. | — |
| [`create_ai_prompt_config`](../../reference/step-02a-shared-runtime-config/create_ai_prompt_config.md) | function | Create the AI prompt-template configuration used by FabricOps. | — |
| [`create_framework_config`](../../reference/step-02a-shared-runtime-config/create_framework_config.md) | function | Create the top-level FabricOps framework configuration contract. | — |
| [`create_governance_config`](../../reference/step-02a-shared-runtime-config/create_governance_config.md) | function | Create governance policy defaults for FabricOps runtime checks. | — |
| [`create_lineage_config`](../../reference/step-02a-shared-runtime-config/create_lineage_config.md) | function | Create lineage capture defaults for FabricOps handover traceability. | — |
| [`create_notebook_runtime_config`](../../reference/step-02a-shared-runtime-config/create_notebook_runtime_config.md) | function | Create notebook naming-policy configuration for runtime guards. | — |
| [`create_path_config`](../../reference/step-02a-shared-runtime-config/create_path_config.md) | function | Create environment-to-target routing used by Fabric IO helpers. | — |
| [`create_quality_config`](../../reference/step-02a-shared-runtime-config/create_quality_config.md) | function | Create the default quality policy used during FabricOps checks. | — |
| [`get_path`](../../reference/step-02a-shared-runtime-config/get_path.md) | function | Resolve a configured Fabric path for an environment and target. | — |
| [`run_config_smoke_tests`](../../reference/step-02b-notebook-startup-checks/run_config_smoke_tests.md) | function | Run 00_env_config readiness smoke checks for configuration bootstrap. | [`_check_spark_session`](../../reference/internal/config/_check_spark_session.md) (internal), [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) (internal) |
| [`validate_framework_config`](../../reference/step-02a-shared-runtime-config/validate_framework_config.md) | function | Validate and normalize framework configuration input. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_check_spark_session`](../../reference/internal/config/_check_spark_session.md) | [`run_config_smoke_tests`](../../reference/step-02b-notebook-startup-checks/run_config_smoke_tests.md) |
| [`_default_schema_text`](../../reference/internal/config/_default_schema_text.md) | — |
| [`_format_error_path`](../../reference/internal/config/_format_error_path.md) | — |
| [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) | [`bootstrap_fabric_env`](../../reference/step-02b-notebook-startup-checks/bootstrap_fabric_env.md), [`run_config_smoke_tests`](../../reference/step-02b-notebook-startup-checks/run_config_smoke_tests.md) |
| [`_load_schema`](../../reference/internal/config/_load_schema.md) | — |
