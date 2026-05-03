# Fabric notebook runtime helpers

This framework keeps **GitHub as the source of truth** and treats the **Fabric notebook as the execution environment**.

The helpers in `fabric_data_product_framework.runtime` and `fabric_data_product_framework.fabric_io` provide a lightweight way to standardize runtime setup now, without waiting for full engine features.

## Recommended notebook startup pattern

1. Create runtime context at the top of every notebook.
2. Validate notebook naming convention before expensive reads/writes.
3. Build table identifiers and call adapter-based read/write helpers.

```python
from fabric_data_product_framework.runtime import (
    assert_notebook_name_valid,
    build_runtime_context,
)
from fabric_data_product_framework.fabric_io import build_table_identifier, read_table, write_table

ctx = build_runtime_context(
    dataset_name="synthetic_orders",
    environment="dev",
    source_table="source.synthetic_orders",
    target_table="product.synthetic_orders",
    notebook_name="03_pc_email_metadata_source_to_unified",
)

assert_notebook_name_valid(
    ctx["notebook_name"],
)

source_identifier = build_table_identifier(schema="source", table="synthetic_orders")
target_identifier = build_table_identifier(schema="product", table="synthetic_orders")

# Wrap your team-specific Fabric helpers.
df = read_table(source_identifier, reader=my_fabric_reader)
write_table(df, target_identifier, writer=my_fabric_writer, mode="append")
```

## Why adapters for read/write

`read_table` and `write_table` are adapter helpers. They intentionally do not call Fabric-specific APIs directly. Teams can wrap existing lakehouse helper functions and keep code reusable across projects.

This PR intentionally does not implement real Fabric APIs because teams may use different lakehouse helper functions and notebook utility wrappers.
