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



These three lifecycle templates are supported only as `.ipynb` for Fabric notebook use.

## Contract strategy: Open Data Contract principles, Fabric-first execution

FabricOps follows Open Data Contract principles, but adapts authoring and enforcement for Microsoft Fabric.

FabricOps adopts Open Data Contract principles in a Fabric-first form. Contracts are authored and approved through notebooks/tables, stored as metadata tables for operational enforcement, and can later be exported/imported as ODCS YAML for open-standard portability.

In a Fabric-first workflow:
- Exploration notebooks help profile data and draft contract expectations.
- AI may suggest required columns, DQ rules, and classifications, but humans approve them.
- Approved contracts should be stored in Fabric metadata tables, not only in YAML files.
- Pipeline notebooks load the approved contract from metadata tables and enforce it.
- ODCS YAML is an optional import/export format for interoperability and Git-based workflows.

Recommended operational flow:
`02_ex` notebook -> profile source data -> draft contract as Python dict/table -> human/steward approval -> write approved contract to metadata tables

`03_pc` notebook -> load approved contract from metadata tables -> enforce required columns, DQ rules, classifications, business keys -> write output and metadata records

"Source input contract" means the minimum expectations the pipeline requires from upstream data. It does not mean FabricOps owns the upstream producer.

