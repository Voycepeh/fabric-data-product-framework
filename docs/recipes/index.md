# Notebook recipes

These recipes are copy-paste runnable notebook patterns built from the public callable surface in [src/README.md](../../src/README.md).

## Recipe list

- [Local-safe smoke recipe](local-safe-smoke.md): minimal local run with profiling, DQ, contracts, and lineage.
- [Fabric dry run recipe](fabric-dry-run.md): Fabric notebook dry run with Lakehouse paths and governance checks.
- [Contract-first one-call recipe](contract-first-one-call.md): execute the product through `run_data_product`.
- [Full metadata chaining recipe](profile-dq-governance-lineage-handover.md): profile → DQ → governance → drift → lineage artifacts in one flow.

## Function groups used

- Profiling: `run_profile_workflow`
- Data quality: `run_dq_workflow`, `run_dq_rules`
- Governance: `classify_columns`, `summarize_governance_classifications`
- Contracts: `load_data_contract`, `run_data_product`, `assert_data_product_passed`
- Drift: `check_schema_drift`, `check_profile_drift`, `summarize_drift_results`
- Lineage: `build_lineage_records`, `generate_mermaid_lineage`, `build_transformation_summary_markdown`

See full callable details in [src/README.md](../../src/README.md).
