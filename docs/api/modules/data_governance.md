# `data_governance` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`draft_governance`](../../reference/draft_governance/) | function | Compatibility-friendly short alias for :func:`suggest_pii_labels`. | — |
| [`load_governance`](../../reference/load_governance/) | function | Load approved governance metadata as read-only agreement context. | [`_coerce_row_dicts`](../../reference/internal/data_governance/_coerce_row_dicts/) (internal) |
| [`review_governance`](../../reference/review_governance/) | function | Display governance review widget and capture approve/reject decisions in module state. | [`_undo_last_action`](../../reference/internal/data_governance/_undo_last_action/) (internal) |
| [`write_governance`](../../reference/write_governance/) | function | Persist approved governance rows to metadata table. | [`_approved_widget_rows`](../../reference/internal/data_governance/_approved_widget_rows/) (internal) |

## Optional callables

No advanced helpers listed for this module.

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_approved_widget_rows`](../../reference/internal/data_governance/_approved_widget_rows/) | [`write_governance`](../../reference/write_governance/) |
| [`_coerce_row_dicts`](../../reference/internal/data_governance/_coerce_row_dicts/) | [`load_governance`](../../reference/load_governance/) |
| [`_undo_last_action`](../../reference/internal/data_governance/_undo_last_action/) | [`review_governance`](../../reference/review_governance/) |
