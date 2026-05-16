from __future__ import annotations

from typing import Any

_SELECTED_AGREEMENT: dict[str, Any] | None = None


def _coerce_row_dicts(rows: Any) -> list[dict[str, Any]]:
    if rows is None:
        return []
    if hasattr(rows, "collect"):
        rows = rows.collect()
    out = []
    for row in rows:
        if hasattr(row, "asDict"):
            out.append(row.asDict(recursive=True))
        else:
            out.append(dict(row))
    return out


def _latest_distinct_agreements(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        agreement_id = str(row.get("agreement_id") or "").strip()
        if not agreement_id:
            continue
        cur = latest.get(agreement_id)
        row_ts = str(row.get("updated_at") or row.get("approved_at") or "")
        cur_ts = str((cur or {}).get("updated_at") or (cur or {}).get("approved_at") or "")
        if cur is None or row_ts >= cur_ts:
            latest[agreement_id] = row
    return list(latest.values())


def load_agreements(spark, metadata_table: str = "METADATA_DATA_AGREEMENT", missing_ok: bool = False) -> list[dict[str, Any]]:
    """Load latest distinct agreement metadata rows for widget selection."""
    try:
        rows = _coerce_row_dicts(spark.table(metadata_table))
    except Exception:
        if missing_ok:
            return []
        raise RuntimeError("No agreements found. Run 01_da first.")
    picked = []
    for row in _latest_distinct_agreements(rows):
        picked.append(
            {
                "agreement_id": row.get("agreement_id"),
                "agreement_name": row.get("agreement_name") or row.get("agreement_id"),
                "approved_usage": row.get("approved_usage", ""),
                "business_context": row.get("business_context", ""),
                "ownership": row.get("ownership", ""),
                "updated_at": row.get("updated_at"),
                "approved_at": row.get("approved_at"),
            }
        )
    return picked


def _agreement_option_label(row: dict[str, Any]) -> str:
    return f"{row.get('agreement_name') or row.get('agreement_id') or 'unknown'} | {row.get('agreement_id') or 'unknown'} | {row.get('approved_usage') or ''}"


def select_agreement(agreement_rows_or_df) -> None:
    """Render a widget dropdown and store selected agreement metadata row in module state."""
    import ipywidgets as widgets
    from IPython.display import display

    global _SELECTED_AGREEMENT
    rows = _coerce_row_dicts(agreement_rows_or_df)
    if not rows:
        raise ValueError("No agreements found. Save a data agreement in notebook 01 first.")
    options = [(_agreement_option_label(r), r) for r in rows]
    dropdown = widgets.Dropdown(options=options, description="Agreement", layout=widgets.Layout(width="1000px"))

    def _on_change(change):
        if change.get("name") == "value" and change.get("new") is not None:
            _SELECTED_AGREEMENT = dict(change["new"])
            globals()["_SELECTED_AGREEMENT"] = _SELECTED_AGREEMENT

    dropdown.observe(_on_change)
    _SELECTED_AGREEMENT = dict(options[0][1])
    display(dropdown)


def get_selected_agreement() -> dict[str, Any]:
    """Return selected agreement from widget flow."""
    if not _SELECTED_AGREEMENT:
        raise RuntimeError("No agreement selected. Run select_agreement(...) and pick an agreement first.")
    return dict(_SELECTED_AGREEMENT)
