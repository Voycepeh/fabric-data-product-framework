"""Lightweight Fabric adapter helpers that avoid runtime-specific dependencies."""

from __future__ import annotations

VALID_WRITE_MODES = {"append", "overwrite", "merge"}


def build_table_identifier(
    lakehouse: str | None = None,
    schema: str | None = None,
    table: str | None = None,
) -> str:
    """Build table identifier.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    lakehouse : Any
    Description of `lakehouse`.
    schema : Any
    Description of `schema`.
    table : Any
    Description of `table`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_table_identifier(...)
    """
    parts = [part for part in [lakehouse, schema, table] if part]
    if not parts:
        raise ValueError("At least one identifier component is required (table, schema.table, or lakehouse.schema.table).")
    return ".".join(parts)


def read_table(table_identifier: str, reader=None):
    """Read table.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    table_identifier : Any
    Description of `table_identifier`.
    reader : Any
    Description of `reader`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> read_table(...)
    """
    if reader is None:
        raise NotImplementedError(
            "No table reader provided. Inject a Fabric-compatible reader function, for example a notebook helper wrapper."
        )
    return reader(table_identifier)


def validate_write_mode(mode: str) -> str:
    """Validate write mode.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    mode : Any
    Description of `mode`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> validate_write_mode(...)
    """
    normalized_mode = (mode or "").strip().lower()
    if normalized_mode not in VALID_WRITE_MODES:
        raise ValueError("Invalid write mode. Expected one of: append, overwrite, merge.")
    return normalized_mode


def write_table(df, table_identifier: str, writer=None, mode: str = "append", **options):
    """Write table.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    df : Any
    Description of `df`.
    table_identifier : Any
    Description of `table_identifier`.
    writer : Any
    Description of `writer`.
    mode : Any
    Description of `mode`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> write_table(...)
    """
    normalized_mode = validate_write_mode(mode)
    if writer is None:
        raise NotImplementedError(
            "No table writer provided. Inject a Fabric-compatible writer function, for example a notebook helper wrapper."
        )
    return writer(df, table_identifier, mode=normalized_mode, **options)
