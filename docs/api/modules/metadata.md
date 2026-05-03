# `metadata` module

## Module contents

- Public callables: 1
- Related internal helpers: 1
- Other internal objects: 4
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`build_dataset_run_record`](#build-dataset-run-record) | Internal | Function | Build dataset run record. | — | [Jump](#build-dataset-run-record) |
| [`build_quality_result_records`](#build-quality-result-records) | Internal | Function | Build quality result records. | — | [Jump](#build-quality-result-records) |
| [`build_schema_drift_records`](#build-schema-drift-records) | Internal | Function | Build schema drift records. | — | [Jump](#build-schema-drift-records) |
| [`build_schema_snapshot_records`](#build-schema-snapshot-records) | Internal | Function | Build schema snapshot records. | — | [Jump](#build-schema-snapshot-records) |
| [`write_metadata_records`](#write-metadata-records) | Internal helper | Function | Write metadata records. | [`write_multiple_metadata_outputs`](#write-multiple-metadata-outputs) | [Jump](#write-metadata-records) |
| [`write_multiple_metadata_outputs`](#write-multiple-metadata-outputs) | Public | Function | Write multiple metadata outputs. | — | [Jump](#write-multiple-metadata-outputs) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`write_multiple_metadata_outputs`](#write-multiple-metadata-outputs) | Function | Write multiple metadata outputs. | [`write_metadata_records`](#write-metadata-records) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`write_metadata_records`](#write-metadata-records) | [`write_multiple_metadata_outputs`](#write-multiple-metadata-outputs) |

## Full module API

::: fabric_data_product_framework.metadata
