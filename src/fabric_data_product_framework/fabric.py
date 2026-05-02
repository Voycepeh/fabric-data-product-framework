"""Lightweight Fabric adapter helpers that avoid runtime-specific dependencies."""

from __future__ import annotations

VALID_WRITE_MODES = {"append", "overwrite", "merge"}


def build_table_identifier(
    lakehouse: str | None = None,
    schema: str | None = None,
    table: str | None = None,
) -> str:
    """Build table identifier.

    Run `build_table_identifier`.

    Parameters
    ----------
    lakehouse : str | None, optional
        Parameter `lakehouse`.
    schema : str | None, optional
        Parameter `schema`.
    table : str | None, optional
        Parameter `table`.

    Returns
    -------
    result : str
        Return value from `build_table_identifier`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> build_table_identifier(lakehouse, schema)
    """
    parts = [part for part in [lakehouse, schema, table] if part]
    if not parts:
        raise ValueError("At least one identifier component is required (table, schema.table, or lakehouse.schema.table).")
    return ".".join(parts)


def read_table(table_identifier: str, reader=None):
    """Read table.

    Run `read_table`.

    Parameters
    ----------
    table_identifier : str
        Parameter `table_identifier`.
    reader : object, optional
        Parameter `reader`.

    Returns
    -------
    result : object
        Return value from `read_table`.

    Raises
    ------
    NotImplementedError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> read_table(table_identifier, reader)
    """
    if reader is None:
        raise NotImplementedError(
            "No table reader provided. Inject a Fabric-compatible reader function, for example a notebook helper wrapper."
        )
    return reader(table_identifier)


def validate_write_mode(mode: str) -> str:
    """Validate write mode.

    Run `validate_write_mode`.

    Parameters
    ----------
    mode : str
        Parameter `mode`.

    Returns
    -------
    result : str
        Return value from `validate_write_mode`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> validate_write_mode(mode)
    """
    normalized_mode = (mode or "").strip().lower()
    if normalized_mode not in VALID_WRITE_MODES:
        raise ValueError("Invalid write mode. Expected one of: append, overwrite, merge.")
    return normalized_mode


def write_table(df, table_identifier: str, writer=None, mode: str = "append", **options):
    """Write table.

    Run `write_table`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    table_identifier : str
        Parameter `table_identifier`.
    writer : object, optional
        Parameter `writer`.
    mode : str, optional
        Parameter `mode`.

    Returns
    -------
    result : object
        Return value from `write_table`.

    Raises
    ------
    NotImplementedError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> write_table(df, table_identifier)
    """
    normalized_mode = validate_write_mode(mode)
    if writer is None:
        raise NotImplementedError(
            "No table writer provided. Inject a Fabric-compatible writer function, for example a notebook helper wrapper."
        )
    return writer(df, table_identifier, mode=normalized_mode, **options)


# --- merged from fabric_notebook.py ---

from dataclasses import dataclass
from typing import Any, Dict
from datetime import datetime, timezone
from pathlib import Path
import uuid
import tempfile
import hashlib
import ast

import pandas as pd

from fabric_data_product_framework.technical_columns import add_system_technical_columns, clean_datetime_columns
from fabric_data_product_framework.profiling import ODI_METADATA_LOGGER
from fabric_data_product_framework.lineage import transformation_reasons, transformation_summary
from fabric_data_product_framework.runtime import assert_notebook_name_valid


@dataclass(frozen=True)
class Housepath:
    """Housepath.

    Public class used by the framework API for `Housepath`.

    Examples
    --------
    >>> Housepath(... )
    """
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


def load_fabric_config(path: str | Path) -> dict[str, dict[str, Housepath]]:
    """Load fabric config.

    Run `load_fabric_config`.

    Parameters
    ----------
    path : str | Path
        Parameter `path`.

    Returns
    -------
    result : dict[str, dict[str, Housepath]]
        Return value from `load_fabric_config`.

    Raises
    ------
    FileNotFoundError
        Raised when input validation or runtime checks fail.
    ImportError
        Raised when input validation or runtime checks fail.
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> load_fabric_config(path)
    """
    try:
        import yaml
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required to load Fabric config files. Install with `pip install pyyaml`."
        ) from exc

    config_path = Path(path)
    if not config_path.exists():
        path_str = str(path)
        if path_str.startswith("Files/") or path_str.startswith("Files\\"):
            config_path = Path("/lakehouse/default") / path_str
        if not config_path.exists():
            raise FileNotFoundError(f"Missing config file: {path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    environments = raw.get("environments")
    if not isinstance(environments, dict) or not environments:
        raise ValueError("Missing environments mapping. Add a top-level 'environments:' section.")

    required = {"workspace_id", "house_id", "house_name", "root"}
    parsed: dict[str, dict[str, Housepath]] = {}
    for env_name, targets in environments.items():
        if not isinstance(targets, dict) or not targets:
            raise ValueError(f"Environment '{env_name}' must contain target mappings.")

        parsed[env_name] = {}
        for target_name, payload in targets.items():
            if not isinstance(payload, dict):
                raise ValueError(f"Missing target mapping for '{env_name}/{target_name}'.")
            missing = required - set(payload.keys())
            if missing:
                missing_fields = ", ".join(sorted(missing))
                raise ValueError(
                    f"Target '{env_name}/{target_name}' is missing required fields: {missing_fields}. "
                    "Required fields are workspace_id, house_id, house_name, root."
                )
            parsed[env_name][target_name] = Housepath(
                workspace_id=str(payload["workspace_id"]),
                house_id=str(payload["house_id"]),
                house_name=str(payload["house_name"]),
                root=str(payload["root"]),
            )

    return parsed


def get_path(
    env: str = DEFAULT_ENV,
    target: str = DEFAULT_TARGET,
    config: dict | None = None,
    use_example_config: bool = False,
) -> Any:
    """Get path.

    Run `get_path`.

    Parameters
    ----------
    env : str, optional
        Parameter `env`.
    target : str, optional
        Parameter `target`.
    config : dict | None, optional
        Parameter `config`.
    use_example_config : bool, optional
        Parameter `use_example_config`.

    Returns
    -------
    result : object
        Return value from `get_path`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> get_path(env, target)
    """
    if config is None:
        if not use_example_config:
            raise ValueError(
                "No Fabric config was provided. Load one with load_fabric_config(...) "
                "and pass config=config."
            )
        active_config = EXAMPLE_CONFIG
    else:
        active_config = config

    try:
        return active_config[env][target]
    except KeyError as exc:
        if env not in active_config:
            available_envs = ", ".join(sorted(active_config.keys())) or "<none>"
            raise ValueError(
                f"Environment '{env}' was not found in Fabric config. Available environments: {available_envs}."
            ) from exc
        available_targets = ", ".join(sorted(active_config[env].keys())) or "<none>"
        raise ValueError(
            f"Target '{target}' was not found under environment '{env}'. "
            f"Available targets: {available_targets}."
        ) from exc


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
    """Lakehouse table read.

    Run `lakehouse_table_read`.

    Parameters
    ----------
    lh : Any
        Parameter `lh`.
    tablename : Any
        Parameter `tablename`.
    spark_session : object, optional
        Parameter `spark_session`.

    Returns
    -------
    result : object
        Return value from `lakehouse_table_read`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> lakehouse_table_read(lh, tablename)
    """
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
    """Lakehouse table write.

    Run `lakehouse_table_write`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    lh : Any
        Parameter `lh`.
    tablename : Any
        Parameter `tablename`.
    mode : object, optional
        Parameter `mode`.
    partition_by : object, optional
        Parameter `partition_by`.
    repartition_by : object, optional
        Parameter `repartition_by`.
    overwrite_schema : object, optional
        Parameter `overwrite_schema`.

    Returns
    -------
    result : None
        Return value from `lakehouse_table_write`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> lakehouse_table_write(df, lh)
    """
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
    """Lakehouse csv read.

    Run `lakehouse_csv_read`.

    Parameters
    ----------
    lh : Any
        Parameter `lh`.
    relative_path : Any
        Parameter `relative_path`.
    spark_session : object, optional
        Parameter `spark_session`.
    header : object, optional
        Parameter `header`.

    Returns
    -------
    result : object
        Return value from `lakehouse_csv_read`.

    Examples
    --------
    >>> lakehouse_csv_read(lh, relative_path)
    """
    if not getattr(lh, "root", None):
        raise ValueError("lh.root is required.")
    if not relative_path:
        raise ValueError("relative_path is required.")
    spark_obj = _get_spark(spark_session)
    path = f"{lh.root}/{relative_path}"
    return spark_obj.read.option("header", header).csv(path)


def warehouse_read(env, target, schema, table, config=None, spark_session=None):
    """Warehouse read.

    Run `warehouse_read`.

    Parameters
    ----------
    env : Any
        Parameter `env`.
    target : Any
        Parameter `target`.
    schema : Any
        Parameter `schema`.
    table : Any
        Parameter `table`.
    config : object, optional
        Parameter `config`.
    spark_session : object, optional
        Parameter `spark_session`.

    Returns
    -------
    result : object
        Return value from `warehouse_read`.

    Examples
    --------
    >>> warehouse_read(env, target)
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
    """Warehouse write.

    Run `warehouse_write`.

    Parameters
    ----------
    df : Any
        Parameter `df`.
    env : Any
        Parameter `env`.
    target : Any
        Parameter `target`.
    schema : Any
        Parameter `schema`.
    table : Any
        Parameter `table`.
    mode : object, optional
        Parameter `mode`.
    config : object, optional
        Parameter `config`.

    Returns
    -------
    result : None
        Return value from `warehouse_write`.

    Examples
    --------
    >>> warehouse_write(df, env)
    """
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
    """Single file ns to us.

    Run `single_file_ns_to_us`.

    Parameters
    ----------
    local_in_path : Any
        Parameter `local_in_path`.
    local_out_path : Any
        Parameter `local_out_path`.
    verbose : object, optional
        Parameter `verbose`.

    Returns
    -------
    result : None
        Return value from `single_file_ns_to_us`.

    Examples
    --------
    >>> single_file_ns_to_us(local_in_path, local_out_path)
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
    """Lakehouse parquet read as spark.

    Run `lakehouse_parquet_read_as_spark`.

    Parameters
    ----------
    lh : Any
        Parameter `lh`.
    relative_path : Any
        Parameter `relative_path`.
    verbose : object, optional
        Parameter `verbose`.
    spark_session : object, optional
        Parameter `spark_session`.

    Returns
    -------
    result : object
        Return value from `lakehouse_parquet_read_as_spark`.

    Raises
    ------
    RuntimeError
        Raised when input validation or runtime checks fail.
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> lakehouse_parquet_read_as_spark(lh, relative_path)
    """
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
    """Lakehouse excel read as spark.

    Run `lakehouse_excel_read_as_spark`.

    Parameters
    ----------
    lh : Any
        Parameter `lh`.
    relative_path : Any
        Parameter `relative_path`.
    sheet_name : object, optional
        Parameter `sheet_name`.
    spark_session : object, optional
        Parameter `spark_session`.

    Returns
    -------
    result : object
        Return value from `lakehouse_excel_read_as_spark`.

    Raises
    ------
    FileNotFoundError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> lakehouse_excel_read_as_spark(lh, relative_path)
    """
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
    """Check naming convention.

    Run `check_naming_convention`.

    Parameters
    ----------
    notebook_name : object, optional
        Parameter `notebook_name`.
    allowed_prefixes : object, optional
        Parameter `allowed_prefixes`.
    fail_on_error : object, optional
        Parameter `fail_on_error`.

    Returns
    -------
    result : object
        Return value from `check_naming_convention`.

    Raises
    ------
    ValueError
        Raised when input validation or runtime checks fail.

    Examples
    --------
    >>> check_naming_convention(notebook_name, allowed_prefixes)
    """
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
    try:
        assert_notebook_name_valid(notebook_name_normalized, prefixes)
        match = True
    except Exception:
        match = False
    status = "comply" if match else "failed - please follow standard naming convention for notebook"

    print(f"Notebook name: {notebook_name_normalized}")
    print(f"Naming convention check: {status}\n")

    df = pd.DataFrame({"No": list(range(1, len(prefixes) + 1)), "Allowed Prefix": prefixes})
    print("Standard Naming Convention Prefix List:")
    print(df.to_string(index=False))

    if not match and fail_on_error:
        assert_notebook_name_valid(notebook_name_normalized, prefixes)

    return {
        "notebook_name": notebook_name_normalized,
        "compliant": match,
        "allowed_prefixes": prefixes,
        "message": status,
    }


def pass_if_yes_else_run(condition, code):
    """Pass if yes else run.

    Run `pass_if_yes_else_run`.

    Parameters
    ----------
    condition : Any
        Parameter `condition`.
    code : Any
        Parameter `code`.

    Returns
    -------
    result : object
        Return value from `pass_if_yes_else_run`.

    Examples
    --------
    >>> pass_if_yes_else_run(condition, code)
    """
    if str(condition).lower() == "yes":
        return None
    exec(code)
    return None
