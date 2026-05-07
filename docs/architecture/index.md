# Architecture overview

FabricOps Starter Kit is a Fabric-native operating model for repeatable data product delivery. It combines local engineering discipline with notebook-first execution so teams can move from exploration to governed production handover without changing platforms.

## The end-to-end story

1. **Develop locally in VS Code.**
   Engineers build and test reusable logic in the Python package, alongside contracts and documentation.
2. **Build the wheel.**
   The package is built as a wheel so the same tested code can be installed in Fabric.
3. **Install in a Fabric Environment.**
   Fabric Environments pin the framework and dependencies for consistent notebook execution.
4. **Configure runtime context in `00_env_config`.**
   Notebook runs initialize environment-specific settings before pipeline logic begins.
5. **Run exploration notebooks.**
   Teams profile sources, inspect schemas, and capture context needed for data product decisions.
6. **Run pipeline contract notebooks.**
   Contract-driven notebooks validate source assumptions, apply transformation logic, and write outputs.
7. **Persist across Source, Unified, and Product stores.**
   Data flows from source-aligned ingestion to unified modeling and product-ready datasets.
8. **Capture metadata tables.**
   Profiling, schema state, lineage, DQ results, summaries, and run context are written as durable metadata.
9. **Maintain a DQ rule registry.**
   Candidate and approved rules are stored centrally and reused by execution notebooks.
10. **Keep AI in the loop with human accountability.**
    AI suggests rule candidates, classifications, summaries, and context packaging; humans approve before rules become enforceable.
11. **Enforce in pipelines.**
    Approved rules run during notebook pipelines, with failed rows and quality metrics persisted for auditability.
12. **Monitor through Warehouse or Power BI.**
    SQL-friendly monitoring views and BI models expose operational and governance status.
13. **Complete handover with documentation.**
    Teams publish run summaries and architecture-aware documentation for downstream owners.

## Core design principles

- **Fabric-native execution:** notebooks and Fabric storage are first-class, not afterthoughts.
- **Reusable logic, explicit orchestration:** package code handles repeatable logic while notebooks stay readable and operational.
- **AI-assisted, human-approved governance:** AI accelerates suggestion and summarization, but humans remain accountable for approval and enforcement decisions.
- **Monitoring by default:** metadata and DQ outputs are persisted in forms suitable for Warehouse SQL and Power BI.
- **Handover-friendly delivery:** architecture and run artifacts are organized so first-time readers can understand the operating model before diving into function-level references.

## Where to go next

- Read the **Storage model** page for responsibility boundaries across Lakehouse, Warehouse, files, environments, and notebooks.
- Read the **Data quality architecture** page for the AI-in-the-loop quality lifecycle and governance flow.
