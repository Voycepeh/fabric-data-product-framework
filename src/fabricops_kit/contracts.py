"""ODCS adapter helpers for FabricOps lifecycle notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_odcs_contract(path: str | Path) -> dict[str, Any]:
    """Load an Open Data Contract Standard YAML file from disk.

    Parameters
    ----------
    path : str | Path
        File path to an ODCS YAML contract.

    Returns
    -------
    dict[str, Any]
        Parsed ODCS contract dictionary.

    Raises
    ------
    ValueError
        If YAML cannot be parsed or the result is not a valid DataContract shape.
    """

    contract_path = Path(path)
    try:
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid ODCS YAML at {contract_path}: {exc}") from exc

    if not isinstance(contract, dict):
        raise ValueError(f"ODCS contract at {contract_path} must deserialize to a mapping.")

    errors = validate_odcs_contract(contract)
    if errors:
        raise ValueError("ODCS contract validation failed: " + " | ".join(errors))
    return contract


def validate_odcs_contract(contract: dict[str, Any]) -> list[str]:
    """Validate a minimal structural subset of an ODCS contract.

    Parameters
    ----------
    contract : dict[str, Any]
        ODCS contract mapping to validate.

    Returns
    -------
    list[str]
        Validation errors; empty list means pass.
    """

    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["Contract must be a dictionary."]
    if contract.get("kind") != "DataContract":
        errors.append("kind must be DataContract")
    if not contract.get("apiVersion"):
        errors.append("apiVersion is required")
    if not (contract.get("id") or contract.get("name")):
        errors.append("id or name is required")
    if not contract.get("version"):
        errors.append("version is required")
    schema = contract.get("schema")
    if not isinstance(schema, list):
        errors.append("schema must be a list")
        return errors
    for idx, obj in enumerate(schema):
        if not isinstance(obj, dict):
            errors.append(f"schema[{idx}] must be an object")
            continue
        if not obj.get("name"):
            errors.append(f"schema[{idx}].name is required")
        properties = obj.get("properties")
        if properties is not None:
            if not isinstance(properties, list):
                errors.append(f"schema[{idx}].properties must be a list when present")
            else:
                for p_idx, prop in enumerate(properties):
                    if not isinstance(prop, dict) or not prop.get("name"):
                        errors.append(f"schema[{idx}].properties[{p_idx}].name is required")
    return errors


def get_odcs_object(contract: dict[str, Any], object_name: str) -> dict[str, Any]:
    """Get an ODCS schema object by logical or physical name."""
    for obj in contract.get("schema", []) or []:
        if obj.get("name") == object_name or obj.get("physicalName") == object_name:
            return obj
    raise ValueError(f"ODCS object '{object_name}' not found in contract schema.")


def extract_required_columns(contract: dict[str, Any], object_name: str) -> list[str]:
    """Extract required column names for an ODCS object."""
    properties = get_odcs_object(contract, object_name).get("properties") or []
    out: list[str] = []
    for prop in properties:
        if prop.get("required") is True or prop.get("nullable") is False:
            if prop.get("name"):
                out.append(prop["name"])
    return out


def extract_optional_columns(contract: dict[str, Any], object_name: str) -> list[str]:
    """Extract optional column names for an ODCS object."""
    properties = get_odcs_object(contract, object_name).get("properties") or []
    out: list[str] = []
    for prop in properties:
        if prop.get("name") and not (prop.get("required") is True or prop.get("nullable") is False):
            out.append(prop["name"])
    return out


def extract_expected_types(contract: dict[str, Any], object_name: str) -> dict[str, str]:
    """Extract expected column types preferring physicalType then logicalType."""
    properties = get_odcs_object(contract, object_name).get("properties") or []
    out: dict[str, str] = {}
    for prop in properties:
        name = prop.get("name")
        if not name:
            continue
        out[name] = prop.get("physicalType") or prop.get("logicalType")
    return {k: v for k, v in out.items() if v}


def extract_business_keys(contract: dict[str, Any], object_name: str) -> list[str]:
    """Extract business key columns for an ODCS object."""
    obj = get_odcs_object(contract, object_name)
    properties = obj.get("properties") or []
    custom = ((contract.get("customProperties") or {}).get("x-fabricops") or {}).get("businessKeys") or []
    out: list[str] = []
    for prop in properties:
        name = prop.get("name")
        if not name:
            continue
        if prop.get("primaryKey") is True or prop.get("primaryKeyPosition") is not None or name in custom:
            out.append(name)
    return out


def extract_classifications(contract: dict[str, Any], object_name: str) -> dict[str, str]:
    """Extract column classifications for an ODCS object."""
    properties = get_odcs_object(contract, object_name).get("properties") or []
    out: dict[str, str] = {}
    for prop in properties:
        name = prop.get("name")
        if not name:
            continue
        label = prop.get("classification") or prop.get("x-classification") or prop.get("x-fabricops.classification")
        if label:
            out[name] = label
    return out


def extract_quality_rules(contract: dict[str, Any], object_name: str) -> list[dict[str, Any]]:
    """Extract ODCS quality rules relevant to the specified object."""
    rules = contract.get("quality") or []
    matched: list[dict[str, Any]] = []
    for rule in rules:
        object_ref = rule.get("object") or rule.get("objectName") or rule.get("table") or rule.get("physicalName")
        if object_ref == object_name:
            matched.append(rule)
    return matched


def map_odcs_quality_rules_to_fabricops_rules(contract: dict[str, Any], object_name: str) -> list[dict[str, Any]]:
    """Map ODCS quality rules to FabricOps runtime quality rule dictionaries."""
    rules = extract_quality_rules(contract, object_name)
    mapped: list[dict[str, Any]] = []
    for rule in rules:
        source_rule = str(rule.get("rule", "")).strip()
        normalized = source_rule.lower()
        severity = str(rule.get("severity", "warning")).lower()
        mapped_severity = "critical" if severity in {"error", "critical"} else "warning"
        col = rule.get("column") or rule.get("property")
        cols = rule.get("columns")
        if normalized in {"required", "not_null", "notnull"}:
            mapped.append({"rule_type": "not_null", "column": col, "severity": mapped_severity, "name": rule.get("name")})
        elif normalized == "unique":
            mapped.append({"rule_type": "unique", "column": col, "severity": mapped_severity, "name": rule.get("name")})
        elif normalized in {"uniquecombination", "unique_combination"}:
            mapped.append({"rule_type": "unique_combination", "columns": cols or ([col] if col else []), "severity": mapped_severity, "name": rule.get("name")})
        elif normalized == "validvalues":
            mapped.append({"rule_type": "accepted_values", "column": col, "allowed_values": rule.get("validValues", []), "severity": mapped_severity, "name": rule.get("name")})
        elif normalized == "rowcount":
            if rule.get("mustBeGreaterOrEqualTo") is not None:
                mapped.append({"rule_type": "row_count_min", "min_value": rule.get("mustBeGreaterOrEqualTo"), "severity": mapped_severity, "name": rule.get("name")})
            elif rule.get("mustBeGreaterThan") is not None:
                mapped.append({"rule_type": "row_count_min", "min_value": rule.get("mustBeGreaterThan") + 1, "severity": mapped_severity, "name": rule.get("name")})
            elif isinstance(rule.get("mustBeBetween"), list) and len(rule["mustBeBetween"]) == 2:
                mapped.append({"rule_type": "row_count_between", "min_value": rule["mustBeBetween"][0], "max_value": rule["mustBeBetween"][1], "severity": mapped_severity, "name": rule.get("name")})
            else:
                mapped.append({"skipped": True, "reason": "Unsupported rowCount operator", "name": rule.get("name")})
        elif normalized == "freshness":
            mapped.append({"rule_type": "freshness_check", "column": col, "severity": mapped_severity, "name": rule.get("name")})
        else:
            mapped.append({"skipped": True, "reason": f"Unsupported ODCS rule '{source_rule}'", "name": rule.get("name")})
    return mapped


def _build_contract_summary(contract: dict[str, Any], object_name: str) -> dict[str, Any]:
    return {
        "contract_id": contract.get("id") or contract.get("name"),
        "contract_version": contract.get("version"),
        "object_name": object_name,
        "required_columns": extract_required_columns(contract, object_name),
        "optional_columns": extract_optional_columns(contract, object_name),
        "expected_types": extract_expected_types(contract, object_name),
        "business_keys": extract_business_keys(contract, object_name),
        "classifications": extract_classifications(contract, object_name),
        "quality_rule_count": len(extract_quality_rules(contract, object_name)),
    }


def build_source_input_contract_summary(contract: dict[str, Any], object_name: str) -> dict[str, Any]:
    """Build a concise source input contract summary for notebook enforcement."""
    return _build_contract_summary(contract, object_name)


def build_output_contract_summary(contract: dict[str, Any], object_name: str) -> dict[str, Any]:
    """Build a concise output product contract summary for notebook enforcement."""
    return _build_contract_summary(contract, object_name)
