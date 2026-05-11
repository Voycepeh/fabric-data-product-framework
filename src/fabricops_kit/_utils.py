from __future__ import annotations

from typing import Any


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    try:
        import pandas as pd
        missing = pd.isna(value)
    except Exception:
        missing = False
    if isinstance(missing, bool) and missing:
        return None
    return value
