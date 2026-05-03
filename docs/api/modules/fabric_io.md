# `fabric_io` module

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `get_path` | function | Return the Fabric path object for an environment and target. | — |
| `Housepath` | class | Fabric lakehouse or warehouse connection details. | — |
| `lakehouse_csv_read` | function | Read a CSV file from a Fabric lakehouse Files path. | `_get_spark` (internal) |
| `lakehouse_excel_read_as_spark` | function | Read an Excel file from a Fabric lakehouse Files path. | `_get_spark` (internal) |
| `lakehouse_parquet_read_as_spark` | function | Read a Parquet file from a Fabric lakehouse Files path. | `_convert_single_parquet_ns_to_us` (internal), `_get_spark` (internal) |
| `lakehouse_table_read` | function | Read a Delta table from a Fabric lakehouse. | `_get_spark` (internal) |
| `lakehouse_table_write` | function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| `load_fabric_config` | function | Validate and return a Fabric config mapping. | — |
| `warehouse_read` | function | Read a table from a Microsoft Fabric warehouse. | `_get_spark` (internal) |
| `warehouse_write` | function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Internal helpers (module-level)

| Helper | Related public callables |
|---|---|
| `_convert_single_parquet_ns_to_us` | `lakehouse_parquet_read_as_spark` |
| `_get_fabric_runtime_context` | — |
| `_get_spark` | `lakehouse_csv_read`, `lakehouse_excel_read_as_spark`, `lakehouse_parquet_read_as_spark`, `lakehouse_table_read`, `warehouse_read` |

## Full module API

::: fabric_data_product_framework.fabric_io
