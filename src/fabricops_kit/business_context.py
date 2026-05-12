from __future__ import annotations

import ast
import json
from datetime import datetime, timezone

from .metadata import build_metadata_column_key, build_metadata_table_key

COLUMN_BUSINESS_CONTEXT_FROM_WIDGET: list[dict] = []

BUSINESS_CONTEXT_PROMPT = """
Infer business meaning for a column. Do not classify personal data.
Use: table_name={table_name}, table_context={table_context}, column_name={column_name}, data_type={data_type},
null_count={null_count}, distinct_count={distinct_count}, observed_values_sample={observed_values_sample}.
Return Python dict BUSINESS_CONTEXT={{"column_name": "...", "business_context": "...", "notes": "..."}}
""".strip()


def prepare_business_context_profile_input(profile_rows: list[dict], table_name: str, table_context: str = "") -> list[dict]:
    out = []
    for row in profile_rows or []:
        out.append(
            {
                "table_name": table_name,
                "table_context": table_context,
                "column_name": row.get("column_name") or row.get("COLUMN_NAME"),
                "data_type": row.get("data_type") or row.get("DATA_TYPE"),
                "row_count": row.get("row_count") or row.get("ROW_COUNT"),
                "null_count": row.get("null_count") or row.get("NULL_COUNT"),
                "distinct_count": row.get("distinct_count") or row.get("DISTINCT_COUNT"),
                "observed_values_sample": row.get("observed_values_sample") or row.get("OBSERVED_VALUES_SAMPLE") or "",
            }
        )
    return out


def suggest_column_business_contexts(profile_input_rows: list[dict], prompt_template: str = BUSINESS_CONTEXT_PROMPT) -> list[dict]:
    return [{**row, "prompt": prompt_template} for row in profile_input_rows]


def _parse_ai_dict_response(text: str) -> dict:
    cleaned = str(text or "").strip()
    marker = "BUSINESS_CONTEXT"
    if marker in cleaned and "=" in cleaned:
        cleaned = cleaned.split("=", 1)[1].strip()
    try:
        obj = ast.literal_eval(cleaned)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        try:
            obj = json.loads(cleaned)
            return obj if isinstance(obj, dict) else {}
        except Exception:
            return {}


def extract_column_business_context_suggestions(response_rows: list[dict]) -> list[dict]:
    out = []
    for row in response_rows or []:
        parsed = _parse_ai_dict_response(row.get("response") or row.get("ai_response") or "")
        if parsed:
            out.append(parsed)
    return out


def capture_column_business_context(suggestions: list[dict], environment_name: str, dataset_name: str, table_name: str, default_approval_status: str = "pending") -> list[dict]:
    global COLUMN_BUSINESS_CONTEXT_FROM_WIDGET
    results = []
    for s in suggestions or []:
        col = s.get("column_name")
        results.append(
            {
                "environment_name": environment_name,
                "dataset_name": dataset_name,
                "table_name": table_name,
                "column_name": col,
                "metadata_table_key": build_metadata_table_key(environment_name, dataset_name, table_name),
                "metadata_column_key": build_metadata_column_key(environment_name, dataset_name, table_name, col),
                "ai_suggested_business_context": s.get("business_context", ""),
                "approved_business_context": s.get("business_context", ""),
                "business_context_notes": s.get("notes", ""),
                "approval_status": default_approval_status,
                "reviewer_notes": "",
                "approved_by": None,
                "approved_at": datetime.now(timezone.utc).isoformat() if default_approval_status == "approved" else None,
            }
        )
    COLUMN_BUSINESS_CONTEXT_FROM_WIDGET = results
    return results
