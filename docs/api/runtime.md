# Runtime API Reference

## Module purpose
`fabric_data_product_framework.runtime` builds run identifiers, enforces notebook naming rules, and creates a runtime context shared across notebook stages.

## Core public callables
- `generate_run_id(prefix="run")`
- `validate_notebook_name(name, allowed_prefixes)`
- `assert_notebook_name_valid(name, allowed_prefixes)`
- `build_runtime_context(dataset_name, environment, source_table, target_table, notebook_name=None, run_id=None)`

## Typical chaining
1. `generate_run_id`
2. `build_runtime_context`
3. pass context into profiling, quality, drift, lineage, and run-summary steps.
