"""Engine detection and validation utilities for dataframe operations."""

from __future__ import annotations

from typing import Any

import pandas as pd


SUPPORTED_ENGINES = {"auto", "pandas", "spark"}


class UnsupportedDataFrameEngineError(TypeError):
    """Unsupporteddataframeengineerror.

    Public class used by the framework API for `UnsupportedDataFrameEngineError`.

    Examples
    --------
    >>> UnsupportedDataFrameEngineError(... )
    """


def validate_engine(engine: str) -> str:
    """Validate engine.

    Execute `validate_engine`.

    Parameters
    ----------
    engine : str
        Value for `engine`.

    Returns
    -------
    result : str
        Result returned by `validate_engine`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> validate_engine(engine)
    """
    normalized = (engine or "").strip().lower()
    if normalized not in SUPPORTED_ENGINES:
        raise ValueError(f"Unsupported engine '{engine}'. Expected one of: auto, pandas, spark.")
    return normalized


def detect_dataframe_engine(df: Any) -> str:
    """Detect dataframe engine.

    Execute `detect_dataframe_engine`.

    Parameters
    ----------
    df : Any
        Value for `df`.

    Returns
    -------
    result : str
        Result returned by `detect_dataframe_engine`.

    Raises
    ------
    UnsupportedDataFrameEngineError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> detect_dataframe_engine(df)
    """
    if isinstance(df, pd.DataFrame):
        return "pandas"

    cls = df.__class__
    module_name = (getattr(cls, "__module__", "") or "").lower()
    class_name = (getattr(cls, "__name__", "") or "").lower()

    looks_like_spark = any(
        [
            "pyspark" in module_name,
            "spark" in module_name,
            "spark" in class_name,
            hasattr(df, "schema"),
            hasattr(df, "printSchema"),
            hasattr(df, "toDF"),
        ]
    )
    if looks_like_spark:
        return "spark"

    raise UnsupportedDataFrameEngineError(
        f"Could not detect dataframe engine for type '{module_name}.{class_name}'. "
        "Supported inputs are pandas DataFrame and Spark-like DataFrame objects."
    )
