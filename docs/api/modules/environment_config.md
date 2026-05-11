# `environment_config` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`configure_fabric_ai_functions`](../../reference/step-01-governance-context/configure_fabric_ai_functions.md) | function | Apply optional default Fabric AI Function configuration. | — |
| [`get_path`](../../reference/step-02a-shared-runtime-config/get_path.md) | function | Resolve a configured Fabric path for an environment and target. | — |
| [`load_fabric_config`](../../reference/step-02a-shared-runtime-config/load_fabric_config.md) | function | Validate and return a user-supplied framework configuration. | [`_validate_framework_config`](../../reference/internal/config/_validate_framework_config.md) (internal) |
| [`setup_fabricops_notebook`](../../reference/step-02b-notebook-startup-checks/setup_fabricops_notebook.md) | function | Run consolidated FabricOps startup for exploration and pipeline notebooks. | [`_check_fabric_ai_functions_available`](../../reference/internal/config/_check_fabric_ai_functions_available.md) (internal), [`_run_config_smoke_tests`](../../reference/internal/config/_run_config_smoke_tests.md) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_bootstrap_fabric_env`](../../reference/internal/config/_bootstrap_fabric_env.md) | — |
| [`_check_fabric_ai_functions_available`](../../reference/internal/config/_check_fabric_ai_functions_available.md) | [`setup_fabricops_notebook`](../../reference/step-02b-notebook-startup-checks/setup_fabricops_notebook.md) |
| [`_check_spark_session`](../../reference/internal/config/_check_spark_session.md) | — |
| [`_default_schema_text`](../../reference/internal/config/_default_schema_text.md) | — |
| [`_format_error_path`](../../reference/internal/config/_format_error_path.md) | — |
| [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata.md) | — |
| [`_load_schema`](../../reference/internal/config/_load_schema.md) | — |
| [`_run_config_smoke_tests`](../../reference/internal/config/_run_config_smoke_tests.md) | [`setup_fabricops_notebook`](../../reference/step-02b-notebook-startup-checks/setup_fabricops_notebook.md) |
| [`_validate_framework_config`](../../reference/internal/config/_validate_framework_config.md) | [`load_fabric_config`](../../reference/step-02a-shared-runtime-config/load_fabric_config.md) |
