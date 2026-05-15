# `config` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`get_path`](../../reference/get_path/) | function | Resolve a configured Fabric path for an environment and target. | — |
| [`load_config`](../../reference/load_config/) | function | Validate and return a user-supplied framework configuration. | [`_validate_framework_config`](../../reference/internal/config/_validate_framework_config/) (internal) |
| [`setup_notebook`](../../reference/setup_notebook/) | function | Run consolidated FabricOps startup for exploration and pipeline notebooks. | [`_check_fabric_ai_functions_available`](../../reference/internal/config/_check_fabric_ai_functions_available/) (internal), [`_configure_fabric_ai_functions`](../../reference/internal/config/_configure_fabric_ai_functions/) (internal), [`_run_config_smoke_tests`](../../reference/internal/config/_run_config_smoke_tests/) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_bootstrap_fabric_env`](../../reference/internal/config/_bootstrap_fabric_env/) | — |
| [`_check_fabric_ai_functions_available`](../../reference/internal/config/_check_fabric_ai_functions_available/) | [`setup_notebook`](../../reference/setup_notebook/) |
| [`_check_spark_session`](../../reference/internal/config/_check_spark_session/) | — |
| [`_configure_fabric_ai_functions`](../../reference/internal/config/_configure_fabric_ai_functions/) | [`setup_notebook`](../../reference/setup_notebook/) |
| [`_default_schema_text`](../../reference/internal/config/_default_schema_text/) | — |
| [`_format_error_path`](../../reference/internal/config/_format_error_path/) | — |
| [`_get_fabric_runtime_metadata`](../../reference/internal/config/_get_fabric_runtime_metadata/) | — |
| [`_load_schema`](../../reference/internal/config/_load_schema/) | — |
| [`_normalize_name`](../../reference/internal/config/_normalize_name/) | — |
| [`_run_config_smoke_tests`](../../reference/internal/config/_run_config_smoke_tests/) | [`setup_notebook`](../../reference/setup_notebook/) |
| [`_validate_framework_config`](../../reference/internal/config/_validate_framework_config/) | [`load_config`](../../reference/load_config/) |
| [`_validate_notebook_name`](../../reference/internal/config/_validate_notebook_name/) | — |
