# Notebook recipes

Run the minimal end to end sample:
1. Run `00_env_config`.
2. Run `02_ex_agreement_topic` with `USE_SAMPLE_DATA = True`.
3. Run `03_pc_agreement_source_to_target` with `USE_SAMPLE_DATA = True`.

This proves the core flow: source read, profile, DQ suggestion, approved contract, contract driven DQ, valid/quarantine split, output write, and handover summary.

Templates are copy ready, not source ready. For real projects, replace source paths, target paths, contract values, transformation logic, approval details, and lineage notes.
