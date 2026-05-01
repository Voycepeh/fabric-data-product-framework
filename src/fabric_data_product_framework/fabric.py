"""Lightweight Fabric adapter helpers that avoid runtime-specific dependencies."""

from __future__ import annotations

VALID_WRITE_MODES = {"append", "overwrite", "merge"}


def build_table_identifier(
    lakehouse: str | None = None,
    schema: str | None = None,
    table: str | None = None,
) -> str:
    """Build table identifier.

    Use this callable to support the framework workflow step implemented by `build_table_identifier`.

    Parameters
    ----------
    lakehouse : str | None, optional
        Input value for `lakehouse`.
    schema : str | None, optional
        Input value for `schema`.
    table : str | None, optional
        Input value for `table`.

    Returns
    -------
    result : str
        Output produced by `build_table_identifier`.

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

    Use this callable to support the framework workflow step implemented by `read_table`.

    Parameters
    ----------
    table_identifier : str
        Input value for `table_identifier`.
    reader : Any, optional
        Input value for `reader`.

    Returns
    -------
    result : Any
        Output produced by `read_table`.

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

    Use this callable to support the framework workflow step implemented by `validate_write_mode`.

    Parameters
    ----------
    mode : str
        Input value for `mode`.

    Returns
    -------
    result : str
        Output produced by `validate_write_mode`.

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

    Use this callable to support the framework workflow step implemented by `write_table`.

    Parameters
    ----------
    df : Any
        Input value for `df`.
    table_identifier : str
        Input value for `table_identifier`.
    writer : Any, optional
        Input value for `writer`.
    mode : str, optional
        Input value for `mode`.

    Returns
    -------
    result : Any
        Output produced by `write_table`.

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
