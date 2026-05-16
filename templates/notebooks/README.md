# Notebook templates

Run the minimal end-to-end sample in the canonical framework lifecycle:
1. `00_env_config` = runtime/environment paths and shared runtime configuration.
2. `01_da_agreement_template` = approved usage + agreement context + stewardship notes.
3. `02_ex_*` = exploration, profiling, AI-assisted proposals, and evidence capture for governance/pipeline handoff.
4. `03_pc_*` = deterministic enforcement from approved metadata.
5. Seed/create the sample source table (`minimal_source`) from generated rows in notebook code, then run `02_ex_agreement_topic` and `03_pc_agreement_pipeline_template` with `USE_SAMPLE_DATA = True`.

This proves the core flow: generated sample DataFrame -> persisted source table -> proposal evidence created in `02_ex` -> governance-approved metadata maintained in `01_da` -> approved metadata loaded/enforced in `03_pc` -> valid/quarantine split -> output write.

Templates are copy ready, not source ready. For real projects, replace source paths, target paths, contract values, transformation logic, approval details, and lineage notes.

Local metadata fallback is optional for local-only runs. Set `USE_LOCAL_SAMPLE_METADATA = True` in both `02_ex` and `03_pc` when you need local metadata artifacts under `samples/end_to_end/_output/metadata`.

## Template notebook purposes
- `01_da_agreement_template.ipynb`: Captures approved usage, business context, stewardship notes, and agreement-level governance context reused by AI-assisted DQ and governance workflows.
