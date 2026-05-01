"""Row-level helpers to annotate and split valid/quarantine records."""

from __future__ import annotations

import pandas as pd

from .quality import _resolve_engine

ROW_LEVEL_SUPPORTED = {"not_null", "regex_check", "accepted_values", "range_check", "unique", "unique_combination"}
AGGREGATE_ONLY = {"row_count_min", "row_count_between", "freshness_check"}


def _severity_bucket(severity: str) -> str:
    return "dq_errors" if str(severity).lower() == "critical" else "dq_warnings"


def build_quarantine_rule_coverage_records(rules, run_id, dataset_name, table_name):
    """Summarize whether each rule can run at row-level for quarantine splits."""
    rows = []
    for i, rule in enumerate(rules):
        rt = rule.get("rule_type")
        if rt in ROW_LEVEL_SUPPORTED:
            status, message = "row_level_supported", "Rule evaluated at row level"
        elif rt in AGGREGATE_ONLY:
            status, message = "aggregate_only", "Rule is aggregate-level and not row-level executable"
        else:
            status, message = "unsupported", "Unsupported or unknown rule_type for quarantine row-level execution"
        rows.append({"run_id": run_id, "dataset_name": dataset_name, "table_name": table_name, "rule_id": rule.get("rule_id", f"DQ{i + 1:03d}"), "rule_type": rt, "coverage_status": status, "coverage_message": message})
    return rows


def add_dq_failure_columns(df, rules, engine="auto"):
    """Annotate dataframe rows with rule-level failure arrays.

    Parameters
    ----------
    df : pandas.DataFrame or pyspark.sql.DataFrame
        Input dataset to annotate.
    rules : list[dict]
        Executable quality rules with ``rule_type`` and ``severity`` fields.
    engine : str, default "auto"
        ``pandas``, ``spark``, or ``auto``.

    Returns
    -------
    DataFrame
        Input dataframe plus ``dq_errors`` and ``dq_warnings`` columns.

    Notes
    -----
    This function supports row-level quarantine handoff. Aggregate-only rules
    are excluded from row annotations by design.
    """
    resolved = _resolve_engine(df, engine)
    return _add_spark(df, rules) if resolved == "spark" else _add_pandas(df, rules)


def split_valid_and_quarantine(df, rules, engine="auto"):
    """Split dataset into pipeline-safe rows and quarantined rows.

    Parameters
    ----------
    df : pandas.DataFrame or pyspark.sql.DataFrame
        Input records to evaluate.
    rules : list[dict]
        Row-level executable rules.
    engine : str, default "auto"
        Execution engine selector.

    Returns
    -------
    tuple
        ``(valid_df, quarantine_df)`` where quarantine rows have at least one
        critical row-level failure in ``dq_errors``.
    """
    enriched = add_dq_failure_columns(df, rules, engine=engine)
    if _resolve_engine(enriched, engine) == "spark":
        from pyspark.sql import functions as F

        return enriched.filter(F.size("dq_errors") == 0), enriched.filter(F.size("dq_errors") > 0)
    return enriched[~enriched["dq_errors"].map(bool)].copy(), enriched[enriched["dq_errors"].map(bool)].copy()


def build_quarantine_summary_records(quarantine_df, run_id, dataset_name, table_name, engine="auto"):
    """Build metadata rows summarizing quarantine volume for a pipeline run.

    Parameters
    ----------
    quarantine_df : pandas.DataFrame or pyspark.sql.DataFrame
        Quarantine partition returned by :func:`split_valid_and_quarantine`.
    run_id, dataset_name, table_name : str
        Run and dataset identifiers persisted with the summary.
    engine : str, default "auto"
        Execution engine selector.

    Returns
    -------
    list[dict]
        Metadata-table-ready summary records that can be surfaced in monitoring,
        run summaries, and AI/human handover context.
    """
    resolved = _resolve_engine(quarantine_df, engine)
    q_count = quarantine_df.count() if resolved == "spark" else len(quarantine_df)
    return [{"run_id": run_id, "dataset_name": dataset_name, "table_name": table_name, "quarantine_row_count": int(q_count), "engine": resolved}]


def _add_pandas(df: pd.DataFrame, rules):
    out = df.copy()
    out["dq_errors"] = [[] for _ in range(len(out))]
    out["dq_warnings"] = [[] for _ in range(len(out))]

    for i, rule in enumerate(rules):
        rt = rule.get("rule_type")
        if rt not in ROW_LEVEL_SUPPORTED:
            continue
        msg = f"{rule.get('rule_id', f'DQ{i + 1:03d}')}: {rule.get('reason') or rt}"
        bucket = _severity_bucket(rule.get("severity", "critical"))
        mask = pd.Series(False, index=out.index)

        if rt == "not_null":
            mask = out[rule["column"]].isna()
        elif rt == "regex_check":
            s = out[rule["column"]].dropna().astype(str)
            mask.loc[s[~s.str.match(rule.get("pattern", ""), na=False)].index] = True
        elif rt == "accepted_values":
            mask = out[rule["column"]].notna() & ~out[rule["column"]].isin(rule.get("accepted_values", []))
        elif rt == "range_check":
            s = out[rule["column"]]
            if rule.get("min_value") is not None:
                mask |= s.notna() & (s < rule["min_value"])
            if rule.get("max_value") is not None:
                mask |= s.notna() & (s > rule["max_value"])
        elif rt == "unique":
            mask = out[rule["column"]].duplicated(keep=False) & out[rule["column"]].notna()
        elif rt == "unique_combination":
            cols = rule.get("columns", [])
            if cols:
                mask = out.duplicated(subset=cols, keep=False)

        for pos, failed in enumerate(mask.tolist()):
            if failed:
                out.iat[pos, out.columns.get_loc(bucket)].append(msg)
    return out


def _add_spark(df, rules):
    from pyspark.sql import functions as F

    out = df.withColumn("dq_errors", F.array().cast("array<string>")).withColumn("dq_warnings", F.array().cast("array<string>"))
    for i, rule in enumerate(rules):
        rt = rule.get("rule_type")
        if rt not in ROW_LEVEL_SUPPORTED:
            continue
        msg = f"{rule.get('rule_id', f'DQ{i + 1:03d}')}: {rule.get('reason') or rt}"
        bucket = _severity_bucket(rule.get("severity", "critical"))
        cond = None
        if rt == "not_null":
            cond = F.col(rule["column"]).isNull()
        elif rt == "regex_check":
            cond = F.col(rule["column"]).isNotNull() & ~F.col(rule["column"]).rlike(rule.get("pattern", ""))
        elif rt == "accepted_values":
            cond = F.col(rule["column"]).isNotNull() & ~F.col(rule["column"]).isin(rule.get("accepted_values", []))
        elif rt == "range_check":
            cond = F.lit(False)
            if rule.get("min_value") is not None:
                cond = cond | (F.col(rule["column"]) < F.lit(rule["min_value"]))
            if rule.get("max_value") is not None:
                cond = cond | (F.col(rule["column"]) > F.lit(rule["max_value"]))
            cond = F.col(rule["column"]).isNotNull() & cond
        elif rt == "unique":
            c = rule["column"]
            dup_keys = (
                df.groupBy(c)
                .count()
                .filter(F.col(c).isNotNull() & (F.col("count") > 1))
                .select(F.col(c).alias("__dup_key"))
                .withColumn("__dup_marker", F.lit(True))
            )
            joined = out.join(dup_keys, out[c] == F.col("__dup_key"), "left")
            out = joined.withColumn(bucket, F.when(F.col("__dup_marker") == True, F.array_union(F.col(bucket), F.array(F.lit(msg)))).otherwise(F.col(bucket))).drop("__dup_key", "__dup_marker")
            continue
        elif rt == "unique_combination":
            cols = rule.get("columns", [])
            if cols:
                dup_combo = (
                    df.groupBy(*cols)
                    .count()
                    .filter(F.col("count") > 1)
                    .select(*[F.col(c).alias(f"__dup_{c}") for c in cols])
                    .withColumn("__dup_marker", F.lit(True))
                )
                join_cond = [out[c] == F.col(f"__dup_{c}") for c in cols]
                joined = out.join(dup_combo, join_cond, "left")
                drop_cols = [f"__dup_{c}" for c in cols] + ["__dup_marker"]
                out = joined.withColumn(bucket, F.when(F.col("__dup_marker") == True, F.array_union(F.col(bucket), F.array(F.lit(msg)))).otherwise(F.col(bucket))).drop(*drop_cols)
                continue
        if cond is None:
            continue
        out = out.withColumn(bucket, F.when(cond, F.array_union(F.col(bucket), F.array(F.lit(msg)))).otherwise(F.col(bucket)))
    return out
