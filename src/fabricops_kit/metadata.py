"""Metadata record shaping and adapter-based writer helpers."""

from __future__ import annotations

from typing import Any

from fabricops_kit.profiling import to_jsonable


def build_dataset_run_record(
    *,
    run_id: str,
    dataset_name: str,
    environment: str,
    source_table: str,
    target_table: str,
    status: str = "started",
    started_at_utc: str | None = None,
    ended_at_utc: str | None = None,
    row_count_source: int | None = None,
    row_count_output: int | None = None,
    notes: str | None = None,
) -> dict:
    """Execute the `build_dataset_run_record` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        None
            This function does not require explicit parameters.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> build_dataset_run_record()
        """
    return to_jsonable(
        {
            "run_id": run_id,
            "dataset_name": dataset_name,
            "environment": environment,
            "source_table": source_table,
            "target_table": target_table,
            "status": status,
            "started_at_utc": started_at_utc,
            "ended_at_utc": ended_at_utc,
            "row_count_source": row_count_source,
            "row_count_output": row_count_output,
            "notes": notes,
        }
    )


def build_schema_snapshot_records(snapshot: dict, *, run_id: str, table_stage: str) -> list[dict]:
    """Execute the `build_schema_snapshot_records` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        snapshot : Any
            Input parameter `snapshot`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> build_schema_snapshot_records(...)
        """
    base = {
        "run_id": run_id,
        "dataset_name": snapshot.get("dataset_name"),
        "table_name": snapshot.get("table_name"),
        "table_stage": table_stage,
        "engine": snapshot.get("engine"),
        "generated_at": snapshot.get("generated_at"),
    }
    return [
        to_jsonable(
            {
                **base,
                "column_name": col.get("column_name"),
                "ordinal_position": col.get("ordinal_position"),
                "data_type": col.get("data_type"),
                "nullable": col.get("nullable"),
                "column_hash": col.get("column_hash"),
            }
        )
        for col in snapshot.get("columns", [])
    ]


def build_schema_drift_records(drift_result: dict, *, run_id: str, table_stage: str) -> list[dict]:
    """Execute the `build_schema_drift_records` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        drift_result : Any
            Input parameter `drift_result`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> build_schema_drift_records(...)
        """
    base = {
        "run_id": run_id,
        "dataset_name": drift_result.get("dataset_name"),
        "table_name": drift_result.get("table_name"),
        "table_stage": table_stage,
        "baseline_engine": drift_result.get("baseline_engine"),
        "current_engine": drift_result.get("current_engine"),
        "status": drift_result.get("status"),
        "can_continue": drift_result.get("can_continue"),
    }
    changes = drift_result.get("changes", [])
    if not changes:
        return [
            to_jsonable(
                {
                    **base,
                    "drift_type": "none",
                    "column_name": None,
                    "previous_value": None,
                    "current_value": None,
                    "severity": "info",
                    "action": "allow",
                    "message": "No schema drift detected.",
                }
            )
        ]

    return [
        to_jsonable(
            {
                **base,
                "drift_type": change.get("drift_type"),
                "column_name": change.get("column_name"),
                "previous_value": change.get("previous_value"),
                "current_value": change.get("current_value"),
                "severity": change.get("severity"),
                "action": change.get("action"),
                "message": change.get("message"),
            }
        )
        for change in changes
    ]


def build_quality_result_records(
    quality_result: dict | list[dict],
    *,
    run_id: str,
    dataset_name: str,
    table_name: str,
    table_stage: str,
) -> list[dict]:
    """Execute the `build_quality_result_records` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        quality_result : Any
            Input parameter `quality_result`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> build_quality_result_records(...)
        """
    results: list[dict[str, Any]]
    if isinstance(quality_result, dict):
        results = list(quality_result.get("results", []))
    else:
        results = list(quality_result)

    rows = []
    for result in results:
        rows.append(
            to_jsonable(
                {
                    "run_id": run_id,
                    "dataset_name": dataset_name,
                    "table_name": table_name,
                    "table_stage": table_stage,
                    "rule_id": result.get("rule_id"),
                    "rule_type": result.get("rule_type"),
                    "column_name": result.get("column_name"),
                    "columns": to_jsonable(result.get("columns")),
                    "severity": result.get("severity"),
                    "status": result.get("status"),
                    "failed_count": result.get("failed_count"),
                    "total_count": result.get("total_count"),
                    "failed_pct": result.get("failed_pct"),
                    "message": result.get("message"),
                }
            )
        )
    return rows


def write_metadata_records(records: list[dict], table_identifier: str, writer=None, mode: str = "append", **options):
    """Execute the `write_metadata_records` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        records : Any
            Input parameter `records`.
        table_identifier : Any
            Input parameter `table_identifier`.
        writer : Any
            Input parameter `writer`.
        mode : Any
            Input parameter `mode`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> write_metadata_records(..., ..., ..., ...)
        """
    if not records:
        return None
    if writer is None:
        raise NotImplementedError(
            "No metadata writer provided. Inject a writer(records, table_identifier, mode='append', **options) adapter."
        )
    return writer(records, table_identifier, mode=mode, **options)


def write_multiple_metadata_outputs(
    outputs: dict[str, list[dict]],
    table_mapping: dict[str, str],
    writer=None,
    mode: str = "append",
    **options,
) -> dict:
    """Execute the `write_multiple_metadata_outputs` workflow step in FabricOps.
    
        Use this callable at its corresponding stage of the pipeline contract
        (configuration, IO, profiling, quality, drift, lineage, or handover)
        to produce deterministic artifacts and validation evidence.
    
        Parameters
        ----------
        outputs : Any
            Input parameter `outputs`.
        table_mapping : Any
            Input parameter `table_mapping`.
        writer : Any
            Input parameter `writer`.
        mode : Any
            Input parameter `mode`.
    
        Returns
        -------
        Any
            Function output used by downstream FabricOps workflow steps.
    
        Raises
        ------
        Exception
            Propagates validation, runtime, or storage errors from underlying
            operations when execution cannot continue safely.
    
        Notes
        -----
        Side effects may include metadata writes, quality evidence generation,
        or persisted drift/lineage/handover artifacts depending on the function.
    
        Examples
        --------
        >>> write_multiple_metadata_outputs(..., ..., ..., ...)
        """
    results = {}
    for output_name, records in outputs.items():
        if not records:
            continue
        table_identifier = table_mapping.get(output_name)
        if not table_identifier:
            raise ValueError(f"Missing table mapping for metadata output '{output_name}'.")
        results[output_name] = write_metadata_records(
            records=records,
            table_identifier=table_identifier,
            writer=writer,
            mode=mode,
            **options,
        )
    return results
