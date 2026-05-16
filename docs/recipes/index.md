# Notebook recipes

## Minimal end-to-end sample

Run the minimal end-to-end sample in the canonical framework lifecycle:
1. Run `00_env_config`.
2. Seed/create the sample source table (`minimal_source`) from generated rows in notebook code.
3. Run `02_ex_agreement_topic` with `USE_SAMPLE_DATA = True`.
4. Run `03_pc_agreement_source_to_target` with `USE_SAMPLE_DATA = True`.

This proves the core flow: generated sample DataFrame -> persisted source table -> proposal evidence created in `02_ex` -> governance-approved metadata maintained in `01_da` -> approved metadata loaded/enforced in `03_pc` -> valid/quarantine split -> output write.

Templates are copy ready, not source ready. For real projects, replace source paths, target paths, contract values, transformation logic, approval details, and lineage notes.

## Available recipes

- [Local-safe smoke path](local-safe-smoke.md)
- [Fabric dry run path](fabric-dry-run.md)
- [Fabric notebook workflow smoke test recipe](fabric_mvp_smoke_test.md)
- [Wheel release checklist](mvp_wheel_release_checklist.md)
- [Contract-first one-call execution](contract-first-one-call.md)
- [Profile to DQ to governance to lineage to handover](profile-dq-governance-lineage-handover.md)

## How to use these recipes

1. Start with the local-safe smoke path if you want the fastest low-risk test.
2. Use the Fabric dry run path when validating setup inside Fabric.
3. Use the contract-first path when your contract is already defined.
4. Use the full chaining path when you want the metadata-first AI-in-the-loop workflow.

In this sample flow, there is no checked-in sample CSV or pre-seeded contract file: `02_ex` writes proposal evidence metadata (or local metadata fallback), then governance-approved metadata is consumed by `03_pc` for enforcement.
