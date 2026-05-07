"""Runtime validation helpers for fail-fast Fabric notebook execution.

This module validates notebook naming and runtime context so pipelines stop
early when orchestration contracts are violated, before IO, quality, and
lineage artifacts are produced with ambiguous run metadata.
"""

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




def _infer_notebook_name_from_runtime() -> str | None:
    """Infer current notebook name from Fabric runtime context when available."""
    try:
        from notebookutils import runtime  # type: ignore

        context = runtime.context
    except Exception:
        return None

    if isinstance(context, dict):
        return context.get("currentNotebookName")
    if hasattr(context, "get"):
        try:
            return context.get("currentNotebookName")
        except Exception:
            pass
    return getattr(context, "currentNotebookName", None)


def validate_notebook_name(name: str | None = None, allowed_prefixes: list[str] | None = None, config: object | None = None, local_fallback_name: str | None = None) -> list[str]:
    """Validate notebook names against the framework workspace notebook model.

    Parameters
    ----------
    name : str | None, optional
        Notebook name to validate. When omitted, the function attempts to infer
        the current Fabric notebook name from runtime context.
    local_fallback_name : str | None, optional
        Local-development-only fallback when running outside Fabric runtime.
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
    runtime_name = name or _infer_notebook_name_from_runtime() or local_fallback_name
    normalized_name = (runtime_name or "").strip()
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


def assert_notebook_name_valid(name: str | None = None, allowed_prefixes: list[str] | None = None, config: object | None = None, local_fallback_name: str | None = None) -> None:
    """Raise :class:`NotebookNamingError` when a notebook name is invalid.

    Parameters
    ----------
    name : str | None, optional
        Notebook name. When omitted, inferred from Fabric runtime context.
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
    errors = validate_notebook_name(name=name, allowed_prefixes=allowed_prefixes, config=config, local_fallback_name=local_fallback_name)
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
    >>> from fabricops_kit.runtime import build_runtime_context
    >>> build_runtime_context(
    ...     dataset_name="orders",
    ...     environment="Sandbox",
    ...     source_table="raw_orders",
    ...     target_table="clean_orders",
    ...     notebook_name="03_pc_orders_source_to_product",
    ... )  # doctest: +SKIP
    {'dataset_name': 'orders', ...}
    """
    resolved_notebook_name = notebook_name or _infer_notebook_name_from_runtime()
    return {
        "dataset_name": str(dataset_name),
        "environment": str(environment),
        "source_table": str(source_table),
        "target_table": str(target_table),
        "notebook_name": None if resolved_notebook_name is None else str(resolved_notebook_name),
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
    """Execute the `validate_engine` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        engine : Any
            Input parameter `engine`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> validate_engine(...)
        """
    normalized = (engine or "").strip().lower()
    if normalized not in SUPPORTED_ENGINES:
        raise ValueError(f"Unsupported engine '{engine}'. Expected one of: auto, pandas, spark.")
    return normalized


def detect_dataframe_engine(df: Any) -> str:
    """Execute the `detect_dataframe_engine` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        df : Any
            Input parameter `df`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
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
