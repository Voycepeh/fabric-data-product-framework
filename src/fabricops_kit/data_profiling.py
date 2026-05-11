"""Fabric-first profiling utilities for standardized metadata evidence.

This module focuses on producing a stable, metadata-compatible metadata profile from a
Spark DataFrame. The profile can be written to metadata tables and reused as
AI-ready context for deterministic data quality rule hinting.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import re
from typing import Any


from fabricops_kit.technical_columns import _default_technical_columns


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^[+()\-\s0-9]{7,}$")



def _get_profiled_columns(df, exclude_columns: list[str] | set[str] | None = None) -> list[str]:
    """Return non-technical column names from a Spark DataFrame.

    Parameters
    ----------
    df : Any
        Spark DataFrame-like object with a ``dtypes`` attribute.
    exclude_columns : list[str] | set[str] | None, optional
        Additional columns to exclude from profiling.

    Returns
    -------
    list[str]
        Eligible business columns to profile.
    """
    excluded = set(_default_technical_columns())
    if exclude_columns:
        excluded.update(exclude_columns)
    return [name for name, _dtype in df.dtypes if name not in excluded]


def _is_min_max_supported_type(data_type: str) -> bool:
    """Return whether min/max aggregation is safe for a Spark type string."""
    value = (data_type or "").lower()
    unsupported = ("array", "map", "struct", "binary")
    if any(token in value for token in unsupported):
        return False
    supported = (
        "tinyint",
        "smallint",
        "int",
        "bigint",
        "float",
        "double",
        "decimal",
        "date",
        "timestamp",
        "string",
        "char",
        "varchar",
    )
    return any(token in value for token in supported)


def _profile_metadata_to_records(profile_df) -> list[dict[str, Any]]:
    """Convert Spark metadata profile rows into JSON-friendly dictionaries."""
    records = []
    for row in profile_df.collect():
        item = row.asDict() if hasattr(row, "asDict") else dict(row)
        normalized = {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in item.items()}
        records.append(normalized)
    return records


def build_ai_quality_context(
    profile_df,
    *,
    dataset_name: str,
    table_name: str,
    business_context: str | None = None,
    high_null_threshold: float = 30.0,
    unique_threshold: float = 99.0,
    low_cardinality_threshold: float = 5.0,
) -> dict[str, Any]:
    """Build deterministic AI-ready context from standard metadata profile rows.

    The output is evidence-only context intended for AI/Copilot suggestion flows;
    final DQ rule definition, approval, and execution are owned elsewhere.

    Examples
    --------
    >>> ai_context = build_ai_quality_context(
    ...     profile_df,
    ...     dataset_name="orders",
    ...     table_name="orders_clean",
    ...     business_context="Customer orders used for sales reporting",
    ... )
    """
    records = _profile_metadata_to_records(profile_df)
    row_count = int(records[0].get("ROW_COUNT", 0)) if records else 0
    columns = [r.get("COLUMN_NAME") for r in records]

    def _num(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    columns_with_nulls = [r["COLUMN_NAME"] for r in records if _num(r.get("NULL_COUNT"), 0) > 0]
    high_null_columns = [r["COLUMN_NAME"] for r in records if _num(r.get("NULL_PERCENT"), 0) >= high_null_threshold]
    high_cardinality_columns = [r["COLUMN_NAME"] for r in records if _num(r.get("DISTINCT_PERCENT"), 0) >= unique_threshold]
    low_cardinality_columns = [r["COLUMN_NAME"] for r in records if _num(r.get("DISTINCT_PERCENT"), 0) <= low_cardinality_threshold]

    likely_identifier_columns = [
        r["COLUMN_NAME"]
        for r in records
        if "id" in str(r.get("COLUMN_NAME", "")).lower() or _num(r.get("DISTINCT_PERCENT"), 0) >= unique_threshold
    ]
    likely_date_columns = [
        r["COLUMN_NAME"]
        for r in records
        if any(token in str(r.get("DATA_TYPE", "")).lower() for token in ("date", "timestamp"))
    ]

    candidate_rule_hints = []
    column_profiles = []
    for r in records:
        col = r.get("COLUMN_NAME")
        dtype = str(r.get("DATA_TYPE", "")).lower()
        null_pct = _num(r.get("NULL_PERCENT"), 0)
        distinct_pct = _num(r.get("DISTINCT_PERCENT"), 0)
        distinct_count = int(_num(r.get("DISTINCT_COUNT"), 0))
        has_range = r.get("MIN_VALUE") is not None and r.get("MAX_VALUE") is not None

        column_profiles.append({k: r.get(k) for k in ("COLUMN_NAME", "DATA_TYPE", "ROW_COUNT", "NULL_COUNT", "NULL_PERCENT", "DISTINCT_COUNT", "DISTINCT_PERCENT", "MIN_VALUE", "MAX_VALUE")})

        if row_count > 0 and null_pct <= 0.1:
            candidate_rule_hints.append({"column": col, "hint": "NOT_NULL_CANDIDATE"})
        if row_count > 0 and distinct_pct >= unique_threshold:
            candidate_rule_hints.append({"column": col, "hint": "UNIQUE_CANDIDATE"})
        if ("date" in dtype or "timestamp" in dtype) and has_range:
            candidate_rule_hints.append({"column": col, "hint": "DATE_RANGE_CANDIDATE"})
        if row_count > 0 and distinct_count > 0 and distinct_pct <= low_cardinality_threshold:
            candidate_rule_hints.append({"column": col, "hint": "ACCEPTED_VALUES_CANDIDATE"})
        if any(token in dtype for token in ("int", "bigint", "float", "double", "decimal")) and has_range:
            candidate_rule_hints.append({"column": col, "hint": "NUMERIC_RANGE_CANDIDATE"})
        if any(token in str(col).lower() for token in ("event", "load", "update", "create")) and "timestamp" in dtype:
            candidate_rule_hints.append({"column": col, "hint": "FRESHNESS_CANDIDATE"})

    return {
        "dataset_name": dataset_name,
        "table_name": table_name,
        "business_context": business_context,
        "row_count": row_count,
        "column_count": len(columns),
        "columns": columns,
        "column_profiles": column_profiles,
        "columns_with_nulls": columns_with_nulls,
        "high_null_columns": high_null_columns,
        "high_cardinality_columns": high_cardinality_columns,
        "low_cardinality_columns": low_cardinality_columns,
        "likely_identifier_columns": sorted(set(likely_identifier_columns)),
        "likely_date_columns": likely_date_columns,
        "candidate_rule_hints": candidate_rule_hints,
    }


def profile_dataframe(
    df,
    table_name: str,
    *,
    exclude_columns=None,
    run_timestamp_timezone="Asia/Singapore",
    include_ai_context: bool = False,
    dataset_name: str | None = None,
    business_context: str | None = None,
):
    """Build canonical DQ-ready profiling rows from a Spark DataFrame."""
    from pyspark.sql import functions as F


    eligible_columns = _get_profiled_columns(df, exclude_columns=exclude_columns)
    if not eligible_columns:
        raise ValueError("No eligible non-technical columns found for metadata profiling.")

    dtype_map = dict(df.dtypes)
    row_count = int(df.count())

    agg_exprs = []
    for column_name in eligible_columns:
        agg_exprs.append(F.sum(F.col(column_name).isNull().cast("int")).alias(f"{column_name}_NULL_COUNT"))
        agg_exprs.append(F.countDistinct(F.col(column_name)).alias(f"{column_name}_DISTINCT_COUNT"))
        if _is_min_max_supported_type(dtype_map[column_name]):
            agg_exprs.append(F.min(F.col(column_name)).alias(f"{column_name}_MIN"))
            agg_exprs.append(F.max(F.col(column_name)).alias(f"{column_name}_MAX"))

    agg_df = df.agg(*agg_exprs)
    denominator = F.lit(row_count if row_count > 0 else 1).cast("double")

    rows = []
    for column_name in eligible_columns:
        rows.append(
            agg_df.select(
                F.lit(table_name).alias("TABLE_NAME"),
                F.from_utc_timestamp(F.current_timestamp(), run_timestamp_timezone).alias("RUN_TIMESTAMP"),
                F.lit(column_name).alias("COLUMN_NAME"),
                F.lit(dtype_map[column_name]).alias("DATA_TYPE"),
                F.lit(row_count).alias("ROW_COUNT"),
                F.coalesce(F.col(f"{column_name}_NULL_COUNT"), F.lit(0)).cast("long").alias("NULL_COUNT"),
                F.round((F.coalesce(F.col(f"{column_name}_NULL_COUNT"), F.lit(0)).cast("double") / denominator) * 100, 3).alias("NULL_PERCENT"),
                F.coalesce(F.col(f"{column_name}_DISTINCT_COUNT"), F.lit(0)).cast("long").alias("DISTINCT_COUNT"),
                F.round((F.coalesce(F.col(f"{column_name}_DISTINCT_COUNT"), F.lit(0)).cast("double") / denominator) * 100, 3).alias("DISTINCT_PERCENT"),
                F.col(f"{column_name}_MIN").cast("string").alias("MIN_VALUE") if f"{column_name}_MIN" in agg_df.columns else F.lit(None).cast("string").alias("MIN_VALUE"),
                F.col(f"{column_name}_MAX").cast("string").alias("MAX_VALUE") if f"{column_name}_MAX" in agg_df.columns else F.lit(None).cast("string").alias("MAX_VALUE"),
            )
        )

    out = rows[0]
    for next_row in rows[1:]:
        out = out.unionByName(next_row)
    return out
    if include_ai_context:
        ai_context = build_ai_quality_context(
            out,
            dataset_name=dataset_name or table_name,
            table_name=table_name,
            business_context=business_context,
        )
        return out, ai_context
    return out


