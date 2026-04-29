"""Row-level helpers to annotate and split valid/quarantine records."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .quality import _resolve_engine


def _severity_bucket(severity: str) -> str:
    return "dq_errors" if str(severity).lower() == "critical" else "dq_warnings"


def add_dq_failure_columns(df, rules, engine="auto"):
    resolved = _resolve_engine(df, engine)
    if resolved == "spark":
        return _add_spark(df, rules)
    return _add_pandas(df, rules)


def split_valid_and_quarantine(df, rules, engine="auto"):
    enriched = add_dq_failure_columns(df, rules, engine=engine)
    if _resolve_engine(enriched, engine) == "spark":
        from pyspark.sql import functions as F

        return enriched.filter(F.size("dq_errors") == 0), enriched.filter(F.size("dq_errors") > 0)
    return enriched[~enriched["dq_errors"].map(bool)].copy(), enriched[enriched["dq_errors"].map(bool)].copy()


def build_quarantine_summary_records(quarantine_df, run_id, dataset_name, table_name, engine="auto"):
    resolved = _resolve_engine(quarantine_df, engine)
    if resolved == "spark":
        q_count = quarantine_df.count()
    else:
        q_count = len(quarantine_df)
    return [{"run_id": run_id, "dataset_name": dataset_name, "table_name": table_name, "quarantine_row_count": int(q_count), "engine": resolved}]


def _add_pandas(df: pd.DataFrame, rules):
    out = df.copy()
    out["dq_errors"] = [[] for _ in range(len(out))]
    out["dq_warnings"] = [[] for _ in range(len(out))]
    for i, rule in enumerate(rules):
        msg = f"{rule.get('rule_id', f'DQ{i + 1:03d}')}: {rule.get('reason') or rule.get('rule_type')}"
        bucket = _severity_bucket(rule.get("severity", "critical"))
        mask = pd.Series(False, index=out.index)
        rt = rule.get("rule_type")
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
        else:
            continue
        for pos, failed in enumerate(mask.tolist()):
            if failed:
                out.iat[pos, out.columns.get_loc(bucket)].append(msg)
    return out


def _add_spark(df, rules):
    from pyspark.sql import functions as F

    out = df.withColumn("dq_errors", F.array().cast("array<string>")).withColumn("dq_warnings", F.array().cast("array<string>"))
    for i, rule in enumerate(rules):
        msg = f"{rule.get('rule_id', f'DQ{i + 1:03d}')}: {rule.get('reason') or rule.get('rule_type')}"
        bucket = _severity_bucket(rule.get("severity", "critical"))
        rt = rule.get("rule_type")
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
        if cond is None:
            continue
        out = out.withColumn(bucket, F.when(cond, F.array_union(F.col(bucket), F.array(F.lit(msg)))).otherwise(F.col(bucket)))
    return out
