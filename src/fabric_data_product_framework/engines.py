"""Engine detection and validation utilities for dataframe operations."""

from __future__ import annotations

from typing import Any

import pandas as pd


SUPPORTED_ENGINES = {"auto", "pandas", "spark"}


class UnsupportedDataFrameEngineError(TypeError):
    """Unsupporteddataframeengineerror.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> UnsupportedDataFrameEngineError(...)
    """
    """Raised when a dataframe type cannot be mapped to a supported engine."""


def validate_engine(engine: str) -> str:
    """Validate engine.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    engine : Any
    Description of `engine`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> validate_engine(...)
    """
    normalized = (engine or "").strip().lower()
    if normalized not in SUPPORTED_ENGINES:
        raise ValueError(f"Unsupported engine '{engine}'. Expected one of: auto, pandas, spark.")
    return normalized


def detect_dataframe_engine(df: Any) -> str:
    """Detect dataframe engine.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    df : Any
    Description of `df`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> detect_dataframe_engine(...)
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
