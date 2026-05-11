# `environment_config` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Recommended notebook entrypoints

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`bootstrap_fabric_env`](../../reference/step-02b-notebook-startup-checks/bootstrap_fabric_env.md) | function | Bootstrap 00_env_config environment readiness for FabricOps notebooks. | [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) (internal) |
| [`FrameworkConfig`](../../reference/step-02a-shared-runtime-config/FrameworkConfig.md) | class | Top-level framework configuration object. | — |
| [`get_path`](../../reference/step-02a-shared-runtime-config/get_path.md) | function | Resolve a configured Fabric path for an environment and target. | — |
| [`load_fabric_config`](../../reference/step-02a-shared-runtime-config/load_fabric_config.md) | function | Validate and return a user-supplied framework configuration. | — |
| [`PathConfig`](../../reference/step-02a-shared-runtime-config/PathConfig.md) | class | Environment-to-target mapping used for lakehouse/warehouse routing. | — |
| [`validate_framework_config`](../../reference/step-02a-shared-runtime-config/validate_framework_config.md) | function | Validate and normalize framework configuration input. | — |

## Advanced helpers

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`AIPromptConfig`](../../reference/step-02a-shared-runtime-config/AIPromptConfig.md) | class | Prompt templates used by AI-assisted framework workflows. | — |
| [`check_fabric_ai_functions_available`](../../reference/step-02a-shared-runtime-config/check_fabric_ai_functions_available.md) | function | Check whether Fabric AI Functions are available in the current runtime. | — |
| [`configure_fabric_ai_functions`](../../reference/step-01-governance-context/configure_fabric_ai_functions.md) | function | Apply optional default Fabric AI Function configuration. | — |
| [`GovernanceConfig`](../../reference/step-02a-shared-runtime-config/GovernanceConfig.md) | class | Default governance-policy options for metadata/classification checks. | — |
| [`LineageConfig`](../../reference/step-02a-shared-runtime-config/LineageConfig.md) | class | Default lineage-capture behavior for pipeline traceability. | — |
| [`NotebookRuntimeConfig`](../../reference/step-02a-shared-runtime-config/NotebookRuntimeConfig.md) | class | Runtime options used by notebook-oriented helpers. | — |
| [`QualityConfig`](../../reference/step-02a-shared-runtime-config/QualityConfig.md) | class | Default quality-policy options for FabricOps validation stages. | — |
| [`run_config_smoke_tests`](../../reference/step-02b-notebook-startup-checks/run_config_smoke_tests.md) | function | Run 00_env_config readiness smoke checks for configuration bootstrap. | [`_check_spark_session`](../../reference/internal/config/_check_spark_session.md) (internal), [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_check_spark_session`](../../reference/internal/config/_check_spark_session.md) | [`run_config_smoke_tests`](../../reference/step-02b-notebook-startup-checks/run_config_smoke_tests.md) |
| [`_default_schema_text`](../../reference/internal/config/_default_schema_text.md) | — |
| [`_format_error_path`](../../reference/internal/config/_format_error_path.md) | — |
| [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) | [`bootstrap_fabric_env`](../../reference/step-02b-notebook-startup-checks/bootstrap_fabric_env.md), [`run_config_smoke_tests`](../../reference/step-02b-notebook-startup-checks/run_config_smoke_tests.md) |
| [`_load_schema`](../../reference/internal/config/_load_schema.md) | — |
