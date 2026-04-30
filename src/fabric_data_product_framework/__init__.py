"""Fabric Data Product Framework package."""

from .fabric_notebook import (
    Housepath,
    ODI_METADATA_LOGGER,
    add_system_technical_columns,
    check_naming_convention,
    clean_datetime_columns,
    get_path,
    lakehouse_csv_read,
    lakehouse_excel_read_as_spark,
    lakehouse_parquet_read_as_spark,
    lakehouse_table_read,
    lakehouse_table_write,
    pass_if_yes_else_run,
    transformation_reasons,
    transformation_summary,
    warehouse_read,
    warehouse_write,
)
from .template_generator import create_pipeline_notebook_template

__version__ = "0.1.0"

__all__ = [
    "Housepath",
    "get_path",
    "lakehouse_table_read",
    "lakehouse_table_write",
    "lakehouse_csv_read",
    "lakehouse_parquet_read_as_spark",
    "lakehouse_excel_read_as_spark",
    "warehouse_read",
    "warehouse_write",
    "check_naming_convention",
    "clean_datetime_columns",
    "add_system_technical_columns",
    "ODI_METADATA_LOGGER",
    "transformation_summary",
    "transformation_reasons",
    "pass_if_yes_else_run",
    "create_pipeline_notebook_template",
]
