"""Notebook runtime helpers for Fabric-oriented execution patterns."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from uuid import uuid4


class NotebookNamingError(ValueError):
    """Notebooknamingerror.

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
    >>> NotebookNamingError(...)
    """
    """Raised when a notebook name does not follow allowed naming conventions."""


def get_current_timestamp_utc() -> str:
    """Get current timestamp utc.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> get_current_timestamp_utc(...)
    """
    return datetime.now(timezone.utc).isoformat()


def generate_run_id(prefix: str = "run") -> str:
    """Generate run id.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    prefix : Any
    Description of `prefix`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> generate_run_id(...)
    """
    normalized_prefix = normalize_name(prefix) or "run"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short_uuid = uuid4().hex[:8]
    return f"{normalized_prefix}_{timestamp}_{short_uuid}"


def normalize_name(value: str) -> str:
    """Normalize name.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    value : Any
    Description of `value`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> normalize_name(...)
    """
    normalized = re.sub(r"[^a-z0-9_]+", "_", (value or "").strip().lower().replace(" ", "_"))
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized


def validate_notebook_name(name: str, allowed_prefixes: list[str]) -> list[str]:
    """Validate notebook name.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    name : Any
    Description of `name`.
    allowed_prefixes : Any
    Description of `allowed_prefixes`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> validate_notebook_name(...)
    """
    errors: list[str] = []
    normalized_name = (name or "").strip()
    if not normalized_name:
        errors.append("Notebook name must not be empty.")
        return errors

    if not allowed_prefixes:
        errors.append("At least one allowed prefix must be provided.")
        return errors

    if not any(normalized_name.startswith(prefix) for prefix in allowed_prefixes):
        prefix_list = ", ".join(allowed_prefixes)
        errors.append(
            f"Notebook name '{normalized_name}' must start with one of: {prefix_list}."
        )

    if normalize_name(normalized_name) != normalized_name:
        errors.append(
            "Notebook name should be lowercase with underscores only (no spaces or unsafe characters)."
        )

    return errors


def assert_notebook_name_valid(name: str, allowed_prefixes: list[str]) -> None:
    """Assert notebook name valid.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    name : Any
    Description of `name`.
    allowed_prefixes : Any
    Description of `allowed_prefixes`.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> assert_notebook_name_valid(...)
    """
    errors = validate_notebook_name(name=name, allowed_prefixes=allowed_prefixes)
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
    """Build runtime context.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    dataset_name : Any
    Description of `dataset_name`.
    environment : Any
    Description of `environment`.
    source_table : Any
    Description of `source_table`.
    target_table : Any
    Description of `target_table`.
    notebook_name : Any
    Description of `notebook_name`.
    run_id : Any
    Description of `run_id`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_runtime_context(...)
    """
    return {
        "dataset_name": str(dataset_name),
        "environment": str(environment),
        "source_table": str(source_table),
        "target_table": str(target_table),
        "notebook_name": None if notebook_name is None else str(notebook_name),
        "run_id": str(run_id) if run_id else generate_run_id(),
        "started_at_utc": get_current_timestamp_utc(),
    }
