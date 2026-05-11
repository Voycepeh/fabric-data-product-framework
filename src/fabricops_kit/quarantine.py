from __future__ import annotations
from typing import Any
from datetime import datetime, timezone
import uuid
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def split_valid_quarantine_and_failures(
    df,
    rules: list[dict[str, Any]],
    dq_run_id: str | None = None,
    row_id_columns: list[str] | None = None,
):
    """
    Split a DataFrame into accepted rows, quarantined rows, and row-rule failure evidence.

    Returns
    -------
    tuple
        (df_valid, df_quarantine_rows, df_quarantine_failures)

    Design
    ------
    df_valid:
        Rows that pass all row-level DQ rules.

    df_quarantine_rows:
        Original rows that fail at least one row-level DQ rule.
        One row appears once, even if it fails multiple rules.

    df_quarantine_failures:
        One row per failed rule per quarantined source row.
        This is the proper evidence table for remediation and audit.

    Notes
    -----
    - dq_run_id ties all records to one DQ run.
    - dq_row_id ties the accepted/quarantined/failure records back to the source row for that run.
    - dq_quarantine_id ties one quarantined source row to all of its failed rule records.
    """
    _validate_dq_rules(rules)

    if dq_run_id is None:
        dq_run_id = str(uuid.uuid4())

    run_ts = datetime.now(timezone.utc).isoformat()

    # Add a stable row id for this run.
    # If business keys are supplied, hash them.
    # Otherwise, use monotonically_increasing_id for demo/runtime traceability.
    if row_id_columns:
        df_with_ids = df.withColumn(
            "dq_row_id",
            F.sha2(
                F.concat_ws(
                    "||",
                    *[
                        F.coalesce(F.col(c).cast("string"), F.lit("<NULL>"))
                        for c in row_id_columns
                    ],
                ),
                256,
            ),
        )
    else:
        df_with_ids = df.withColumn(
            "dq_row_id",
            F.sha2(
                F.concat_ws(
                    "||",
                    *[
                        F.coalesce(F.col(c).cast("string"), F.lit("<NULL>"))
                        for c in df.columns
                    ],
                    F.monotonically_increasing_id().cast("string"),
                ),
                256,
            ),
        )

    df_with_ids = df_with_ids.withColumn("dq_run_id", F.lit(dq_run_id))

    failure_dfs = []

    working = df_with_ids

    for rule in rules:
        rule_id = str(rule["rule_id"])
        rule_type = str(rule["rule_type"])
        columns = rule["columns"]
        col_name = columns[0]
        severity = str(rule.get("severity", "warning"))
        description = str(rule.get("description", ""))

        if rule_type == "not_null":
            failed = F.col(col_name).isNull() | (F.trim(F.col(col_name).cast("string")) == "")

        elif rule_type == "unique_key":
            duplicate_count_col = f"__dq_duplicate_count_{rule_id}"
            working = working.withColumn(
                duplicate_count_col,
                F.count(F.lit(1)).over(Window.partitionBy(*[F.col(c) for c in columns])),
            )
            failed = F.col(duplicate_count_col) > F.lit(1)

        elif rule_type == "accepted_values":
            failed = F.col(col_name).isNotNull() & ~F.col(col_name).isin(rule["allowed_values"])

        elif rule_type == "value_range":
            failed_condition = F.lit(False)

            if rule.get("min_value") is not None:
                failed_condition = failed_condition | (
                    F.col(col_name).cast("double") < F.lit(float(rule["min_value"]))
                )

            if rule.get("max_value") is not None:
                failed_condition = failed_condition | (
                    F.col(col_name).cast("double") > F.lit(float(rule["max_value"]))
                )

            failed = F.col(col_name).isNotNull() & failed_condition

        elif rule_type == "regex_format":
            failed = F.col(col_name).isNotNull() & ~F.col(col_name).rlike(rule["regex_pattern"])

        else:
            # Contract guardrails are not row-level quarantine rules.
            continue

        failed = F.coalesce(failed, F.lit(False))

        failure_df = (
            working
            .filter(failed)
            .select(
                F.col("dq_run_id"),
                F.col("dq_row_id"),
                F.lit(rule_id).alias("rule_id"),
                F.lit(rule_type).alias("rule_type"),
                F.lit(",".join(columns)).alias("failed_columns"),
                F.lit(severity).alias("severity"),
                F.lit(description).alias("description"),
                F.lit(run_ts).alias("dq_failed_ts"),
            )
        )

        failure_dfs.append(failure_df)

        if rule_type == "unique_key":
            working = working.drop(duplicate_count_col)

    if not failure_dfs:
        empty_failures = df.sparkSession.createDataFrame(
            [],
            """
            dq_run_id string,
            dq_row_id string,
            dq_quarantine_id string,
            rule_id string,
            rule_type string,
            failed_columns string,
            severity string,
            description string,
            dq_failed_ts string
            """,
        )
        return df_with_ids, df.limit(0), empty_failures

    df_quarantine_failures = failure_dfs[0]
    for item in failure_dfs[1:]:
        df_quarantine_failures = df_quarantine_failures.unionByName(item)

    # One quarantine id per bad source row in this DQ run.
    quarantine_ids = (
        df_quarantine_failures
        .select("dq_run_id", "dq_row_id")
        .distinct()
        .withColumn(
            "dq_quarantine_id",
            F.sha2(F.concat_ws("||", F.col("dq_run_id"), F.col("dq_row_id")), 256),
        )
    )

    df_quarantine_failures = (
        df_quarantine_failures
        .join(quarantine_ids, on=["dq_run_id", "dq_row_id"], how="left")
        .select(
            "dq_run_id",
            "dq_row_id",
            "dq_quarantine_id",
            "rule_id",
            "rule_type",
            "failed_columns",
            "severity",
            "description",
            "dq_failed_ts",
        )
    )

    df_quarantine_rows = (
        working
        .join(quarantine_ids, on=["dq_run_id", "dq_row_id"], how="inner")
        .withColumn("dq_quarantine_ts", F.lit(run_ts))
    )

    df_valid = (
        working
        .join(quarantine_ids.select("dq_run_id", "dq_row_id"), on=["dq_run_id", "dq_row_id"], how="left_anti")
    )

    return df_valid, df_quarantine_rows, df_quarantine_failures
from .dq_rules import validate_dq_rules as _validate_dq_rules
