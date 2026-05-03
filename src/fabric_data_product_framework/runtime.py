"""Notebook runtime helpers for Fabric-oriented execution patterns."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from uuid import uuid4


class NotebookNamingError(ValueError):
    """Raised when notebook naming validation fails."""


def get_current_timestamp_utc() -> str:
    """Return the current UTC timestamp in ISO-8601 format.

    Returns
    -------
    str
        Timestamp such as ``2026-05-02T10:20:30.123456+00:00``.

    Notes
    -----
    Useful for runtime context values persisted in Fabric logs and metadata tables.
    """
    return datetime.now(timezone.utc).isoformat()


def generate_run_id(prefix: str = "run") -> str:
    """Generate a notebook-safe run identifier.

    Parameters
    ----------
    prefix : str, default="run"
        Human-friendly prefix, typically a dataset name.

    Returns
    -------
    str
        Identifier in the form ``<normalized_prefix>_<utc_timestamp>_<short_uuid>``.

    Examples
    --------
    >>> generate_run_id("orders")  # doctest: +SKIP
    'orders_20260502T102030Z_1a2b3c4d'
    """
    normalized_prefix = normalize_name(prefix) or "run"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short_uuid = uuid4().hex[:8]
    return f"{normalized_prefix}_{timestamp}_{short_uuid}"


def normalize_name(value: str) -> str:
    """Normalize a value for safe Fabric notebook and table-style naming.

    Parameters
    ----------
    value : str
        Input text.

    Returns
    -------
    str
        Lowercase value with non ``[a-z0-9_]`` characters replaced by underscores.
    """
    normalized = re.sub(r"[^a-z0-9_]+", "_", (value or "").strip().lower().replace(" ", "_"))
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized


def validate_notebook_name(name: str, allowed_prefixes: list[str] | None = None, config: dict | object | None = None) -> list[str]:
    """Validate notebook names against the framework workspace notebook model.

    Parameters
    ----------
    name : str
        Notebook name to validate.
    allowed_prefixes : list[str] | None, optional
        Optional legacy prefix list retained for backward compatibility with
        older projects. New projects should use the default finalized model:
        ``00_env_config``, ``01_data_sharing_agreement_<agreement>``,
        ``02_ex_<agreement>_<topic>``, and
        ``03_pc_<agreement>_<from>_to_<to>``.

    Returns
    -------
    list[str]
        Validation error messages. An empty list means the name is valid.

    Examples
    --------
    >>> validate_notebook_name("00_env_config")
    []
    >>> validate_notebook_name("03_pc_email_metadata_source_to_unified")
    []
    """
    errors: list[str] = []
    normalized_name = (name or "").strip()
    if not normalized_name:
        errors.append("Notebook name must not be empty.")
        return errors

    if normalize_name(normalized_name) != normalized_name:
        errors.append(
            "Notebook name should be lowercase with underscores only (no spaces or unsafe characters)."
        )
        return errors

    if allowed_prefixes is None and config is not None:
        runtime_config = getattr(config, "notebook_runtime_config", None)
        if runtime_config is None and isinstance(config, dict):
            runtime_config = config.get("notebook_runtime_config")
        config_prefixes = getattr(runtime_config, "allowed_notebook_prefixes", None)
        if config_prefixes:
            allowed_prefixes = list(config_prefixes)

    if allowed_prefixes:
        if not any(normalized_name.startswith(prefix) for prefix in allowed_prefixes):
            prefix_list = ", ".join(allowed_prefixes)
            errors.append(
                f"Notebook name '{normalized_name}' must start with one of: {prefix_list}."
            )
        return errors

    agreement_segment = r"[a-z0-9]+(?:_[a-z0-9]+)*"
    notebook_patterns = (
        r"^00_env_config$",
        rf"^01_data_sharing_agreement_{agreement_segment}$",
        rf"^02_ex_{agreement_segment}_{agreement_segment}$",
        rf"^03_pc_{agreement_segment}_{agreement_segment}_to_{agreement_segment}$",
    )
    if not any(re.fullmatch(pattern, normalized_name) for pattern in notebook_patterns):
        errors.append(
            "Notebook name must follow one of: "
            "00_env_config, "
            "01_data_sharing_agreement_<agreement>, "
            "02_ex_<agreement>_<topic>, or "
            "03_pc_<agreement>_<from>_to_<to>."
        )

    return errors


def assert_notebook_name_valid(name: str, allowed_prefixes: list[str] | None = None, config: dict | object | None = None) -> None:
    """Raise :class:`NotebookNamingError` when a notebook name is invalid.

    Parameters
    ----------
    name : str
        Notebook name.
    allowed_prefixes : list[str] | None, optional
        Optional legacy prefix list. When omitted, the finalized notebook model
        is enforced.

    Raises
    ------
    NotebookNamingError
        If ``name`` fails :func:`validate_notebook_name` checks.

    Examples
    --------
    >>> assert_notebook_name_valid("02_ex_email_metadata_event_logic")
    >>> assert_notebook_name_valid("03_pc_email_metadata_source_to_unified")
    """
    errors = validate_notebook_name(name=name, allowed_prefixes=allowed_prefixes, config=config)
    if errors:
        raise NotebookNamingError(" ".join(errors))


def build_runtime_context(
    dataset_name: str,
    environment: str,
    source_table: str,
    target_table: str,
    notebook_name: str | None = None,
    run_id: str | None = None,
) -> dict:
    """Build a standard runtime context dictionary for Fabric notebooks.

    Parameters
    ----------
    dataset_name : str
        Logical dataset name (for example ``orders``).
    environment : str
        Deployment environment label (for example ``Sandbox``).
    source_table : str
        Source object name used in the run.
    target_table : str
        Target object name used in the run.
    notebook_name : str | None, optional
        Notebook name if available.
    run_id : str | None, optional
        Pre-generated run id. When omitted, :func:`generate_run_id` is used.

    Returns
    -------
    dict
        Notebook runtime context with run metadata.

    Examples
    --------
    >>> from fabric_data_product_framework.runtime import build_runtime_context
    >>> build_runtime_context(
    ...     dataset_name="orders",
    ...     environment="Sandbox",
    ...     source_table="raw_orders",
    ...     target_table="clean_orders",
    ...     notebook_name="03_pc_orders_source_to_product",
    ... )  # doctest: +SKIP
    {'dataset_name': 'orders', ...}
    """
    return {
        "dataset_name": str(dataset_name),
        "environment": str(environment),
        "source_table": str(source_table),
        "target_table": str(target_table),
        "notebook_name": None if notebook_name is None else str(notebook_name),
        "run_id": str(run_id) if run_id else generate_run_id(str(dataset_name)),
        "started_at_utc": get_current_timestamp_utc(),
    }


# --- merged from engines.py ---
"""Engine detection and validation utilities for dataframe operations."""


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

    Run `validate_engine`.

    Parameters
    ----------
    engine : str
        Parameter `engine`.

    Returns
    -------
    result : str
        Return value from `validate_engine`.

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

    Run `detect_dataframe_engine`.

    Parameters
    ----------
    df : Any
        Parameter `df`.

    Returns
    -------
    result : str
        Return value from `detect_dataframe_engine`.

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
