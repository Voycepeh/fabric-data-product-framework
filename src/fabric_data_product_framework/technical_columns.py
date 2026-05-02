"""Reusable technical column and datetime helpers for pandas and Spark dataframes."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any

import pandas as pd

from fabric_data_product_framework.engines import detect_dataframe_engine, validate_engine


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
    return [
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
        "ingest_run_id",
    ]


def _resolve_engine(df: Any, engine: str) -> str:
    selected_engine = validate_engine(engine)
    return detect_dataframe_engine(df) if selected_engine == "auto" else selected_engine


def _assert_columns_exist(df: Any, columns: list[str]) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def _non_technical_columns(df: Any) -> list[str]:
    technical = set(default_technical_columns())
    return [c for c in df.columns if c not in technical]


def _safe_string(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "<NULL>"
    return str(value)


def _hash_row(values: list[Any]) -> str:
    joined = "||".join(_safe_string(v) for v in values)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def add_literal_column(df, column_name: str, value, engine: str = "auto"):
    """Add literal column.

    Run `add_literal_column`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    column_name : str
        Parameter `column_name`.
    value : Any
        Parameter `value`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_literal_column`.

    Examples
    --------
    >>> add_literal_column(df, column_name)
    """
    selected_engine = _resolve_engine(df, engine)
    if selected_engine == "pandas":
        out = df.copy()
        out[column_name] = value
        return out

    from pyspark.sql import functions as F

    return df.withColumn(column_name, F.lit(value))


def add_pipeline_run_id(df, run_id: str, column_name: str = "_pipeline_run_id", engine: str = "auto"):
    """Add pipeline run id.

    Run `add_pipeline_run_id`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    run_id : str
        Parameter `run_id`.
    column_name : str, optional
        Parameter `column_name`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_pipeline_run_id`.

    Examples
    --------
    >>> add_pipeline_run_id(df, run_id)
    """
    return add_literal_column(df, column_name=column_name, value=run_id, engine=engine)


def add_pipeline_metadata(df, *, run_id: str, pipeline_name: str | None = None, environment: str | None = None, column_prefix: str = "_", engine: str = "auto"):
    """Add pipeline metadata.

    Run `add_pipeline_metadata`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    run_id : str
        Parameter `run_id`.
    pipeline_name : str | None, optional
        Parameter `pipeline_name`.
    environment : str | None, optional
        Parameter `environment`.
    column_prefix : str, optional
        Parameter `column_prefix`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_pipeline_metadata`.

    Examples
    --------
    >>> add_pipeline_metadata(df, run_id)
    """
    out = add_pipeline_run_id(df, run_id=run_id, column_name=f"{column_prefix}pipeline_run_id", engine=engine)
    if pipeline_name is not None:
        out = add_literal_column(out, column_name=f"{column_prefix}pipeline_name", value=pipeline_name, engine=engine)
    if environment is not None:
        out = add_literal_column(out, column_name=f"{column_prefix}pipeline_environment", value=environment, engine=engine)
    return out


def add_source_metadata(df, *, source_system: str | None = None, source_table: str | None = None, source_extract_timestamp: str | None = None, column_prefix: str = "_", engine: str = "auto"):
    """Add source metadata.

    Run `add_source_metadata`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    source_system : str | None, optional
        Parameter `source_system`.
    source_table : str | None, optional
        Parameter `source_table`.
    source_extract_timestamp : str | None, optional
        Parameter `source_extract_timestamp`.
    column_prefix : str, optional
        Parameter `column_prefix`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_source_metadata`.

    Examples
    --------
    >>> add_source_metadata(df, source_system)
    """
    out = df
    if source_system is not None:
        out = add_literal_column(out, column_name=f"{column_prefix}source_system", value=source_system, engine=engine)
    if source_table is not None:
        out = add_literal_column(out, column_name=f"{column_prefix}source_table", value=source_table, engine=engine)
    if source_extract_timestamp is not None:
        out = add_literal_column(out, column_name=f"{column_prefix}source_extract_timestamp", value=source_extract_timestamp, engine=engine)
    return out


def add_loaded_at(df, timestamp: str | None = None, column_name: str = "_record_loaded_timestamp", engine: str = "auto"):
    """Add loaded at.

    Run `add_loaded_at`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    timestamp : str | None, optional
        Parameter `timestamp`.
    column_name : str, optional
        Parameter `column_name`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_loaded_at`.

    Examples
    --------
    >>> add_loaded_at(df, timestamp)
    """
    selected_engine = _resolve_engine(df, engine)
    if timestamp is not None:
        return add_literal_column(df, column_name=column_name, value=timestamp, engine=selected_engine)
    if selected_engine == "pandas":
        now_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        return add_literal_column(df, column_name=column_name, value=now_utc, engine="pandas")

    from pyspark.sql import functions as F

    return df.withColumn(column_name, F.current_timestamp())


def add_watermark_value(df, watermark_column: str, output_column: str = "_watermark_value", engine: str = "auto"):
    """Add watermark value.

    Run `add_watermark_value`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    watermark_column : str
        Parameter `watermark_column`.
    output_column : str, optional
        Parameter `output_column`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_watermark_value`.

    Examples
    --------
    >>> add_watermark_value(df, watermark_column)
    """
    _assert_columns_exist(df, [watermark_column])
    selected_engine = _resolve_engine(df, engine)
    if selected_engine == "pandas":
        out = df.copy()
        out[output_column] = out[watermark_column]
        return out

    from pyspark.sql import functions as F

    return df.withColumn(output_column, F.col(watermark_column))


def add_row_hash(df, columns: list[str] | None = None, output_column: str = "_row_hash", engine: str = "auto"):
    """Add row hash.

    Run `add_row_hash`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    columns : list[str] | None, optional
        Parameter `columns`.
    output_column : str, optional
        Parameter `output_column`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_row_hash`.

    Examples
    --------
    >>> add_row_hash(df, columns)
    """
    selected_engine = _resolve_engine(df, engine)
    columns = columns or _non_technical_columns(df)
    _assert_columns_exist(df, columns)
    if selected_engine == "pandas":
        out = df.copy()
        out[output_column] = out[columns].apply(lambda row: _hash_row(row.tolist()), axis=1)
        return out

    from pyspark.sql import functions as F

    return df.withColumn(output_column, F.sha2(F.concat_ws("||", *[F.col(c) for c in columns]), 256))


def add_business_key_hash(df, business_keys: list[str], output_column: str = "_business_key_hash", engine: str = "auto"):
    """Add business key hash.

    Run `add_business_key_hash`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    business_keys : list[str]
        Parameter `business_keys`.
    output_column : str, optional
        Parameter `output_column`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_business_key_hash`.

    Examples
    --------
    >>> add_business_key_hash(df, business_keys)
    """
    _assert_columns_exist(df, business_keys)
    selected_engine = _resolve_engine(df, engine)
    if selected_engine == "pandas":
        out = df.copy()
        out[output_column] = out[business_keys].apply(lambda row: _hash_row(row.tolist()), axis=1)
        return out

    from pyspark.sql import functions as F

    return df.withColumn(output_column, F.sha2(F.concat_ws("||", *[F.col(c) for c in business_keys]), 256))


def add_datetime_parts(df, datetime_column: str, *, timezone: str = "Asia/Singapore", prefix: str | None = None, include_date: bool = True, include_time: bool = True, include_hour: bool = True, include_30_min_block: bool = True, engine: str = "auto"):
    """Add datetime parts.

    Run `add_datetime_parts`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    datetime_column : str
        Parameter `datetime_column`.
    timezone : str, optional
        Parameter `timezone`.
    prefix : str | None, optional
        Parameter `prefix`.
    include_date : bool, optional
        Parameter `include_date`.
    include_time : bool, optional
        Parameter `include_time`.
    include_hour : bool, optional
        Parameter `include_hour`.
    include_30_min_block : bool, optional
        Parameter `include_30_min_block`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_datetime_parts`.

    Examples
    --------
    >>> add_datetime_parts(df, datetime_column)
    """
    _assert_columns_exist(df, [datetime_column])
    selected_engine = _resolve_engine(df, engine)
    col_prefix = prefix or datetime_column
    if selected_engine == "pandas":
        out = df.copy()
        parsed = pd.to_datetime(out[datetime_column], errors="coerce", utc=True)
        if timezone:
            parsed = parsed.dt.tz_convert(timezone)
        if include_date:
            out[f"{col_prefix}_date"] = parsed.dt.strftime("%Y-%m-%d")
        if include_time:
            out[f"{col_prefix}_time"] = parsed.dt.strftime("%H:%M:%S")
        if include_hour:
            out[f"{col_prefix}_hour"] = parsed.dt.hour
        if include_30_min_block:
            out[f"{col_prefix}_time_block_30min"] = parsed.dt.strftime("%H:") + parsed.dt.minute.apply(lambda m: "00" if pd.notna(m) and m < 30 else "30")
        return out

    from pyspark.sql import functions as F

    localized = F.from_utc_timestamp(F.col(datetime_column), timezone)
    out = df
    if include_date:
        out = out.withColumn(f"{col_prefix}_date", F.to_date(localized))
    if include_time:
        out = out.withColumn(f"{col_prefix}_time", F.date_format(localized, "HH:mm:ss"))
    if include_hour:
        out = out.withColumn(f"{col_prefix}_hour", F.hour(localized))
    if include_30_min_block:
        out = out.withColumn(
            f"{col_prefix}_time_block_30min",
            F.when(F.minute(localized) < 30, F.concat(F.date_format(localized, "HH:"), F.lit("00"))).otherwise(F.concat(F.date_format(localized, "HH:"), F.lit("30"))),
        )
    return out


def add_standard_technical_columns(df, *, run_id: str, pipeline_name: str | None = None, environment: str | None = None, source_system: str | None = None, source_table: str | None = None, source_extract_timestamp: str | None = None, watermark_column: str | None = None, business_keys: list[str] | None = None, add_hash: bool = True, engine: str = "auto"):
    """Add standard technical columns.

    Run `add_standard_technical_columns`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    run_id : str
        Parameter `run_id`.
    pipeline_name : str | None, optional
        Parameter `pipeline_name`.
    environment : str | None, optional
        Parameter `environment`.
    source_system : str | None, optional
        Parameter `source_system`.
    source_table : str | None, optional
        Parameter `source_table`.
    source_extract_timestamp : str | None, optional
        Parameter `source_extract_timestamp`.
    watermark_column : str | None, optional
        Parameter `watermark_column`.
    business_keys : list[str] | None, optional
        Parameter `business_keys`.
    add_hash : bool, optional
        Parameter `add_hash`.
    engine : str, optional
        Parameter `engine`.

    Returns
    -------
    result : object
        Return value from `add_standard_technical_columns`.

    Examples
    --------
    >>> add_standard_technical_columns(df, run_id)
    """
    out = add_pipeline_metadata(df, run_id=run_id, pipeline_name=pipeline_name, environment=environment, engine=engine)
    out = add_source_metadata(out, source_system=source_system, source_table=source_table, source_extract_timestamp=source_extract_timestamp, engine=engine)
    out = add_loaded_at(out, engine=engine)
    if watermark_column:
        out = add_watermark_value(out, watermark_column=watermark_column, engine=engine)
    if business_keys:
        out = add_business_key_hash(out, business_keys=business_keys, engine=engine)
    if add_hash:
        out = add_row_hash(out, engine=engine)
    return out
