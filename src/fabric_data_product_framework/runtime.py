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


def validate_notebook_name(name: str, allowed_prefixes: list[str]) -> list[str]:
    """Validate a Fabric notebook name against required prefixes and format.

    Parameters
    ----------
    name : str
        Notebook name to validate.
    allowed_prefixes : list[str]
        Permitted prefixes (for example ``dex_source_to_dex_unified``).

    Returns
    -------
    list[str]
        Validation error messages. Empty list means the name is valid.
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
    """Raise :class:`NotebookNamingError` when a notebook name is invalid.

    Parameters
    ----------
    name : str
        Notebook name.
    allowed_prefixes : list[str]
        Allowed naming prefixes.

    Raises
    ------
    NotebookNamingError
        If ``name`` fails :func:`validate_notebook_name` checks.
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
    ...     notebook_name="dex_source_to_dex_unified_orders",
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
