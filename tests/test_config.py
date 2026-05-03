from importlib.resources import files
from pathlib import Path

import pytest

from fabricops_kit.config import (
    DatasetContractValidationError,
    assert_valid_dataset_contract,
    load_and_validate_dataset_contract,
    load_dataset_contract,
    validate_dataset_contract,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures"
VALID_FIXTURE = FIXTURES_DIR / "valid_dataset_contract.yaml"
MISSING_REQUIRED_FIXTURE = FIXTURES_DIR / "invalid_dataset_contract_missing_required.yaml"
BAD_POLICY_FIXTURE = FIXTURES_DIR / "invalid_dataset_contract_bad_policy.yaml"


def test_load_dataset_contract_loads_yaml_correctly() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)

    assert contract["dataset"]["name"] == "synthetic_customer_orders_product"
    assert contract["target"]["write_mode"] == "merge"


def test_valid_contract_returns_no_errors() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)

    errors = validate_dataset_contract(contract)

    assert errors == []


def test_missing_required_section_returns_errors() -> None:
    contract = load_dataset_contract(MISSING_REQUIRED_FIXTURE)

    errors = validate_dataset_contract(contract)

    assert errors
    assert any("source" in error and "required property" in error for error in errors)


def test_invalid_refresh_mode_returns_validation_error() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["refresh"]["mode"] = "daily_incremental"

    errors = validate_dataset_contract(contract)

    assert any("refresh.mode" in error and "not one of" in error for error in errors)


def test_invalid_write_mode_returns_validation_error() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["target"]["write_mode"] = "upsert"

    errors = validate_dataset_contract(contract)

    assert any("target.write_mode" in error and "not one of" in error for error in errors)


def test_invalid_policy_fixture_returns_readable_errors() -> None:
    contract = load_dataset_contract(BAD_POLICY_FIXTURE)

    errors = validate_dataset_contract(contract)

    assert errors
    assert any(
        "policies.incremental_safety.closed_partition_grace_days" in error for error in errors
    )


def test_load_and_validate_dataset_contract_returns_contract_and_errors() -> None:
    contract, errors = load_and_validate_dataset_contract(MISSING_REQUIRED_FIXTURE)

    assert isinstance(contract, dict)
    assert errors


def test_default_schema_loading_from_package_resource_path() -> None:
    schema_resource = files("fabricops_kit.schemas").joinpath(
        "dataset_contract.schema.json"
    )

    assert schema_resource.is_file()

    _, errors = load_and_validate_dataset_contract(VALID_FIXTURE)
    assert errors == []


def test_unknown_typo_fields_are_rejected() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["dataset"]["owenr"] = "typo_field"

    errors = validate_dataset_contract(contract)

    assert any("dataset" in error and "Additional properties are not allowed" in error for error in errors)


def test_full_refresh_contract_does_not_require_watermark_or_partition() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["refresh"]["mode"] = "full_refresh"
    contract["refresh"].pop("watermark_column")
    contract["refresh"].pop("partition_column")

    errors = validate_dataset_contract(contract)

    assert errors == []


def test_incremental_contract_requires_watermark_and_partition() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)
    contract["refresh"]["mode"] = "incremental"
    contract["refresh"].pop("watermark_column")
    contract["refresh"].pop("partition_column")

    errors = validate_dataset_contract(contract)

    assert any("refresh.watermark_column" in error for error in errors)
    assert any("refresh.partition_column" in error for error in errors)


def test_assert_valid_dataset_contract_raises_on_invalid_contract() -> None:
    contract = load_dataset_contract(MISSING_REQUIRED_FIXTURE)

    with pytest.raises(DatasetContractValidationError):
        assert_valid_dataset_contract(contract)


def test_assert_valid_dataset_contract_does_not_raise_on_valid_contract() -> None:
    contract = load_dataset_contract(VALID_FIXTURE)

    assert_valid_dataset_contract(contract)
