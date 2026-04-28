from pathlib import Path

from fabric_data_product_framework.config import (
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


def test_default_schema_path_works_without_explicit_argument() -> None:
    _, errors = load_and_validate_dataset_contract(VALID_FIXTURE)

    assert errors == []
