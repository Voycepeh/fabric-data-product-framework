# MVP 13-step roadmap

This roadmap defines the canonical lifecycle for the MVP notebook flow used in Microsoft Fabric.

## Canonical flow

| Step | Name | Owner | Primary outputs | Supporting module group | Planned cleanup PR |
|---|---|---|---|---|---|
| 1 | Package and runtime setup | framework | `runtime_context` | Runtime + Fabric IO (`runtime.py`, `fabric_io.py`) | Runtime/Fabric alignment PR |
| 2 | Fabric config and paths | human | `fabric_config`, `path_context` | Config + Fabric IO (`config.py`, `fabric_io.py`) | Runtime/Fabric alignment PR |
| 3 | Pull source data | framework | `source_dataframe` | Fabric IO (`fabric_io.py`) | Runtime/Fabric alignment PR |
| 4 | Source profiling | framework | `source_profile` | Profiling + metadata (`profiling.py`) | Profiling/metadata cleanup PR |
| 5 | AI assisted DQ rule drafting | ai_assisted | `draft_dq_rules` | AI quality + rule compile (`ai_quality_rules.py`, `rule_compiler.py`) | DQ workflow cleanup PR |
| 6 | Human review of rules and metadata | human | `approved_dq_rules`, `approved_metadata_notes` | Rule compile + metadata (`rule_compiler.py`, `metadata.py`) | DQ workflow cleanup PR |
| 7 | Compile and run DQ checks | framework | `compiled_dq_rules`, `dq_results` | Quality + rule compile (`quality.py`, `rule_compiler.py`) | DQ workflow cleanup PR |
| 8 | Schema/profile/data drift checks | framework | `drift_results` | Drift + incremental (`drift.py`, `incremental.py`) | Drift/incremental cleanup PR |
| 9 | Core transformation | mixed | `transformed_dataframe` | Transformation orchestration (`fabric_io.py`, `contracts.py`) | Transformation patterns cleanup PR |
| 10 | Standard technical columns | framework | `output_with_technical_columns` | Technical columns (`technical_columns.py`, `fabric_io.py`) | Technical columns cleanup PR |
| 11 | Write output and profile output | framework | `target_write_result`, `output_profile` | Fabric IO + profiling + metadata | Output write/profile cleanup PR |
| 12 | Governance classification and lineage | mixed | `governance_labels`, `lineage_records` | Governance + lineage (`governance.py`, `lineage.py`, `ai_lineage_summary.py`) | Governance/lineage cleanup PR |
| 13 | Run summary and handover package | framework | `run_summary`, `handover_package` | Run summary + metadata (`run_summary.py`, `metadata.py`) | Run summary/handover cleanup PR |

## Source of truth files

- MVP execution template: `templates/notebooks/fabric_data_product_mvp.py`
- Registry and artifact validation: `src/fabric_data_product_framework/mvp_steps.py`

## Scope note

This roadmap PR defines lifecycle structure only. Module-by-module consolidation is intentionally deferred to follow-up cleanup PRs listed above.
