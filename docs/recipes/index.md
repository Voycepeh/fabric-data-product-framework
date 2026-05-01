# Notebook recipes

These recipes are copy-paste notebook patterns aligned to the current
public callables in [src/README.md](../../src/README.md).

## Recipe list

- [Local-safe smoke recipe](local-safe-smoke.md): local pandas-safe profile, quality, governance, drift, and lineage smoke flow.
- [Fabric dry run recipe](fabric-dry-run.md): Fabric Lakehouse read/write with Spark DQ workflow and governance summary.
- [Contract-first one-call recipe](contract-first-one-call.md): run contract-driven execution via `run_data_product`.
- [Full metadata chaining recipe](profile-dq-governance-lineage-handover.md): profile → DQ workflow → governance → drift → lineage artifacts in one path.

## Function groups used

- Profiling: `profile_dataframe`, `summarize_profile`
- Data quality: `run_quality_rules` (local-safe), `run_dq_workflow` (Fabric/Spark)
- Governance: `classify_columns`, `summarize_governance_classifications`, `build_governance_classification_records`
- Contracts: `load_data_contract`, `validate_data_contract_shape`, `run_data_product`, `assert_data_product_passed`
- Drift: `check_profile_drift`, `summarize_drift_results`
- Lineage: `build_lineage_records`, `generate_mermaid_lineage`, `build_transformation_summary_markdown`

See full callable details in [src/README.md](../../src/README.md).
