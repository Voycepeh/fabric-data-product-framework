"""Configuration bootstrap and contract validation for FabricOps notebook pipelines.

This module is the workflow entrypoint for establishing the ``00_env_config``
contract, standard environment path definitions, notebook prefix policies, AI
prompt templates, and smoke-check validation before data movement starts.
Use it early in a Fabric run so downstream IO, quality, lineage, and handover
steps execute with explicit, validated runtime context.
"""

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
    """Create environment-to-target routing used by Fabric IO helpers.

    Use this in the ``00_env_config`` bootstrap stage to define which
    workspace/lakehouse/warehouse targets are valid for each environment
    (for example, ``dev`` and ``prod``).

    Parameters
    ----------
    paths : dict[str, dict[str, Any]]
        Mapping of environment names to target mappings. Each target value is
        typically a ``Housepath``-compatible object used later by
        :func:`get_path` and read/write helpers.

    Returns
    -------
    PathConfig
        Immutable path configuration wrapper.

    Raises
    ------
    ValueError
        Raised when ``paths`` is empty or not a mapping.

    Examples
    --------
    >>> create_path_config({"dev": {"raw": object()}}).paths["dev"] is not None
    True
    """
    if not isinstance(paths, dict) or not paths:
        raise ValueError("paths must be a non-empty mapping of environments to targets.")
    return PathConfig(paths=paths)


def create_notebook_runtime_config(allowed_notebook_prefixes: list[str] | tuple[str, ...]) -> NotebookRuntimeConfig:
    """Create notebook naming-policy configuration for runtime guards.

    This is typically configured during ``00_env_config`` so notebook
    validation helpers can enforce a consistent execution contract.

    Parameters
    ----------
    allowed_notebook_prefixes : list[str] | tuple[str, ...]
        Prefixes accepted by notebook-name validation helpers.

    Returns
    -------
    NotebookRuntimeConfig
        Immutable runtime policy containing normalized prefixes.

    Raises
    ------
    ValueError
        Raised when no non-empty prefix remains after normalization.
    """
    prefixes = tuple(prefix.strip() for prefix in allowed_notebook_prefixes if str(prefix).strip())
    if not prefixes:
        raise ValueError("allowed_notebook_prefixes must contain at least one non-empty prefix.")
    return NotebookRuntimeConfig(allowed_notebook_prefixes=prefixes)


def create_ai_prompt_config(
    dq_rule_candidate_template: str,
    governance_candidate_template: str,
    handover_summary_template: str,
) -> AIPromptConfig:
    """Create the AI prompt-template configuration used by FabricOps.

    Use this in ``00_env_config`` to register the prompt templates that power
    AI-assisted DQ rule generation, governance suggestion generation, and
    handover summary drafting before downstream notebooks execute.

    Parameters
    ----------
    dq_rule_candidate_template : str
        Template used to ask Fabric AI for candidate DQ rules.
    governance_candidate_template : str
        Template used to ask Fabric AI for governance and classification suggestions.
    handover_summary_template : str
        Template used to ask Fabric AI for pipeline handover summaries.

    Returns
    -------
    AIPromptConfig
        Frozen configuration object containing the validated prompt templates.

    Raises
    ------
    ValueError
        Raised when any prompt template is empty or not a string.

    Examples
    --------
    >>> ai_prompts = create_ai_prompt_config(
    ...     dq_rule_candidate_template="Generate DQ checks for {table_name}",
    ...     governance_candidate_template="Suggest governance metadata for {dataset_name}",
    ...     handover_summary_template="Summarize lineage and handover notes for {pipeline_name}",
    ... )
    >>> ai_prompts.dq_rule_candidate_template
    'Generate DQ checks for {table_name}'
    """
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
    """Resolve a configured Fabric path for an environment and target.

    Parameters
    ----------
    env : str
        Environment key such as ``Sandbox``, ``DE``, or ``Prod``.
    target : str
        Target key such as ``Source``, ``Unified``, ``Product``, or ``Warehouse``.
    config : FrameworkConfig | PathConfig | None
        Configuration that contains environment-to-target path mappings.

    Returns
    -------
    Any
        Housepath-style object with ``workspace_id``, ``house_id``, ``house_name``, and ``root``.

    Raises
    ------
    ValueError
        If config is missing, or if the environment/target mapping does not exist.

    Examples
    --------
    >>> get_path("Sandbox", "Source", config=CONFIG)
    Housepath(...)
    """
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
    """Run 00_env_config readiness smoke checks for configuration bootstrap.

    Use this during environment bootstrap to verify Spark availability, Fabric
    runtime context access, required path mappings, notebook naming policy, and
    optional AI/IO import readiness before executing downstream notebook steps.

    Parameters
    ----------
    config : FrameworkConfig
        Validated framework configuration to evaluate.
    env : str, default="Sandbox"
        Environment key used when resolving required target paths.
    required_targets : list[str] | None, optional
        Required targets expected in ``config.path_config``. Defaults to
        ``["Source", "Unified"]`` when not provided.
    check_ai : bool, default=True
        Whether to run the Fabric AI availability check.
    check_io_import : bool, default=False
        Whether to test importability of ``fabric_io`` helpers.
    notebook_name : str | None, optional
        Notebook name to validate against configured naming prefixes.
    ai_result : dict[str, Any] | None, optional
        Optional precomputed AI availability payload to reuse instead of
        re-running the runtime import check.

    Returns
    -------
    list[ConfigSmokeCheckResult]
        Ordered check results with ``pass``, ``warn``, ``fail``, or ``skipped``
        statuses for each readiness dimension.

    Raises
    ------
    ValueError
        Propagated from config/path validation helpers when required targets or
        configured environments are invalid.

    Notes
    -----
    This helper performs validation and lightweight import/runtime checks only.
    It does not create or mutate Fabric resources.

    Examples
    --------
    >>> checks = run_config_smoke_tests(config=my_config, env="Sandbox", notebook_name="00_env_config")
    >>> any(c.status == "fail" for c in checks)
    False
    """
    from .runtime import validate_notebook_name

    results: list[ConfigSmokeCheckResult] = []
    required_targets = required_targets or ["Source", "Unified"]
    spark_ready, spark_message = _check_spark_session()
    results.append(ConfigSmokeCheckResult("spark_session", "pass" if spark_ready else "warn", spark_message))

    runtime_meta = _get_fabric_runtime_metadata(notebook_name=notebook_name)
    runtime_status = "pass" if runtime_meta.get("runtime_available") else "skipped"
    runtime_message = "Fabric runtime context is readable." if runtime_meta.get("runtime_available") else "notebookutils.runtime unavailable outside Fabric runtime."
    results.append(ConfigSmokeCheckResult("fabric_runtime_context", runtime_status, runtime_message))
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
    """Bootstrap 00_env_config environment readiness for FabricOps notebooks.

    This is a one-call bootstrap helper used at the start of a FabricOps run.
    It validates/loads configuration, resolves required environment targets,
    gathers runtime and AI availability metadata, and optionally executes smoke
    checks before quality/governance/lineage workflows continue.

    Parameters
    ----------
    env : str, default="Sandbox"
        Environment key to bootstrap from ``path_config``.
    required_targets : list[str] | None, optional
        Target names that must resolve for the selected environment. Defaults
        to ``["Source", "Unified"]``.
    check_ai : bool, default=True
        Whether to include Fabric AI availability checks.
    smoke_test : bool, default=True
        Whether to execute :func:`run_config_smoke_tests`.
    config : FrameworkConfig | dict[str, Any] | None, optional
        Framework configuration object or compatible mapping.
    notebook_name : str | None, optional
        Notebook name used in runtime metadata and naming checks.

    Returns
    -------
    ConfigBootstrapResult
        Structured bootstrap result containing resolved paths, runtime metadata,
        AI status, smoke-check results, and overall readiness status.

    Raises
    ------
    ValueError
        Raised when ``config`` is missing or fails configuration/path
        validation.

    Notes
    -----
    Side effects are limited to runtime/import checks. The helper does not
    create Fabric assets or write persistent state.

    Examples
    --------
    >>> result = bootstrap_fabric_env(config=my_config, env="Sandbox", notebook_name="00_env_config")
    >>> result.readiness_status in {"ready", "not_ready"}
    True
    """
    normalized = load_fabric_config(config) if config is not None else None
    if normalized is None:
        raise ValueError("config is required for bootstrap_fabric_env.")
    required_targets = required_targets or ["Source", "Unified"]
    resolved_paths = {target: get_path(env=env, target=target, config=normalized) for target in required_targets}
    ai_result = check_fabric_ai_functions_available() if check_ai else {"available": None, "message": "AI check disabled."}
    runtime_meta = _get_fabric_runtime_metadata(notebook_name=notebook_name)
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
        runtime_metadata=runtime_meta,
        ai_availability=ai_result,
        smoke_test_results=smoke,
        readiness_status=status,
    )


def check_fabric_ai_functions_available() -> dict[str, Any]:
    """Check whether Fabric AI Functions are available in the current runtime.

    Returns
    -------
    dict[str, Any]
        Diagnostic payload containing an ``available`` flag and a message.

    Notes
    -----
    This is a config-facing wrapper around the AI module so readiness checks are callable from ``config``.
    """
    from .ai import check_fabric_ai_functions_available as _check

    return _check()


def _check_spark_session() -> tuple[bool, str]:
    """Check whether a Spark session is available."""
    spark_obj = globals().get("spark")
    if spark_obj is not None:
        return True, "Spark session is available."
    return False, "Spark session not found; local fallback mode."


def _get_fabric_runtime_metadata(notebook_name: str | None = None) -> dict[str, Any]:
    """Best-effort retrieval of Fabric runtime metadata."""
    metadata: dict[str, Any] = {
        "notebook_name": notebook_name,
        "workspace_name": None,
        "user_name": None,
        "runtime_available": False,
    }
    try:
        import notebookutils.runtime as nb_runtime  # type: ignore

        metadata["runtime_available"] = True
        context = getattr(nb_runtime, "context", None)
        if context is not None:
            def _ctx_value(*keys: str) -> Any:
                for key in keys:
                    if hasattr(context, key):
                        value = getattr(context, key, None)
                        if value is not None:
                            return value
                    if isinstance(context, dict):
                        value = context.get(key)
                        if value is not None:
                            return value
                    get_method = getattr(context, "get", None)
                    if callable(get_method):
                        value = get_method(key)
                        if value is not None:
                            return value
                return None

            metadata["notebook_name"] = metadata["notebook_name"] or _ctx_value("currentNotebookName", "current_notebook_name")
            metadata["workspace_name"] = _ctx_value("currentWorkspaceName", "workspaceName", "workspace_name")
            metadata["user_name"] = _ctx_value("userName", "user_name")
    except Exception:
        pass
    return metadata


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
    """Load a dataset contract YAML file into a dictionary.

    Parameters
    ----------
    path : str or Path
        Path to a dataset-contract file, typically versioned beside pipeline
        notebooks or in a shared config folder.

    Returns
    -------
    dict
        Parsed contract content. Empty files return ``{}``; non-mapping YAML
        values are wrapped as ``{"value": <loaded_value>}`` for safer handling.

    Examples
    --------
    >>> contract = load_dataset_contract("configs/sales_contract.yml")
    >>> isinstance(contract, dict)
    True
    """
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
    """Validate a loaded dataset contract against the JSON schema.

    Parameters
    ----------
    contract : dict
        Dataset contract content produced by :func:`load_dataset_contract`.
    schema_path : str or Path or None, default=None
        Optional custom schema location. When omitted, the packaged FabricOps
        dataset-contract schema is used.

    Returns
    -------
    list of str
        Validation error messages using normalized property paths that are
        suitable for notebook run summaries and handover logs.

    Notes
    -----
    This function does not raise by default, allowing notebook orchestration to
    collect all schema issues before deciding whether to fail fast.
    """
    schema = _load_schema(schema_path=schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(contract), key=lambda error: (list(error.path), error.message))
    return [f"{_format_error_path(list(error.path), error.message, error.validator)}: {error.message}" for error in errors]

def assert_valid_dataset_contract(contract: dict, schema_path: str | Path | None = None) -> None:
    """Raise when a dataset contract violates the expected schema.

    Parameters
    ----------
    contract : dict
        Contract content to validate before executing ingestion, quality, and
        metadata stages.
    schema_path : str or Path or None, default=None
        Optional custom schema location. The built-in schema is used when this
        value is ``None``.

    Raises
    ------
    DatasetContractValidationError
        Raised when one or more validation issues are found.
    """
    errors = validate_dataset_contract(contract, schema_path=schema_path)
    if errors:
        raise DatasetContractValidationError("Dataset contract validation failed:\n" + "\n".join(f"- {e}" for e in errors))

def load_and_validate_dataset_contract(path: str | Path, schema_path: str | Path | None = None) -> tuple[dict, list[str]]:
    """Load a dataset contract file and return schema validation findings.

    Parameters
    ----------
    path : str or Path
        Contract YAML path used by a Fabric notebook or pipeline run.
    schema_path : str or Path or None, default=None
        Optional schema override for custom contract extensions.

    Returns
    -------
    tuple of (dict, list of str)
        Loaded contract payload and a list of validation errors.

    Examples
    --------
    >>> contract, errors = load_and_validate_dataset_contract("configs/orders.yml")
    >>> len(errors) >= 0
    True
    """
    contract = load_dataset_contract(path)
    return contract, validate_dataset_contract(contract, schema_path=schema_path)
