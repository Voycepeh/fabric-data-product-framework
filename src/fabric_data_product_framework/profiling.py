"""Fabric-first profiling utilities for standardized metadata evidence.

This module focuses on producing a stable, ODI-compatible metadata profile from a
Spark DataFrame. The profile can be written to metadata tables and reused as
AI-ready context for deterministic data quality rule hinting.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import re
from typing import Any

import pandas as pd

from fabric_data_product_framework.engines import detect_dataframe_engine, validate_engine
from fabric_data_product_framework.technical_columns import default_technical_columns


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^[+()\-\s0-9]{7,}$")


@dataclass
class ColumnProfile:
    """Columnprofile.

    Public class used by the framework API for `ColumnProfile`.

    Examples
    --------
    >>> ColumnProfile(... )
    """
    column_name: str
    data_type: str
    non_null_count: int
    null_count: int
    null_pct: float
    distinct_count: int
    distinct_pct: float
    sample_values: list[Any]
    min_value: Any
    max_value: Any
    mean_value: float | None
    median_value: float | None
    std_value: float | None
    top_values: list[dict[str, Any]]
    inferred_semantic_type: str


@dataclass
class DataFrameProfile:
    """Dataframeprofile.

    Public class used by the framework API for `DataFrameProfile`.

    Examples
    --------
    >>> DataFrameProfile(... )
    """
    dataset_name: str
    engine: str
    row_count: int
    column_count: int
    duplicate_row_count: int | None
    duplicate_row_pct: float | None
    columns: list[dict[str, Any]]
    generated_at: str


def to_jsonable(value: Any) -> Any:
    """Convert a value recursively into JSON-serializable primitives."""
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_jsonable(v) for v in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    try:
        missing = pd.isna(value)
    except Exception:
        missing = False
    if isinstance(missing, bool) and missing:
        return None
    return value


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


# Legacy compatibility shims
def profile_dataframe(df, dataset_name: str = "unknown", sample_size: int = 5, top_n: int = 5, engine: str = "auto") -> dict[str, Any]:
    """Build a lightweight profile for pandas or Spark-like DataFrames."""
    selected_engine = validate_engine(engine)
    resolved_engine = detect_dataframe_engine(df) if selected_engine == "auto" else selected_engine
    if resolved_engine == "pandas":
        pdf = df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)
        row_count = int(len(pdf))
        columns = []
        for name in pdf.columns:
            series = pdf[name]
            non_null_count = int(series.notna().sum())
            null_count = int(series.isna().sum())
            null_pct = float((null_count / row_count) * 100) if row_count else 0.0
            distinct_count = int(series.nunique(dropna=True))
            distinct_pct = float((distinct_count / row_count) * 100) if row_count else 0.0
            non_null_values = series.dropna()
            min_value = to_jsonable(non_null_values.min()) if not non_null_values.empty else None
            max_value = to_jsonable(non_null_values.max()) if not non_null_values.empty else None
            sample_values = [to_jsonable(v) for v in non_null_values.head(sample_size).tolist()]
            top_series = series.value_counts(dropna=True).head(top_n)
            top_values = [{"value": to_jsonable(idx), "count": int(count)} for idx, count in top_series.items()]
            columns.append(
                asdict(
                    ColumnProfile(
                        column_name=name,
                        data_type=str(series.dtype),
                        non_null_count=non_null_count,
                        null_count=null_count,
                        null_pct=null_pct,
                        distinct_count=distinct_count,
                        distinct_pct=distinct_pct,
                        sample_values=sample_values,
                        min_value=min_value,
                        max_value=max_value,
                        mean_value=float(non_null_values.mean()) if pd.api.types.is_numeric_dtype(series.dtype) and not non_null_values.empty else None,
                        median_value=float(non_null_values.median()) if pd.api.types.is_numeric_dtype(series.dtype) and not non_null_values.empty else None,
                        std_value=float(non_null_values.std()) if pd.api.types.is_numeric_dtype(series.dtype) and len(non_null_values) > 1 else None,
                        top_values=top_values,
                        inferred_semantic_type="unknown",
                    )
                )
            )
        return asdict(
            DataFrameProfile(
                dataset_name=dataset_name,
                engine=resolved_engine,
                row_count=row_count,
                column_count=len(pdf.columns),
                duplicate_row_count=int(pdf.duplicated().sum()),
                duplicate_row_pct=float((pdf.duplicated().sum() / row_count) * 100) if row_count else 0.0,
                columns=columns,
                generated_at=datetime.utcnow().isoformat(),
            )
        )
    if detect_dataframe_engine(df) == "spark":
        metadata_df = profile_dataframe_to_metadata(df, table_name=dataset_name)
        records = profile_metadata_to_records(metadata_df)
        return {
            "dataset_name": dataset_name,
            "engine": "spark",
            "row_count": int(records[0].get("ROW_COUNT", 0)) if records else 0,
            "column_count": len(records),
            "columns": records,
            "generated_at": datetime.utcnow().isoformat(),
        }
    raise TypeError("Unsupported dataframe type for profile_dataframe.")


def summarize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Deprecated legacy API.

    Raises
    ------
    NotImplementedError
        Always raised. Use ``profile_dataframe_to_metadata`` and
        ``build_ai_quality_context`` instead.
    """
    raise NotImplementedError(
        "summarize_profile is deprecated. Use profile_dataframe_to_metadata and build_ai_quality_context."
    )


def flatten_profile_for_metadata(
    profile: dict[str, Any],
    table_name: str,
    run_id: str,
    profile_role: str,
    exclude_columns: list[str] | set[str] | None = None,
) -> list[dict[str, Any]]:
    """Flatten a profile dictionary into metadata-friendly row records."""
    def first_present(mapping: dict[str, Any], *keys: str) -> Any:
        for key in keys:
            if key in mapping and mapping[key] is not None:
                return mapping[key]
        return None

    excluded = set(exclude_columns or [])
    rows: list[dict[str, Any]] = []
    for col in profile.get("columns", []):
        column_name = first_present(col, "column_name", "COLUMN_NAME")
        if column_name in excluded:
            continue
        rows.append(
            {
                "run_id": run_id,
                "table_name": table_name,
                "profile_role": profile_role,
                "column_name": column_name,
                "data_type": first_present(col, "data_type", "DATA_TYPE"),
                "row_count": col.get("row_count", profile.get("row_count")),
                "null_count": first_present(col, "null_count", "NULL_COUNT"),
                "null_pct": first_present(col, "null_pct", "NULL_PERCENT"),
                "distinct_count": first_present(col, "distinct_count", "DISTINCT_COUNT"),
                "distinct_pct": first_present(col, "distinct_pct", "DISTINCT_PERCENT"),
                "min_value": to_jsonable(first_present(col, "min_value", "MIN_VALUE")),
                "max_value": to_jsonable(first_present(col, "max_value", "MAX_VALUE")),
                "generated_at": profile.get("generated_at", datetime.utcnow().isoformat()),
            }
        )
    return rows
