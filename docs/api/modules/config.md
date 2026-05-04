# `config` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`create_ai_prompt_config`](../../reference/step-02-runtime-environment-path-rules/create_ai_prompt_config.md) | function | Create AI prompt-template configuration. | — |
| [`create_framework_config`](../../reference/step-02-runtime-environment-path-rules/create_framework_config.md) | function | Create the top-level framework configuration object. | — |
| [`create_governance_config`](../../reference/step-02-runtime-environment-path-rules/create_governance_config.md) | function | Create governance-default configuration. | — |
| [`create_lineage_config`](../../reference/step-02-runtime-environment-path-rules/create_lineage_config.md) | function | Create lineage-default configuration. | — |
| [`create_notebook_runtime_config`](../../reference/step-02-runtime-environment-path-rules/create_notebook_runtime_config.md) | function | Create notebook runtime configuration. | — |
| [`create_path_config`](../../reference/step-02-runtime-environment-path-rules/create_path_config.md) | function | Create a validated :class:`PathConfig` object. | — |
| [`create_quality_config`](../../reference/step-02-runtime-environment-path-rules/create_quality_config.md) | function | Create quality-default configuration. | — |
| [`validate_framework_config`](../../reference/step-02-runtime-environment-path-rules/validate_framework_config.md) | function | Validate and normalize framework config input. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_default_schema_text`](../../reference/internal/config/_default_schema_text.md) | — |
| [`_format_error_path`](../../reference/internal/config/_format_error_path.md) | — |
| [`_load_schema`](../../reference/internal/config/_load_schema.md) | — |


Added readiness APIs: `bootstrap_fabric_env`, `run_config_smoke_tests`, and `check_fabric_ai_functions_available` under config. IO helpers remain under `fabric_io`.
