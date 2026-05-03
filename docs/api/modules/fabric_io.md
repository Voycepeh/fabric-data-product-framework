# `fabric_io` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`get_path`](#get_path) | function | Return the Fabric path object for an environment and target. | — |
| [`Housepath`](#housepath) | class | Fabric lakehouse or warehouse connection details. | — |
| [`lakehouse_csv_read`](#lakehouse_csv_read) | function | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_excel_read_as_spark`](#lakehouse_excel_read_as_spark) | function | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_parquet_read_as_spark`](#lakehouse_parquet_read_as_spark) | function | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_read`](#lakehouse_table_read) | function | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`lakehouse_table_write`](#lakehouse_table_write) | function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`load_fabric_config`](#load_fabric_config) | function | Validate and return a Fabric config mapping. | — |
| [`warehouse_read`](#warehouse_read) | function | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`warehouse_write`](#warehouse_write) | function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Public callable details

### get_path

::: fabric_data_product_framework.fabric_io.get_path

### Housepath

::: fabric_data_product_framework.fabric_io.Housepath

### lakehouse_csv_read

::: fabric_data_product_framework.fabric_io.lakehouse_csv_read

### lakehouse_excel_read_as_spark

::: fabric_data_product_framework.fabric_io.lakehouse_excel_read_as_spark

### lakehouse_parquet_read_as_spark

::: fabric_data_product_framework.fabric_io.lakehouse_parquet_read_as_spark

### lakehouse_table_read

::: fabric_data_product_framework.fabric_io.lakehouse_table_read

### lakehouse_table_write

::: fabric_data_product_framework.fabric_io.lakehouse_table_write

### load_fabric_config

::: fabric_data_product_framework.fabric_io.load_fabric_config

### warehouse_read

::: fabric_data_product_framework.fabric_io.warehouse_read

### warehouse_write

::: fabric_data_product_framework.fabric_io.warehouse_write

??? note "Internal helpers (collapsed)"

    Internal helpers are documented separately for maintainers:

    - [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) (used by: `lakehouse_parquet_read_as_spark`)
    - [`_get_fabric_runtime_context`](../../reference/internal/fabric_io/_get_fabric_runtime_context.md)
    - [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (used by: `lakehouse_csv_read`, `lakehouse_excel_read_as_spark`, `lakehouse_parquet_read_as_spark`, `lakehouse_table_read`, `warehouse_read`)
