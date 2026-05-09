# `runtime_context` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`assert_notebook_name_valid`](../../reference/step-01-governance-context/assert_notebook_name_valid.md) | function | Raise :class:`NotebookNamingError` when a notebook name is invalid. | — |
| [`build_runtime_context`](../../reference/step-01-governance-context/build_runtime_context.md) | function | Build a standard runtime context dictionary for Fabric notebooks. | [`_infer_notebook_name_from_runtime`](../../reference/internal/runtime_context/_infer_notebook_name_from_runtime.md) (internal) |
| [`generate_run_id`](../../reference/step-01-governance-context/generate_run_id.md) | function | Generate a notebook-safe run identifier. | — |
| [`validate_notebook_name`](../../reference/step-01-governance-context/validate_notebook_name.md) | function | Validate notebook names against the framework workspace notebook model. | [`_infer_notebook_name_from_runtime`](../../reference/internal/runtime_context/_infer_notebook_name_from_runtime.md) (internal) |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_infer_notebook_name_from_runtime`](../../reference/internal/runtime_context/_infer_notebook_name_from_runtime.md) | [`build_runtime_context`](../../reference/step-01-governance-context/build_runtime_context.md), [`validate_notebook_name`](../../reference/step-01-governance-context/validate_notebook_name.md) |
