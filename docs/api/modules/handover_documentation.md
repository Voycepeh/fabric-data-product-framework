# `handover_documentation` module

<div class="api-status-block">
  <span class="api-chip api-chip-internal">Advanced supporting module</span>
  <div class="api-chip-subtitle">Used by workflow references but not promoted as a primary notebook module.</div>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| — | — | No recommended entrypoints configured. | — |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_run_summary`](../../reference/step-10-lineage-handover-documentation/build_run_summary.md) | function | Build a handover-friendly summary for one data product run. | — |
| [`render_run_summary_markdown`](../../reference/step-10-lineage-handover-documentation/render_run_summary_markdown.md) | function | Render a run summary dictionary into Markdown for handover notes. | [`_status_of`](../../reference/internal/run_summary/_status_of.md) (internal) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_status_of`](../../reference/internal/run_summary/_status_of.md) | [`render_run_summary_markdown`](../../reference/step-10-lineage-handover-documentation/render_run_summary_markdown.md) |
