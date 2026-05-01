"""Lightweight Fabric adapter helpers that avoid runtime-specific dependencies."""

from __future__ import annotations

VALID_WRITE_MODES = {"append", "overwrite", "merge"}


def build_table_identifier(
    lakehouse: str | None = None,
    schema: str | None = None,
    table: str | None = None,
) -> str:
    """Build table identifier.

    Execute `build_table_identifier`.

    Parameters
    ----------
    lakehouse : str | None, optional
        Value for `lakehouse`.
    schema : str | None, optional
        Value for `schema`.
    table : str | None, optional
        Value for `table`.

    Returns
    -------
    result : str
        Result returned by `build_table_identifier`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> build_table_identifier(lakehouse, schema)
    """
    parts = [part for part in [lakehouse, schema, table] if part]
    if not parts:
        raise ValueError("At least one identifier component is required (table, schema.table, or lakehouse.schema.table).")
    return ".".join(parts)


def read_table(table_identifier: str, reader=None):
    """Read table.

    Execute `read_table`.

    Parameters
    ----------
    table_identifier : str
        Value for `table_identifier`.
    reader : Any, optional
        Value for `reader`.

    Returns
    -------
    result : Any
        Result returned by `read_table`.

    Raises
    ------
    NotImplementedError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> read_table(table_identifier, reader)
    """
    if reader is None:
        raise NotImplementedError(
            "No table reader provided. Inject a Fabric-compatible reader function, for example a notebook helper wrapper."
        )
    return reader(table_identifier)


def validate_write_mode(mode: str) -> str:
    """Validate write mode.

    Execute `validate_write_mode`.

    Parameters
    ----------
    mode : str
        Value for `mode`.

    Returns
    -------
    result : str
        Result returned by `validate_write_mode`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> validate_write_mode(mode)
    """
    normalized_mode = (mode or "").strip().lower()
    if normalized_mode not in VALID_WRITE_MODES:
        raise ValueError("Invalid write mode. Expected one of: append, overwrite, merge.")
    return normalized_mode


def write_table(df, table_identifier: str, writer=None, mode: str = "append", **options):
    """Write table.

    Execute `write_table`.

    Parameters
    ----------
    df : Any
        Value for `df`.
    table_identifier : str
        Value for `table_identifier`.
    writer : Any, optional
        Value for `writer`.
    mode : str, optional
        Value for `mode`.

    Returns
    -------
    result : Any
        Result returned by `write_table`.

    Raises
    ------
    NotImplementedError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> write_table(df, table_identifier)
    """
    normalized_mode = validate_write_mode(mode)
    if writer is None:
        raise NotImplementedError(
            "No table writer provided. Inject a Fabric-compatible writer function, for example a notebook helper wrapper."
        )
    return writer(df, table_identifier, mode=normalized_mode, **options)
