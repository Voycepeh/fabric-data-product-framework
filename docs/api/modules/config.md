# `config` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`bootstrap_fabric_env`](../../reference/step-02-runtime-environment-path-rules/bootstrap_fabric_env.md) | function | One-line environment bootstrap for Fabric runtime readiness. | [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) (internal) |
| [`check_fabric_ai_functions_available`](../../reference/step-02-runtime-environment-path-rules/check_fabric_ai_functions_available.md) | function | Fabric AI readiness check for notebook runtime availability. | — |
| [`create_ai_prompt_config`](../../reference/step-02-runtime-environment-path-rules/create_ai_prompt_config.md) | function | Create AI prompt-template configuration. | — |
| [`create_framework_config`](../../reference/step-02-runtime-environment-path-rules/create_framework_config.md) | function | Create the top-level framework configuration object. | — |
| [`create_governance_config`](../../reference/step-02-runtime-environment-path-rules/create_governance_config.md) | function | Create governance-default configuration. | — |
| [`create_lineage_config`](../../reference/step-02-runtime-environment-path-rules/create_lineage_config.md) | function | Create lineage-default configuration. | — |
| [`create_notebook_runtime_config`](../../reference/step-02-runtime-environment-path-rules/create_notebook_runtime_config.md) | function | Create notebook runtime configuration. | — |
| [`create_path_config`](../../reference/step-02-runtime-environment-path-rules/create_path_config.md) | function | Create a validated :class:`PathConfig` object. | — |
| [`create_quality_config`](../../reference/step-02-runtime-environment-path-rules/create_quality_config.md) | function | Create quality-default configuration. | — |
| [`get_path`](../../reference/step-02-runtime-environment-path-rules/get_path.md) | function | Environment/target path resolver for configured Fabric routes. | — |
| [`run_config_smoke_tests`](../../reference/step-02-runtime-environment-path-rules/run_config_smoke_tests.md) | function | Smoke-test orchestrator for config readiness checks. | [`_check_spark_session`](../../reference/internal/config/_check_spark_session.md) (internal), [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) (internal) |
| [`validate_framework_config`](../../reference/step-02-runtime-environment-path-rules/validate_framework_config.md) | function | Validate and normalize framework config input. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_check_spark_session`](../../reference/internal/config/_check_spark_session.md) | [`run_config_smoke_tests`](../../reference/step-02-runtime-environment-path-rules/run_config_smoke_tests.md) |
| [`_default_schema_text`](../../reference/internal/config/_default_schema_text.md) | — |
| [`_format_error_path`](../../reference/internal/config/_format_error_path.md) | — |
| [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) | [`bootstrap_fabric_env`](../../reference/step-02-runtime-environment-path-rules/bootstrap_fabric_env.md), [`run_config_smoke_tests`](../../reference/step-02-runtime-environment-path-rules/run_config_smoke_tests.md) |
| [`_load_schema`](../../reference/internal/config/_load_schema.md) | — |
