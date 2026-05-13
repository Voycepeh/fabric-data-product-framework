# `data_governance` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`extract_pii_suggestions`](../../reference/extract_pii_suggestions/) | function | Extract governance suggestions from Spark/list response payloads. | — |
| [`load_governance`](../../reference/load_governance/) | function | Load approved governance metadata as read-only context. | [`_coerce_row_dicts`](../../reference/internal/data_governance/_coerce_row_dicts/) (internal) |
| [`prepare_governance_input`](../../reference/prepare_governance_input/) | function | Join approved business context into profile rows for governance AI suggestions. | — |
| [`review_governance`](../../reference/review_governance/) | function | Display governance review widget and capture decisions. | — |
| [`suggest_pii_labels`](../../reference/suggest_pii_labels/) | function | Run Fabric AI personal-identifier suggestion prompt on prepared governance rows. | — |
| [`write_governance`](../../reference/write_governance/) | function | Persist approved governance rows to metadata table. | [`_approved_widget_rows`](../../reference/internal/data_governance/_approved_widget_rows/) (internal) |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_context`](../../reference/build_governance_context/) | function | Build governance prompt context fields for notebook workflows. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_approved_widget_rows`](../../reference/internal/data_governance/_approved_widget_rows/) | [`write_governance`](../../reference/write_governance/) |
| [`_coerce_row_dicts`](../../reference/internal/data_governance/_coerce_row_dicts/) | [`load_governance`](../../reference/load_governance/) |
