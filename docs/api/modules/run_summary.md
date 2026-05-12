# `run_summary` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_run_summary`](../../reference/build_run_summary.md) | function | Build a handover-friendly summary for one data product run. | — |
| [`render_run_summary_markdown`](../../reference/render_run_summary_markdown.md) | function | Render a run summary dictionary into Markdown for handover notes. | [`_status_of`](../../reference/internal/run_summary/_status_of.md) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_status_of`](../../reference/internal/run_summary/_status_of.md) | [`render_run_summary_markdown`](../../reference/render_run_summary_markdown.md) |
