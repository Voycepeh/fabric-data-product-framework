"""Dataset contract loading and schema validation utilities."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
import re

import yaml
from jsonschema import Draft202012Validator


class DatasetContractValidationError(Exception):
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
    """Load a dataset contract YAML file from disk."""
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
    """Validate a dataset contract dictionary against the JSON Schema."""
    schema = _load_schema(schema_path=schema_path)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(contract), key=lambda error: (list(error.path), error.message))

    formatted_errors: list[str] = []
    for error in errors:
        error_path = _format_error_path(list(error.path), error.message, error.validator)
        formatted_errors.append(f"{error_path}: {error.message}")

    return formatted_errors


def assert_valid_dataset_contract(contract: dict, schema_path: str | Path | None = None) -> None:
    """Validate a contract and raise a custom exception when validation fails."""
    errors = validate_dataset_contract(contract, schema_path=schema_path)
    if errors:
        joined_errors = "\n".join(f"- {error}" for error in errors)
        raise DatasetContractValidationError(f"Dataset contract validation failed:\n{joined_errors}")


def load_and_validate_dataset_contract(
    path: str | Path,
    schema_path: str | Path | None = None,
) -> tuple[dict, list[str]]:
    """Load a dataset contract file and validate it against the JSON Schema."""
    contract = load_dataset_contract(path)
    errors = validate_dataset_contract(contract, schema_path=schema_path)
    return contract, errors
