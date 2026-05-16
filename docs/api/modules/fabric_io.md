# `fabric_input_output` module

<div class="api-status-block">
  <span class="api-chip api-chip-module">Module overview</span>
</div>

## Public callables from `__all__`

| Callable | Type | Summary | Related helpers |
|---|---|---|---|
| [`read_lakehouse_csv`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_csv.md) | function | Read a CSV file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`read_lakehouse_excel`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_excel.md) | function | Read an Excel file from a Fabric lakehouse Files path. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`read_lakehouse_parquet`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_parquet.md) | function | Read a Parquet file from a Fabric lakehouse Files path. | [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`read_lakehouse_table`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_table.md) | function | Read a Delta table from a Fabric lakehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`write_lakehouse_table`](../../reference/step-06d-controlled-outputs/write_lakehouse_table.md) | function | Write a Spark DataFrame to a Fabric lakehouse Delta table. | — |
| [`load_config`](../../reference/step-02a-shared-runtime-config/load_config.md) | function | Validate and return a user-supplied framework configuration. | — |
| [`read_warehouse_table`](../../reference/step-03-source-contract-ingestion-pattern/read_warehouse_table.md) | function | Read a table from a Microsoft Fabric warehouse. | [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) (internal) |
| [`write_warehouse_table`](../../reference/step-06d-controlled-outputs/write_warehouse_table.md) | function | Write a Spark DataFrame to a Microsoft Fabric warehouse table. | — |

## Internal helpers

| Helper | Related public callables |
|---|---|
| [`_convert_single_parquet_ns_to_us`](../../reference/internal/fabric_io/_convert_single_parquet_ns_to_us.md) | [`read_lakehouse_parquet`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_parquet.md) |
| [`_get_fabric_runtime_context`](../../reference/internal/fabric_io/_get_fabric_runtime_context.md) | — |
| [`_get_spark`](../../reference/internal/fabric_io/_get_spark.md) | [`read_lakehouse_csv`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_csv.md), [`read_lakehouse_excel`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_excel.md), [`read_lakehouse_parquet`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_parquet.md), [`read_lakehouse_table`](../../reference/step-03-source-contract-ingestion-pattern/read_lakehouse_table.md), [`read_warehouse_table`](../../reference/step-03-source-contract-ingestion-pattern/read_warehouse_table.md) |
