"""Contract-first orchestration API for running a framework data product."""

from __future__ import annotations

from pathlib import Path

from fabric_data_product_framework.config import load_dataset_contract
from fabric_data_product_framework.contracts import build_contract_validation_records, validate_runtime_contracts
from fabric_data_product_framework.drift import build_schema_snapshot
from fabric_data_product_framework.incremental import build_partition_snapshot
from fabric_data_product_framework.lineage import build_lineage_records
from fabric_data_product_framework.metadata import build_dataset_run_record, build_schema_snapshot_records, write_metadata_records
from fabric_data_product_framework.profiling import default_technical_columns, flatten_profile_for_metadata, profile_dataframe
from fabric_data_product_framework.quality import run_quality_rules
from fabric_data_product_framework.quarantine import split_valid_and_quarantine
from fabric_data_product_framework.run_summary import build_run_summary, build_run_summary_record
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.technical_columns import add_standard_technical_columns

_REQUIRED_TOP_LEVEL_KEYS = ["dataset", "environment", "source", "target", "keys", "schema", "quality", "drift", "metadata"]


def load_data_contract(path_or_dict: str | Path | dict) -> dict:
    if isinstance(path_or_dict, dict):
        return dict(path_or_dict)
    return load_dataset_contract(path_or_dict)


def validate_data_contract_shape(contract: dict) -> list[str]:
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
        "metadata": ["source_profile_table", "output_profile_table", "schema_snapshot_table", "partition_snapshot_table", "quality_result_table", "quarantine_table", "contract_validation_table", "lineage_table", "run_summary_table", "dataset_runs_table"],
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




def _write_dataframe_to_table(spark, df, table: str, mode: str = "append") -> None:
    if hasattr(df, "write"):
        df.write.mode(mode).saveAsTable(table)
        return
    spark.createDataFrame(df.to_dict(orient="records")).write.mode(mode).saveAsTable(table)

def _runtime_validation_contract(contract: dict) -> dict:
    mapped = dict(contract)
    mapped["contracts"] = mapped.get("contracts") or {
        "upstream": {"expected_columns": contract.get("schema", {}).get("required_source_columns", [])},
        "downstream": {"guaranteed_columns": contract.get("schema", {}).get("required_output_columns", [])},
    }
    mapped["refresh"] = mapped.get("refresh") or {"watermark_column": contract.get("keys", {}).get("watermark_column")}
    return mapped


def run_data_product(spark, contract: dict, transform=None, source_df=None, write: bool | None = None, *, write_target: bool = True, write_metadata: bool = True) -> dict:
    if write is not None:
        write_target = bool(write)

    shape_errors = validate_data_contract_shape(contract)
    if shape_errors:
        return {"status": "failed", "can_continue": False, "errors": shape_errors}

    ctx = build_runtime_context_from_contract(contract)
    dataset_name, source_table, target_table, metadata = contract["dataset"]["name"], contract["source"]["table"], contract["target"]["table"], contract["metadata"]
    src_df = source_df if source_df is not None else spark.table(source_table)

    source_profile = profile_dataframe(src_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(source_profile, source_table, ctx["run_id"], "source"), metadata["source_profile_table"])

    source_schema_snapshot = build_schema_snapshot(src_df, dataset_name=dataset_name, table_name=source_table)
    if write_metadata:
        _write_records_spark(spark, build_schema_snapshot_records(source_schema_snapshot, run_id=ctx["run_id"], table_stage="source"), metadata["schema_snapshot_table"])

    partition_snapshot = None
    if contract["keys"].get("partition_column"):
        try:
            partition_snapshot = build_partition_snapshot(src_df, dataset_name=dataset_name, table_name=source_table, partition_column=contract["keys"]["partition_column"], business_keys=contract["keys"].get("business_keys", []), watermark_column=contract["keys"].get("watermark_column"), run_id=ctx["run_id"], engine="auto")
            if write_metadata:
                _write_records_spark(spark, partition_snapshot, metadata["partition_snapshot_table"])
        except Exception:
            partition_snapshot = None

    out_df = transform(src_df, ctx, contract) if transform else src_df
    watermark_column = contract["keys"].get("watermark_column")
    out_df = add_standard_technical_columns(out_df, run_id=ctx["run_id"], pipeline_name=dataset_name, environment=ctx["environment"], source_table=source_table, watermark_column=(watermark_column if watermark_column in getattr(out_df, "columns", []) else None), business_keys=contract["keys"].get("business_keys", []))

    output_profile = profile_dataframe(out_df, dataset_name=dataset_name)
    if write_metadata:
        _write_records_spark(spark, flatten_profile_for_metadata(output_profile, target_table, ctx["run_id"], "output", exclude_columns=default_technical_columns()), metadata["output_profile_table"])

    rules = contract["quality"].get("rules", [])
    quality_result = run_quality_rules(out_df, rules, dataset_name=dataset_name, table_name=target_table, engine="auto")
    if write_metadata:
        _write_records_spark(spark, quality_result.get("results", []), metadata["quality_result_table"])

    valid_df, quarantine_df = split_valid_and_quarantine(out_df, rules=rules, engine="auto")
    if write_target and write_metadata and metadata.get("quarantine_table") and quarantine_df is not None:
        _write_dataframe_to_table(spark, quarantine_df, metadata["quarantine_table"], mode="append")

    contract_result = validate_runtime_contracts(source_df=src_df, output_df=valid_df, contract=_runtime_validation_contract(contract), engine="auto")
    if write_metadata:
        _write_records_spark(spark, build_contract_validation_records(contract_result, run_id=ctx["run_id"]), metadata["contract_validation_table"])

    lineage_rows = build_lineage_records(run_id=ctx["run_id"], dataset_name=dataset_name, source_tables=[source_table], target_table=target_table, transformation_steps=[])
    if write_metadata and metadata.get("lineage_table"):
        _write_records_spark(spark, lineage_rows, metadata["lineage_table"])

    run_summary = build_run_summary(runtime_context=ctx, contract=contract, source_profile=source_profile, output_profile=output_profile, quality_result=quality_result, contract_validation_result=contract_result)
    if write_metadata:
        _write_records_spark(spark, [build_run_summary_record(run_summary)], metadata["run_summary_table"])

    can_continue = bool(quality_result.get("can_continue", True)) and bool(contract_result.get("can_continue", True))
    status = "passed" if can_continue else "failed"
    if write_target and can_continue:
        _write_dataframe_to_table(spark, valid_df, target_table, mode=contract["target"].get("mode", "append"))

    dataset_run = build_dataset_run_record(run_id=ctx["run_id"], dataset_name=dataset_name, environment=ctx["environment"], source_table=source_table, target_table=target_table, status=status, started_at_utc=ctx.get("started_at_utc"), row_count_source=source_profile.get("row_count"), row_count_output=output_profile.get("row_count"))
    if write_metadata:
        _write_records_spark(spark, [dataset_run], metadata["dataset_runs_table"])

    return {"status": status, "can_continue": can_continue, "runtime_context": ctx, "source_profile": source_profile, "output_profile": output_profile, "schema_snapshot": source_schema_snapshot, "partition_snapshot": partition_snapshot, "quality_result": quality_result, "contract_validation_result": contract_result, "lineage_records": lineage_rows, "run_summary": run_summary, "dataset_run": dataset_run, "quarantine_written": quarantine_df is not None}


def assert_data_product_passed(result: dict) -> None:
    if result.get("status") != "passed":
        raise RuntimeError("Data product run failed contract/quality gates")
