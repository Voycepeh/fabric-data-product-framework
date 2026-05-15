# `handover` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_handover`](../../reference/build_handover/) | function | Build a handover-friendly summary for one data product run. | — |
| [`render_handover_markdown`](../../reference/render_handover_markdown/) | function | Render a handover summary dictionary into Markdown for handover notes. | [`_status_of`](../../reference/internal/handover/_status_of/) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_status_of`](../../reference/internal/handover/_status_of/) | [`render_handover_markdown`](../../reference/render_handover_markdown/) |
