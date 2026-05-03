# `fabric_io` module

## Module contents

- Public callables: 10
- Related internal helpers: 2
- Other internal objects: 2
- Deprecated objects: 0

| Name | Status | Type | Purpose | Used by / related public callable | API link |
|---|---|---|---|---|---|
| [`_convert_single_parquet_ns_to_us`](#convert-single-parquet-ns-to-us) | Internal helper | Function | Convert one Parquet file from nanosecond to microsecond timestamps. | [`lakehouse_parquet_read_as_spark`](#lakehouse-parquet-read-as-spark) | [Jump](#convert-single-parquet-ns-to-us) |
| [`_get_fabric_runtime_context`](#get-fabric-runtime-context) | Internal | Function | Return the Fabric notebook runtime context when available. | — | [Jump](#get-fabric-runtime-context) |
| [`_get_spark`](#get-spark) | Internal helper | Function | Return an explicit Spark session or the active notebook global `spark`. | [`lakehouse_csv_read`](#lakehouse-csv-read), [`lakehouse_excel_read_as_spark`](#lakehouse-excel-read-as-spark), [`lakehouse_parquet_read_as_spark`](#lakehouse-parquet-read-as-spark), [`lakehouse_table_read`](#lakehouse-table-read), [`warehouse_read`](#warehouse-read) | [Jump](#get-spark) |
| [`check_naming_convention`](#check-naming-convention) | Internal | Function | Check whether a Fabric notebook name starts with an allowed prefix. | — | [Jump](#check-naming-convention) |
| [`get_path`](#get-path) | Public | Function | Return the Fabric path object for an environment and target. | [`warehouse_read`](#warehouse-read), [`warehouse_write`](#warehouse-write) | [Jump](#get-path) |
| [`Housepath`](#housepath) | Public | Dataclass | Fabric lakehouse or warehouse connection details. | — | [Jump](#housepath) |
| [`lakehouse_csv_read`](#lakehouse-csv-read) | Public | Function | Read a CSV file from a Fabric lakehouse Files path. | — | [Jump](#lakehouse-csv-read) |
| [`lakehouse_excel_read_as_spark`](#lakehouse-excel-read-as-spark) | Public | Function | Read an Excel file from a Fabric lakehouse Files path. | — | [Jump](#lakehouse-excel-read-as-spark) |
| [`lakehouse_parquet_read_as_spark`](#lakehouse-parquet-read-as-spark) | Public | Function | Read a Parquet file from a Fabric lakehouse Files path. | — | [Jump](#lakehouse-parquet-read-as-spark) |
| [`lakehouse_table_read`](#lakehouse-table-read) | Public | Function | Read a Delta table from a Fabric lakehouse. | — | [Jump](#lakehouse-table-read) |
| [`lakehouse_table_write`](#lakehouse-table-write) | Public | Function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — | [Jump](#lakehouse-table-write) |
| [`load_fabric_config`](#load-fabric-config) | Public | Function | Validate and return a Fabric config mapping. | — | [Jump](#load-fabric-config) |
| [`warehouse_read`](#warehouse-read) | Public | Function | Read a table from a Microsoft Fabric warehouse. | — | [Jump](#warehouse-read) |
| [`warehouse_write`](#warehouse-write) | Public | Function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — | [Jump](#warehouse-write) |

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`get_path`](#get-path) | Function | Return the Fabric path object for an environment and target. | — |
| [`Housepath`](#housepath) | Dataclass | Fabric lakehouse or warehouse connection details. | — |
| [`lakehouse_csv_read`](#lakehouse-csv-read) | Function | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](#get-spark) |
| [`lakehouse_excel_read_as_spark`](#lakehouse-excel-read-as-spark) | Function | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](#get-spark) |
| [`lakehouse_parquet_read_as_spark`](#lakehouse-parquet-read-as-spark) | Function | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](#convert-single-parquet-ns-to-us), [`_get_spark`](#get-spark) |
| [`lakehouse_table_read`](#lakehouse-table-read) | Function | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](#get-spark) |
| [`lakehouse_table_write`](#lakehouse-table-write) | Function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`load_fabric_config`](#load-fabric-config) | Function | Validate and return a Fabric config mapping. | — |
| [`warehouse_read`](#warehouse-read) | Function | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](#get-spark) |
| [`warehouse_write`](#warehouse-write) | Function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Related internal helpers

| Helper | Related public callables |
|---|---|
| [`_convert_single_parquet_ns_to_us`](#convert-single-parquet-ns-to-us) | [`lakehouse_parquet_read_as_spark`](#lakehouse-parquet-read-as-spark) |
| [`_get_spark`](#get-spark) | [`lakehouse_csv_read`](#lakehouse-csv-read), [`lakehouse_excel_read_as_spark`](#lakehouse-excel-read-as-spark), [`lakehouse_parquet_read_as_spark`](#lakehouse-parquet-read-as-spark), [`lakehouse_table_read`](#lakehouse-table-read), [`warehouse_read`](#warehouse-read) |

## Full module API

::: fabric_data_product_framework.fabric_io
