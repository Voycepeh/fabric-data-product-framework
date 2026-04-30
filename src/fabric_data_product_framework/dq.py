"""Contract-driven data quality workflow helpers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .ai_quality_rules import parse_ai_quality_rule_candidates
from .quality import SUPPORTED_RULE_TYPES, assert_quality_gate, run_quality_rules


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_rule_id(rule: dict[str, Any]) -> str:
    return str(rule.get("rule_id") or rule.get("name") or "DQ_RULE")


def generate_dq_rule_candidates(
    profile: dict,
    metadata: dict | None = None,
    business_context: str | dict | None = None,
    dataset_name: str | None = None,
    table_name: str | None = None,
) -> list[dict]:
    """Generate conservative DQ candidate rules from profiling/metadata context."""
    profile = profile or {}
    metadata = metadata or {}
    candidates: list[dict[str, Any]] = []
    for col in profile.get("columns", []):
        if not isinstance(col, dict):
            continue
        column = col.get("column_name") or col.get("column")
        if not column:
            continue
        null_count = col.get("null_count")
        row_count = profile.get("row_count")
        if isinstance(null_count, int) and isinstance(row_count, int) and row_count > 0 and null_count == 0:
            candidates.append({"rule_id": f"{column}_not_null", "column": column, "rule_type": "not_null", "severity": "warning", "description": f"{column} should not be null"})
        distinct_count = col.get("distinct_count")
        if isinstance(distinct_count, int) and isinstance(row_count, int) and row_count > 0 and distinct_count == row_count:
            candidates.append({"rule_id": f"{column}_unique", "column": column, "rule_type": "unique", "severity": "warning", "description": f"{column} should be unique"})

    if metadata.get("ai_response"):
        parsed = parse_ai_quality_rule_candidates(metadata["ai_response"])
        for candidate in parsed.get("candidates", []):
            rule = {"rule_id": candidate.get("rule_id") or candidate.get("name"), "column": candidate.get("column"), "columns": candidate.get("columns"), "rule_type": candidate.get("rule_type"), "severity": candidate.get("severity", "warning"), "description": candidate.get("layman_rule") or candidate.get("reason")}
            cfg = candidate.get("rule_config") or {}
            if isinstance(cfg, dict):
                rule.update(cfg)
            candidates.append(rule)

    out = []
    for c in candidates:
        n = normalize_dq_rule(c)
        n.setdefault("dataset_name", dataset_name or profile.get("dataset_name"))
        n.setdefault("table_name", table_name or profile.get("table_name"))
        n.setdefault("business_context", business_context)
        out.append(n)
    return out


def normalize_dq_rule(rule: dict) -> dict:
    r = dict(rule or {})
    if "rule_id" not in r:
        r["rule_id"] = r.get("id") or r.get("name") or "DQ_RULE"
    if "table_name" not in r and r.get("table"):
        r["table_name"] = r.get("table")
    if "column" not in r and r.get("field"):
        r["column"] = r.get("field")
    if "accepted_values" not in r:
        if r.get("allowed") is not None:
            r["accepted_values"] = r.get("allowed")
        elif r.get("allowed_values") is not None:
            r["accepted_values"] = r.get("allowed_values")
        elif r.get("values") is not None:
            r["accepted_values"] = r.get("values")
    if "min_value" not in r and "min" in r:
        r["min_value"] = r.get("min")
    if "max_value" not in r and "max" in r:
        r["max_value"] = r.get("max")

    alias = {
        "min_value": "range_check",
        "max_value": "range_check",
        "between": "range_check",
        "in_set": "accepted_values",
        "allowed_values": "accepted_values",
        "not_empty": "not_null",
    }
    rtype = str(r.get("rule_type") or "").strip().lower()
    if not rtype:
        if "min_value" in r or "max_value" in r:
            rtype = "range_check"
    r["rule_type"] = alias.get(rtype, rtype)

    r["severity"] = str(r.get("severity") or "warning").lower()
    r["status"] = str(r.get("status") or "candidate").lower()
    r["generated_by"] = r.get("generated_by") or "framework"
    if not r.get("description"):
        desc_col = r.get("column") or ",".join(r.get("columns") or []) or "dataset"
        r["description"] = f"{r.get('rule_type') or 'rule'} check for {desc_col}"
    return r


def normalize_dq_rules(rules: list[dict] | None) -> list[dict]:
    return [normalize_dq_rule(r) for r in (rules or [])]


def build_dq_rule_records(rules: list[dict], dataset_name: str, table_name: str, run_id: str | None = None, status: str = "candidate", generated_by: str = "framework") -> list[dict]:
    created_at = _now_iso()
    rows = []
    for rule in normalize_dq_rules(rules):
        stored_status = rule.get("status")
        if not stored_status or stored_status == "candidate":
            stored_status = status
        rule_for_json = dict(rule)
        rule_for_json["status"] = stored_status
        rows.append({
            "rule_id": _build_rule_id(rule_for_json), "dataset_name": dataset_name, "table_name": table_name,
            "source_table": rule_for_json.get("source_table") or table_name, "column": rule_for_json.get("column"), "rule_type": rule_for_json.get("rule_type"),
            "description": rule_for_json.get("description"), "severity": rule_for_json.get("severity", "warning"), "status": stored_status,
            "generated_by": rule_for_json.get("generated_by", generated_by), "approved_by": rule_for_json.get("approved_by"), "approved_at": rule_for_json.get("approved_at"),
            "run_id": run_id, "rule_json": json.dumps(rule_for_json, ensure_ascii=False), "created_at": created_at,
        })
    return rows


def store_dq_rules(spark, rules: list[dict], table_name: str, dataset_name: str | None = None, source_table: str | None = None, run_id: str | None = None, status: str = "candidate", generated_by: str = "framework", mode: str = "append") -> list[dict]:
    ds = dataset_name or "unknown"
    st = source_table or "unknown"
    records = build_dq_rule_records(rules, dataset_name=ds, table_name=st, run_id=run_id, status=status, generated_by=generated_by)
    if records:
        spark.createDataFrame(records).write.mode(mode).saveAsTable(table_name)
    return records


def load_dq_rules(spark, table_name: str, dataset_name: str | None = None, source_table: str | None = None, status: str | list[str] = "approved") -> list[dict]:
    rows = spark.table(table_name)
    if dataset_name is not None:
        rows = rows[rows["dataset_name"] == dataset_name] if hasattr(rows, "__getitem__") and "dataset_name" in rows.columns else rows
    if source_table is not None:
        for col in ("table_name", "source_table"):
            if hasattr(rows, "columns") and col in rows.columns:
                rows = rows[rows[col] == source_table]
                break
    statuses = [status] if isinstance(status, str) else list(status)
    if statuses and hasattr(rows, "columns") and "status" in rows.columns:
        rows = rows[rows["status"].isin(statuses)]
    records = rows.to_dict(orient="records") if hasattr(rows, "to_dict") else [r.asDict() for r in rows.collect()]

    rules = []
    for row in records:
        raw = row.get("rule_json")
        if raw:
            try:
                parsed = json.loads(raw) if isinstance(raw, str) else raw
                if isinstance(parsed, dict):
                    rules.append(normalize_dq_rule(parsed)); continue
            except Exception:
                pass
        rules.append(normalize_dq_rule(row))
    return rules


def run_dq_rules(df, rules: list[dict], dataset_name: str, table_name: str, engine: str = "spark", fail_on: str = "critical") -> dict:
    normalized = normalize_dq_rules(rules)
    result = run_quality_rules(df, normalized, dataset_name=dataset_name, table_name=table_name, engine=engine)
    supported = sorted(SUPPORTED_RULE_TYPES)
    for r in result.get("results", []):
        rule = next((x for x in normalized if x.get("rule_id") == r.get("rule_id")), None)
        if not rule:
            continue
        rtype = rule.get("rule_type")
        severity = str(rule.get("severity", "warning")).lower()
        if rtype not in SUPPORTED_RULE_TYPES:
            if severity == "critical":
                r.update({"status": "failed", "action": "block", "message": f"Unsupported critical rule_type '{rtype}'. Supported rule types: {supported}"})
                result["can_continue"] = False
                result["status"] = "failed"
            elif severity == "warning":
                r.update({"status": "skipped", "action": "warn", "message": f"Unsupported warning rule_type '{rtype}'. Supported rule types: {supported}"})
            else:
                r.update({"status": "skipped", "action": "allow", "message": f"Unsupported info rule_type '{rtype}'. Supported rule types: {supported}"})
    return result


def run_dq_workflow(spark, df, quality_contract, dataset_name: str, table_name: str, run_id: str | None = None, profile: dict | None = None, metadata: dict | None = None, business_context: str | dict | None = None, engine: str = "spark") -> dict:
    qc = quality_contract
    explicit_rules = list(getattr(qc, "rules", None) or (qc.get("rules") if isinstance(qc, dict) else []) or [])
    loaded_rules: list[dict] = []
    generated_candidates: list[dict] = []
    stored_candidate_records: list[dict] = []

    use_store = bool(getattr(qc, "use_rule_store", False) if not isinstance(qc, dict) else qc.get("use_rule_store", False))
    rule_store_table = getattr(qc, "rule_store_table", None) if not isinstance(qc, dict) else qc.get("rule_store_table")
    rule_status = getattr(qc, "rule_status", "approved") if not isinstance(qc, dict) else qc.get("rule_status", "approved")
    generate_candidates = bool(getattr(qc, "generate_candidates", False) if not isinstance(qc, dict) else qc.get("generate_candidates", False))
    fail_on = getattr(qc, "fail_on", "critical") if not isinstance(qc, dict) else qc.get("fail_on", "critical")

    if use_store and rule_store_table:
        loaded_rules = load_dq_rules(spark, rule_store_table, dataset_name=dataset_name, source_table=table_name, status=rule_status)

    if generate_candidates:
        generated_candidates = generate_dq_rule_candidates(profile or {}, metadata=metadata, business_context=business_context, dataset_name=dataset_name, table_name=table_name)
        if rule_store_table:
            stored_candidate_records = store_dq_rules(spark, generated_candidates, rule_store_table, dataset_name=dataset_name, source_table=table_name, run_id=run_id, status="candidate")

    combined = []
    seen = set()
    for r in [*explicit_rules, *loaded_rules]:
        nr = normalize_dq_rule(r)
        rid = nr.get("rule_id")
        if rid and rid in seen:
            continue
        if rid:
            seen.add(rid)
        combined.append(nr)

    quality_result = run_dq_rules(df, combined, dataset_name=dataset_name, table_name=table_name, engine=engine, fail_on=fail_on)
    gate_passed = True
    gate_error = None
    try:
        assert_quality_gate(quality_result, fail_on=fail_on)
    except Exception as exc:
        gate_passed = False
        gate_error = str(exc)

    return {
        "rules": combined,
        "generated_candidates": generated_candidates,
        "stored_candidate_records": stored_candidate_records,
        "loaded_rules": loaded_rules,
        "quality_result": quality_result,
        "gate_passed": gate_passed,
        "gate_error": gate_error,
        "rule_store_table": rule_store_table,
        "enforceable_rule_count": len(combined),
    }
