"""Fabric-first contract metadata helpers for notebook workflows."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

from fabricops_kit.fabric_io import Housepath, lakehouse_table_read, lakehouse_table_write

CONTRACT_TYPES = {"source_input", "output_product"}
CONTRACT_STATUSES = {"draft", "approved", "retired"}


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_contract_dict(contract: dict) -> dict:
    """Normalize a notebook-authored contract dictionary to a stable shape.

    Parameters
    ----------
    contract : dict
        Contract dictionary authored in notebook code.

    Returns
    -------
    dict
        Normalized contract dictionary with required collection keys present.
    """
    c = dict(contract or {})
    c.setdefault("description", None)
    c.setdefault("grain", None)
    c.setdefault("approved_by", None)
    c.setdefault("approval_note", None)
    c["required_columns"] = list(c.get("required_columns") or [])
    c["optional_columns"] = list(c.get("optional_columns") or [])
    c["business_keys"] = list(c.get("business_keys") or [])
    c["classifications"] = dict(c.get("classifications") or {})
    c["quality_rules"] = list(c.get("quality_rules") or [])
    c["column_types"] = dict(c.get("column_types") or {})
    return c


def validate_contract_dict(contract: dict) -> list[str]:
    """Validate a contract dictionary and return error strings without raising."""
    raw = dict(contract or {})
    errors: list[str] = []
    for field, expected_type in [
        ("required_columns", list),
        ("optional_columns", list),
        ("business_keys", list),
        ("classifications", dict),
        ("quality_rules", list),
    ]:
        if field in raw and raw[field] is not None and not isinstance(raw[field], expected_type):
            errors.append(f"{field} must be a {expected_type.__name__}")

    c = normalize_contract_dict(contract)
    for key in ["contract_id", "contract_type", "dataset_name", "object_name", "version", "status"]:
        if not c.get(key):
            errors.append(f"Missing required field: {key}")
    if c.get("contract_type") and c["contract_type"] not in CONTRACT_TYPES:
        errors.append("contract_type must be one of: source_input, output_product")
    if c.get("status") and c["status"] not in CONTRACT_STATUSES:
        errors.append("status must be one of: draft, approved, retired")
    columns = set(c.get("required_columns", [])) | set(c.get("optional_columns", []))
    for idx, rule in enumerate(c.get("quality_rules", [])):
        if not isinstance(rule, dict):
            errors.append(f"quality_rules[{idx}] must be a dict")
            continue
        for field in ["rule_id", "rule_type", "severity"]:
            if not rule.get(field):
                errors.append(f"quality_rules[{idx}] missing required field: {field}")
        col = rule.get("column")
        is_table_level = bool(rule.get("columns")) or rule.get("table_level") is True or str(rule.get("scope", "")).lower() == "table"
        if col and col not in columns and not is_table_level:
            errors.append(f"quality_rules[{idx}] column '{col}' is not in required_columns or optional_columns")
    return errors


def build_contract_header_record(contract: dict) -> dict:
    """Build one header row for FABRICOPS_CONTRACTS."""
    c = normalize_contract_dict(contract)
    timestamp = _now_utc_iso()
    approved_at = c.get("approved_at_utc")
    if c.get("status") == "approved" and not approved_at:
        approved_at = timestamp
    return {
        "contract_id": c.get("contract_id"),
        "contract_type": c.get("contract_type"),
        "dataset_name": c.get("dataset_name"),
        "object_name": c.get("object_name"),
        "version": c.get("version"),
        "status": c.get("status"),
        "description": c.get("description"),
        "grain": c.get("grain"),
        "approved_by": c.get("approved_by"),
        "approval_note": c.get("approval_note"),
        "approved_at_utc": approved_at,
        "created_at_utc": timestamp,
        "contract_json": json.dumps(c, ensure_ascii=False, default=str),
    }


def build_contract_column_records(contract: dict) -> list[dict]:
    c = normalize_contract_dict(contract)
    ts = _now_utc_iso()
    keys = {v: i + 1 for i, v in enumerate(c.get("business_keys", []))}
    rows = []
    for required, columns in ((True, c["required_columns"]), (False, c["optional_columns"])):
        for col in columns:
            types = c.get("column_types", {}).get(col, {})
            rows.append({
                "contract_id": c.get("contract_id"), "contract_type": c.get("contract_type"),
                "dataset_name": c.get("dataset_name"), "object_name": c.get("object_name"), "version": c.get("version"),
                "column_name": col, "required": required, "business_key": col in keys,
                "business_key_position": keys.get(col), "classification": c.get("classifications", {}).get(col),
                "logical_type": types.get("logical_type"), "physical_type": types.get("physical_type"),
                "description": None, "created_at_utc": ts,
            })
    return rows


def build_contract_rule_records(contract: dict) -> list[dict]:
    c = normalize_contract_dict(contract)
    ts = _now_utc_iso()
    rows = []
    for rule in c["quality_rules"]:
        rows.append({
            "contract_id": c.get("contract_id"), "contract_type": c.get("contract_type"),
            "dataset_name": c.get("dataset_name"), "object_name": c.get("object_name"), "version": c.get("version"),
            "rule_id": rule.get("rule_id"), "rule_type": rule.get("rule_type"), "column_name": rule.get("column"),
            "severity": rule.get("severity"), "status": c.get("status"), "rule_json": json.dumps(rule, ensure_ascii=False, default=str),
            "created_at_utc": ts,
        })
    return rows


def build_contract_records(contract: dict) -> dict:
    return {"contracts": [build_contract_header_record(contract)], "columns": build_contract_column_records(contract), "rules": build_contract_rule_records(contract)}


def contract_records_to_spark(records: list[dict], schema_name: str | None = None):
    """Convert record dictionaries into a Spark DataFrame when Spark is available."""
    from pyspark.sql import SparkSession

    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    return spark.createDataFrame(records, schema=schema_name)


def write_contract_to_lakehouse(contract, metadata_path: Housepath, mode: str = "append"):
    errs = validate_contract_dict(contract)
    if errs:
        raise ValueError("Contract validation failed: " + " | ".join(errs))
    records = build_contract_records(contract)
    contracts_df = contract_records_to_spark(records["contracts"])
    columns_df = contract_records_to_spark(records["columns"])
    lakehouse_table_write(contracts_df, metadata_path, "FABRICOPS_CONTRACTS", mode=mode)
    lakehouse_table_write(columns_df, metadata_path, "FABRICOPS_CONTRACT_COLUMNS", mode=mode)
    if records["rules"]:
        rules_df = contract_records_to_spark(records["rules"])
        lakehouse_table_write(rules_df, metadata_path, "FABRICOPS_CONTRACT_RULES", mode=mode)
    return records


def _select_latest(records: list[dict]) -> dict | None:
    if not records:
        return None
    return sorted(records, key=lambda r: (str(r.get("approved_at_utc") or ""), str(r.get("created_at_utc") or ""), str(r.get("version") or "")), reverse=True)[0]


def _to_records(table_result: Any) -> list[dict]:
    """Convert Spark-like table read output to list-of-dict records."""
    if table_result is None:
        return []
    if isinstance(table_result, list):
        rows = []
        for item in table_result:
            if isinstance(item, dict):
                rows.append(item)
            elif hasattr(item, "asDict"):
                rows.append(item.asDict(recursive=True))
            else:
                rows.append(dict(item))
        return rows
    if hasattr(table_result, "collect"):
        return [row.asDict(recursive=True) if hasattr(row, "asDict") else dict(row) for row in table_result.collect()]
    if hasattr(table_result, "toPandas"):
        return table_result.toPandas().to_dict(orient="records")
    return []


def load_contract_from_lakehouse(metadata_path: Housepath, contract_id: str, version: str | None = None) -> dict:
    headers = _to_records(lakehouse_table_read(metadata_path, "FABRICOPS_CONTRACTS"))
    candidates = [r for r in headers if r.get("contract_id") == contract_id]
    if version is not None:
        candidates = [r for r in candidates if r.get("version") == version]
    else:
        candidates = [r for r in candidates if r.get("status") == "approved"]
    selected = _select_latest(candidates)
    if not selected:
        raise ValueError(f"No contract found for contract_id='{contract_id}' version='{version}'")

    base = json.loads(selected.get("contract_json") or "{}")
    base = normalize_contract_dict(base)
    base.update({k: selected.get(k, base.get(k)) for k in ["contract_id", "contract_type", "dataset_name", "object_name", "version", "status", "description", "grain", "approved_by", "approval_note"]})
    return base


def load_latest_approved_contract(metadata_path: Housepath, dataset_name: str, object_name: str, contract_type: str = "source_input") -> dict:
    headers = _to_records(lakehouse_table_read(metadata_path, "FABRICOPS_CONTRACTS"))
    matches = [
        r for r in headers
        if r.get("dataset_name") == dataset_name and r.get("object_name") == object_name and r.get("contract_type") == contract_type and r.get("status") == "approved"
    ]
    selected = _select_latest(matches)
    if not selected:
        raise ValueError("No approved contract found for dataset/object/contract_type")
    return load_contract_from_lakehouse(metadata_path, contract_id=selected["contract_id"], version=selected.get("version"))


def extract_required_columns(contract: dict) -> list[str]:
    return list(normalize_contract_dict(contract).get("required_columns", []))


def extract_optional_columns(contract: dict) -> list[str]:
    return list(normalize_contract_dict(contract).get("optional_columns", []))


def extract_business_keys(contract: dict) -> list[str]:
    return list(normalize_contract_dict(contract).get("business_keys", []))


def extract_classifications(contract: dict) -> dict:
    return dict(normalize_contract_dict(contract).get("classifications", {}))


def extract_quality_rules(contract: dict) -> list[dict]:
    return list(normalize_contract_dict(contract).get("quality_rules", []))


def get_executable_quality_rules(contract: dict) -> list[dict]:
    return extract_quality_rules(contract)


def build_contract_summary(contract: dict) -> dict:
    c = normalize_contract_dict(contract)
    return {
        "contract_id": c.get("contract_id"), "contract_type": c.get("contract_type"), "dataset_name": c.get("dataset_name"),
        "object_name": c.get("object_name"), "version": c.get("version"), "status": c.get("status"),
        "required_column_count": len(c.get("required_columns", [])), "optional_column_count": len(c.get("optional_columns", [])),
        "business_key_count": len(c.get("business_keys", [])), "quality_rule_count": len(c.get("quality_rules", [])),
        "classification_count": len(c.get("classifications", {})),
    }
