# `fabric_io` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`get_path`](../../reference/step-02-runtime-configuration/get_path.md) | function | Return the Fabric path object for an environment and target. | — |
| [`Housepath`](../../reference/step-02-runtime-configuration/Housepath.md) | class | Fabric lakehouse or warehouse connection details. | — |
| [`lakehouse_csv_read`](../../reference/step-03-source-declaration-paths/lakehouse_csv_read.md) | function | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_excel_read_as_spark`](../../reference/step-03-source-declaration-paths/lakehouse_excel_read_as_spark.md) | function | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_parquet_read_as_spark`](../../reference/step-03-source-declaration-paths/lakehouse_parquet_read_as_spark.md) | function | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_read`](../../reference/step-03-source-declaration-paths/lakehouse_table_read.md) | function | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_write`](../../reference/step-11-output-write-metadata-logging/lakehouse_table_write.md) | function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`load_fabric_config`](../../reference/step-02-runtime-configuration/load_fabric_config.md) | function | Validate and return a framework config mapping. | — |
| [`warehouse_read`](../../reference/step-03-source-declaration-paths/warehouse_read.md) | function | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`warehouse_write`](../../reference/step-11-output-write-metadata-logging/warehouse_write.md) | function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) | [`lakehouse_parquet_read_as_spark`](../../reference/step-03-source-declaration-paths/lakehouse_parquet_read_as_spark.md) |
| [`_get_fabric_runtime_context`](../../reference/internal/fabric_io/_get_fabric_runtime_context.md) | — |
| [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) | [`lakehouse_csv_read`](../../reference/step-03-source-declaration-paths/lakehouse_csv_read.md), [`lakehouse_excel_read_as_spark`](../../reference/step-03-source-declaration-paths/lakehouse_excel_read_as_spark.md), [`lakehouse_parquet_read_as_spark`](../../reference/step-03-source-declaration-paths/lakehouse_parquet_read_as_spark.md), [`lakehouse_table_read`](../../reference/step-03-source-declaration-paths/lakehouse_table_read.md), [`warehouse_read`](../../reference/step-03-source-declaration-paths/warehouse_read.md) |
