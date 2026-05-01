"""Notebook runtime helpers for Fabric-oriented execution patterns."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from uuid import uuid4


class NotebookNamingError(ValueError):
    """Notebooknamingerror.

    Public class used by the framework API for `NotebookNamingError`.

    Examples
    --------
    >>> NotebookNamingError(... )
    """


def get_current_timestamp_utc() -> str:
    """Get current timestamp utc.

    Use this callable to support the framework workflow step implemented by `get_current_timestamp_utc`.

    Parameters
    ----------
    None
        This callable does not require user-provided parameters.

    Returns
    -------
    result : str
        Output produced by `get_current_timestamp_utc`.

    Examples
    --------
    >>> get_current_timestamp_utc()
    """
    return datetime.now(timezone.utc).isoformat()


def generate_run_id(prefix: str = "run") -> str:
    """Generate run id.

    Use this callable to support the framework workflow step implemented by `generate_run_id`.

    Parameters
    ----------
    prefix : str, optional
        Input value for `prefix`.

    Returns
    -------
    result : str
        Output produced by `generate_run_id`.

    Examples
    --------
    >>> generate_run_id(prefix)
    """
    normalized_prefix = normalize_name(prefix) or "run"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short_uuid = uuid4().hex[:8]
    return f"{normalized_prefix}_{timestamp}_{short_uuid}"


def normalize_name(value: str) -> str:
    """Normalize name.

    Use this callable to support the framework workflow step implemented by `normalize_name`.

    Parameters
    ----------
    value : str
        Input value for `value`.

    Returns
    -------
    result : str
        Output produced by `normalize_name`.

    Examples
    --------
    >>> normalize_name(value)
    """
    normalized = re.sub(r"[^a-z0-9_]+", "_", (value or "").strip().lower().replace(" ", "_"))
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized


def validate_notebook_name(name: str, allowed_prefixes: list[str]) -> list[str]:
    """Validate notebook name.

    Use this callable to support the framework workflow step implemented by `validate_notebook_name`.

    Parameters
    ----------
    name : str
        Input value for `name`.
    allowed_prefixes : list[str]
        Input value for `allowed_prefixes`.

    Returns
    -------
    result : list[str]
        Output produced by `validate_notebook_name`.

    Examples
    --------
    >>> validate_notebook_name(name, allowed_prefixes)
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

    Use this callable to support the framework workflow step implemented by `assert_notebook_name_valid`.

    Parameters
    ----------
    name : str
        Input value for `name`.
    allowed_prefixes : list[str]
        Input value for `allowed_prefixes`.

    Returns
    -------
    result : None
        Output produced by `assert_notebook_name_valid`.

    Raises
    ------
    NotebookNamingError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> assert_notebook_name_valid(name, allowed_prefixes)
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

    Use this callable to support the framework workflow step implemented by `build_runtime_context`.

    Parameters
    ----------
    dataset_name : str
        Input value for `dataset_name`.
    environment : str
        Input value for `environment`.
    source_table : str
        Input value for `source_table`.
    target_table : str
        Input value for `target_table`.
    notebook_name : str | None, optional
        Input value for `notebook_name`.
    run_id : str | None, optional
        Input value for `run_id`.

    Returns
    -------
    result : dict
        Output produced by `build_runtime_context`.

    Examples
    --------
    >>> build_runtime_context(dataset_name, environment)
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
