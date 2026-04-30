"""Contract-first orchestration API for running a framework data product."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fabric_data_product_framework.config import load_dataset_contract
from fabric_data_product_framework.contracts import build_contract_validation_records, validate_runtime_contracts
from fabric_data_product_framework.drift import build_schema_snapshot
from fabric_data_product_framework.incremental import build_partition_snapshot
from fabric_data_product_framework.lineage import build_lineage_records
from fabric_data_product_framework.metadata import (
    build_dataset_run_record,
    build_schema_snapshot_records,
    write_metadata_records,
)
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.quality import run_quality_rules
from fabric_data_product_framework.quarantine import add_dq_failure_columns, split_valid_and_quarantine
from fabric_data_product_framework.run_summary import build_run_summary, build_run_summary_record
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.technical_columns import add_standard_technical_columns


_REQUIRED_TOP_LEVEL_KEYS = [
    "dataset",
    "environment",
    "source",
    "target",
    "keys",
    "schema",
    "quality",
    "drift",
    "metadata",
]


def load_data_contract(path_or_dict: str | Path | dict) -> dict:
    """Load a contract from a YAML path or return a shallow copy of a provided dict."""
    if isinstance(path_or_dict, dict):
        return dict(path_or_dict)
    return load_dataset_contract(path_or_dict)


def validate_data_contract_shape(contract: dict) -> list[str]:
    """Validate required shape for contract-first orchestration."""
    errors: list[str] = []
    for key in _REQUIRED_TOP_LEVEL_KEYS:
        if key not in contract:
            errors.append(f"Missing required section: {key}")

    required_nested = {
        "dataset": ["name", "description", "owner", "approved_usage"],
        "environment": ["name", "metadata_schema"],
        "source": ["table", "format"],
        "target": ["table", "mode", "format"],
        "keys": ["business_keys", "watermark_column", "partition_column"],
        "schema": ["required_source_columns", "required_output_columns"],
        "quality": ["rules"],
        "drift": ["schema_policy", "incremental_policy"],
        "metadata": [
            "source_profile_table",
            "output_profile_table",
            "schema_snapshot_table",
            "partition_snapshot_table",
            "quality_result_table",
            "quarantine_table",
            "contract_validation_table",
            "lineage_table",
            "run_summary_table",
            "dataset_runs_table",
        ],
    }
    for section, required_keys in required_nested.items():
        value = contract.get(section, {})
        if not isinstance(value, dict):
            errors.append(f"Section '{section}' must be a dictionary")
            continue
        for key in required_keys:
            if key not in value:
                errors.append(f"Missing required key: {section}.{key}")
    return errors


def build_runtime_context_from_contract(contract: dict, overrides: dict | None = None) -> dict:
    """Build runtime context using required contract fields and optional overrides."""
    context = build_runtime_context(
        dataset_name=contract["dataset"]["name"],
        environment=contract["environment"]["name"],
        source_table=contract["source"]["table"],
        target_table=contract["target"]["table"],
        notebook_name=contract.get("runtime", {}).get("notebook_name"),
        run_id=(overrides or {}).get("run_id"),
    )
    if overrides:
        context.update(overrides)
    return context


def _write_records_spark(spark, records: list[dict], table: str, mode: str = "append") -> None:
    if not records:
        return
    write_metadata_records(records, table, writer=lambda rows, t, mode="append", **_: spark.createDataFrame(rows).write.mode(mode).saveAsTable(t), mode=mode)


def run_data_product(spark, contract: dict, transform=None, source_df=None, write: bool = True) -> dict:
    """Run end-to-end contract-first orchestration with framework building blocks."""
    shape_errors = validate_data_contract_shape(contract)
    if shape_errors:
        return {"status": "failed", "can_continue": False, "errors": shape_errors}

    ctx = build_runtime_context_from_contract(contract)
    dataset_name = contract["dataset"]["name"]
    source_table = contract["source"]["table"]
    target_table = contract["target"]["table"]
    metadata = contract["metadata"]

    src_df = source_df if source_df is not None else spark.table(source_table)

    source_profile = profile_dataframe(src_df, dataset_name=dataset_name, table_name=source_table)
    _write_records_spark(spark, source_profile.get("columns", []), metadata["source_profile_table"])

    source_schema_snapshot = build_schema_snapshot(src_df, dataset_name=dataset_name, table_name=source_table)
    _write_records_spark(spark, build_schema_snapshot_records(source_schema_snapshot, run_id=ctx["run_id"], table_stage="source"), metadata["schema_snapshot_table"])

    partition_snapshot = None
    if contract["keys"].get("partition_column"):
        partition_snapshot = build_partition_snapshot(
            src_df,
            dataset_name=dataset_name,
            table_name=source_table,
            partition_column=contract["keys"]["partition_column"],
            business_keys=contract["keys"].get("business_keys", []),
            watermark_column=contract["keys"].get("watermark_column"),
            run_id=ctx["run_id"],
            engine="auto",
        )
        _write_records_spark(spark, partition_snapshot, metadata["partition_snapshot_table"])

    out_df = transform(src_df, ctx, contract) if transform else src_df
    out_df = add_standard_technical_columns(
        out_df,
        run_id=ctx["run_id"],
        pipeline_name=dataset_name,
        environment=ctx["environment"],
        source_table=source_table,
        watermark_column=contract["keys"].get("watermark_column"),
        business_keys=contract["keys"].get("business_keys", []),
    )

    output_profile = profile_dataframe(out_df, dataset_name=dataset_name, table_name=target_table)
    _write_records_spark(spark, output_profile.get("columns", []), metadata["output_profile_table"])

    quality_result = run_quality_rules(out_df, contract["quality"].get("rules", []), dataset_name=dataset_name, table_name=target_table, engine="auto")
    _write_records_spark(spark, quality_result.get("results", []), metadata["quality_result_table"])

    quarantine_df = None
    valid_df = out_df
    if metadata.get("quarantine_table"):
        annotated = add_dq_failure_columns(out_df, quality_result.get("results", []), engine="auto")
        valid_df, quarantine_df = split_valid_and_quarantine(annotated, engine="auto")
        if write and quarantine_df is not None:
            quarantine_df.write.mode("append").saveAsTable(metadata["quarantine_table"])

    contract_result = validate_runtime_contracts(source_df=src_df, output_df=valid_df, contract=contract, engine="auto")
    _write_records_spark(spark, build_contract_validation_records(contract_result, run_id=ctx["run_id"]), metadata["contract_validation_table"])

    lineage_rows = []
    if metadata.get("lineage_table"):
        lineage_rows = build_lineage_records(
            run_id=ctx["run_id"],
            dataset_name=dataset_name,
            source_tables=[source_table],
            target_table=target_table,
            transformation_steps=[],
        )
        _write_records_spark(spark, lineage_rows, metadata["lineage_table"])

    run_summary = build_run_summary(
        runtime_context=ctx,
        contract=contract,
        source_profile=source_profile,
        output_profile=output_profile,
        quality_result=quality_result,
        contract_validation_result=contract_result,
    )
    _write_records_spark(spark, [build_run_summary_record(run_summary)], metadata["run_summary_table"])

    can_continue = bool(quality_result.get("can_continue", True)) and bool(contract_result.get("can_continue", True))
    status = "passed" if can_continue else "failed"

    if write and can_continue:
        valid_df.write.mode(contract["target"].get("mode", "append")).saveAsTable(target_table)

    dataset_run = build_dataset_run_record(
        run_id=ctx["run_id"],
        dataset_name=dataset_name,
        environment=ctx["environment"],
        source_table=source_table,
        target_table=target_table,
        status=status,
        started_at_utc=ctx.get("started_at_utc"),
        row_count_source=source_profile.get("row_count"),
        row_count_output=output_profile.get("row_count"),
    )
    _write_records_spark(spark, [dataset_run], metadata["dataset_runs_table"])

    return {
        "status": status,
        "can_continue": can_continue,
        "runtime_context": ctx,
        "source_profile": source_profile,
        "output_profile": output_profile,
        "schema_snapshot": source_schema_snapshot,
        "partition_snapshot": partition_snapshot,
        "quality_result": quality_result,
        "contract_validation_result": contract_result,
        "lineage_records": lineage_rows,
        "run_summary": run_summary,
        "dataset_run": dataset_run,
        "quarantine_written": quarantine_df is not None,
    }


def assert_data_product_passed(result: dict) -> None:
    """Raise when `run_data_product` status is not passed."""
    if result.get("status") != "passed":
        raise RuntimeError("Data product run failed contract/quality gates")
