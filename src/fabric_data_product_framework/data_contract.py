"""Contract-first orchestration API for running a framework data product."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from fabric_data_product_framework.config import load_dataset_contract
from fabric_data_product_framework.contracts import build_contract_validation_records, validate_runtime_contracts
from fabric_data_product_framework.drift import build_schema_snapshot
from fabric_data_product_framework.incremental import build_partition_snapshot
from fabric_data_product_framework.lineage import build_lineage_records
from fabric_data_product_framework.metadata import build_dataset_run_record, build_schema_snapshot_records, write_metadata_records
from fabric_data_product_framework.profiling import default_technical_columns, flatten_profile_for_metadata, profile_dataframe
from fabric_data_product_framework.quality import build_quality_result_records, run_quality_rules
from fabric_data_product_framework.quarantine import split_valid_and_quarantine
from fabric_data_product_framework.run_summary import build_run_summary, build_run_summary_record
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.technical_columns import add_standard_technical_columns

_ALLOWED_REFRESH_MODES = {"full", "incremental", "snapshot", "append"}


@dataclass
class SourceContract:
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
    table: str | None = None
    path: str | None = None
    format: str = "delta"
    mode: str = "append"
    partition_column: str | None = None
    write_options: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityContract:
    rules: list[dict[str, Any]] = field(default_factory=list)
    rule_store_table: str | None = None
    use_rule_store: bool = False
    rule_status: str = "approved"
    generate_candidates: bool = False
    fail_on: str = "critical"
    quarantine_enabled: bool = True
    quarantine_table: str | None = None


@dataclass
class DriftContract:
    schema_enabled: bool = True
    data_enabled: bool = False
    schema_policy: dict[str, Any] = field(default_factory=dict)
    data_policy: dict[str, Any] = field(default_factory=dict)
    baseline_schema_table: str | None = None
    baseline_partition_table: str | None = None


@dataclass
class GovernanceContract:
    classify_columns: bool = False
    classification_table: str | None = None
    require_human_approval: bool = True
    rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MetadataContract:
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
    dataset_name: str = ""
    environment: str = "fabric"
    notebook_name: str | None = None
    run_id_prefix: str | None = None
    pipeline_name: str | None = None
    source_system: str | None = None


@dataclass
class DataProductContract:
    dataset: dict[str, Any] = field(default_factory=dict)
    source: SourceContract = field(default_factory=SourceContract)
    target: TargetContract = field(default_factory=TargetContract)
    quality: QualityContract = field(default_factory=QualityContract)
    drift: DriftContract = field(default_factory=DriftContract)
    governance: GovernanceContract = field(default_factory=GovernanceContract)
    metadata: MetadataContract = field(default_factory=MetadataContract)
    runtime: RuntimeContract = field(default_factory=RuntimeContract)
    raw: dict[str, Any] = field(default_factory=dict)


def _dict(config: dict | None) -> dict:
    return config if isinstance(config, dict) else {}


def build_source_contract(config: dict) -> SourceContract:
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
    c = _dict(config)
    return TargetContract(
        table=c.get("table"),
        path=c.get("path"),
        format=str(c.get("format") or "delta"),
        mode=str(c.get("mode") or "append"),
        partition_column=c.get("partition_column"),
        write_options=dict(c.get("write_options") or {}),
    )


def build_quality_contract(config: dict) -> QualityContract:
    c = _dict(config)
    return QualityContract(
        rules=list(c.get("rules") or []),
        rule_store_table=c.get("rule_store_table"),
        use_rule_store=bool(c.get("use_rule_store", False)),
        rule_status=str(c.get("rule_status") or "approved"),
        generate_candidates=bool(c.get("generate_candidates", False)),
        fail_on=str(c.get("fail_on") or "critical"),
        quarantine_enabled=bool(c.get("quarantine_enabled", True)),
        quarantine_table=c.get("quarantine_table"),
    )


def build_drift_contract(config: dict) -> DriftContract:
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
    c = _dict(config)
    return GovernanceContract(
        classify_columns=bool(c.get("classify_columns", False)),
        classification_table=c.get("classification_table"),
        require_human_approval=bool(c.get("require_human_approval", True)),
        rules=list(c.get("rules") or []),
    )


def build_metadata_contract(config: dict) -> MetadataContract:
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
    return asdict(contract)


def load_data_contract(path_or_dict: str | Path | dict) -> DataProductContract:
    raw = dict(path_or_dict) if isinstance(path_or_dict, dict) else load_dataset_contract(path_or_dict)
    return normalize_data_product_contract(raw)


def _refresh_mode(contract: dict) -> str:
    return str((contract.get("refresh") or {}).get("mode") or "full").strip().lower()


def validate_data_contract_shape(contract: dict | DataProductContract) -> list[str]:
    n = normalize_data_product_contract(contract)
    raw = n.raw
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
            errors.append("Missing required key for incremental mode: keys.partition_column")
        if not n.source.business_keys:
            errors.append("Incremental mode requires non-empty keys.business_keys")
    return errors


def build_runtime_context_from_contract(contract: dict | DataProductContract, overrides: dict | None = None) -> dict:
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
    raw = dict(n.raw)
    raw["contracts"] = raw.get("contracts") or {"upstream": {"expected_columns": n.source.required_columns}, "downstream": {"guaranteed_columns": (raw.get("downstream_contract") or {}).get("required_columns", (raw.get("schema") or {}).get("required_output_columns", []))}}
    raw["refresh"] = raw.get("refresh") or {"watermark_column": n.source.watermark_column}
    return raw


def run_data_product(spark, contract: dict | DataProductContract, transform=None, source_df=None, write: bool | None = None, *, write_target: bool = True, write_metadata: bool = True) -> dict:
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
    mode = _refresh_mode(n.raw)
    src_df = source_df if source_df is not None else spark.table(source_table)
    md = asdict(metadata)

    source_profile = profile_dataframe(src_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(source_profile, source_table, ctx["run_id"], "source"), md["source_profile_table"])
    source_schema_snapshot = build_schema_snapshot(src_df, dataset_name=dataset_name, table_name=source_table)
    if write_metadata:
        _write_records_spark(spark, build_schema_snapshot_records(source_schema_snapshot, run_id=ctx["run_id"], table_stage="source"), md["schema_snapshot_table"])

    partition_snapshot = None
    if mode == "incremental":
        try:
            partition_snapshot = build_partition_snapshot(src_df, dataset_name=dataset_name, table_name=source_table, partition_column=n.source.partition_column, business_keys=n.source.business_keys, watermark_column=n.source.watermark_column, run_id=ctx["run_id"], engine="auto")
        except (ValueError, KeyError, TypeError) as exc:
            return {"status": "failed", "can_continue": False, "errors": [f"Incremental partition snapshot failed: {exc}"], "runtime_context": ctx}
        if write_metadata:
            _write_records_spark(spark, partition_snapshot, md["partition_snapshot_table"])

    out_df = transform(src_df, ctx, n.raw) if transform else src_df
    out_df = add_standard_technical_columns(out_df, run_id=ctx["run_id"], pipeline_name=dataset_name, environment=ctx["environment"], source_table=source_table, watermark_column=(n.source.watermark_column if n.source.watermark_column in getattr(out_df, "columns", []) else None), business_keys=n.source.business_keys)

    output_profile = profile_dataframe(out_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(output_profile, target_table, ctx["run_id"], "output", exclude_columns=default_technical_columns()), md["output_profile_table"])

    rules = n.quality.rules
    quality_result = run_quality_rules(out_df, rules, dataset_name=dataset_name, table_name=target_table, engine="auto")
    if write_metadata:
        _write_records_spark(spark, build_quality_result_records(quality_result, run_id=ctx["run_id"]), md["quality_result_table"])

    valid_df, quarantine_df = split_valid_and_quarantine(out_df, rules=rules, engine="auto")
    quarantine_row_count = len(quarantine_df) if hasattr(quarantine_df, "__len__") else int(quarantine_df.count())
    quarantine_written = False
    if write_target and write_metadata and md.get("quarantine_table") and quarantine_row_count > 0:
        _write_dataframe_to_table(spark, quarantine_df, md["quarantine_table"], mode="append")
        quarantine_written = True

    contract_result = validate_runtime_contracts(source_df=src_df, output_df=valid_df, contract=_runtime_validation_contract(n), engine="auto")
    if write_metadata:
        _write_records_spark(spark, build_contract_validation_records(contract_result, run_id=ctx["run_id"]), md["contract_validation_table"])

    lineage_rows = build_lineage_records(run_id=ctx["run_id"], dataset_name=dataset_name, source_tables=[source_table], target_table=target_table, transformation_steps=[])
    if write_metadata and md.get("lineage_table"):
        _write_records_spark(spark, lineage_rows, md["lineage_table"])

    run_summary = build_run_summary(runtime_context=ctx, contract=n.raw, source_profile=source_profile, output_profile=output_profile, quality_result=quality_result, contract_validation_result=contract_result)
    if write_metadata:
        _write_records_spark(spark, [build_run_summary_record(run_summary)], md["run_summary_table"])

    can_continue = bool(quality_result.get("can_continue", True)) and bool(contract_result.get("can_continue", True))
    status = "passed" if can_continue else "failed"
    if write_target and can_continue:
        _write_dataframe_to_table(spark, valid_df, target_table, mode=n.target.mode)

    dataset_run = build_dataset_run_record(run_id=ctx["run_id"], dataset_name=dataset_name, environment=ctx["environment"], source_table=source_table, target_table=target_table, status=status, started_at_utc=ctx.get("started_at_utc"), row_count_source=source_profile.get("row_count"), row_count_output=output_profile.get("row_count"))
    if write_metadata:
        _write_records_spark(spark, [dataset_run], md["dataset_runs_table"])

    return {"status": status, "can_continue": can_continue, "runtime_context": ctx, "source_profile": source_profile, "output_profile": output_profile, "schema_snapshot": source_schema_snapshot, "partition_snapshot": partition_snapshot, "quality_result": quality_result, "contract_validation_result": contract_result, "lineage_records": lineage_rows, "run_summary": run_summary, "dataset_run": dataset_run, "quarantine_written": quarantine_written, "quarantine_row_count": quarantine_row_count}


def assert_data_product_passed(result: dict) -> None:
    if result.get("status") != "passed":
        raise RuntimeError("Data product run failed contract/quality gates")
