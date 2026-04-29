"""Engine detection and validation utilities for dataframe operations."""

from __future__ import annotations

from typing import Any

import pandas as pd


SUPPORTED_ENGINES = {"auto", "pandas", "spark"}


class UnsupportedDataFrameEngineError(TypeError):
    """Raised when a dataframe type cannot be mapped to a supported engine."""


def validate_engine(engine: str) -> str:
    """Validate and normalize an engine selector."""
    normalized = (engine or "").strip().lower()
    if normalized not in SUPPORTED_ENGINES:
        raise ValueError(f"Unsupported engine '{engine}'. Expected one of: auto, pandas, spark.")
    return normalized


def detect_dataframe_engine(df: Any) -> str:
    """Detect whether an input dataframe is pandas or Spark-like."""
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
