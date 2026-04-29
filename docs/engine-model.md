# Engine Model

The framework supports three engine selectors for dataframe-facing APIs:

- `engine="auto"`: detect dataframe engine at runtime.
- `engine="pandas"`: force pandas execution.
- `engine="spark"`: reserve Spark execution path (planned for incremental implementation).

## Why pandas exists

Pandas is intentionally supported for:

- local/small synthetic datasets,
- CSV/Excel prototyping,
- laptop-first development,
- fast unit tests in public repositories.

## Why Spark matters in Fabric

Microsoft Fabric lakehouse workloads are expected to run on Spark for scale, distributed execution, and operational consistency.

## Auto detection

Engine detection is defensive and does not add a runtime PySpark dependency. Spark-like objects are detected via type/module/schema traits.

## No automatic `toPandas` rule

The framework does **not** automatically convert Spark DataFrames to pandas. This prevents accidental memory pressure, silent sampling mistakes, and hidden runtime cost.

## Future engine support

Additional engines can be added after public API stability and lifecycle standards are locked.

## Example API signatures

```python
profile_dataframe(df, dataset_name="orders", engine="auto")
profile_dataframe(df, dataset_name="orders", engine="pandas")
profile_dataframe(df, dataset_name="orders", engine="spark")
```
