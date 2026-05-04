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

    dq_rule_candidate_template: str
    governance_candidate_template: str
    handover_summary_template: str


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


@dataclass(frozen=True)
class ConfigSmokeCheckResult:
    """Represent one readiness or smoke-test check."""

    name: str
    status: str
    message: str


@dataclass(frozen=True)
class ConfigBootstrapResult:
    """Structured output returned by :func:`bootstrap_fabric_env`."""

    environment: str
    paths: dict[str, Any]
    runtime_metadata: dict[str, Any]
    ai_availability: dict[str, Any]
    smoke_test_results: list[ConfigSmokeCheckResult]
    readiness_status: str


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
    dq_rule_candidate_template: str,
    governance_candidate_template: str,
    handover_summary_template: str,
) -> AIPromptConfig:
    """Create AI prompt-template configuration."""
    for label, value in {
        "dq_rule_candidate_template": dq_rule_candidate_template,
        "governance_candidate_template": governance_candidate_template,
        "handover_summary_template": handover_summary_template,
    }.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} must be a non-empty string.")

    return AIPromptConfig(
        dq_rule_candidate_template=dq_rule_candidate_template,
        governance_candidate_template=governance_candidate_template,
        handover_summary_template=handover_summary_template,
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


def get_path(env: str, target: str, config: FrameworkConfig | PathConfig | None) -> Any:
    """Resolve a configured environment/target entry into a path object."""
    if config is None:
        raise ValueError("No Fabric config was provided. Pass a FrameworkConfig or PathConfig instance.")
    paths = config.path_config.paths if isinstance(config, FrameworkConfig) else config.paths
    if env not in paths:
        available_envs = ", ".join(sorted(paths.keys())) or "<none>"
        raise ValueError(f"Environment '{env}' was not found in Fabric config. Available environments: {available_envs}.")
    if target not in paths[env]:
        available_targets = ", ".join(sorted(paths[env].keys())) or "<none>"
        raise ValueError(f"Target '{target}' was not found under environment '{env}'. Available targets: {available_targets}.")
    return paths[env][target]


def run_config_smoke_tests(
    config: FrameworkConfig,
    env: str = "Sandbox",
    required_targets: list[str] | None = None,
    check_ai: bool = True,
    check_io_import: bool = False,
    notebook_name: str | None = None,
    ai_result: dict[str, Any] | None = None,
) -> list[ConfigSmokeCheckResult]:
    """Run readiness-oriented config checks with optional lightweight IO checks."""
    from .runtime import validate_notebook_name

    results: list[ConfigSmokeCheckResult] = []
    required_targets = required_targets or ["Source", "Unified"]
    try:
        for target in required_targets:
            p = get_path(env=env, target=target, config=config)
            missing = [attr for attr in ("workspace_id", "house_id", "house_name", "root") if not getattr(p, attr, None)]
            if missing:
                results.append(ConfigSmokeCheckResult(f"path:{target}", "fail", f"Missing required fields: {missing}"))
            elif str(p.root).startswith("abfss://"):
                results.append(ConfigSmokeCheckResult(f"path:{target}", "pass", "Path is populated and ABFSS formatted."))
            else:
                results.append(ConfigSmokeCheckResult(f"path:{target}", "warn", "Path root is populated but not ABFSS-formatted."))
    except Exception as exc:
        results.append(ConfigSmokeCheckResult("path_resolution", "fail", str(exc)))

    if notebook_name:
        errors = validate_notebook_name(notebook_name, config=config)
        results.append(ConfigSmokeCheckResult("notebook_naming", "pass" if not errors else "fail", "; ".join(errors) or "Notebook name is valid."))
    else:
        results.append(ConfigSmokeCheckResult("notebook_naming", "skipped", "Notebook name check skipped."))

    if check_ai:
        ai_status = ai_result or check_fabric_ai_functions_available()
        results.append(ConfigSmokeCheckResult("fabric_ai", "pass" if ai_status.get("available") else "warn", ai_status.get("message", "")))
    else:
        results.append(ConfigSmokeCheckResult("fabric_ai", "skipped", "AI check disabled."))

    if check_io_import:
        try:
            from .fabric_io import lakehouse_table_read  # noqa: F401
            results.append(ConfigSmokeCheckResult("fabric_io_import", "pass", "fabric_io helpers are importable."))
        except Exception as exc:
            results.append(ConfigSmokeCheckResult("fabric_io_import", "fail", str(exc)))
    else:
        results.append(ConfigSmokeCheckResult("fabric_io_import", "skipped", "IO import check disabled."))
    return results


def bootstrap_fabric_env(
    env: str = "Sandbox",
    required_targets: list[str] | None = None,
    check_ai: bool = True,
    smoke_test: bool = True,
    config: FrameworkConfig | dict[str, Any] | None = None,
    notebook_name: str | None = None,
) -> ConfigBootstrapResult:
    """Bootstrap environment readiness for notebook execution."""
    normalized = load_fabric_config(config) if config is not None else None
    if normalized is None:
        raise ValueError("config is required for bootstrap_fabric_env.")
    required_targets = required_targets or ["Source", "Unified"]
    resolved_paths = {target: get_path(env=env, target=target, config=normalized) for target in required_targets}
    ai_result = check_fabric_ai_functions_available() if check_ai else {"available": None, "message": "AI check disabled."}
    smoke = run_config_smoke_tests(
        normalized,
        env=env,
        required_targets=required_targets,
        check_ai=check_ai,
        check_io_import=False,
        notebook_name=notebook_name,
        ai_result=ai_result,
    ) if smoke_test else []
    status = "ready" if all(r.status in {"pass", "skipped", "warn"} for r in smoke) else "not_ready"
    return ConfigBootstrapResult(
        environment=env,
        paths=resolved_paths,
        runtime_metadata={"notebook_name": notebook_name},
        ai_availability=ai_result,
        smoke_test_results=smoke,
        readiness_status=status,
    )


def check_fabric_ai_functions_available() -> dict[str, Any]:
    """Return Fabric AI availability from the config/readiness API surface."""
    from .ai import check_fabric_ai_functions_available as _check

    return _check()


def _default_schema_text() -> str:
    return (
        files("fabricops_kit.schemas")
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
    try:
        spark_obj = globals().get("spark")
        if spark_obj is not None:
            results.append(ConfigSmokeCheckResult("spark_session", "pass", "Spark session is available."))
        else:
            results.append(ConfigSmokeCheckResult("spark_session", "warn", "Spark session not found; local fallback mode."))
    except Exception as exc:
        results.append(ConfigSmokeCheckResult("spark_session", "warn", f"Spark check skipped: {exc}"))

    try:
        import notebookutils.runtime as nb_runtime  # type: ignore

        _ = getattr(nb_runtime, "context", None)
        results.append(ConfigSmokeCheckResult("fabric_runtime_context", "pass", "Fabric runtime context is readable."))
    except Exception:
        results.append(ConfigSmokeCheckResult("fabric_runtime_context", "skipped", "notebookutils.runtime unavailable outside Fabric runtime."))
