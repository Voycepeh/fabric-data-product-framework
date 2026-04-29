# Capability Status

This page is the canonical public status view for framework capabilities.

## Implemented
- Dataset contract schema load/validation helpers.
- DataFrame profiling utilities (pandas + Spark-aware paths).
- Schema snapshot and schema drift comparison.
- Incremental safety snapshot and comparison helpers.
- Data quality execution and quality gate helpers.
- Runtime contract validation helpers.
- Run summary and lineage record builders.
- AI-assist helper utilities for DQ-rule and transformation-summary prompt/parse flows.

## Pattern/template
- Human approval workflow pattern (documented, not a full app-backed workflow).
- Fabric notebook adapter pattern for read/write/metadata persistence.
- Quarantine routing pattern with rule-type coverage limits.

## Fabric only
- Notebook runtime execution with PySpark.
- Lakehouse/OneLake read/write and notebookutils-dependent integrations.
- Fabric AI function calls used from notebook code.

## Planned
- Governance labeling checks and enforcement helpers.
- Broader AI context export helpers.
- Expanded quarantine coverage across all rule patterns.

See implementation-oriented detail in [framework-status.md](framework-status.md).
