# API surface policy

- **Essential**: callable helpers used in the standard `00 → 01 → 02 → 03` FabricOps workflow.
- **Optional**: supported helper utilities that are not required for the core workflow.
- **Internal**: implementation plumbing for framework internals, not intended for day-to-day notebook author usage.

## Naming convention

Public notebook-first names should be short, verb-first actions (for example `load_config`, `setup_notebook`, `read_lakehouse_table`, `enforce_dq`). Legacy names stay importable as compatibility aliases.

## TODO

- Review future business-context/governance additions against this policy before expanding the essential surface.
