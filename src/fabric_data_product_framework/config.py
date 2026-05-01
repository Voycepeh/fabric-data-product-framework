"""Dataset contract loading and schema validation utilities."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
import re

import yaml
from jsonschema import Draft202012Validator


class DatasetContractValidationError(Exception):
    """Datasetcontractvalidationerror.

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
    >>> DatasetContractValidationError(...)
    """
    """Raised when strict dataset contract validation fails."""


def _default_schema_text() -> str:
    return (
        files("fabric_data_product_framework.schemas")
        .joinpath("dataset_contract.schema.json")
        .read_text(encoding="utf-8")
    )


def _format_error_path(error_path: list[object], message: str, validator: str) -> str:
    parts = [str(part) for part in error_path]
    base_path = ".".join(parts)

    if validator == "required":
        match = re.search(r"'([^']+)' is a required property", message)
        if match:
            missing_property = match.group(1)
            return f"{base_path}.{missing_property}" if base_path else missing_property

    return base_path or "$"


def load_dataset_contract(path: str | Path) -> dict:
    """Load dataset contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    path : Any
    Description of `path`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> load_dataset_contract(...)
    """
    contract_path = Path(path)
    with contract_path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)

    if loaded is None:
        return {}

    if not isinstance(loaded, dict):
        return {"value": loaded}

    return loaded


def _load_schema(schema_path: str | Path | None = None) -> dict:
    if schema_path is None:
        return yaml.safe_load(_default_schema_text())

    resolved_schema_path = Path(schema_path)
    with resolved_schema_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_dataset_contract(contract: dict, schema_path: str | Path | None = None) -> list[str]:
    """Validate dataset contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    contract : Any
    Description of `contract`.
    schema_path : Any
    Description of `schema_path`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> validate_dataset_contract(...)
    """
    schema = _load_schema(schema_path=schema_path)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(contract), key=lambda error: (list(error.path), error.message))

    formatted_errors: list[str] = []
    for error in errors:
        error_path = _format_error_path(list(error.path), error.message, error.validator)
        formatted_errors.append(f"{error_path}: {error.message}")

    return formatted_errors


def assert_valid_dataset_contract(contract: dict, schema_path: str | Path | None = None) -> None:
    """Assert valid dataset contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    contract : Any
    Description of `contract`.
    schema_path : Any
    Description of `schema_path`.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> assert_valid_dataset_contract(...)
    """
    errors = validate_dataset_contract(contract, schema_path=schema_path)
    if errors:
        joined_errors = "\n".join(f"- {error}" for error in errors)
        raise DatasetContractValidationError(f"Dataset contract validation failed:\n{joined_errors}")


def load_and_validate_dataset_contract(
    path: str | Path,
    schema_path: str | Path | None = None,
) -> tuple[dict, list[str]]:
    """Load and validate dataset contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    path : Any
    Description of `path`.
    schema_path : Any
    Description of `schema_path`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> load_and_validate_dataset_contract(...)
    """
    contract = load_dataset_contract(path)
    errors = validate_dataset_contract(contract, schema_path=schema_path)
    return contract, errors
