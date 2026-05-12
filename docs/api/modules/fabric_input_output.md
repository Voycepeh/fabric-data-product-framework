# `fabric_input_output` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Essential callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`lakehouse_csv_read`](../../reference/#lakehouse_csv_read) | function | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_input_output/_get_spark.md) (internal) |
| [`lakehouse_excel_read_as_spark`](../../reference/#lakehouse_excel_read_as_spark) | function | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_input_output/_get_spark.md) (internal) |
| [`lakehouse_parquet_read_as_spark`](../../reference/#lakehouse_parquet_read_as_spark) | function | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_input_output/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](../../reference/internal/fabric_input_output/_get_spark.md) (internal) |
| [`lakehouse_table_read`](../../reference/#lakehouse_table_read) | function | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](../../reference/internal/fabric_input_output/_get_spark.md) (internal) |
| [`lakehouse_table_write`](../../reference/#lakehouse_table_write) | function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`warehouse_read`](../../reference/#warehouse_read) | function | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](../../reference/internal/fabric_input_output/_get_spark.md) (internal) |
| [`warehouse_write`](../../reference/#warehouse_write) | function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Optional callables

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`seed_minimal_sample_source_table`](../../reference/#seed_minimal_sample_source_table) | function | Create and persist deterministic demo rows into a sample source table. | [`_get_spark`](../../reference/internal/fabric_input_output/_get_spark.md) (internal) |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_input_output/_convert_single_parquet_ns_to_us.md) | [`lakehouse_parquet_read_as_spark`](../../reference/#lakehouse_parquet_read_as_spark) |
| [`_get_fabric_runtime_context`](../../reference/internal/fabric_input_output/_get_fabric_runtime_context.md) | — |
| [`_get_spark`](../../reference/internal/fabric_input_output/_get_spark.md) | [`lakehouse_csv_read`](../../reference/#lakehouse_csv_read), [`lakehouse_excel_read_as_spark`](../../reference/#lakehouse_excel_read_as_spark), [`lakehouse_parquet_read_as_spark`](../../reference/#lakehouse_parquet_read_as_spark), [`lakehouse_table_read`](../../reference/#lakehouse_table_read), [`seed_minimal_sample_source_table`](../../reference/#seed_minimal_sample_source_table), [`warehouse_read`](../../reference/#warehouse_read) |
