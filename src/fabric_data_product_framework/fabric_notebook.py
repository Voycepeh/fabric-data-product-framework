from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
from datetime import datetime, timedelta, timezone
import uuid
import tempfile
import hashlib
import ast

import pandas as pd


@dataclass(frozen=True)
class Housepath:
    workspace_id: str
    house_id: str
    house_name: str
    root: str


DEFAULT_ENV = "Sandbox"
DEFAULT_TARGET = "Source"

EXAMPLE_CONFIG: Dict[str, Dict[str, Housepath]] = {
    "Sandbox": {
        "Source": Housepath(
            workspace_id="<workspace-id>",
            house_id="<lakehouse-id>",
            house_name="SAMPLE_SOURCE",
            root="abfss://<workspace-id>@onelake.dfs.fabric.microsoft.com/<lakehouse-id>",
        ),
        "Unified": Housepath(
            workspace_id="<workspace-id>",
            house_id="<lakehouse-id>",
            house_name="SAMPLE_UNIFIED",
            root="abfss://<workspace-id>@onelake.dfs.fabric.microsoft.com/<lakehouse-id>",
        ),
        "Product": Housepath(
            workspace_id="<workspace-id>",
            house_id="<lakehouse-id>",
            house_name="SAMPLE_PRODUCT",
            root="abfss://<workspace-id>@onelake.dfs.fabric.microsoft.com/<lakehouse-id>",
        ),
    }
}


def get_path(env: str = DEFAULT_ENV, target: str = DEFAULT_TARGET, config: dict | None = None) -> Any:
    active_config = config or EXAMPLE_CONFIG
    try:
        return active_config[env][target]
    except KeyError as exc:
        raise ValueError(f"Invalid env/target: {env}/{target}") from exc


def _get_spark(spark_session=None):
    if spark_session is not None:
        return spark_session
    try:
        return globals()["spark"]
    except KeyError as exc:
        raise RuntimeError(
            "Spark session was not provided and global 'spark' was not found. "
            "Run this inside Fabric/Spark or pass spark_session explicitly."
        ) from exc


def lakehouse_table_read(lh, tablename, spark_session=None):
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not tablename:
        raise ValueError("tablename is required.")
    spark_obj = _get_spark(spark_session)
    path = f"{lh.root}/Tables/{tablename}"
    return spark_obj.read.format("delta").load(path)


def lakehouse_table_write(
    df,
    lh,
    tablename,
    mode="append",
    partition_by=None,
    repartition_by=None,
    overwrite_schema=True,
):
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not tablename:
        raise ValueError("tablename is required.")

    normalized_mode = str(mode or "").lower().strip()
    if normalized_mode not in {"append", "overwrite", "errorifexists", "ignore"}:
        raise ValueError("mode must be one of append, overwrite, errorifexists, ignore.")

    path = f"{lh.root}/Tables/{tablename}"

    if repartition_by is not None:
        if isinstance(repartition_by, (list, tuple)):
            if len(repartition_by) > 0 and isinstance(repartition_by[0], int):
                df = df.repartition(repartition_by[0], *repartition_by[1:])
            else:
                df = df.repartition(*repartition_by)
        elif isinstance(repartition_by, int):
            df = df.repartition(repartition_by)
        else:
            df = df.repartition(repartition_by)

    writer = df.write.mode(normalized_mode).format("delta")

    if partition_by is not None:
        if isinstance(partition_by, (list, tuple)):
            writer = writer.partitionBy(*partition_by)
        else:
            writer = writer.partitionBy(partition_by)

    if overwrite_schema:
        writer = writer.option("overwriteSchema", "true")

    writer.save(path)


def lakehouse_csv_read(lh, relative_path, spark_session=None, header=True):
    spark_obj = _get_spark(spark_session)
    path = f"{lh.root}/{relative_path}"
    return spark_obj.read.option("header", header).csv(path)


def warehouse_read(env, target, schema, table, config=None, spark_session=None):
    spark_obj = _get_spark(spark_session)
    p = get_path(env, target, config=config)
    import com.microsoft.spark.fabric
    from com.microsoft.spark.fabric.Constants import Constants

    return (
        spark_obj.read.option(Constants.WorkspaceId, p.workspace_id)
        .option(Constants.DatawarehouseId, p.house_id)
        .synapsesql(f"{p.house_name}.{schema}.{table}")
    )


def warehouse_write(df, env, target, schema, table, mode="append", config=None):
    p = get_path(env, target, config=config)
    import com.microsoft.spark.fabric
    from com.microsoft.spark.fabric.Constants import Constants

    (
        df.write.mode(mode)
        .option(Constants.WorkspaceId, p.workspace_id)
        .option(Constants.DatawarehouseId, p.house_id)
        .synapsesql(f"{p.house_name}.{schema}.{table}")
    )


def single_file_ns_to_us(local_in_path, local_out_path, verbose=True):
    import pyarrow as pa
    import pyarrow.parquet as pq

    try:
        if verbose:
            print(f"Reading with pyarrow: {local_in_path}")
            print(f"Writing us timestamps to: {local_out_path}")
        pdf = pd.read_parquet(local_in_path, engine="pyarrow")
        table = pa.Table.from_pandas(pdf, preserve_index=False)
        pq.write_table(
            table,
            local_out_path,
            coerce_timestamps="us",
            allow_truncated_timestamps=True,
        )
        if verbose:
            print(f"done: {local_out_path}")
    except Exception as exc:
        print(f"FAILED converting ns to us for file {local_in_path}: {exc}")


def lakehouse_parquet_read_as_spark(lh, relative_path, verbose=True, spark_session=None):
    spark_obj = _get_spark(spark_session)

    orig_spark_path = "Files/" + relative_path
    lakehouse_prefix = "/lakehouse/default/"
    parts = relative_path.split("/")
    if len(parts) < 2:
        raise ValueError("relative_path should look like folder/folder2/file.parquet")

    tsus_dir = parts[:-2] + [parts[-2] + "_tsus"]
    tsus_relative_path = "/".join(tsus_dir + [parts[-1]])
    tsus_spark_path = "Files/" + tsus_relative_path

    orig_local_path = lakehouse_prefix + orig_spark_path
    tsus_local_path = lakehouse_prefix + tsus_spark_path

    if verbose:
        print(f"Try Spark read: {orig_spark_path}")
    try:
        df = spark_obj.read.parquet(orig_spark_path)
        _ = df.limit(1).collect()
        if verbose:
            print("SUCCESS: Spark read original path.")
        return df
    except Exception:
        pass

    for try_convert in range(2):
        if verbose:
            tag = " after single-file convert" if try_convert else ""
            print(f"Try Spark read: {tsus_spark_path}{tag}")

        try:
            df = spark_obj.read.parquet(tsus_spark_path)
            _ = df.limit(1).collect()
            if verbose:
                print("SUCCESS: Spark read _tsus path.")
            return df
        except Exception as exc:
            msg = str(exc)
            path_not_found = (
                "[PATH_NOT_FOUND]" in msg
                or "Path does not exist" in msg
                or "No such file or directory" in msg
            )
            if try_convert == 0 and path_not_found:
                if verbose:
                    print("PATH NOT FOUND for _tsus parquet. Will convert one file and retry.")
                try:
                    mssparkutils.fs.mkdirs("/".join(tsus_dir))
                except Exception:
                    pass
                single_file_ns_to_us(
                    local_in_path=orig_local_path,
                    local_out_path=tsus_local_path,
                    verbose=verbose,
                )
            else:
                if verbose:
                    print(f"FAILED: Spark read _tsus path. Exception: {exc}")
                break

    raise RuntimeError("Failed to read from both original and _tsus paths.")


def lakehouse_excel_read_as_spark(lh, relative_path, sheet_name=0, spark_session=None):
    spark_obj = _get_spark(spark_session)
    lakehouse_file_path = f"{lh.root}/{relative_path}"

    bin_df = (
        spark_obj.read.format("binaryFile")
        .option("recursiveFileLookup", "false")
        .load(lakehouse_file_path)
    )

    if bin_df.count() == 0:
        raise FileNotFoundError(f"No file found at path: {lakehouse_file_path}")

    content = bin_df.select("content").collect()[0][0]
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    with open(temp_file.name, "wb") as f:
        f.write(bytearray(content))

    pandas_df = pd.read_excel(temp_file.name, sheet_name=sheet_name)
    return spark_obj.createDataFrame(pandas_df)


NOTEBOOK_PREFIX_LIST = [
    "edlh_bronze_to_dex_source",
    "edlh_silver_to_dex_source",
    "edlh_gold_to_dex_source",
    "dex_byod_to_dex_source",
    "dex_source_to_dex_unified",
    "dex_unified_to_dex_product",
]


def _get_fabric_runtime_context():
    try:
        from notebookutils import runtime

        return runtime.context
    except Exception:
        return {}


def check_naming_convention(notebook_name=None, allowed_prefixes=None, fail_on_error=True):
    prefixes = allowed_prefixes or NOTEBOOK_PREFIX_LIST

    if notebook_name is None:
        context = _get_fabric_runtime_context()
        notebook_name = context.get("currentNotebookName")

    if not notebook_name:
        message = "Notebook name is unavailable. Pass notebook_name or run inside Fabric."
        if fail_on_error:
            raise ValueError(message)
        return {
            "notebook_name": None,
            "compliant": False,
            "allowed_prefixes": prefixes,
            "message": message,
        }

    notebook_name_normalized = notebook_name.lower()
    match = any(notebook_name_normalized.startswith(prefix) for prefix in prefixes)
    status = "comply" if match else "failed - please follow standard naming convention for notebook"

    print(f"Notebook name: {notebook_name_normalized}")
    print(f"Naming convention check: {status}\n")

    df = pd.DataFrame({"No": list(range(1, len(prefixes) + 1)), "Allowed Prefix": prefixes})
    print("Standard Naming Convention Prefix List:")
    print(df.to_string(index=False))

    if not match and fail_on_error:
        raise ValueError(
            f"Notebook name '{notebook_name_normalized}' does not comply with naming conventions. "
            "Please use one of the standard prefixes listed above."
        )

    return {
        "notebook_name": notebook_name_normalized,
        "compliant": match,
        "allowed_prefixes": prefixes,
        "message": status,
    }


def clean_datetime_columns(df, datetime_col, prefix, tz_region="Asia/Singapore", time_block_col="TIME_BLOCK_30_MIN"):
    if datetime_col not in df.columns:
        raise ValueError(f"Column not found: {datetime_col}")

    from pyspark.sql.functions import from_utc_timestamp, to_date, date_format, expr

    dt_utc_name = f"{prefix}_DTM_UTC8"
    dt_date_name = f"{prefix}_DATE_UTC8"
    dt_time_name = f"{prefix}_TIME_UTC8"

    df = df.withColumn(dt_utc_name, from_utc_timestamp(df[datetime_col], tz_region))
    df = df.withColumn(dt_date_name, to_date(df[dt_utc_name]))
    df = df.withColumn(dt_time_name, date_format(df[dt_utc_name], "HH:mm"))
    df = df.withColumn(
        time_block_col,
        date_format(
            expr(
                f"timestampadd(MINUTE, floor(minute({dt_utc_name})/30)*30-MINUTE({dt_utc_name}), {dt_utc_name})"
            ),
            "HH:mm",
        ),
    )
    return df


def add_system_technical_columns(df, hash_col, bucket_size=512, run_id=None, notebook_name=None, loaded_by=None):
    if hash_col not in df.columns:
        raise ValueError(f"Column not found: {hash_col}")

    if bucket_size not in {128, 256, 512, 1024}:
        raise ValueError("bucket_size must be one of 128, 256, 512, or 1024.")

    from pyspark.sql.functions import (
        from_utc_timestamp,
        current_timestamp,
        lit,
        abs as F_abs,
        hash as F_hash,
        monotonically_increasing_id,
    )

    context = _get_fabric_runtime_context()
    resolved_notebook_name = notebook_name or context.get("currentNotebookName", "local_notebook")
    resolved_loaded_by = loaded_by or context.get("userName", "local_user")
    ingest_run_id = run_id or str(uuid.uuid4())

    df = df.withColumn("pipeline_ts", from_utc_timestamp(current_timestamp(), "Asia/Singapore"))
    df = df.withColumn("notebook_name", lit(resolved_notebook_name))
    df = df.withColumn("loaded_by", lit(resolved_loaded_by))
    df = df.withColumn("p_bucket", F_abs(F_hash(hash_col)) % bucket_size)
    df = df.withColumn("sample_bucket", F_abs(F_hash(hash_col)) % 1000000)
    df = df.withColumn("row_ingest_id", monotonically_increasing_id())
    df = df.withColumn("ingest_run_id", lit(ingest_run_id))
    return df


def pass_if_yes_else_run(condition, code):
    if str(condition).lower() == "yes":
        return None
    exec(code)
    return None


def ODI_METADATA_LOGGER(df, tablename: str, exclude_columns=None, run_timestamp_timezone="Asia/Singapore"):
    from pyspark.sql import functions as F

    technicalcol = {
        "pipeline_ts",
        "notebook_name",
        "loaded_by",
        "p_bucket",
        "sample_bucket",
        "row_ingest_id",
        "ingest_run_id",
    }

    if exclude_columns:
        technicalcol.update(exclude_columns)

    eligible_columns = [c for c, _ in df.dtypes if c not in technicalcol]
    if not eligible_columns:
        raise ValueError("No eligible non-technical columns found for metadata profiling.")

    row_count = df.count()
    agg_exprs = []

    for c, t in df.dtypes:
        if c in technicalcol:
            continue

        agg_exprs.append(F.sum(F.col(c).isNull().cast("int")).alias(f"{c}_NULL_COUNT"))
        agg_exprs.append(F.countDistinct(F.col(c)).alias(f"{c}_DISTINCT_COUNT"))

        if t in ("int", "bigint", "double", "float", "decimal", "timestamp", "date"):
            agg_exprs.append(F.min(F.col(c)).alias(f"{c}_MIN"))
            agg_exprs.append(F.max(F.col(c)).alias(f"{c}_MAX"))

    agg_df = df.agg(*agg_exprs)

    rows = []
    for c, t in df.dtypes:
        if c in technicalcol:
            continue

        rows.append(
            agg_df.select(
                F.lit(tablename).alias("TABLE_NAME"),
                F.from_utc_timestamp(F.current_timestamp(), run_timestamp_timezone).alias("RUN_TIMESTAMP"),
                F.lit(c).alias("COLUMN_NAME"),
                F.lit(t).alias("DATA_TYPE"),
                F.lit(row_count).alias("ROW_COUNT"),
                F.col(f"{c}_NULL_COUNT").alias("NULL_COUNT"),
                F.round((F.col(f"{c}_NULL_COUNT").cast("double") / F.lit(row_count)) * 100, 3).alias("NULL_PERCENT"),
                F.col(f"{c}_DISTINCT_COUNT").alias("DISTINCT_COUNT"),
                F.round((F.col(f"{c}_DISTINCT_COUNT").cast("double") / F.lit(row_count)) * 100, 3).alias("DISTINCT_PERCENT"),
                F.col(f"{c}_MIN").cast("string").alias("MIN_VALUE") if f"{c}_MIN" in agg_df.columns else F.lit(None).cast("string").alias("MIN_VALUE"),
                F.col(f"{c}_MAX").cast("string").alias("MAX_VALUE") if f"{c}_MAX" in agg_df.columns else F.lit(None).cast("string").alias("MAX_VALUE"),
            )
        )

    df_profile = rows[0]
    for r in rows[1:]:
        df_profile = df_profile.unionByName(r)

    return df_profile


def transformation_summary(transformation_details):
    if isinstance(transformation_details, str):
        try:
            transformation_details = ast.literal_eval(transformation_details)
        except (ValueError, SyntaxError):
            return transformation_details

    if isinstance(transformation_details, dict):
        lines = []
        for key, value in transformation_details.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    return str(transformation_details)


def transformation_reasons(step_name=None, reason=None, context=None):
    runtime_context = context or _get_fabric_runtime_context()
    payload = {
        "step_name": step_name,
        "reason": reason,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_date_local": (datetime.now(timezone.utc) + timedelta(hours=8)).date().isoformat(),
        "notebook_name": runtime_context.get("currentNotebookName", "local_notebook"),
        "run_hash": hashlib.sha256(f"{step_name}|{reason}".encode("utf-8")).hexdigest()[:16],
    }
    return payload
