"""Governance labeling module scaffold."""


# --- merged from governance_classifier.py ---

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

from fabricops_kit._utils import _to_jsonable

DEFAULT_CLASSIFICATION_TERMS: dict[str, list[str]] = {
    "identifier": ["staff_id", "student_id", "employee_id", "user_id", "person_id", "nric", "national_id", "passport", "matric", "account_id"],
    "contact": ["email", "mail", "phone", "mobile", "address"],
    "personal_data": ["name", "full_name", "first_name", "last_name", "date_of_birth", "dob", "gender", "nationality"],
    "financial": ["salary", "payroll", "payment", "amount", "bank", "account_number", "invoice"],
    "health": ["diagnosis", "medical", "patient", "clinic", "health"],
    "academic": ["grade", "gpa", "exam", "course", "module", "programme", "enrollment", "admission"],
    "sensitive_free_text": ["comment", "remarks", "notes", "description", "free_text", "message", "content"],
}

DEFAULT_ACTION_BY_CLASSIFICATION = {
    "public": "no_action",
    "internal": "review",
    "identifier": "restrict_access",
    "contact": "restrict_access",
    "personal_data": "classify_in_catalog",
    "financial": "restrict_access",
    "health": "restrict_access",
    "academic": "review",
    "sensitive_free_text": "mask_or_tokenize",
    "unknown": "review",
}


def build_governance_prompt_context(
    business_context: str,
    approved_usage: str,
    dataset_context: str,
    profile_context: str = "",
    glossary_context: str = "",
    steward_notes: str = "",
) -> dict[str, str]:
    """Build first-class governance prompt context fields for notebook workflows."""
    return {
        "business_context": business_context or "",
        "approved_usage": approved_usage or "",
        "dataset_context": dataset_context or "",
        "profile_context": profile_context or "",
        "glossary_context": glossary_context or "",
        "steward_notes": steward_notes or "",
    }


def build_governance_review_rows(classifications: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert governance suggestions into notebook-editable review rows."""
    rows: list[dict[str, Any]] = []
    for item in classifications or []:
        rows.append(
            {
                "suggestion_type": "governance_classification",
                "target_column": item.get("column_name"),
                "rule_name": "classification",
                "proposed_rule_payload": json.dumps(_to_jsonable(item), sort_keys=True),
                "business_reason": item.get("reason", ""),
                "evidence": json.dumps(_to_jsonable(item.get("evidence") or {}), sort_keys=True),
                "confidence": item.get("confidence"),
                "approval_status": "pending",
                "reviewer_notes": "",
                "approved_label": item.get("suggested_classification"),
            }
        )
    return rows


def build_approved_governance_records(review_rows: list[dict[str, Any]], dataset_name: str, table_name: str, run_id: str | None = None) -> list[dict[str, Any]]:
    """Convert reviewed governance rows into approval-ready metadata records."""
    out: list[dict[str, Any]] = []
    for row in review_rows or []:
        if str(row.get("approval_status", "")).lower() != "approved":
            continue
        payload = row.get("proposed_rule_payload") or "{}"
        suggestion = json.loads(payload) if isinstance(payload, str) else dict(payload)
        out.append(
            {
                "run_id": run_id,
                "dataset_name": dataset_name,
                "table_name": table_name,
                "column_name": row.get("target_column"),
                "approved_classification": row.get("approved_label") or suggestion.get("suggested_classification"),
                "business_reason": row.get("business_reason"),
                "reviewer_notes": row.get("reviewer_notes", ""),
                "evidence_json": row.get("evidence", "{}"),
                "source_suggestion_json": json.dumps(_to_jsonable(suggestion), sort_keys=True),
                "status": "approved",
            }
        )
    return out


def _normalize_columns(profile: dict | list[dict]) -> list[dict]:
    if isinstance(profile, dict):
        columns = profile.get("columns")
        if isinstance(columns, dict):
            return [{"column_name": k, **(v if isinstance(v, dict) else {})} for k, v in columns.items()]
        if isinstance(columns, list):
            return list(columns)
        return [{"column_name": k, **(v if isinstance(v, dict) else {})} for k, v in profile.items() if isinstance(v, dict)]
    return list(profile or [])


def _column_name(rec: dict) -> str:
    return str(rec.get("column_name") or rec.get("COLUMN_NAME") or rec.get("name") or rec.get("column") or "")


def _tokenize_text(text: str) -> set[str]:
    base = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text or "")
    tokens = [t for t in re.split(r"[^a-zA-Z0-9]+", base.lower()) if t]
    return set(tokens)


def _phrase_in_text(phrase: str, text: str) -> bool:
    text_base = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text or "")
    phrase_base = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", phrase or "")
    normalized_text = " ".join(t for t in re.split(r"[^a-zA-Z0-9]+", text_base.lower()) if t)
    normalized_phrase = " ".join(t for t in re.split(r"[^a-zA-Z0-9]+", phrase_base.lower()) if t)
    return bool(normalized_phrase) and normalized_phrase in normalized_text


def _match_terms(text: str, terms: list[str]) -> list[str]:
    tokens = _tokenize_text(text)
    matched = []
    token_variants = tokens | {t[:-1] for t in tokens if len(t) > 3 and t.endswith("s")}
    for term in terms:
        term_tokens = _tokenize_text(term)
        if not term_tokens:
            continue
        if len(term_tokens) == 1 and next(iter(term_tokens)) in token_variants:
            matched.append(term)
        elif len(term_tokens) > 1 and term_tokens.issubset(tokens):
            matched.append(term)
    return matched


def classify_column(
    column_name: str,
    data_type: str | None = None,
    profile: dict | None = None,
    metadata: dict | None = None,
    business_context: str | dict | None = None,
    rules: list[dict] | None = None,
) -> dict:
    """Classify one column using term matching, metadata cues, and business context.
    
        Parameters
        ----------
        column_name : Any
            Value used by this callable.
        data_type : Any
            Value used by this callable.
        profile : Any
            Value used by this callable.
        metadata : Any
            Value used by this callable.
        business_context : Any
            Value used by this callable.
        rules : Any
            Value used by this callable.
    
        Returns
        -------
        dict
            Structured output produced by this callable.
    """
    profile = profile or {}
    metadata = metadata or {}
    text_parts = [column_name, str(metadata.get("description") or ""), str(metadata.get("business_term") or "")]
    if isinstance(business_context, str):
        text_parts.append(business_context)
    elif isinstance(business_context, dict):
        text_parts.extend(str(v) for v in business_context.values())
    text_blob = " ".join(p for p in text_parts if p)

    matched_terms: list[str] = []
    inferred_semantic_type = str(profile.get("inferred_semantic_type") or "").lower()
    matched_rule_ids: list[str] = []
    profile_signals: dict[str, Any] = {}
    business_signals: list[str] = []

    best = {"classification": "unknown", "confidence": 0.2, "reason": "No governance signal detected", "action": "review"}

    semantic_map = {
        "email": ("contact", 0.82, "Profile semantic type indicates contact data"),
        "phone": ("contact", 0.8, "Profile semantic type indicates contact data"),
        "person_name": ("personal_data", 0.8, "Profile semantic type indicates personal data"),
        "identifier": ("identifier", 0.85, "Profile semantic type indicates identifier"),
        "amount": ("financial", 0.8, "Profile semantic type indicates financial data"),
        "free_text": ("sensitive_free_text", 0.72, "Profile semantic type indicates free text"),
    }
    if inferred_semantic_type in semantic_map:
        cls, conf, reason = semantic_map[inferred_semantic_type]
        best = {"classification": cls, "confidence": conf, "reason": reason, "action": DEFAULT_ACTION_BY_CLASSIFICATION.get(cls, "review")}

    for category, terms in DEFAULT_CLASSIFICATION_TERMS.items():
        matches = _match_terms(text_blob, terms)
        if matches:
            conf = 0.75 if category in {"identifier", "contact", "financial", "health"} else 0.7
            if category == "sensitive_free_text":
                conf = 0.68
            if conf > best["confidence"]:
                best = {"classification": category, "confidence": conf, "reason": f"Name/metadata matched {category} terms", "action": DEFAULT_ACTION_BY_CLASSIFICATION.get(category, "review")}
            matched_terms.extend(matches)

    avg_len = profile.get("avg_length") or profile.get("average_length")
    distinct_pct = profile.get("distinct_pct")
    if isinstance(avg_len, (int, float)) and avg_len >= 80:
        profile_signals["long_text"] = True
        if best["classification"] == "sensitive_free_text":
            best["confidence"] = max(best["confidence"], 0.82)
    if isinstance(distinct_pct, (int, float)) and distinct_pct >= 95:
        profile_signals["high_uniqueness"] = True
        if best["classification"] in {"identifier", "contact"}:
            best["confidence"] = max(best["confidence"], 0.9)

    for rule in rules or []:
        patterns = [str(p).lower() for p in (rule.get("patterns") or [])]
        if any(_phrase_in_text(p, text_blob) for p in patterns):
            matched_rule_ids.append(str(rule.get("rule_id") or ""))
            if (rule.get("confidence") or 0) >= best["confidence"]:
                best = {
                    "classification": str(rule.get("classification") or best["classification"]),
                    "confidence": float(rule.get("confidence") or best["confidence"]),
                    "reason": str(rule.get("reason") or "Matched custom governance rule"),
                    "action": str(rule.get("action") or DEFAULT_ACTION_BY_CLASSIFICATION.get(str(rule.get("classification") or "unknown"), "review")),
                }

    for token in ["student", "staff", "hr", "payroll", "medical"]:
        if token in text_blob.lower():
            business_signals.append(token)

    return {
        "column_name": column_name,
        "data_type": data_type,
        "suggested_classification": best["classification"],
        "confidence": max(0.0, min(1.0, float(best["confidence"]))),
        "reason": best["reason"],
        "evidence": {
            "matched_terms": sorted(set(matched_terms)),
            "matched_rule_ids": [rid for rid in matched_rule_ids if rid],
            "data_type": data_type,
            "profile_signals": _to_jsonable(profile_signals),
            "business_context_signals": sorted(set(business_signals)),
        },
        "suggested_action": best["action"],
        "status": "suggested",
        "generated_by": "framework",
        "approved_by": None,
        "approved_at": None,
    }


def classify_columns(profile: dict | list[dict], metadata: dict | list[dict] | None = None, business_context: str | dict | None = None, rules: list[dict] | None = None, dataset_name: str | None = None, table_name: str | None = None, run_id: str | None = None) -> list[dict]:
    """Classify multiple columns and return normalized governance suggestions.
    
        Parameters
        ----------
        profile : Any
            Value used by this callable.
        metadata : Any
            Value used by this callable.
        business_context : Any
            Value used by this callable.
        rules : Any
            Value used by this callable.
        dataset_name : Any
            Value used by this callable.
        table_name : Any
            Value used by this callable.
        run_id : Any
            Value used by this callable.
    
        Returns
        -------
        list[dict]
            Structured output produced by this callable.
    """
    del dataset_name, table_name, run_id
    columns = _normalize_columns(profile)
    meta_lookup: dict[str, dict] = {}
    if isinstance(metadata, dict):
        if all(isinstance(v, dict) for v in metadata.values()):
            meta_lookup = {str(k): v for k, v in metadata.items()}
        else:
            meta_lookup = {str(metadata.get("column_name") or ""): metadata}
    elif isinstance(metadata, list):
        meta_lookup = {str(_column_name(m)): m for m in metadata}

    out = []
    for col in columns:
        name = _column_name(col)
        if not name:
            continue
        out.append(classify_column(name, data_type=str(col.get("data_type") or col.get("dtype") or "") or None, profile=col, metadata=meta_lookup.get(name, {}), business_context=business_context, rules=rules))
    return out


def build_governance_classification_records(classifications: list[dict], dataset_name: str, table_name: str, run_id: str | None = None, status: str = "suggested", generated_by: str = "framework") -> list[dict]:
    """Build metadata-ready governance classification records from column suggestions.
    
        Parameters
        ----------
        classifications : Any
            Value used by this callable.
        dataset_name : Any
            Value used by this callable.
        table_name : Any
            Value used by this callable.
        run_id : Any
            Value used by this callable.
        status : Any
            Value used by this callable.
        generated_by : Any
            Value used by this callable.
    
        Returns
        -------
        list[dict]
            Structured output produced by this callable.
    """
    rows = []
    for item in classifications:
        safe_item = _to_jsonable(item)
        rows.append(
            {
                "run_id": run_id,
                "dataset_name": dataset_name,
                "table_name": table_name,
                "column_name": item.get("column_name"),
                "data_type": item.get("data_type"),
                "suggested_classification": item.get("suggested_classification"),
                "confidence": item.get("confidence"),
                "reason": item.get("reason"),
                "suggested_action": item.get("suggested_action"),
                "status": status,
                "generated_by": generated_by,
                "approved_by": item.get("approved_by"),
                "approved_at": item.get("approved_at"),
                "evidence_json": json.dumps(_to_jsonable(item.get("evidence") or {}), sort_keys=True),
                "classification_json": json.dumps(safe_item, sort_keys=True),
            }
        )
    return rows


def _spark_create_governance_metadata_dataframe(spark, rows: list[dict]):
    if not rows:
        return None
    normalized = [_to_jsonable(dict(r)) for r in rows]
    json_rows = [json.dumps(r, sort_keys=True) for r in normalized]
    return spark.read.json(spark.sparkContext.parallelize(json_rows))


def write_governance_classifications(spark, classifications: list[dict], table_name: str, dataset_name: str | None = None, source_table: str | None = None, run_id: str | None = None, status: str = "suggested", generated_by: str = "framework", mode: str = "append") -> list[dict]:
    """Persist governance classifications to a metadata destination.
    
        Parameters
        ----------
        spark : Any
            Value used by this callable.
        classifications : Any
            Value used by this callable.
        table_name : Any
            Value used by this callable.
        dataset_name : Any
            Value used by this callable.
        source_table : Any
            Value used by this callable.
        run_id : Any
            Value used by this callable.
        status : Any
            Value used by this callable.
        generated_by : Any
            Value used by this callable.
        mode : Any
            Value used by this callable.
    
        Returns
        -------
        list[dict]
            Structured output produced by this callable.
    """
    dataset = dataset_name or "unknown"
    source = source_table or table_name
    records = build_governance_classification_records(classifications=classifications, dataset_name=dataset, table_name=source, run_id=run_id, status=status, generated_by=generated_by)

    def _spark_writer(rows, table_identifier, mode="append", **_):
        df = _spark_create_governance_metadata_dataframe(spark, rows)
        if df is None:
            return None
        df.write.mode(mode).saveAsTable(table_identifier)
        return df

    _spark_writer(records, table_name, mode=mode)
    return records


def summarize_governance_classifications(classifications: list[dict]) -> dict:
    """Summarize governance classification outputs into review-friendly counts.
    
        Parameters
        ----------
        classifications : Any
            Value used by this callable.
    
        Returns
        -------
        dict
            Structured output produced by this callable.
    """
    by_classification = Counter(c.get("suggested_classification", "unknown") for c in classifications)
    by_action = Counter(c.get("suggested_action", "review") for c in classifications)
    review_required_count = sum(1 for c in classifications if c.get("suggested_action") in {"review", "restrict_access", "mask_or_tokenize", "classify_in_catalog"})
    high_confidence_count = sum(1 for c in classifications if float(c.get("confidence") or 0) >= 0.85)
    return {
        "total_columns": len(classifications),
        "by_classification": dict(by_classification),
        "by_action": dict(by_action),
        "review_required_count": review_required_count,
        "high_confidence_count": high_confidence_count,
        "unknown_count": int(by_classification.get("unknown", 0)),
    }
