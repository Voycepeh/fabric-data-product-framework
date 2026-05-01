"""Contract-first orchestration API for running a framework data product."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from fabric_data_product_framework.config import load_dataset_contract
from fabric_data_product_framework.contracts import build_contract_validation_records, validate_runtime_contracts
from fabric_data_product_framework.drift_checkers import (
    build_and_write_partition_snapshot,
    build_and_write_schema_snapshot,
    check_partition_drift,
    check_schema_drift,
    load_latest_partition_snapshot,
    load_latest_schema_snapshot,
    summarize_drift_results,
)
from fabric_data_product_framework.lineage import build_lineage_records
from fabric_data_product_framework.metadata import build_dataset_run_record, write_metadata_records
from fabric_data_product_framework.profiling import default_technical_columns, flatten_profile_for_metadata, profile_dataframe
from fabric_data_product_framework.dq import run_dq_workflow
from fabric_data_product_framework.governance_classifier import (
    build_governance_classification_records,
    classify_columns,
    summarize_governance_classifications,
    write_governance_classifications,
)
from fabric_data_product_framework.quality import build_quality_result_records
from fabric_data_product_framework.quarantine import split_valid_and_quarantine
from fabric_data_product_framework.run_summary import build_run_summary, build_run_summary_record
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.technical_columns import add_standard_technical_columns

_ALLOWED_REFRESH_MODES = {"full", "incremental", "snapshot", "append"}


@dataclass
class SourceContract:
    """Sourcecontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> SourceContract(...)
    """
    """Source-side contract settings for ingestion and validation."""
    name: str | None = None
    type: str = "table"
    table: str | None = None
    path: str | None = None
    format: str = "delta"
    required_columns: list[str] = field(default_factory=list)
    business_keys: list[str] = field(default_factory=list)
    watermark_column: str | None = None
    partition_column: str | None = None
    read_options: dict[str, Any] = field(default_factory=dict)


@dataclass
class TargetContract:
    """Targetcontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> TargetContract(...)
    """
    """Target write contract settings for curated outputs."""
    table: str | None = None
    path: str | None = None
    format: str = "delta"
    mode: str = "append"
    partition_column: str | None = None
    required_columns: list[str] = field(default_factory=list)
    write_options: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityContract:
    """Qualitycontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> QualityContract(...)
    """
    """Quality workflow configuration including rule-store and gating behavior."""
    rules: list[dict[str, Any]] = field(default_factory=list)
    rule_store_table: str | None = None
    use_rule_store: bool = False
    rule_status: str = "approved"
    generate_candidates: bool = False
    candidate_generation_method: str = "profile"
    fail_on: str = "critical"
    quarantine_enabled: bool = True
    quarantine_table: str | None = None


@dataclass
class DriftContract:
    """Driftcontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> DriftContract(...)
    """
    """Schema/data drift policy and baseline table references."""
    schema_enabled: bool = True
    data_enabled: bool = False
    schema_policy: dict[str, Any] = field(default_factory=dict)
    data_policy: dict[str, Any] = field(default_factory=dict)
    baseline_schema_table: str | None = None
    baseline_partition_table: str | None = None


@dataclass
class GovernanceContract:
    """Governancecontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> GovernanceContract(...)
    """
    """Governance classification policy for sensitive columns and review."""
    classify_columns: bool = False
    classification_table: str | None = None
    require_human_approval: bool = True
    rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MetadataContract:
    """Metadatacontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> MetadataContract(...)
    """
    """Metadata table destinations used across the pipeline lifecycle."""
    schema: str = "fw_metadata"
    source_profile_table: str | None = None
    output_profile_table: str | None = None
    schema_snapshot_table: str | None = None
    partition_snapshot_table: str | None = None
    quality_result_table: str | None = None
    quarantine_table: str | None = None
    contract_validation_table: str | None = None
    lineage_table: str | None = None
    run_summary_table: str | None = None
    dataset_runs_table: str | None = None
    ai_context_table: str | None = None


@dataclass
class RuntimeContract:
    """Runtimecontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> RuntimeContract(...)
    """
    """Runtime context defaults such as dataset, environment, and naming."""
    dataset_name: str = ""
    environment: str = "fabric"
    notebook_name: str | None = None
    run_id_prefix: str | None = None
    pipeline_name: str | None = None
    source_system: str | None = None


@dataclass
class DataProductContract:
    """Dataproductcontract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    None
    This callable does not require public parameters.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> DataProductContract(...)
    """
    """Top-level contract model used by ``run_data_product`` orchestration."""
    dataset: dict[str, Any] = field(default_factory=dict)
    source: SourceContract = field(default_factory=SourceContract)
    target: TargetContract = field(default_factory=TargetContract)
    quality: QualityContract = field(default_factory=QualityContract)
    drift: DriftContract = field(default_factory=DriftContract)
    governance: GovernanceContract = field(default_factory=GovernanceContract)
    metadata: MetadataContract = field(default_factory=MetadataContract)
    runtime: RuntimeContract = field(default_factory=RuntimeContract)
    raw: dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Any:
        return _effective_contract_dict(self)[key]


def _dict(config: dict | None) -> dict:
    """Return a dictionary or an empty default for optional config fragments."""
    return config if isinstance(config, dict) else {}


def build_source_contract(config: dict) -> SourceContract:
    """Build source contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    config : Any
    Description of `config`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_source_contract(...)
    """
    c = _dict(config)
    return SourceContract(
        name=c.get("name"),
        type=str(c.get("type") or "table"),
        table=c.get("table"),
        path=c.get("path"),
        format=str(c.get("format") or "delta"),
        required_columns=list(c.get("required_columns") or []),
        business_keys=list(c.get("business_keys") or []),
        watermark_column=c.get("watermark_column"),
        partition_column=c.get("partition_column"),
        read_options=dict(c.get("read_options") or {}),
    )


def build_target_contract(config: dict) -> TargetContract:
    """Build target contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    config : Any
    Description of `config`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_target_contract(...)
    """
    c = _dict(config)
    return TargetContract(
        table=c.get("table"),
        path=c.get("path"),
        format=str(c.get("format") or "delta"),
        mode=str(c.get("mode") or "append"),
        partition_column=c.get("partition_column"),
        required_columns=list(c.get("required_columns") or []),
        write_options=dict(c.get("write_options") or {}),
    )


def build_quality_contract(config: dict) -> QualityContract:
    """Build quality contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    config : Any
    Description of `config`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_quality_contract(...)
    """
    c = _dict(config)
    return QualityContract(
        rules=list(c.get("rules") or []),
        rule_store_table=c.get("rule_store_table"),
        use_rule_store=bool(c.get("use_rule_store", False)),
        rule_status=str(c.get("rule_status") or "approved"),
        generate_candidates=bool(c.get("generate_candidates", False)),
        candidate_generation_method=str(c.get("candidate_generation_method") or "profile"),
        fail_on=str(c.get("fail_on") or "critical"),
        quarantine_enabled=bool(c.get("quarantine_enabled", True)),
        quarantine_table=c.get("quarantine_table"),
    )


def build_drift_contract(config: dict) -> DriftContract:
    """Build drift contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    config : Any
    Description of `config`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_drift_contract(...)
    """
    c = _dict(config)
    return DriftContract(
        schema_enabled=bool(c.get("schema_enabled", True)),
        data_enabled=bool(c.get("data_enabled", False)),
        schema_policy=dict(c.get("schema_policy") or {}),
        data_policy=dict(c.get("data_policy") or {}),
        baseline_schema_table=c.get("baseline_schema_table"),
        baseline_partition_table=c.get("baseline_partition_table"),
    )


def build_governance_contract(config: dict) -> GovernanceContract:
    """Build governance contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    config : Any
    Description of `config`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_governance_contract(...)
    """
    c = _dict(config)
    return GovernanceContract(
        classify_columns=bool(c.get("classify_columns", False)),
        classification_table=c.get("classification_table"),
        require_human_approval=bool(c.get("require_human_approval", True)),
        rules=list(c.get("rules") or []),
    )


def build_metadata_contract(config: dict) -> MetadataContract:
    """Build metadata contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    config : Any
    Description of `config`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_metadata_contract(...)
    """
    c = _dict(config)
    return MetadataContract(
        schema=str(c.get("schema") or "fw_metadata"),
        source_profile_table=c.get("source_profile_table"),
        output_profile_table=c.get("output_profile_table"),
        schema_snapshot_table=c.get("schema_snapshot_table"),
        partition_snapshot_table=c.get("partition_snapshot_table"),
        quality_result_table=c.get("quality_result_table"),
        quarantine_table=c.get("quarantine_table"),
        contract_validation_table=c.get("contract_validation_table"),
        lineage_table=c.get("lineage_table"),
        run_summary_table=c.get("run_summary_table"),
        dataset_runs_table=c.get("dataset_runs_table"),
        ai_context_table=c.get("ai_context_table"),
    )


def build_runtime_contract(config: dict) -> RuntimeContract:
    """Build runtime contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    config : Any
    Description of `config`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_runtime_contract(...)
    """
    c = _dict(config)
    return RuntimeContract(
        dataset_name=str(c.get("dataset_name") or ""),
        environment=str(c.get("environment") or "fabric"),
        notebook_name=c.get("notebook_name"),
        run_id_prefix=c.get("run_id_prefix"),
        pipeline_name=c.get("pipeline_name"),
        source_system=c.get("source_system"),
    )


def normalize_data_product_contract(contract: dict | DataProductContract) -> DataProductContract:
    """Normalize data product contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    contract : Any
    Description of `contract`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> normalize_data_product_contract(...)
    """
    if isinstance(contract, DataProductContract):
        return contract
    raw = dict(contract)
    dataset = dict(raw.get("dataset") or {})
    upstream = _dict(raw.get("upstream_contract"))
    downstream = _dict(raw.get("downstream_contract"))

    source_cfg = dict(raw.get("source") or {})
    source_cfg.setdefault("table", upstream.get("table_name"))
    source_cfg.setdefault("required_columns", upstream.get("required_columns", (raw.get("schema") or {}).get("required_source_columns", [])))
    source_cfg.setdefault("business_keys", upstream.get("business_keys", (raw.get("keys") or {}).get("business_keys", [])))
    source_cfg.setdefault("watermark_column", upstream.get("watermark_column", (raw.get("keys") or {}).get("watermark_column")))
    source_cfg.setdefault("partition_column", (raw.get("keys") or {}).get("partition_column"))

    target_cfg = dict(raw.get("target") or {})
    target_cfg.setdefault("table", downstream.get("table_name"))
    target_cfg.setdefault("required_columns", downstream.get("required_columns", (raw.get("schema") or {}).get("required_output_columns", [])))

    metadata_cfg = dict(raw.get("metadata") or {})
    metadata_cfg.setdefault("schema", raw.get("metadata_schema") or (raw.get("environment") or {}).get("metadata_schema") or "fw_metadata")

    quality_cfg = dict(raw.get("quality") or {})
    quality_cfg.setdefault("quarantine_table", metadata_cfg.get("quarantine_table"))

    drift_raw = dict(raw.get("drift") or {})
    drift_cfg = {
        "schema_enabled": drift_raw.get("schema_enabled", True),
        "data_enabled": drift_raw.get("data_enabled", False),
        "schema_policy": drift_raw.get("schema_policy", {}),
        "data_policy": drift_raw.get("data_policy", drift_raw.get("incremental_policy", {})),
        "baseline_schema_table": drift_raw.get("baseline_schema_table"),
        "baseline_partition_table": drift_raw.get("baseline_partition_table"),
    }

    runtime_cfg = dict(raw.get("runtime") or {})
    runtime_cfg.setdefault("dataset_name", dataset.get("name", ""))
    runtime_cfg.setdefault("environment", runtime_cfg.get("environment") or (raw.get("environment") or {}).get("name") or "fabric")

    return DataProductContract(
        dataset=dataset,
        source=build_source_contract(source_cfg),
        target=build_target_contract(target_cfg),
        quality=build_quality_contract(quality_cfg),
        drift=build_drift_contract(drift_cfg),
        governance=build_governance_contract(raw.get("governance") or {}),
        metadata=build_metadata_contract(metadata_cfg),
        runtime=build_runtime_contract(runtime_cfg),
        raw=raw,
    )


def data_product_contract_to_dict(contract: DataProductContract) -> dict:
    """Data product contract to dict.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    contract : Any
    Description of `contract`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> data_product_contract_to_dict(...)
    """
    return asdict(contract)


def _effective_contract_dict(contract: dict | DataProductContract) -> dict:
    n = normalize_data_product_contract(contract)
    raw = dict(n.raw) if n.raw else {}
    effective = {
        "dataset": dict(n.dataset),
        "source": asdict(n.source),
        "target": asdict(n.target),
        "quality": asdict(n.quality),
        "drift": asdict(n.drift),
        "governance": asdict(n.governance),
        "metadata": asdict(n.metadata),
        "runtime": asdict(n.runtime),
        "refresh": dict(raw.get("refresh") or {}),
    }
    effective["environment"] = dict(raw.get("environment") or {"name": n.runtime.environment, "metadata_schema": n.metadata.schema})
    effective["keys"] = {
        "business_keys": list(n.source.business_keys),
        "watermark_column": n.source.watermark_column,
        "partition_column": n.source.partition_column,
    }
    effective["schema"] = {
        "required_source_columns": list(n.source.required_columns),
        "required_output_columns": list(n.target.required_columns),
    }
    return effective


def load_data_contract(path_or_dict: str | Path | dict) -> DataProductContract:
    """Load data contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    path_or_dict : Any
    Description of `path_or_dict`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> load_data_contract(...)
    """
    raw = dict(path_or_dict) if isinstance(path_or_dict, dict) else load_dataset_contract(path_or_dict)
    return normalize_data_product_contract(raw)


def _refresh_mode(contract: dict) -> str:
    return str((contract.get("refresh") or {}).get("mode") or "full").strip().lower()


def validate_data_contract_shape(contract: dict | DataProductContract) -> list[str]:
    """Validate data contract shape.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    contract : Any
    Description of `contract`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> validate_data_contract_shape(...)
    """
    n = normalize_data_product_contract(contract)
    raw = _effective_contract_dict(n)
    errors: list[str] = []
    if not n.dataset.get("name"):
        errors.append("Missing required key: dataset.name")
    if not n.source.table:
        errors.append("Missing required key: source.table")
    if not n.target.table:
        errors.append("Missing required key: target.table")
    required_metadata = ["source_profile_table", "output_profile_table", "schema_snapshot_table", "partition_snapshot_table", "quality_result_table", "quarantine_table", "contract_validation_table", "lineage_table", "run_summary_table", "dataset_runs_table"]
    md = asdict(n.metadata)
    for k in required_metadata:
        if not md.get(k):
            errors.append(f"Missing required key: metadata.{k}")

    mode = _refresh_mode(raw)
    if mode not in _ALLOWED_REFRESH_MODES:
        errors.append("Invalid refresh.mode. Expected one of: full, incremental, snapshot, append")
    if mode == "incremental":
        if not n.source.partition_column:
            errors.append("Missing required key for incremental mode: source.partition_column")
        if not n.source.business_keys:
            errors.append("Incremental mode requires non-empty source.business_keys")
    return errors


def build_runtime_context_from_contract(contract: dict | DataProductContract, overrides: dict | None = None) -> dict:
    """Build runtime context from contract.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    contract : Any
    Description of `contract`.
    overrides : Any
    Description of `overrides`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> build_runtime_context_from_contract(...)
    """
    n = normalize_data_product_contract(contract)
    context = build_runtime_context(dataset_name=n.dataset.get("name", ""), environment=n.runtime.environment, source_table=n.source.table or "", target_table=n.target.table or "", notebook_name=n.runtime.notebook_name, run_id=(overrides or {}).get("run_id"))
    if overrides:
        context.update(overrides)
    return context

# rest unchanged helpers

def _write_records_spark(spark, records: list[dict], table: str, mode: str = "append") -> None:
    if records:
        write_metadata_records(records, table, writer=lambda rows, t, mode="append", **_: spark.createDataFrame(rows).write.mode(mode).saveAsTable(t), mode=mode)


def _write_dataframe_to_table(spark, df, table: str, mode: str = "append") -> None:
    if hasattr(df, "write"):
        df.write.mode(mode).saveAsTable(table)
    else:
        spark.createDataFrame(df.to_dict(orient="records")).write.mode(mode).saveAsTable(table)


def _runtime_validation_contract(contract: dict | DataProductContract) -> dict:
    n = normalize_data_product_contract(contract)
    effective = _effective_contract_dict(n)
    effective["contracts"] = {"upstream": {"expected_columns": n.source.required_columns}, "downstream": {"guaranteed_columns": n.target.required_columns}}
    effective["refresh"] = effective.get("refresh") or {"watermark_column": n.source.watermark_column}
    return effective


def run_data_product(spark, contract: dict | DataProductContract, transform=None, source_df=None, write: bool | None = None, *, write_target: bool = True, write_metadata: bool = True) -> dict:
    """Run data product.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    spark : Any
    Description of `spark`.
    contract : Any
    Description of `contract`.
    transform : Any
    Description of `transform`.
    source_df : Any
    Description of `source_df`.
    write : Any
    Description of `write`.
    write_target : Any
    Description of `write_target`.
    write_metadata : Any
    Description of `write_metadata`.

    Returns
    -------
    result : Any
    Returned value.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> run_data_product(...)
    """
    n = normalize_data_product_contract(contract)
    if write is False:
        write_target = False
        write_metadata = False
    elif write is True:
        write_target = True

    shape_errors = validate_data_contract_shape(n)
    if shape_errors:
        return {"status": "failed", "can_continue": False, "errors": shape_errors}

    ctx = build_runtime_context_from_contract(n)
    dataset_name, source_table, target_table, metadata = n.dataset["name"], n.source.table, n.target.table, n.metadata
    effective_contract = _effective_contract_dict(n)
    mode = _refresh_mode(effective_contract)
    src_df = source_df if source_df is not None else spark.table(source_table)
    md = asdict(metadata)
    if mode == "incremental" and n.source.partition_column and n.source.partition_column not in getattr(src_df, "columns", []):
        return {"status": "failed", "can_continue": False, "errors": [f"Incremental partition column missing in source dataframe: {n.source.partition_column}"], "runtime_context": ctx}

    source_profile = profile_dataframe(src_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(source_profile, source_table, ctx["run_id"], "source"), md["source_profile_table"])
    schema_drift_result = {"status": "disabled", "can_continue": True}
    schema_snapshot_write = None
    schema_baseline_table = n.drift.baseline_schema_table or md.get("schema_snapshot_table")
    if n.drift.schema_enabled:
        baseline = load_latest_schema_snapshot(spark, schema_baseline_table, dataset_name=dataset_name, table_name=source_table) if schema_baseline_table else None
        schema_drift_result = check_schema_drift(
            df=src_df,
            dataset_name=dataset_name,
            table_name=source_table,
            baseline_snapshot=baseline,
            policy=n.drift.schema_policy,
            engine="auto",
        )
        if write_metadata and md.get("schema_snapshot_table"):
            schema_snapshot_write = build_and_write_schema_snapshot(
                spark=spark, df=src_df, dataset_name=dataset_name, table_name=source_table, metadata_table=md["schema_snapshot_table"], run_id=ctx["run_id"], engine="auto"
            )

    out_df = transform(src_df, ctx, effective_contract) if transform else src_df
    out_df = add_standard_technical_columns(out_df, run_id=ctx["run_id"], pipeline_name=dataset_name, environment=ctx["environment"], source_table=source_table, watermark_column=(n.source.watermark_column if n.source.watermark_column in getattr(out_df, "columns", []) else None), business_keys=n.source.business_keys)

    output_profile = profile_dataframe(out_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(output_profile, target_table, ctx["run_id"], "output", exclude_columns=default_technical_columns()), md["output_profile_table"])

    partition_column = n.drift.data_policy.get("partition_column") or n.source.partition_column
    business_keys = list(n.drift.data_policy.get("business_keys") or n.source.business_keys)
    watermark_column = n.drift.data_policy.get("watermark_column") or n.source.watermark_column
    data_drift_result = {"status": "disabled", "can_continue": True}
    partition_snapshot_write = None
    if n.drift.data_enabled:
        if not partition_column or not business_keys:
            data_drift_result = {"status": "skipped", "can_continue": True, "message": "Data drift skipped due to missing partition_column or business_keys configuration."}
        else:
            out_cols_raw = getattr(out_df, "columns", None)
            out_columns = set(list(out_cols_raw) if out_cols_raw is not None else [])
            missing_cols = [partition_column] + list(business_keys)
            if watermark_column:
                missing_cols.append(watermark_column)
            missing_cols = [c for c in missing_cols if c and c not in out_columns]
            if missing_cols:
                return {
                    "status": "failed",
                    "can_continue": False,
                    "errors": [f"Data drift configuration columns missing in output dataframe: {', '.join(sorted(set(missing_cols)))}"],
                    "runtime_context": ctx,
                }
            baseline_partition_table = n.drift.baseline_partition_table or md.get("partition_snapshot_table")
            partition_baseline = load_latest_partition_snapshot(spark, baseline_partition_table, dataset_name=dataset_name, table_name=target_table) if baseline_partition_table else None
            data_drift_result = check_partition_drift(
                df=out_df, dataset_name=dataset_name, table_name=target_table, partition_column=partition_column, business_keys=business_keys, watermark_column=watermark_column, baseline_snapshot=partition_baseline, policy=n.drift.data_policy, run_id=ctx["run_id"], engine="auto"
            )
            if write_metadata and md.get("partition_snapshot_table"):
                partition_snapshot_write = build_and_write_partition_snapshot(
                    spark=spark, df=out_df, dataset_name=dataset_name, table_name=target_table, metadata_table=md["partition_snapshot_table"], partition_column=partition_column, business_keys=business_keys, watermark_column=watermark_column, run_id=ctx["run_id"], engine="auto"
                )

    dq_workflow = run_dq_workflow(
        spark=spark,
        df=out_df,
        quality_contract=n.quality,
        dataset_name=dataset_name,
        table_name=target_table,
        run_id=ctx["run_id"],
        profile=output_profile,
        metadata=None,
        business_context=None,
        engine="auto",
    )
    rules = dq_workflow["rules"]
    quality_result = dq_workflow["quality_result"]
    if write_metadata:
        _write_records_spark(spark, build_quality_result_records(quality_result, run_id=ctx["run_id"]), md["quality_result_table"])

    enforceable_rules = bool(rules)
    quarantine = {"enabled": bool(n.quality.quarantine_enabled), "written": False}
    valid_df, quarantine_df = out_df, None
    quarantine_row_count = 0
    valid_row_count = output_profile.get("row_count")
    if n.quality.quarantine_enabled and enforceable_rules:
        valid_df, quarantine_df = split_valid_and_quarantine(out_df, rules=rules, engine="auto")
        valid_row_count = len(valid_df) if hasattr(valid_df, "__len__") else int(valid_df.count())
        quarantine_row_count = len(quarantine_df) if hasattr(quarantine_df, "__len__") else int(quarantine_df.count())
        quarantine["row_count"] = quarantine_row_count
        if write_target and write_metadata and md.get("quarantine_table") and quarantine_row_count > 0:
            _write_dataframe_to_table(spark, quarantine_df, md["quarantine_table"], mode="append")
            quarantine["written"] = True

    governance = {"classifications": [], "records": [], "summary": {}, "metadata_table": n.governance.classification_table, "written": False}
    if n.governance.classify_columns:
        classifications = classify_columns(
            profile=output_profile,
            business_context={"dataset_name": dataset_name, "table_name": target_table},
            rules=n.governance.rules,
            dataset_name=dataset_name,
            table_name=target_table,
            run_id=ctx["run_id"],
        )
        gov_records = build_governance_classification_records(classifications, dataset_name=dataset_name, table_name=target_table, run_id=ctx["run_id"])
        written = False
        if write_metadata and n.governance.classification_table:
            write_governance_classifications(spark, classifications=classifications, table_name=n.governance.classification_table, dataset_name=dataset_name, source_table=target_table, run_id=ctx["run_id"])
            written = True
        governance = {"classifications": classifications, "records": gov_records, "summary": summarize_governance_classifications(classifications), "metadata_table": n.governance.classification_table, "written": written}

    contract_result = validate_runtime_contracts(source_df=src_df, output_df=valid_df, contract=_runtime_validation_contract(n), engine="auto")
    if write_metadata:
        _write_records_spark(spark, build_contract_validation_records(contract_result, run_id=ctx["run_id"]), md["contract_validation_table"])

    lineage_rows = build_lineage_records(run_id=ctx["run_id"], dataset_name=dataset_name, source_tables=[source_table], target_table=target_table, transformation_steps=[])
    if write_metadata and md.get("lineage_table"):
        _write_records_spark(spark, lineage_rows, md["lineage_table"])

    run_summary = build_run_summary(runtime_context=ctx, contract=effective_contract, source_profile=source_profile, output_profile=output_profile, quality_result=quality_result, contract_validation_result=contract_result)
    if write_metadata:
        _write_records_spark(spark, [build_run_summary_record(run_summary)], md["run_summary_table"])

    drift_summary = summarize_drift_results(schema_drift_result=schema_drift_result, partition_drift_result=data_drift_result, profile_drift_result=None)
    can_continue = (
        bool(quality_result.get("can_continue", True))
        and bool(contract_result.get("can_continue", True))
        and bool(schema_drift_result.get("can_continue", True))
        and bool(data_drift_result.get("can_continue", True))
    )
    status = "passed" if can_continue else "failed"
    if write_target and can_continue:
        _write_dataframe_to_table(spark, valid_df, target_table, mode=n.target.mode)

    dataset_run = build_dataset_run_record(run_id=ctx["run_id"], dataset_name=dataset_name, environment=ctx["environment"], source_table=source_table, target_table=target_table, status=status, started_at_utc=ctx.get("started_at_utc"), row_count_source=source_profile.get("row_count"), row_count_output=output_profile.get("row_count"))
    if write_metadata:
        _write_records_spark(spark, [dataset_run], md["dataset_runs_table"])

    return {
        "status": status, "can_continue": can_continue, "runtime_context": ctx, "contract": effective_contract,
        "source_profile": source_profile, "output_profile": output_profile,
        "drift": {"schema": schema_drift_result, "data": data_drift_result, "profile": None, "summary": drift_summary, "schema_snapshot_write": schema_snapshot_write, "partition_snapshot_write": partition_snapshot_write},
        "dq_workflow": dq_workflow, "quality_result": quality_result, "quarantine": quarantine, "valid_row_count": valid_row_count, "quarantine_row_count": quarantine_row_count,
        "governance": governance, "contract_validation_result": contract_result, "lineage": lineage_rows, "run_summary": run_summary,
        "target_table": target_table, "written": bool(write_target and can_continue), "dataset_run_record": dataset_run,
        "lineage_records": lineage_rows, "dataset_run": dataset_run, "quarantine_written": quarantine.get("written", False),
    }


def assert_data_product_passed(result: dict) -> None:
    """Assert data product passed.

    Documentation for API-reference generation in NumPy style.

    Parameters
    ----------
    result : Any
    Description of `result`.

    Returns
    -------
    None
    This method updates state in place.

    Notes
    -----
    Fabric notebook runtime may be required for Spark-based paths. Local Python execution is supported for pure-Python paths.

    Examples
    --------
    >>> assert_data_product_passed(...)
    """
    if result.get("status") != "passed":
        raise RuntimeError("Data product run failed contract/quality gates")
