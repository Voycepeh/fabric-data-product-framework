"""Simple, JSON-friendly pandas profiling helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, time
from decimal import Decimal
import math
import re
from typing import Any

import pandas as pd


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^[+()\-\s0-9]{7,}$")


@dataclass
class ColumnProfile:
    column_name: str
    data_type: str
    non_null_count: int
    null_count: int
    null_pct: float
    distinct_count: int
    distinct_pct: float
    sample_values: list[Any]
    min_value: Any
    max_value: Any
    mean_value: float | None
    median_value: float | None
    std_value: float | None
    top_values: list[dict[str, Any]]
    inferred_semantic_type: str


@dataclass
class DataFrameProfile:
    dataset_name: str
    row_count: int
    column_count: int
    duplicate_row_count: int
    duplicate_row_pct: float
    columns: list[dict[str, Any]]
    generated_at: str


def to_jsonable(value: Any) -> Any:
    """Convert common pandas/numpy/python values to JSON-safe primitives."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return value
    if isinstance(value, (datetime, date, time, pd.Timestamp)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if hasattr(value, "item"):
        try:
            return to_jsonable(value.item())
        except Exception:
            return str(value)
    try:
        missing = pd.isna(value)
        if isinstance(missing, bool) and missing:
            return None
    except Exception:
        pass
    return str(value)


def infer_semantic_type(column_name: str, sample_values: list[Any]) -> str:
    """Conservative semantic inference from column name + sample values."""
    name = (column_name or "").lower()
    values = [str(v).strip() for v in sample_values if v is not None and str(v).strip()]

    if any(token in name for token in ["email", "e_mail"]):
        return "email"
    if any(token in name for token in ["phone", "mobile", "tel"]):
        return "phone"
    if any(token in name for token in ["first_name", "last_name", "full_name", "name"]):
        return "person_name"
    if any(token in name for token in ["id", "identifier", "key", "uuid"]):
        return "identifier"
    if any(token in name for token in ["date"]):
        return "date"
    if any(token in name for token in ["timestamp", "datetime", "_at"]):
        return "datetime"
    if any(token in name for token in ["amount", "price", "cost", "revenue", "balance"]):
        return "amount"
    if any(token in name for token in ["is_", "has_", "flag", "active"]):
        return "boolean"

    if values and all(EMAIL_RE.match(v) for v in values[:3]):
        return "email"
    if values and all(PHONE_RE.match(v) for v in values[:3]):
        return "phone"

    return "unknown"


def profile_column(series: pd.Series, sample_size: int = 5, top_n: int = 5) -> dict[str, Any]:
    """Profile a pandas Series into a JSON-serializable dict."""
    row_count = int(series.shape[0])
    non_null = int(series.notna().sum())
    null_count = int(row_count - non_null)
    null_pct = round((null_count / row_count) * 100.0, 4) if row_count else 0.0

    non_null_series = series.dropna()
    distinct_count = int(non_null_series.nunique(dropna=True))
    distinct_pct = round((distinct_count / non_null) * 100.0, 4) if non_null else 0.0

    samples = [to_jsonable(v) for v in non_null_series.head(sample_size).tolist()]

    top_values: list[dict[str, Any]] = []
    if non_null:
        for value, count in non_null_series.value_counts(dropna=True).head(top_n).items():
            top_values.append({"value": to_jsonable(value), "count": int(count)})

    min_value = None
    max_value = None
    mean_value = None
    median_value = None
    std_value = None

    if pd.api.types.is_numeric_dtype(series):
        if non_null:
            min_value = to_jsonable(non_null_series.min())
            max_value = to_jsonable(non_null_series.max())
            mean_value = to_jsonable(float(non_null_series.mean()))
            median_value = to_jsonable(float(non_null_series.median()))
            std_raw = non_null_series.std()
            std_value = to_jsonable(float(std_raw)) if pd.notna(std_raw) else None
    elif pd.api.types.is_datetime64_any_dtype(series):
        if non_null:
            min_value = to_jsonable(non_null_series.min())
            max_value = to_jsonable(non_null_series.max())

    inferred = infer_semantic_type(str(series.name), samples)

    if inferred == "unknown":
        if pd.api.types.is_bool_dtype(series):
            inferred = "boolean"
        elif pd.api.types.is_numeric_dtype(series):
            inferred = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(series):
            inferred = "datetime"
        elif distinct_count <= max(20, int(non_null * 0.2)) and non_null > 0:
            inferred = "category"
        elif non_null > 0 and distinct_count / non_null > 0.8:
            inferred = "free_text"

    profile = ColumnProfile(
        column_name=str(series.name),
        data_type=str(series.dtype),
        non_null_count=non_null,
        null_count=null_count,
        null_pct=null_pct,
        distinct_count=distinct_count,
        distinct_pct=distinct_pct,
        sample_values=samples,
        min_value=min_value,
        max_value=max_value,
        mean_value=mean_value,
        median_value=median_value,
        std_value=std_value,
        top_values=top_values,
        inferred_semantic_type=inferred,
    )
    return to_jsonable(asdict(profile))


def profile_dataframe(
    df: pd.DataFrame,
    dataset_name: str = "unknown",
    sample_size: int = 5,
    top_n: int = 5,
) -> dict[str, Any]:
    """Profile a pandas DataFrame into a JSON-serializable dict."""
    row_count = int(df.shape[0])
    column_count = int(df.shape[1])
    duplicate_row_count = int(df.duplicated().sum()) if row_count else 0
    duplicate_row_pct = round((duplicate_row_count / row_count) * 100.0, 4) if row_count else 0.0

    columns = [profile_column(df[col], sample_size=sample_size, top_n=top_n) for col in df.columns]

    profile = DataFrameProfile(
        dataset_name=dataset_name,
        row_count=row_count,
        column_count=column_count,
        duplicate_row_count=duplicate_row_count,
        duplicate_row_pct=duplicate_row_pct,
        columns=columns,
        generated_at=datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    )
    return to_jsonable(asdict(profile))


def summarize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Create a compact summary from a full DataFrame profile."""
    columns = profile.get("columns", [])
    likely_sensitive = []
    for c in columns:
        if c.get("inferred_semantic_type") in {"email", "phone", "person_name"}:
            likely_sensitive.append(c.get("column_name"))

    return {
        "dataset_name": profile.get("dataset_name"),
        "row_count": profile.get("row_count", 0),
        "column_count": profile.get("column_count", 0),
        "duplicate_row_count": profile.get("duplicate_row_count", 0),
        "columns_with_nulls": [c.get("column_name") for c in columns if c.get("null_count", 0) > 0],
        "likely_identifier_columns": [c.get("column_name") for c in columns if c.get("inferred_semantic_type") == "identifier"],
        "likely_date_columns": [c.get("column_name") for c in columns if c.get("inferred_semantic_type") in {"date", "datetime"}],
        "likely_sensitive_columns": likely_sensitive,
        "generated_at": profile.get("generated_at"),
    }
