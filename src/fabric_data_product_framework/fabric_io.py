"""Fabric path and IO helpers.

This module contains the framework helpers used at the start and end of a
Fabric notebook workflow:

1. Validate Fabric lakehouse and warehouse configuration from a config notebook.
2. Resolve logical environment and target names into Fabric paths.
3. Read source data from lakehouse tables, lakehouse files, and warehouses.
4. Write curated outputs back to lakehouse tables or warehouses.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import tempfile

import pandas as pd

from .config import FrameworkConfig, PathConfig, load_fabric_config as load_framework_config


@dataclass(frozen=True)
class Housepath:
    """Fabric lakehouse or warehouse connection details.

    `Housepath` stores the minimum identifiers needed to read from or write to
    a Fabric lakehouse or warehouse using framework helpers.

    In normal use, define these values in a separate Fabric config notebook,
    validate the `CONFIG` mapping with `load_fabric_config`, then retrieve the
    required environment and target with `get_path`.

    Attributes
    ----------
    workspace_id : str
        Fabric workspace ID that contains the lakehouse or warehouse.
    house_id : str
        Fabric lakehouse or warehouse item ID.
    house_name : str
        Lakehouse or warehouse name.
    root : str
        ABFSS root path for the lakehouse or warehouse.

    Examples
    --------
    >>> lh = Housepath(
    ...     workspace_id="<workspace-id>",
    ...     house_id="<lakehouse-id>",
    ...     house_name="DEX_SB_SOURCE",
    ...     root="abfss://<workspace-id>@onelake.dfs.fabric.microsoft.com/<lakehouse-id>",
    ... )
    >>> lh.house_name
    'DEX_SB_SOURCE'
    """

    workspace_id: str
    house_id: str
    house_name: str
    root: str


DEFAULT_ENV = "Sandbox"
DEFAULT_TARGET = "Source"


def load_fabric_config(config: FrameworkConfig | dict) -> FrameworkConfig:
    """Validate and return a framework config mapping.

    This helper validates a user-maintained ``CONFIG`` object (for example from
    ``00_config``) and returns the normalized framework config. It does not
    create Fabric resources.
    """
    return load_framework_config(config)

def get_path(
    env: str = DEFAULT_ENV,
    target: str = DEFAULT_TARGET,
    config: dict | None = None,
) -> Housepath:
    """Return the Fabric path object for an environment and target.

    Use this after running the separate Fabric config notebook. The config
    notebook should define a `CONFIG` mapping, and this function resolves a
    logical environment/target pair such as `Sandbox/Source` into a `Housepath`.

    Parameters
    ----------
    env : str, default "Sandbox"
        Environment name in the config mapping.
    target : str, default "Source"
        Target name under the selected environment.
    config : dict
        Config mapping from the config notebook. Expected shape:
        `config[environment][target] = Housepath(...)`.

    Returns
    -------
    Housepath
        Fabric lakehouse or warehouse connection details.

    Raises
    ------
    ValueError
        If no config is provided, or if the selected environment or target is
        not available in the config.

    Examples
    --------
    >>> # %run 00_env_config
    >>> lh_source = get_path("Sandbox", "Source", config=CONFIG)
    >>> lh_unified = get_path("Sandbox", "Unified", config=CONFIG)
    >>> lh_source.house_name
    'DEX_SB_SOURCE'
    """
    if config is None:
        raise ValueError(
            "No Fabric config was provided. Run your config notebook first "
            "and pass config=CONFIG."
        )

    try:
        path_config = getattr(config, "path_config", None)
        if isinstance(config, dict) and path_config is None:
            path_config = config.get("path_config")
        if isinstance(path_config, PathConfig):
            paths = path_config.paths
        elif isinstance(path_config, dict):
            paths = path_config
        else:
            paths = config
        return paths[env][target]
    except KeyError as exc:
        path_config = getattr(config, "path_config", None)
        if isinstance(config, dict) and path_config is None:
            path_config = config.get("path_config")
        if isinstance(path_config, PathConfig):
            paths = path_config.paths
        elif isinstance(path_config, dict):
            paths = path_config
        else:
            paths = config

        if env not in paths:
            available_envs = ", ".join(sorted(paths.keys())) or "<none>"
            raise ValueError(
                f"Environment '{env}' was not found in Fabric config. "
                f"Available environments: {available_envs}."
            ) from exc

        available_targets = ", ".join(sorted(paths[env].keys())) or "<none>"
        raise ValueError(
            f"Target '{target}' was not found under environment '{env}'. "
            f"Available targets: {available_targets}."
        ) from exc


def _get_spark(spark_session=None):
    """Return an explicit Spark session or the active notebook global `spark`.

    Most Fabric notebooks already expose a global `spark` object. Tests and
    local scripts can pass `spark_session` explicitly to avoid relying on the
    notebook runtime.

    Parameters
    ----------
    spark_session : object, optional
        Spark session to use instead of the notebook global `spark`.

    Returns
    -------
    object
        Spark session object.

    Raises
    ------
    RuntimeError
        If no Spark session is passed and no global `spark` object exists.
    """
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
    """Read a Delta table from a Fabric lakehouse.

    This reads from the lakehouse `Tables/` area using the ABFSS root stored in
    a `Housepath`.

    Parameters
    ----------
    lh : Housepath
        Lakehouse path object returned by `get_path`.
    tablename : str
        Name of the table under the lakehouse `Tables/` folder.
    spark_session : object, optional
        Spark session to use. If omitted, the helper uses the notebook global
        `spark`.

    Returns
    -------
    pyspark.sql.DataFrame
        Spark DataFrame loaded from the Delta table.

    Raises
    ------
    ValueError
        If `lh.root` or `tablename` is missing.
    RuntimeError
        If no Spark session is available.

    Examples
    --------
    >>> lh_source = get_path("Sandbox", "Source", config=CONFIG)
    >>> df = lakehouse_table_read(lh_source, "RAW_ORDERS")
    """
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not tablename:
        raise ValueError("tablename is required.")

    spark_obj = _get_spark(spark_session)
    path = f"{lh.root.rstrip('/')}/Tables/{tablename}"
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
    """Write a Spark DataFrame to a Fabric lakehouse Delta table.

    This writes to the lakehouse `Tables/` area using the ABFSS root stored in
    a `Housepath`. Use this for saving curated source, unified, or product
    outputs from the MVP notebook workflow.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Spark DataFrame to write.
    lh : Housepath
        Lakehouse path object returned by `get_path`.
    tablename : str
        Target table name under the lakehouse `Tables/` folder.
    mode : str, default "append"
        Spark write mode. Supported values are `"append"`, `"overwrite"`,
        `"errorifexists"`, and `"ignore"`.
    partition_by : str or list[str], optional
        Column or columns used to physically partition the Delta table.
    repartition_by : int, str, list, or tuple, optional
        Optional repartitioning before write.
    overwrite_schema : bool, default True
        Whether to set Spark Delta `overwriteSchema=true` before saving.

    Returns
    -------
    None
        The DataFrame is written to the target Delta table path.

    Raises
    ------
    ValueError
        If `lh.root`, `tablename`, or `mode` is invalid.

    Examples
    --------
    >>> lh_unified = get_path("Sandbox", "Unified", config=CONFIG)
    >>> lakehouse_table_write(
    ...     df,
    ...     lh_unified,
    ...     "CLEAN_ORDERS",
    ...     mode="overwrite",
    ...     partition_by="p_bucket",
    ...     repartition_by=(200, "p_bucket"),
    ... )
    """
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not tablename:
        raise ValueError("tablename is required.")

    normalized_mode = str(mode or "").lower().strip()
    if normalized_mode not in {"append", "overwrite", "errorifexists", "ignore"}:
        raise ValueError("mode must be one of append, overwrite, errorifexists, ignore.")

    path = f"{lh.root.rstrip('/')}/Tables/{tablename}"

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
    """Read a CSV file from a Fabric lakehouse Files path.

    This reads from the lakehouse `Files/` area using the ABFSS root stored in
    a `Housepath`. The `relative_path` should be relative to the lakehouse root.

    Parameters
    ----------
    lh : Housepath
        Lakehouse path object returned by `get_path`.
    relative_path : str
        Path to the CSV file or folder under the lakehouse root, for example
        `"Files/raw/orders.csv"` or `"Files/raw/orders/"`.
    spark_session : object, optional
        Spark session to use. If omitted, the helper uses the notebook global
        `spark`.
    header : bool, default True
        Whether the first row of the CSV file contains column names.

    Returns
    -------
    pyspark.sql.DataFrame
        Spark DataFrame loaded from the CSV path.

    Raises
    ------
    ValueError
        If `lh.root` or `relative_path` is missing.
    RuntimeError
        If no Spark session is available.

    Examples
    --------
    >>> lh_source = get_path("Sandbox", "Source", config=CONFIG)
    >>> df = lakehouse_csv_read(lh_source, "Files/raw/orders.csv")
    """
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not relative_path:
        raise ValueError("relative_path is required.")

    spark_obj = _get_spark(spark_session)
    path = f"{lh.root.rstrip('/')}/{relative_path.lstrip('/')}"
    return spark_obj.read.option("header", header).csv(path)


def warehouse_read(env, target, schema, table, config=None, spark_session=None):
    """Read a table from a Microsoft Fabric warehouse.

    This uses Fabric Spark's `synapsesql` connector to read from a warehouse
    configured in the framework `CONFIG` mapping.

    Parameters
    ----------
    env : str
        Environment name in the config mapping, for example `"Sandbox"` or `"DE"`.
    target : str
        Warehouse target name under the selected environment, for example
        `"Warehouse"` or `"wh_Bronze"`.
    schema : str
        Warehouse schema name, for example `"dbo"`.
    table : str
        Warehouse table name.
    config : dict, optional
        Config mapping from the config notebook. Expected shape:
        `config[environment][target] = Housepath(...)`.
    spark_session : object, optional
        Spark session to use. If omitted, the helper uses the notebook global
        `spark`.

    Returns
    -------
    pyspark.sql.DataFrame
        Spark DataFrame loaded from the Fabric warehouse table.

    Raises
    ------
    RuntimeError
        If the Microsoft Fabric Spark connector is unavailable.
    ValueError
        If the selected environment or target is missing from the config.

    Examples
    --------
    >>> df = warehouse_read(
    ...     env="EDLH",
    ...     target="wh_Bronze",
    ...     schema="dbo",
    ...     table="Customer",
    ...     config=CONFIG,
    ... )
    """
    spark_obj = _get_spark(spark_session)
    p = get_path(env, target, config=config)

    try:
        import com.microsoft.spark.fabric
        from com.microsoft.spark.fabric.Constants import Constants
    except Exception as exc:
        raise RuntimeError(
            "This function must run inside Microsoft Fabric Spark with "
            "com.microsoft.spark.fabric available."
        ) from exc

    return (
        spark_obj.read.option(Constants.WorkspaceId, p.workspace_id)
        .option(Constants.DatawarehouseId, p.house_id)
        .synapsesql(f"{p.house_name}.{schema}.{table}")
    )


def warehouse_write(df, env, target, schema, table, mode="append", config=None):
    """Write a Spark DataFrame to a Microsoft Fabric warehouse table.

    This uses Fabric Spark's `synapsesql` connector to write to a warehouse
    configured in the framework `CONFIG` mapping.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Spark DataFrame to write.
    env : str
        Environment name in the config mapping, for example `"Sandbox"` or `"DE"`.
    target : str
        Warehouse target name under the selected environment, for example
        `"Warehouse"` or `"wh_Bronze"`.
    schema : str
        Warehouse schema name, for example `"dbo"`.
    table : str
        Warehouse table name.
    mode : str, default "append"
        Spark write mode, for example `"append"` or `"overwrite"`.
    config : dict, optional
        Config mapping from the config notebook. Expected shape:
        `config[environment][target] = Housepath(...)`.

    Returns
    -------
    None
        The DataFrame is written to the target warehouse table.

    Raises
    ------
    RuntimeError
        If the Microsoft Fabric Spark connector is unavailable.
    ValueError
        If the selected environment or target is missing from the config.

    Examples
    --------
    >>> warehouse_write(
    ...     df,
    ...     env="EDLH",
    ...     target="wh_Bronze",
    ...     schema="dbo",
    ...     table="Customer",
    ...     mode="append",
    ...     config=CONFIG,
    ... )
    """
    p = get_path(env, target, config=config)

    try:
        import com.microsoft.spark.fabric
        from com.microsoft.spark.fabric.Constants import Constants
    except Exception as exc:
        raise RuntimeError(
            "This function must run inside Microsoft Fabric Spark with "
            "com.microsoft.spark.fabric available."
        ) from exc

    (
        df.write.mode(mode)
        .option(Constants.WorkspaceId, p.workspace_id)
        .option(Constants.DatawarehouseId, p.house_id)
        .synapsesql(f"{p.house_name}.{schema}.{table}")
    )


def _convert_single_parquet_ns_to_us(local_in_path, local_out_path, verbose=True):
    """Convert one Parquet file from nanosecond to microsecond timestamps.

    Spark can fail to read some Parquet files that contain nanosecond timestamp
    precision. This helper reads one local Parquet file with PyArrow, rewrites
    it with microsecond timestamp precision, and saves it to a fallback path.

    This is an internal helper used by `lakehouse_parquet_read_as_spark`.

    Parameters
    ----------
    local_in_path : str
        Local input path to the original Parquet file.
    local_out_path : str
        Local output path for the converted Parquet file.
    verbose : bool, default True
        Whether to print conversion progress.

    Returns
    -------
    None
        The converted Parquet file is written to `local_out_path`.

    Examples
    --------
    >>> _convert_single_parquet_ns_to_us(
    ...     "/lakehouse/default/Files/raw/orders.parquet",
    ...     "/lakehouse/default/Files/raw_tsus/orders.parquet",
    ... )
    """
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
    """Read a Parquet file from a Fabric lakehouse Files path.

    This reads from the lakehouse `Files/` area using Spark. If Spark cannot
    read the original Parquet file because of timestamp precision issues, the
    helper tries a fallback `_tsus` path. If that fallback file does not exist,
    it converts the single local Parquet file from nanosecond to microsecond
    timestamps and retries the fallback path.

    Parameters
    ----------
    lh : Housepath
        Lakehouse path object returned by `get_path`.
    relative_path : str
        Path to the Parquet file under the lakehouse `Files/` folder, without
        the leading `"Files/"`. For example:
        `"raw/orders/orders_2026.parquet"`.
    verbose : bool, default True
        Whether to print read and fallback progress.
    spark_session : object, optional
        Spark session to use. If omitted, the helper uses the notebook global
        `spark`.

    Returns
    -------
    pyspark.sql.DataFrame
        Spark DataFrame loaded from the original or converted Parquet path.

    Raises
    ------
    ValueError
        If `relative_path` is not a nested file path.
    RuntimeError
        If neither the original path nor the converted fallback path can be
        read successfully.

    Examples
    --------
    >>> lh_source = get_path("Sandbox", "Source", config=CONFIG)
    >>> df = lakehouse_parquet_read_as_spark(
    ...     lh_source,
    ...     "raw/orders/orders_2026.parquet",
    ... )
    """
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not relative_path:
        raise ValueError("relative_path is required.")

    spark_obj = _get_spark(spark_session)

    relative_path = relative_path.lstrip("/")
    if relative_path.startswith("Files/"):
        relative_path = relative_path[len("Files/") :]

    orig_spark_path = f"Files/{relative_path}"
    lakehouse_prefix = "/lakehouse/default/"
    parts = relative_path.split("/")

    if len(parts) < 2:
        raise ValueError("relative_path should look like folder/file.parquet or folder/subfolder/file.parquet.")

    tsus_dir = parts[:-2] + [parts[-2] + "_tsus"]
    tsus_relative_path = "/".join(tsus_dir + [parts[-1]])
    tsus_spark_path = f"Files/{tsus_relative_path}"

    orig_local_path = f"{lakehouse_prefix}{orig_spark_path}"
    tsus_local_path = f"{lakehouse_prefix}{tsus_spark_path}"

    if verbose:
        print(f"Try Spark read: {orig_spark_path}")

    try:
        df = spark_obj.read.parquet(orig_spark_path)
        _ = df.limit(1).collect()
        if verbose:
            print("SUCCESS: Spark read original path.")
        return df
    except Exception as exc:
        if verbose:
            print(f"Original Parquet read failed. Will try fallback path. Exception: {exc}")

    for try_convert in range(2):
        tag = " after single-file convert" if try_convert else ""

        if verbose:
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

                _convert_single_parquet_ns_to_us(
                    local_in_path=orig_local_path,
                    local_out_path=tsus_local_path,
                    verbose=verbose,
                )
            else:
                if verbose:
                    print(f"FAILED: Spark read _tsus path. Exception: {exc}")
                break

    raise RuntimeError("Failed to read from both original and _tsus Parquet paths.")


def lakehouse_excel_read_as_spark(lh, relative_path, sheet_name=0, spark_session=None):
    """Read an Excel file from a Fabric lakehouse Files path.

    Spark does not natively read Excel files. This helper reads the Excel file
    as binary from the lakehouse, writes it to a temporary local file, loads it
    with pandas, then converts it into a Spark DataFrame.

    This is intended for small reference files, mapping tables, and manually
    maintained business inputs. Large source datasets should be stored as
    Delta, Parquet, or CSV instead.

    Parameters
    ----------
    lh : Housepath
        Lakehouse path object returned by `get_path`.
    relative_path : str
        Path to the Excel file under the lakehouse root, for example
        `"Files/reference/faculty_mapping.xlsx"`.
    sheet_name : str or int, default 0
        Worksheet name or index to read. Defaults to the first worksheet.
    spark_session : object, optional
        Spark session to use. If omitted, the helper uses the notebook global
        `spark`.

    Returns
    -------
    pyspark.sql.DataFrame
        Spark DataFrame converted from the selected Excel worksheet.

    Raises
    ------
    ValueError
        If `lh.root` or `relative_path` is missing.
    FileNotFoundError
        If the Excel file cannot be found at the resolved lakehouse path.
    RuntimeError
        If no Spark session is available.

    Examples
    --------
    >>> lh_source = get_path("Sandbox", "Source", config=CONFIG)
    >>> df_mapping = lakehouse_excel_read_as_spark(
    ...     lh_source,
    ...     "Files/reference/faculty_mapping.xlsx",
    ...     sheet_name="Mapping",
    ... )
    """
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not relative_path:
        raise ValueError("relative_path is required.")

    spark_obj = _get_spark(spark_session)
    lakehouse_file_path = f"{lh.root.rstrip('/')}/{relative_path.lstrip('/')}"

    bin_df = (
        spark_obj.read.format("binaryFile")
        .option("recursiveFileLookup", "false")
        .load(lakehouse_file_path)
    )

    if bin_df.count() == 0:
        raise FileNotFoundError(f"No file found at path: {lakehouse_file_path}")

    content = bin_df.select("content").collect()[0][0]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        temp_file.write(bytearray(content))
        temp_file_path = temp_file.name

    pandas_df = pd.read_excel(temp_file_path, sheet_name=sheet_name)
    return spark_obj.createDataFrame(pandas_df)


def _get_fabric_runtime_context():
    """Return the Fabric notebook runtime context when available.

    Fabric notebooks expose runtime metadata through `notebookutils.runtime`.
    This helper keeps that dependency optional so the module can still be
    imported in local tests or non-Fabric environments.

    Returns
    -------
    dict
        Fabric runtime context when running inside Fabric. Returns an empty
        dictionary when the context is unavailable.
    """
    try:
        from notebookutils import runtime

        return runtime.context
    except Exception:
        return {}


def check_naming_convention(notebook_name=None, allowed_prefixes=None, fail_on_error=True):
    """Check whether a Fabric notebook name starts with an allowed prefix.

    The allowed prefixes should come from the project config notebook, not from
    this module. This keeps naming policy configurable per project.

    Parameters
    ----------
    notebook_name : str, optional
        Notebook name to check. If omitted, the helper tries to read the
        current Fabric notebook name from `notebookutils.runtime`.
    allowed_prefixes : list[str] or tuple[str, ...]
        Prefixes that are valid for this project.
    fail_on_error : bool, default True
        If True, raise `ValueError` when the notebook name is unavailable or
        invalid. If False, return a result dictionary instead.

    Returns
    -------
    dict
        Validation result containing notebook name, compliance status, allowed
        prefixes, and message.

    Raises
    ------
    ValueError
        If `allowed_prefixes` is missing, the notebook name is unavailable, or
        the notebook name does not match any allowed prefix.

    Examples
    --------
    >>> # %run 00_env_config
    >>> check_naming_convention(allowed_prefixes=NOTEBOOK_PREFIX_LIST)
    """
    if not allowed_prefixes:
        message = "allowed_prefixes is required. Define it in your config notebook and pass it in."
        if fail_on_error:
            raise ValueError(message)
        return {
            "notebook_name": notebook_name,
            "compliant": False,
            "allowed_prefixes": [],
            "message": message,
        }

    prefixes = list(allowed_prefixes)

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
    prefixes_normalized = [prefix.lower() for prefix in prefixes]
    match = any(notebook_name_normalized.startswith(prefix) for prefix in prefixes_normalized)

    status = "comply" if match else "failed - please follow standard naming convention for notebook"

    print(f"Notebook name: {notebook_name_normalized}")
    print(f"Naming convention check: {status}\n")

    df = pd.DataFrame({"No": list(range(1, len(prefixes) + 1)), "Allowed Prefix": prefixes})
    print("Standard Naming Convention Prefix List:")
    print(df.to_string(index=False))

    if not match and fail_on_error:
        raise ValueError(
            f"Notebook name '{notebook_name_normalized}' does not comply with naming conventions. "
            f"Allowed prefixes: {', '.join(prefixes)}"
        )

    return {
        "notebook_name": notebook_name_normalized,
        "compliant": match,
        "allowed_prefixes": prefixes,
        "message": status,
    }
