"""Notebook runtime helpers for Fabric-oriented execution patterns."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from uuid import uuid4


class NotebookNamingError(ValueError):
    """Raised when a notebook name does not follow allowed naming conventions."""


def get_current_timestamp_utc() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def generate_run_id(prefix: str = "run") -> str:
    """Generate a deterministic-format run id using UTC timestamp and short UUID."""
    normalized_prefix = normalize_name(prefix) or "run"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short_uuid = uuid4().hex[:8]
    return f"{normalized_prefix}_{timestamp}_{short_uuid}"


def normalize_name(value: str) -> str:
    """Normalize a name for public-safe runtime usage."""
    normalized = re.sub(r"[^a-z0-9_]+", "_", (value or "").strip().lower().replace(" ", "_"))
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized


def validate_notebook_name(name: str, allowed_prefixes: list[str]) -> list[str]:
    """Validate notebook naming rules and return human-readable errors."""
    errors: list[str] = []
    normalized_name = (name or "").strip()
    if not normalized_name:
        errors.append("Notebook name must not be empty.")
        return errors

    if not allowed_prefixes:
        errors.append("At least one allowed prefix must be provided.")
        return errors

    if not any(normalized_name.startswith(prefix) for prefix in allowed_prefixes):
        prefix_list = ", ".join(allowed_prefixes)
        errors.append(
            f"Notebook name '{normalized_name}' must start with one of: {prefix_list}."
        )

    if normalize_name(normalized_name) != normalized_name:
        errors.append(
            "Notebook name should be lowercase with underscores only (no spaces or unsafe characters)."
        )

    return errors


def assert_notebook_name_valid(name: str, allowed_prefixes: list[str]) -> None:
    """Raise NotebookNamingError when notebook name validation fails."""
    errors = validate_notebook_name(name=name, allowed_prefixes=allowed_prefixes)
    if errors:
        raise NotebookNamingError(" ".join(errors))


def build_runtime_context(
    dataset_name: str,
    environment: str,
    source_table: str,
    target_table: str,
    notebook_name: str | None = None,
    run_id: str | None = None,
) -> dict:
    """Build a JSON-safe runtime context used by notebook orchestration patterns."""
    return {
        "dataset_name": str(dataset_name),
        "environment": str(environment),
        "source_table": str(source_table),
        "target_table": str(target_table),
        "notebook_name": None if notebook_name is None else str(notebook_name),
        "run_id": str(run_id) if run_id else generate_run_id(),
        "started_at_utc": get_current_timestamp_utc(),
    }
