"""Copyable Fabric notebook adapter helpers for smoke tests.

These helpers intentionally avoid import-time Spark dependencies.
In a Microsoft Fabric notebook, ``spark`` is provided by the runtime.
Copy these functions into a notebook cell, or import this file in notebook
contexts where ``spark`` already exists.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence


def fabric_reader(table_identifier):
    """Read a Fabric table by identifier using the notebook ``spark`` session."""
    return spark.read.table(table_identifier)  # noqa: F821 - provided by Fabric runtime


def fabric_table_writer(df, table_identifier, mode="append", **options):
    """Write a Spark DataFrame to a Fabric table with optional partitioning."""
    writer = df.write.mode(mode)
    partition_by = options.get("partitionBy")
    if partition_by:
        writer = writer.partitionBy(partition_by)
    return writer.saveAsTable(table_identifier)


def metadata_writer(records, table_identifier, mode="append", **options):
    """Write metadata records to a Fabric table when records are present."""
    if not records:
        return None
    df = spark.createDataFrame(records)  # noqa: F821 - provided by Fabric runtime
    return df.write.mode(mode).saveAsTable(table_identifier)


def _stringify_nested_metadata_fields(records):
    """Convert nested list/dict values in metadata records to JSON strings."""
    if not records:
        return []

    converted = []
    for record in records:
        if not isinstance(record, Mapping):
            converted.append(record)
            continue

        safe_record = {}
        for key, value in record.items():
            if isinstance(value, Mapping):
                safe_record[key] = json.dumps(value, sort_keys=True)
            elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
                safe_record[key] = json.dumps(value)
            else:
                safe_record[key] = value
        converted.append(safe_record)
    return converted


def metadata_writer_with_schema_hint(records, table_identifier, mode="append", **options):
    """Write metadata after JSON-stringifying nested fields to reduce inference issues."""
    safe_records = _stringify_nested_metadata_fields(records)
    if not safe_records:
        return None
    df = spark.createDataFrame(safe_records)  # noqa: F821 - provided by Fabric runtime
    return df.write.mode(mode).saveAsTable(table_identifier)
