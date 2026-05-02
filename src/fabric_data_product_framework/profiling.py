"""Simple, JSON-friendly dataframe profiling helpers for pandas and Spark."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, time
from decimal import Decimal
import json
import math
import re
from typing import Any

import pandas as pd

from fabric_data_product_framework.engines import detect_dataframe_engine, validate_engine


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
    """To jsonable.

    Run `to_jsonable`.

    Parameters
    ----------
    value : Any
        Parameter `value`.

    Returns
    -------
    result : object
        Return value from `to_jsonable`.

    Examples
    --------
    >>> to_jsonable(value)
    """
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return value
    if isinstance(value, (datetime, date, time, pd.Timestamp)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if hasattr(value, "item"):
        try:
            return to_jsonable(value.item())
        except Exception:
            return str(value)
    try:
        missing = pd.isna(value)
        if isinstance(missing, bool) and missing:
            return None
    except Exception:
        pass
    return str(value)


def infer_semantic_type(column_name: str, sample_values: list[Any]) -> str:
    """Infer semantic type.

    Run `infer_semantic_type`.

    Parameters
    ----------
    column_name : str
        Parameter `column_name`.
    sample_values : list[Any]
        Parameter `sample_values`.

    Returns
    -------
    result : str
        Return value from `infer_semantic_type`.

    Examples
    --------
    >>> infer_semantic_type(column_name, sample_values)
    """
    name = (column_name or "").lower()
    values = [str(v).strip() for v in sample_values if v is not None and str(v).strip()]
    if any(token in name for token in ["email", "e_mail"]):
        return "email"
    if any(token in name for token in ["phone", "mobile", "tel"]):
        return "phone"
    if any(token in name for token in ["first_name", "last_name", "full_name", "name"]):
        return "person_name"
    if any(token in name for token in ["id", "identifier", "key", "uuid"]):
        return "identifier"
    if "date" in name:
        return "date"
    if any(token in name for token in ["timestamp", "datetime", "_at"]):
        return "datetime"
    if any(token in name for token in ["amount", "price", "cost", "revenue", "balance"]):
        return "amount"
    if any(token in name for token in ["is_", "has_", "flag", "active"]):
        return "boolean"
    if values and all(EMAIL_RE.match(v) for v in values[:3]):
        return "email"
    if values and all(PHONE_RE.match(v) for v in values[:3]):
        return "phone"
    return "unknown"


def _is_spark_numeric_type(data_type: str) -> bool:
    value = (data_type or "").lower()
    return any(token in value for token in ["int", "long", "double", "float", "decimal", "short", "byte"])


def _is_spark_date_like_type(data_type: str) -> bool:
    value = (data_type or "").lower()
    return "date" in value or "timestamp" in value


def profile_column(series: pd.Series, sample_size: int = 5, top_n: int = 5) -> dict[str, Any]:
    """Profile column.

    Run `profile_column`.

    Parameters
    ----------
    series : pd.Series
        Parameter `series`.
    sample_size : int, optional
        Parameter `sample_size`.
    top_n : int, optional
        Parameter `top_n`.

    Returns
    -------
    result : dict[str, Any]
        Return value from `profile_column`.

    Examples
    --------
    >>> profile_column(series, sample_size)
    """
    row_count = int(series.shape[0])
    non_null = int(series.notna().sum())
    null_count = int(row_count - non_null)
    null_pct = round((null_count / row_count) * 100.0, 4) if row_count else 0.0
    non_null_series = series.dropna()
    distinct_count = int(non_null_series.nunique(dropna=True))
    distinct_pct = round((distinct_count / non_null) * 100.0, 4) if non_null else 0.0
    samples = [to_jsonable(v) for v in non_null_series.head(sample_size).tolist()]
    top_values = [{"value": to_jsonable(v), "count": int(c)} for v, c in non_null_series.value_counts(dropna=True).head(top_n).items()] if non_null else []

    min_value = max_value = mean_value = median_value = std_value = None
    if pd.api.types.is_numeric_dtype(series) and non_null:
        min_value = to_jsonable(non_null_series.min())
        max_value = to_jsonable(non_null_series.max())
        mean_value = to_jsonable(float(non_null_series.mean()))
        median_value = to_jsonable(float(non_null_series.median()))
        std_raw = non_null_series.std()
        std_value = to_jsonable(float(std_raw)) if pd.notna(std_raw) else None
    elif pd.api.types.is_datetime64_any_dtype(series) and non_null:
        min_value = to_jsonable(non_null_series.min())
        max_value = to_jsonable(non_null_series.max())

    inferred = infer_semantic_type(str(series.name), samples)
    if inferred == "unknown":
        if pd.api.types.is_bool_dtype(series):
            inferred = "boolean"
        elif pd.api.types.is_numeric_dtype(series):
            inferred = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(series):
            inferred = "datetime"
        elif distinct_count <= max(20, int(non_null * 0.2)) and non_null > 0:
            inferred = "category"
        elif non_null > 0 and distinct_count / non_null > 0.8:
            inferred = "free_text"

    return to_jsonable(asdict(ColumnProfile(str(series.name), str(series.dtype), non_null, null_count, null_pct, distinct_count, distinct_pct, samples, min_value, max_value, mean_value, median_value, std_value, top_values, inferred)))


def _profile_spark_dataframe(df, dataset_name: str = "unknown", sample_size: int = 5, top_n: int = 5) -> dict[str, Any]:
    from pyspark.sql import functions as F

    row_count = int(df.count())
    column_count = int(len(df.columns))
    columns = []
    for field in df.schema.fields:
        col = field.name
        dtype = str(field.dataType)
        agg_exprs = [
            F.count(F.col(col)).alias("non_null_count"),
            F.countDistinct(F.col(col)).alias("distinct_count"),
            F.min(F.col(col)).alias("min_value"),
            F.max(F.col(col)).alias("max_value"),
        ]
        if _is_spark_numeric_type(dtype):
            agg_exprs.extend([F.mean(F.col(col)).alias("mean_value"), F.stddev(F.col(col)).alias("std_value")])
        stats = df.agg(*agg_exprs).collect()[0].asDict()
        non_null = int(stats.get("non_null_count", 0) or 0)
        null_count = int(row_count - non_null)
        distinct_count = int(stats.get("distinct_count", 0) or 0)
        sample_values = [to_jsonable(r[col]) for r in df.select(col).where(F.col(col).isNotNull()).limit(sample_size).collect()]
        top_values = [{"value": to_jsonable(r[col]), "count": int(r["count"])} for r in df.groupBy(col).count().orderBy(F.desc("count")).limit(top_n).collect() if r[col] is not None]
        inferred = infer_semantic_type(col, sample_values)
        if inferred == "unknown":
            if _is_spark_numeric_type(dtype):
                inferred = "numeric"
            elif _is_spark_date_like_type(dtype):
                inferred = "datetime"
        columns.append(to_jsonable(asdict(ColumnProfile(col, dtype, non_null, null_count, round((null_count / row_count) * 100.0, 4) if row_count else 0.0, distinct_count, round((distinct_count / non_null) * 100.0, 4) if non_null else 0.0, sample_values, stats.get("min_value"), stats.get("max_value"), stats.get("mean_value"), None, stats.get("std_value"), top_values, inferred))))

    return to_jsonable(asdict(DataFrameProfile(dataset_name=dataset_name, engine="spark", row_count=row_count, column_count=column_count, duplicate_row_count=None, duplicate_row_pct=None, columns=columns, generated_at=datetime.utcnow().replace(microsecond=0).isoformat() + "Z")))


def profile_dataframe(df, dataset_name: str = "unknown", sample_size: int = 5, top_n: int = 5, engine: str = "auto") -> dict[str, Any]:
    """Profile dataframe.

    Run `profile_dataframe`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    dataset_name : str, optional
        Parameter `dataset_name`.
    sample_size : int, optional
        Parameter `sample_size`.
    top_n : int, optional
        Parameter `top_n`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : dict[str, Any]
        Return value from `profile_dataframe`.

    Examples
    --------
    >>> profile_dataframe(df, dataset_name)
    """
    selected_engine = validate_engine(engine)
    if selected_engine == "auto":
        selected_engine = detect_dataframe_engine(df)
    if selected_engine == "spark":
        return _profile_spark_dataframe(df=df, dataset_name=dataset_name, sample_size=sample_size, top_n=top_n)

    row_count = int(df.shape[0]); column_count = int(df.shape[1])
    duplicate_row_count = int(df.duplicated().sum()) if row_count else 0
    duplicate_row_pct = round((duplicate_row_count / row_count) * 100.0, 4) if row_count else 0.0
    cols = [profile_column(df[c], sample_size=sample_size, top_n=top_n) for c in df.columns]
    return to_jsonable(asdict(DataFrameProfile(dataset_name=dataset_name, engine="pandas", row_count=row_count, column_count=column_count, duplicate_row_count=duplicate_row_count, duplicate_row_pct=duplicate_row_pct, columns=cols, generated_at=datetime.utcnow().replace(microsecond=0).isoformat() + "Z")))


def default_technical_columns() -> list[str]:
    """Default technical columns.

    Run `default_technical_columns`.

    Parameters
    ----------
    None
        This callable does not require user-provided parameters.

    Returns
    -------
    result : list[str]
        Return value from `default_technical_columns`.

    Examples
    --------
    >>> default_technical_columns()
    """
    return ["_pipeline_run_id", "_pipeline_name", "_pipeline_environment", "_source_system", "_source_table", "_source_extract_timestamp", "_record_loaded_timestamp", "_record_updated_timestamp", "_effective_start_datetime", "_effective_end_datetime", "_is_current", "_row_hash", "_business_key_hash", "_watermark_value", "pipeline_run_id", "loaded_at", "run_ingest_id", "ingest_run_id"]


def flatten_profile_for_metadata(profile: dict, table_name: str, run_id: str, table_stage: str, exclude_columns: list[str] | None = None) -> list[dict]:
    """Flatten profile for metadata.

    Run `flatten_profile_for_metadata`.

    Parameters
    ----------
    profile : dict
        Parameter `profile`.
    table_name : str
        Parameter `table_name`.
    run_id : str
        Parameter `run_id`.
    table_stage : str
        Parameter `table_stage`.
    exclude_columns : list[str] | None, optional
        Parameter `exclude_columns`.

    Returns
    -------
    result : list[dict]
        Return value from `flatten_profile_for_metadata`.

    Examples
    --------
    >>> flatten_profile_for_metadata(profile, table_name)
    """
    excluded = set(exclude_columns or [])
    rows = []
    for col in profile.get("columns", []):
        if col.get("column_name") in excluded:
            continue
        row = {
            "run_id": run_id,
            "dataset_name": profile.get("dataset_name"),
            "table_name": table_name,
            "table_stage": table_stage,
            "engine": profile.get("engine"),
            "column_name": col.get("column_name"),
            "data_type": col.get("data_type"),
            "row_count": profile.get("row_count"),
            "non_null_count": col.get("non_null_count"),
            "null_count": col.get("null_count"),
            "null_pct": col.get("null_pct"),
            "distinct_count": col.get("distinct_count"),
            "distinct_pct": col.get("distinct_pct"),
            "min_value": col.get("min_value"),
            "max_value": col.get("max_value"),
            "mean_value": col.get("mean_value"),
            "median_value": col.get("median_value"),
            "std_value": col.get("std_value"),
            "sample_values": to_jsonable(col.get("sample_values", [])),
            "top_values": to_jsonable(col.get("top_values", [])),
            "inferred_semantic_type": col.get("inferred_semantic_type"),
            "generated_at": profile.get("generated_at"),
        }
        row["sample_values_json"] = json.dumps(row["sample_values"])
        row["top_values_json"] = json.dumps(row["top_values"])
        rows.append(to_jsonable(row))
    return rows


def _spark_create_metadata_dataframe(spark, rows: list[dict]):
    """Create a Spark dataframe for metadata rows using explicit schema-safe JSON normalization."""
    if not rows:
        return None
    normalized = []
    for row in rows:
        item = dict(row)
        item["sample_values_json"] = json.dumps(to_jsonable(item.get("sample_values", [])))
        item["top_values_json"] = json.dumps(to_jsonable(item.get("top_values", [])))
        item.pop("sample_values", None)
        item.pop("top_values", None)
        normalized.append(to_jsonable(item))
    return spark.read.json(spark.sparkContext.parallelize([json.dumps(r) for r in normalized]))


def write_profile_metadata_rows(
    *,
    spark,
    metadata_rows: list[dict],
    metadata_table: str,
    mode: str = "append",
):
    """Write profile metadata rows.

    Run `write_profile_metadata_rows`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    metadata_rows : list[dict]
        Parameter `metadata_rows`.
    metadata_table : str
        Parameter `metadata_table`.
    mode : str, optional
        Parameter `mode`.

    Returns
    -------
    result : object
        Return value from `write_profile_metadata_rows`.

    Examples
    --------
    >>> write_profile_metadata_rows(spark, metadata_rows)
    """
    df_rows = _spark_create_metadata_dataframe(spark, metadata_rows)
    if df_rows is None:
        return None
    df_rows.write.mode(mode).saveAsTable(metadata_table)
    return df_rows


def profile_and_write_metadata(
    *,
    spark,
    df,
    dataset_name: str,
    table_name: str,
    metadata_table: str,
    run_id: str,
    table_stage: str,
    mode: str = "append",
    exclude_columns: list[str] | None = None,
    sample_size: int = 5,
    top_n: int = 5,
) -> dict[str, Any]:
    """Profile and write metadata.

    Run `profile_and_write_metadata`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    df : Any
        Parameter `df`.
    dataset_name : str
        Parameter `dataset_name`.
    table_name : str
        Parameter `table_name`.
    metadata_table : str
        Parameter `metadata_table`.
    run_id : str
        Parameter `run_id`.
    table_stage : str
        Parameter `table_stage`.
    mode : str, optional
        Parameter `mode`.
    exclude_columns : list[str] | None, optional
        Parameter `exclude_columns`.
    sample_size : int, optional
        Parameter `sample_size`.
    top_n : int, optional
        Parameter `top_n`.

    Returns
    -------
    result : dict[str, Any]
        Return value from `profile_and_write_metadata`.

    Examples
    --------
    >>> profile_and_write_metadata(spark, df)
    """
    profile = profile_dataframe(df=df, dataset_name=dataset_name, sample_size=sample_size, top_n=top_n, engine="auto")
    rows = flatten_profile_for_metadata(
        profile=profile,
        table_name=table_name,
        run_id=run_id,
        table_stage=table_stage,
        exclude_columns=exclude_columns if exclude_columns is not None else default_technical_columns(),
    )
    written_df = write_profile_metadata_rows(spark=spark, metadata_rows=rows, metadata_table=metadata_table, mode=mode)
    return {"profile": profile, "metadata_rows": rows, "written_df": written_df}


def profile_table_and_write_metadata(
    *,
    spark,
    table_name: str,
    dataset_name: str,
    metadata_table: str,
    run_id: str,
    table_stage: str,
    mode: str = "append",
    exclude_columns: list[str] | None = None,
    sample_size: int = 5,
    top_n: int = 5,
) -> dict[str, Any]:
    """Profile table and write metadata.

    Run `profile_table_and_write_metadata`.

    Parameters
    ----------
    spark : Any
        Parameter `spark`.
    table_name : str
        Parameter `table_name`.
    dataset_name : str
        Parameter `dataset_name`.
    metadata_table : str
        Parameter `metadata_table`.
    run_id : str
        Parameter `run_id`.
    table_stage : str
        Parameter `table_stage`.
    mode : str, optional
        Parameter `mode`.
    exclude_columns : list[str] | None, optional
        Parameter `exclude_columns`.
    sample_size : int, optional
        Parameter `sample_size`.
    top_n : int, optional
        Parameter `top_n`.

    Returns
    -------
    result : dict[str, Any]
        Return value from `profile_table_and_write_metadata`.

    Examples
    --------
    >>> profile_table_and_write_metadata(spark, table_name)
    """
    df = spark.table(table_name)
    return profile_and_write_metadata(
        spark=spark,
        df=df,
        dataset_name=dataset_name,
        table_name=table_name,
        metadata_table=metadata_table,
        run_id=run_id,
        table_stage=table_stage,
        mode=mode,
        exclude_columns=exclude_columns,
        sample_size=sample_size,
        top_n=top_n,
    )


def summarize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Summarize profile.

    Run `summarize_profile`.

    Parameters
    ----------
    profile : dict[str, Any]
        Parameter `profile`.

    Returns
    -------
    result : dict[str, Any]
        Return value from `summarize_profile`.

    Examples
    --------
    >>> summarize_profile(profile)
    """
    columns = profile.get("columns", [])
    likely_sensitive = [c.get("column_name") for c in columns if c.get("inferred_semantic_type") in {"email", "phone", "person_name"}]
    return {
        "dataset_name": profile.get("dataset_name"),
        "row_count": profile.get("row_count", 0),
        "column_count": profile.get("column_count", 0),
        "duplicate_row_count": profile.get("duplicate_row_count", 0),
        "columns_with_nulls": [c.get("column_name") for c in columns if c.get("null_count", 0) > 0],
        "likely_identifier_columns": [c.get("column_name") for c in columns if c.get("inferred_semantic_type") == "identifier"],
        "likely_date_columns": [c.get("column_name") for c in columns if c.get("inferred_semantic_type") in {"date", "datetime"}],
        "likely_sensitive_columns": likely_sensitive,
        "generated_at": profile.get("generated_at"),
    }


def ODI_METADATA_LOGGER(df, tablename: str, exclude_columns=None, run_timestamp_timezone="Asia/Singapore"):
    """Odi metadata logger.

    Run `ODI_METADATA_LOGGER`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    tablename : str
        Parameter `tablename`.
    exclude_columns : object, optional
        Parameter `exclude_columns`.
    run_timestamp_timezone : object, optional
        Parameter `run_timestamp_timezone`.

    Returns
    -------
    result : object
        Return value from `ODI_METADATA_LOGGER`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> ODI_METADATA_LOGGER(df, tablename)
    """
    from pyspark.sql import functions as F

    technicalcol = {
        "pipeline_ts",
        "notebook_name",
        "loaded_by",
        "p_bucket",
        "sample_bucket",
        "row_ingest_id",
        "ingest_run_id",
    }

    if exclude_columns:
        technicalcol.update(exclude_columns)

    eligible_columns = [c for c, _ in df.dtypes if c not in technicalcol]
    if not eligible_columns:
        raise ValueError("No eligible non-technical columns found for metadata profiling.")

    row_count = df.count()
    agg_exprs = []

    for c, t in df.dtypes:
        if c in technicalcol:
            continue

        agg_exprs.append(F.sum(F.col(c).isNull().cast("int")).alias(f"{c}_NULL_COUNT"))
        agg_exprs.append(F.countDistinct(F.col(c)).alias(f"{c}_DISTINCT_COUNT"))

        if t in ("int", "bigint", "double", "float", "decimal", "timestamp", "date"):
            agg_exprs.append(F.min(F.col(c)).alias(f"{c}_MIN"))
            agg_exprs.append(F.max(F.col(c)).alias(f"{c}_MAX"))

    agg_df = df.agg(*agg_exprs)

    rows = []
    for c, t in df.dtypes:
        if c in technicalcol:
            continue

        rows.append(
            agg_df.select(
                F.lit(tablename).alias("TABLE_NAME"),
                F.from_utc_timestamp(F.current_timestamp(), run_timestamp_timezone).alias("RUN_TIMESTAMP"),
                F.lit(c).alias("COLUMN_NAME"),
                F.lit(t).alias("DATA_TYPE"),
                F.lit(row_count).alias("ROW_COUNT"),
                F.col(f"{c}_NULL_COUNT").alias("NULL_COUNT"),
                F.round((F.col(f"{c}_NULL_COUNT").cast("double") / F.lit(row_count)) * 100, 3).alias("NULL_PERCENT"),
                F.col(f"{c}_DISTINCT_COUNT").alias("DISTINCT_COUNT"),
                F.round((F.col(f"{c}_DISTINCT_COUNT").cast("double") / F.lit(row_count)) * 100, 3).alias("DISTINCT_PERCENT"),
                F.col(f"{c}_MIN").cast("string").alias("MIN_VALUE") if f"{c}_MIN" in agg_df.columns else F.lit(None).cast("string").alias("MIN_VALUE"),
                F.col(f"{c}_MAX").cast("string").alias("MAX_VALUE") if f"{c}_MAX" in agg_df.columns else F.lit(None).cast("string").alias("MAX_VALUE"),
            )
        )

    df_profile = rows[0]
    for r in rows[1:]:
        df_profile = df_profile.unionByName(r)

    return df_profile
