# `data_governance` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`build_governance_classification_records`](../../reference/build_governance_classification_records/) | function | Build metadata-ready governance classification records from column suggestions. | — |
| [`classify_columns`](../../reference/classify_columns/) | function | Classify multiple columns and return normalized governance suggestions. | [`_column_name`](../../reference/internal/data_governance/_column_name/) (internal), [`_normalize_columns`](../../reference/internal/data_governance/_normalize_columns/) (internal) |
| [`load_governance_context`](../../reference/load_governance_context/) | function | Load approved governance metadata as read-only agreement context for downstream notebooks. | [`_coerce_row_dicts`](../../reference/internal/data_governance/_coerce_row_dicts/) (internal) |
| [`run_governance_widget`](../../reference/run_governance_widget/) | function | Run governance review with AI-advisory suggestions and optional metadata persistence. | — |
| [`summarize_governance_classifications`](../../reference/summarize_governance_classifications/) | function | Summarize governance classification outputs into review-friendly counts. | — |
| [`write_governance_classifications`](../../reference/write_governance_classifications/) | function | Persist governance classifications to a metadata destination. | [`_spark_create_governance_metadata_dataframe`](../../reference/internal/data_governance/_spark_create_governance_metadata_dataframe/) (internal) |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`classify_column`](../../reference/classify_column/) | function | Classify one column using term matching, metadata cues, and business context. | [`_match_terms`](../../reference/internal/data_governance/_match_terms/) (internal), [`_phrase_in_text`](../../reference/internal/data_governance/_phrase_in_text/) (internal) |
| [`extract_personal_identifier_suggestions`](../../reference/extract_personal_identifier_suggestions/) | function | Extract governance suggestions from Spark/list response payloads. | [`_get_governance_ai_suggestion`](../../reference/internal/data_governance/_get_governance_ai_suggestion/) (internal) |
| [`prepare_governance_profile_input`](../../reference/prepare_governance_profile_input/) | function | Join approved business context evidence into profile rows for governance AI suggestion. | — |
| [`review_column_governance_context`](../../reference/review_column_governance_context/) | function | Display governance approval widget. | — |
| [`suggest_personal_identifier_classifications`](../../reference/suggest_personal_identifier_classifications/) | function | Run Fabric AI personal-identifier suggestion prompt on prepared governance rows. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_coerce_row_dicts`](../../reference/internal/data_governance/_coerce_row_dicts/) | [`load_governance_context`](../../reference/load_governance_context/) |
| [`_column_name`](../../reference/internal/data_governance/_column_name/) | [`classify_columns`](../../reference/classify_columns/) |
| [`_get_governance_ai_suggestion`](../../reference/internal/data_governance/_get_governance_ai_suggestion/) | [`extract_personal_identifier_suggestions`](../../reference/extract_personal_identifier_suggestions/) |
| [`_match_terms`](../../reference/internal/data_governance/_match_terms/) | [`classify_column`](../../reference/classify_column/) |
| [`_normalize_columns`](../../reference/internal/data_governance/_normalize_columns/) | [`classify_columns`](../../reference/classify_columns/) |
| [`_phrase_in_text`](../../reference/internal/data_governance/_phrase_in_text/) | [`classify_column`](../../reference/classify_column/) |
| [`_spark_create_governance_metadata_dataframe`](../../reference/internal/data_governance/_spark_create_governance_metadata_dataframe/) | [`write_governance_classifications`](../../reference/write_governance_classifications/) |
| [`_tokenize_text`](../../reference/internal/data_governance/_tokenize_text/) | — |
