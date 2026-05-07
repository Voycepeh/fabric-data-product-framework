# Notebook templates

This folder contains reusable notebook starters for Microsoft Fabric workflows.

## Lifecycle starter templates

- `00_env_config.ipynb`: shared setup notebook for governance context, runtime configuration creation, and startup checks (Step 1, Step 2A, Step 2B).
- `02_ex_agreement_topic.ipynb`: exploration notebook for source profiling, transformation rationale, AI-assisted suggestions, and human review decisions (Step 3, Step 4, Step 5, Step 8, Step 9).
- `03_pc_agreement_source_to_target.ipynb`: run-all-safe pipeline notebook for approved contract enforcement, quality controls, controlled output writes, metadata, and lineage handover (Step 1, Step 2B, Step 3, Step 6A–6D, Step 7, Step 10).
- `fabric_data_product_mvp.py`: existing MVP starter notebook template.
- `fabric_data_product_mvp.md`: usage notes aligned to the 10-step lifecycle flow.

## Clean split to follow

- `00_env_config` = shared setup notebook.
- `02_ex_*` = exploration-only notebook. AI outputs are advisory and must be human-approved.
- `03_pc_*` = enforcement pipeline notebook. Applies only approved rules/labels and writes controlled outputs.

## Important boundary

- Step 8 and Step 9 AI helpers belong in exploration notebooks.
- Production pipeline notebooks should enforce approved deterministic rules and contract checks, and should not make AI decisions during execution.

## Suggested usage

1. Run `00_env_config.ipynb` first to define `CONFIG` and verify startup readiness.
2. Use `02_ex_agreement_topic.ipynb` to profile and document exploratory decisions.
3. Transfer only approved rules/labels/contracts into `03_pc_agreement_source_to_target.ipynb`.
4. Keep exploration logic out of production pipeline execution.


> Note: `.py` versions are source-style exports for code review; `.ipynb` templates are the primary Fabric import format.
