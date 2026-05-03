# `fabric_io` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`get_path`](../../reference/fabric_io/get_path.md) | function | Return the Fabric path object for an environment and target. | — |
| [`Housepath`](../../reference/fabric_io/Housepath.md) | class | Fabric lakehouse or warehouse connection details. | — |
| [`lakehouse_csv_read`](../../reference/fabric_io/lakehouse_csv_read.md) | function | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_excel_read_as_spark`](../../reference/fabric_io/lakehouse_excel_read_as_spark.md) | function | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_parquet_read_as_spark`](../../reference/fabric_io/lakehouse_parquet_read_as_spark.md) | function | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_read`](../../reference/fabric_io/lakehouse_table_read.md) | function | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_write`](../../reference/fabric_io/lakehouse_table_write.md) | function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`load_fabric_config`](../../reference/fabric_io/load_fabric_config.md) | function | Validate and return a Fabric config mapping. | — |
| [`warehouse_read`](../../reference/fabric_io/warehouse_read.md) | function | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`warehouse_write`](../../reference/fabric_io/warehouse_write.md) | function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) | [`lakehouse_parquet_read_as_spark`](../../reference/fabric_io/lakehouse_parquet_read_as_spark.md) |
| [`_get_fabric_runtime_context`](../../reference/internal/fabric_io/_get_fabric_runtime_context.md) | — |
| [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) | [`lakehouse_csv_read`](../../reference/fabric_io/lakehouse_csv_read.md), [`lakehouse_excel_read_as_spark`](../../reference/fabric_io/lakehouse_excel_read_as_spark.md), [`lakehouse_parquet_read_as_spark`](../../reference/fabric_io/lakehouse_parquet_read_as_spark.md), [`lakehouse_table_read`](../../reference/fabric_io/lakehouse_table_read.md), [`warehouse_read`](../../reference/fabric_io/warehouse_read.md) |
