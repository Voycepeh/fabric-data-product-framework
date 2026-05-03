"""Framework configuration builders and dataset-contract validation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
import re
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class DatasetContractValidationError(Exception):
    """Raised when dataset-contract validation fails."""


@dataclass(frozen=True)
class PathConfig:
    """Environment-to-target mapping used for lakehouse/warehouse routing."""

    paths: dict[str, dict[str, Any]]


@dataclass(frozen=True)
class NotebookRuntimeConfig:
    """Runtime options used by notebook-oriented helpers."""

    allowed_notebook_prefixes: tuple[str, ...] = ("00_", "01_", "02_", "03_")


@dataclass(frozen=True)
class AIPromptConfig:
    """Prompt templates used by AI-assisted framework workflows."""

    lineage_summary_template: str
    handover_summary_template: str
    quality_rule_generation_template: str


@dataclass(frozen=True)
class QualityConfig:
    """Default quality-policy options."""

    default_severity: str = "warning"
    fail_on_critical: bool = True
    quarantine_on_failure: bool = False


@dataclass(frozen=True)
class GovernanceConfig:
    """Default governance-policy options."""

    required_classification: bool = True
    sensitivity_rules: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class LineageConfig:
    """Default lineage-capture behavior."""

    capture_ai_summaries: bool = True
    capture_transformation_steps: bool = True


@dataclass(frozen=True)
class FrameworkConfig:
    """Top-level framework configuration object."""

    path_config: PathConfig
    notebook_runtime_config: NotebookRuntimeConfig
    ai_prompt_config: AIPromptConfig
    quality_config: QualityConfig
    governance_config: GovernanceConfig
    lineage_config: LineageConfig


def create_path_config(paths: dict[str, dict[str, Any]]) -> PathConfig:
    """Create a validated :class:`PathConfig` object."""
    if not isinstance(paths, dict) or not paths:
        raise ValueError("paths must be a non-empty mapping of environments to targets.")
    return PathConfig(paths=paths)


def create_notebook_runtime_config(allowed_notebook_prefixes: list[str] | tuple[str, ...]) -> NotebookRuntimeConfig:
    """Create notebook runtime configuration."""
    prefixes = tuple(prefix.strip() for prefix in allowed_notebook_prefixes if str(prefix).strip())
    if not prefixes:
        raise ValueError("allowed_notebook_prefixes must contain at least one non-empty prefix.")
    return NotebookRuntimeConfig(allowed_notebook_prefixes=prefixes)


def create_ai_prompt_config(
    lineage_summary_template: str,
    handover_summary_template: str,
    quality_rule_generation_template: str,
) -> AIPromptConfig:
    """Create AI prompt-template configuration."""
    for label, value in {
        "lineage_summary_template": lineage_summary_template,
        "handover_summary_template": handover_summary_template,
        "quality_rule_generation_template": quality_rule_generation_template,
    }.items():
        if not str(value).strip():
            raise ValueError(f"{label} must be a non-empty string.")
    return AIPromptConfig(
        lineage_summary_template=lineage_summary_template,
        handover_summary_template=handover_summary_template,
        quality_rule_generation_template=quality_rule_generation_template,
    )


def create_quality_config(
    default_severity: str = "warning",
    fail_on_critical: bool = True,
    quarantine_on_failure: bool = False,
) -> QualityConfig:
    """Create quality-default configuration."""
    severity = str(default_severity).strip().lower()
    if severity not in {"info", "warning", "critical"}:
        raise ValueError("default_severity must be one of: info, warning, critical.")
    return QualityConfig(
        default_severity=severity,
        fail_on_critical=bool(fail_on_critical),
        quarantine_on_failure=bool(quarantine_on_failure),
    )


def create_governance_config(
    required_classification: bool = True,
    sensitivity_rules: dict[str, str] | None = None,
) -> GovernanceConfig:
    """Create governance-default configuration."""
    return GovernanceConfig(
        required_classification=bool(required_classification),
        sensitivity_rules=dict(sensitivity_rules or {}),
    )


def create_lineage_config(
    capture_ai_summaries: bool = True,
    capture_transformation_steps: bool = True,
) -> LineageConfig:
    """Create lineage-default configuration."""
    return LineageConfig(
        capture_ai_summaries=bool(capture_ai_summaries),
        capture_transformation_steps=bool(capture_transformation_steps),
    )


def create_framework_config(
    path_config: PathConfig,
    notebook_runtime_config: NotebookRuntimeConfig,
    ai_prompt_config: AIPromptConfig,
    quality_config: QualityConfig,
    governance_config: GovernanceConfig,
    lineage_config: LineageConfig,
) -> FrameworkConfig:
    """Create the top-level framework configuration object."""
    return FrameworkConfig(
        path_config=path_config,
        notebook_runtime_config=notebook_runtime_config,
        ai_prompt_config=ai_prompt_config,
        quality_config=quality_config,
        governance_config=governance_config,
        lineage_config=lineage_config,
    )


def validate_framework_config(config: FrameworkConfig | dict[str, Any]) -> FrameworkConfig:
    """Validate and normalize framework config input."""
    if isinstance(config, FrameworkConfig):
        normalized = config
    elif isinstance(config, dict):
        required_keys = {
            "path_config",
            "notebook_runtime_config",
            "ai_prompt_config",
            "quality_config",
            "governance_config",
            "lineage_config",
        }
        missing_keys = sorted(required_keys.difference(config.keys()))
        if missing_keys:
            raise ValueError(f"Framework config is missing required keys: {', '.join(missing_keys)}.")
        normalized = FrameworkConfig(**config)
    else:
        raise ValueError("config must be a FrameworkConfig object or compatible mapping.")

    if not isinstance(normalized.path_config, PathConfig):
        raise ValueError("path_config must be a PathConfig object.")
    if not isinstance(normalized.notebook_runtime_config, NotebookRuntimeConfig):
        raise ValueError("notebook_runtime_config must be a NotebookRuntimeConfig object.")
    if not isinstance(normalized.ai_prompt_config, AIPromptConfig):
        raise ValueError("ai_prompt_config must be an AIPromptConfig object.")
    if not isinstance(normalized.quality_config, QualityConfig):
        raise ValueError("quality_config must be a QualityConfig object.")
    if not isinstance(normalized.governance_config, GovernanceConfig):
        raise ValueError("governance_config must be a GovernanceConfig object.")
    if not isinstance(normalized.lineage_config, LineageConfig):
        raise ValueError("lineage_config must be a LineageConfig object.")

    for env_name, targets in normalized.path_config.paths.items():
        if not isinstance(targets, dict) or not targets:
            raise ValueError(f"Environment '{env_name}' must contain at least one target.")
        for target_name, housepath in targets.items():
            required = ("workspace_id", "house_id", "house_name", "root")
            if not all(hasattr(housepath, attr) for attr in required):
                raise ValueError(f"Target '{env_name}/{target_name}' must provide Housepath-style fields: {required}.")

    return normalized


def load_fabric_config(config: FrameworkConfig | dict[str, Any]) -> FrameworkConfig:
    """Validate and return a user-supplied framework configuration.

    Notes
    -----
    This helper validates configuration objects only. It does not create or
    mutate Fabric resources such as workspaces, lakehouses, or warehouses.
    """
    return validate_framework_config(config)


def _default_schema_text() -> str:
    return (
        files("fabric_data_product_framework.schemas")
        .joinpath("dataset_contract.schema.json")
        .read_text(encoding="utf-8")
    )

# dataset-contract helpers unchanged

def _format_error_path(error_path: list[object], message: str, validator: str) -> str:
    parts = [str(part) for part in error_path]
    base_path = ".".join(parts)
    if validator == "required":
        match = re.search(r"'([^']+)' is a required property", message)
        if match:
            missing_property = match.group(1)
            return f"{base_path}.{missing_property}" if base_path else missing_property
    return base_path or "$"

def load_dataset_contract(path: str | Path) -> dict:
    contract_path = Path(path)
    with contract_path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        return {"value": loaded}
    return loaded

def _load_schema(schema_path: str | Path | None = None) -> dict:
    if schema_path is None:
        return yaml.safe_load(_default_schema_text())
    with Path(schema_path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def validate_dataset_contract(contract: dict, schema_path: str | Path | None = None) -> list[str]:
    schema = _load_schema(schema_path=schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(contract), key=lambda error: (list(error.path), error.message))
    return [f"{_format_error_path(list(error.path), error.message, error.validator)}: {error.message}" for error in errors]

def assert_valid_dataset_contract(contract: dict, schema_path: str | Path | None = None) -> None:
    errors = validate_dataset_contract(contract, schema_path=schema_path)
    if errors:
        raise DatasetContractValidationError("Dataset contract validation failed:\n" + "\n".join(f"- {e}" for e in errors))

def load_and_validate_dataset_contract(path: str | Path, schema_path: str | Path | None = None) -> tuple[dict, list[str]]:
    contract = load_dataset_contract(path)
    return contract, validate_dataset_contract(contract, schema_path=schema_path)
