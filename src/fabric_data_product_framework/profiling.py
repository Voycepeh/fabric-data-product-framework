"""Fabric-first profiling utilities for standardized metadata evidence.

This module focuses on producing a stable, ODI-compatible metadata profile from a
Spark DataFrame. The profile can be written to metadata tables and reused as
AI-ready context for deterministic data quality rule hinting.
"""

from __future__ import annotations

from typing import Any


def default_technical_columns() -> list[str]:
    """Return the default technical/audit columns excluded from profiling.

    Returns
    -------
    list[str]
        Technical column names that should be excluded by default when building
        standardized metadata profiles.
    """
    return [
        "pipeline_ts",
        "notebook_name",
        "loaded_by",
        "p_bucket",
        "sample_bucket",
        "row_ingest_id",
        "ingest_run_id",
        "_pipeline_run_id",
        "_pipeline_name",
        "_pipeline_environment",
        "_source_system",
        "_source_table",
        "_source_extract_timestamp",
        "_record_loaded_timestamp",
        "_record_updated_timestamp",
        "_effective_start_datetime",
        "_effective_end_datetime",
        "_is_current",
        "_row_hash",
        "_business_key_hash",
        "_watermark_value",
        "pipeline_run_id",
        "loaded_at",
        "run_ingest_id",
    ]


def get_profiled_columns(df, exclude_columns: list[str] | set[str] | None = None) -> list[str]:
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
    excluded = set(default_technical_columns())
    if exclude_columns:
        excluded.update(exclude_columns)
    return [name for name, _dtype in df.dtypes if name not in excluded]


def is_min_max_supported_type(data_type: str) -> bool:
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


def profile_dataframe_to_metadata(
    df,
    table_name: str,
    *,
    exclude_columns: list[str] | set[str] | None = None,
    run_timestamp_timezone: str = "Asia/Singapore",
):
    """Profile a Spark/Fabric DataFrame into ODI-compatible metadata rows.

    Notes
    -----
    This function is Fabric-first and expects a Spark DataFrame runtime.
    It produces standardized metadata facts for logging, governance review,
    schema/drift comparison, and AI-assisted DQ hint generation.

    Examples
    --------
    >>> profile_df = profile_dataframe_to_metadata(df, "orders_clean")
    >>> # lakehouse_table_write(profile_df, lh_out, "METADATA_DEX_UNIFIED", mode="append")
    """
    from pyspark.sql import functions as F

    eligible_columns = get_profiled_columns(df, exclude_columns=exclude_columns)
    if not eligible_columns:
        raise ValueError("No eligible non-technical columns found for metadata profiling.")

    dtype_map = dict(df.dtypes)
    row_count = int(df.count())

    agg_exprs = []
    for column_name in eligible_columns:
        agg_exprs.append(F.sum(F.col(column_name).isNull().cast("int")).alias(f"{column_name}_NULL_COUNT"))
        agg_exprs.append(F.countDistinct(F.col(column_name)).alias(f"{column_name}_DISTINCT_COUNT"))
        if is_min_max_supported_type(dtype_map[column_name]):
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
                F.col(f"{column_name}_NULL_COUNT").alias("NULL_COUNT"),
                F.round((F.col(f"{column_name}_NULL_COUNT").cast("double") / denominator) * 100, 3).alias("NULL_PERCENT"),
                F.col(f"{column_name}_DISTINCT_COUNT").alias("DISTINCT_COUNT"),
                F.round((F.col(f"{column_name}_DISTINCT_COUNT").cast("double") / denominator) * 100, 3).alias("DISTINCT_PERCENT"),
                F.col(f"{column_name}_MIN").cast("string").alias("MIN_VALUE") if f"{column_name}_MIN" in agg_df.columns else F.lit(None).cast("string").alias("MIN_VALUE"),
                F.col(f"{column_name}_MAX").cast("string").alias("MAX_VALUE") if f"{column_name}_MAX" in agg_df.columns else F.lit(None).cast("string").alias("MAX_VALUE"),
            )
        )

    out = rows[0]
    for next_row in rows[1:]:
        out = out.unionByName(next_row)
    return out


def ODI_METADATA_LOGGER(df, tablename: str, exclude_columns=None, run_timestamp_timezone="Asia/Singapore"):
    """Compatibility wrapper kept for existing Fabric notebook workflows.

    Examples
    --------
    >>> ODI_METADATA_LOGGER(df, "orders_clean")
    """
    return profile_dataframe_to_metadata(
        df=df,
        table_name=tablename,
        exclude_columns=exclude_columns,
        run_timestamp_timezone=run_timestamp_timezone,
    )


def profile_metadata_to_records(profile_df) -> list[dict[str, Any]]:
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
    records = profile_metadata_to_records(profile_df)
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
    for r in records:
        col = r.get("COLUMN_NAME")
        dtype = str(r.get("DATA_TYPE", "")).lower()
        null_pct = _num(r.get("NULL_PERCENT"), 0)
        distinct_pct = _num(r.get("DISTINCT_PERCENT"), 0)
        has_range = r.get("MIN_VALUE") is not None and r.get("MAX_VALUE") is not None

        if null_pct <= 0.1:
            candidate_rule_hints.append({"column": col, "hint": "NOT_NULL_CANDIDATE"})
        if distinct_pct >= unique_threshold:
            candidate_rule_hints.append({"column": col, "hint": "UNIQUE_CANDIDATE"})
        if ("date" in dtype or "timestamp" in dtype) and has_range:
            candidate_rule_hints.append({"column": col, "hint": "DATE_RANGE_CANDIDATE"})
        if distinct_pct <= low_cardinality_threshold:
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
        "columns_with_nulls": columns_with_nulls,
        "high_null_columns": high_null_columns,
        "high_cardinality_columns": high_cardinality_columns,
        "low_cardinality_columns": low_cardinality_columns,
        "likely_identifier_columns": sorted(set(likely_identifier_columns)),
        "likely_date_columns": likely_date_columns,
        "candidate_rule_hints": candidate_rule_hints,
    }


# Legacy compatibility shims
def profile_dataframe(df, dataset_name: str = "unknown", sample_size: int = 5, top_n: int = 5, engine: str = "auto") -> dict[str, Any]:
    """Legacy helper retained for compatibility; prefer profile_dataframe_to_metadata."""
    if engine == "pandas":
        return {"dataset_name": dataset_name, "engine": "pandas", "row_count": int(getattr(df, "shape", [0])[0]), "column_count": int(getattr(df, "shape", [0,0])[1]), "columns": []}
    if engine == "auto" and hasattr(df, "shape"):
        return {"dataset_name": dataset_name, "engine": "pandas", "row_count": int(df.shape[0]), "column_count": int(df.shape[1]), "columns": []}
    return {"dataset_name": dataset_name, "engine": "spark", "row_count": 0, "column_count": len(getattr(df, "dtypes", [])), "columns": []}


def summarize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Legacy summary shim retained for compatibility."""
    return {"dataset_name": profile.get("dataset_name"), "row_count": profile.get("row_count", 0), "column_count": profile.get("column_count", 0), "duplicate_row_count": profile.get("duplicate_row_count", 0), "columns_with_nulls": [], "likely_identifier_columns": [], "likely_date_columns": [], "likely_sensitive_columns": [], "generated_at": profile.get("generated_at")}
