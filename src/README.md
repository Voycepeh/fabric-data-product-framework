# Source Scaffold

This `src/` scaffold captures the intended implementation areas for the AI-assisted Fabric framework.

This PR does **not** implement the full validation engine yet. It defines structure and responsibilities for future iterations.

Subfolders:
- `profiling/`: generate source data profiles
- `rule_generation/`: convert metadata and business requirements into suggested DQ rules
- `validation/`: execute approved rules
- `drift_detection/`: detect schema drift and data drift
- `governance_labeling/`: suggest and apply governance/sensitivity labels
- `documentation_generation/`: generate runbooks, test plans, and handover packs from metadata
