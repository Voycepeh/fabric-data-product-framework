# `fabric_io` module

Public callables: 10  
Related internal helpers: 2  
Other internal objects: 2  
Deprecated objects: 0

## Module contents

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [Housepath](#housepath) | Public | Class | Fabric lakehouse or warehouse connection details. | — | [API](#housepath) |
| [_convert_single_parquet_ns_to_us](#-convert-single-parquet-ns-to-us) | Internal helper | Function | Convert one Parquet file from nanosecond to microsecond timestamps. | `lakehouse_parquet_read_as_spark` | [API](#-convert-single-parquet-ns-to-us) |
| [_get_fabric_runtime_context](#-get-fabric-runtime-context) | Internal | Function | Return the Fabric notebook runtime context when available. | — | [API](#-get-fabric-runtime-context) |
| [_get_spark](#-get-spark) | Internal helper | Function | Return an explicit Spark session or the active notebook global `spark`. | `lakehouse_csv_read`, `lakehouse_excel_read_as_spark`, `lakehouse_parquet_read_as_spark`, `lakehouse_table_read`, `warehouse_read` | [API](#-get-spark) |
| [check_naming_convention](#check-naming-convention) | Internal | Function | Check whether a Fabric notebook name starts with an allowed prefix. | — | [API](#check-naming-convention) |
| [get_path](#get-path) | Public | Function | Return the Fabric path object for an environment and target. | `warehouse_read`, `warehouse_write` | [API](#get-path) |
| [lakehouse_csv_read](#lakehouse-csv-read) | Public | Function | Read a CSV file from a Fabric lakehouse Files path. | — | [API](#lakehouse-csv-read) |
| [lakehouse_excel_read_as_spark](#lakehouse-excel-read-as-spark) | Public | Function | Read an Excel file from a Fabric lakehouse Files path. | — | [API](#lakehouse-excel-read-as-spark) |
| [lakehouse_parquet_read_as_spark](#lakehouse-parquet-read-as-spark) | Public | Function | Read a Parquet file from a Fabric lakehouse Files path. | — | [API](#lakehouse-parquet-read-as-spark) |
| [lakehouse_table_read](#lakehouse-table-read) | Public | Function | Read a Delta table from a Fabric lakehouse. | — | [API](#lakehouse-table-read) |
| [lakehouse_table_write](#lakehouse-table-write) | Public | Function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — | [API](#lakehouse-table-write) |
| [load_fabric_config](#load-fabric-config) | Public | Function | Validate and return a Fabric config mapping. | — | [API](#load-fabric-config) |
| [warehouse_read](#warehouse-read) | Public | Function | Read a table from a Microsoft Fabric warehouse. | — | [API](#warehouse-read) |
| [warehouse_write](#warehouse-write) | Public | Function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [API](#warehouse-write) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| `get_path` | Function | Return the Fabric path object for an environment and target. | — |
| `Housepath` | Class | Fabric lakehouse or warehouse connection details. | — |
| `lakehouse_csv_read` | Function | Read a CSV file from a Fabric lakehouse Files path. | `_get_spark` (internal) |
| `lakehouse_excel_read_as_spark` | Function | Read an Excel file from a Fabric lakehouse Files path. | `_get_spark` (internal) |
| `lakehouse_parquet_read_as_spark` | Function | Read a Parquet file from a Fabric lakehouse Files path. | `_convert_single_parquet_ns_to_us` (internal), `_get_spark` (internal) |
| `lakehouse_table_read` | Function | Read a Delta table from a Fabric lakehouse. | `_get_spark` (internal) |
| `lakehouse_table_write` | Function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| `load_fabric_config` | Function | Validate and return a Fabric config mapping. | — |
| `warehouse_read` | Function | Read a table from a Microsoft Fabric warehouse. | `_get_spark` (internal) |
| `warehouse_write` | Function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| `_convert_single_parquet_ns_to_us` | `lakehouse_parquet_read_as_spark` |
| `_get_spark` | `lakehouse_csv_read`, `lakehouse_excel_read_as_spark`, `lakehouse_parquet_read_as_spark`, `lakehouse_table_read`, `warehouse_read` |

## Full module API

::: fabric_data_product_framework.fabric_io
