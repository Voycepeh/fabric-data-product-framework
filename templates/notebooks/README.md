# Notebook templates

Run the minimal end-to-end sample in the canonical framework lifecycle:
1. Run `00_env_config`.
2. Run `01_data_agreement_template` to capture approved usage and agreement-level business context.
3. Seed/create the sample source table (`minimal_source`) from generated rows in notebook code.
4. Run `02_ex_agreement_topic` with `USE_SAMPLE_DATA = True`.
5. Run `03_pc_agreement_source_to_target` with `USE_SAMPLE_DATA = True`.

This proves the core flow: generated sample DataFrame -> persisted source table -> approved contract created in `02_ex` -> approved contract loaded/enforced in `03_pc` -> valid/quarantine split -> output write.

Templates are copy ready, not source ready. For real projects, replace source paths, target paths, contract values, transformation logic, approval details, and lineage notes.

Local metadata fallback is optional for local-only runs. Set `USE_LOCAL_SAMPLE_METADATA = True` in both `02_ex` and `03_pc` when you need local metadata artifacts under `samples/end_to_end/_output/metadata`.

## Template notebook purposes
- `01_data_agreement_template.ipynb`: Captures approved usage, business context, stewardship notes, and agreement-level governance context reused by AI-assisted DQ and governance workflows.
