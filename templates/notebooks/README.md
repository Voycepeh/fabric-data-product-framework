# Notebook templates

Run the minimal end-to-end sample in the canonical framework lifecycle:
1. `00_env_config` = runtime/environment paths and shared runtime configuration.
2. `01_data_agreement_template` = approved usage + agreement context + stewardship notes.
3. `02_ex_*` = profile + AI draft + human approval + metadata write.
4. `03_pc_*` = deterministic enforcement from approved metadata.
5. `04_handover_data_contract_export` = generate metadata-backed handover package and export YAML/JSON.
6. Seed/create the sample source table (`minimal_source`) from generated rows in notebook code, then run `02_ex_agreement_topic`, `03_pc_agreement_source_to_target`, and `04_handover_data_contract_export` with matching metadata paths.

This proves the core flow: generated sample DataFrame -> persisted source table -> approved contract created in `02_ex` -> approved contract loaded/enforced in `03_pc` -> valid/quarantine split -> output write -> quality/lineage evidence write -> handover export package.

Templates are copy ready, not source ready. For real projects, replace source paths, target paths, contract values, transformation logic, approval details, and lineage notes.

Local metadata fallback is optional for local-only runs. Set `USE_LOCAL_SAMPLE_METADATA = True` in both `02_ex` and `03_pc` when you need local metadata artifacts under `samples/end_to_end/_output/metadata`.

## Template notebook purposes
- `01_data_agreement_template.ipynb`: Captures approved usage, business context, stewardship notes, and agreement-level governance context reused by AI-assisted DQ and governance workflows.
