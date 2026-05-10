# Minimal end-to-end sample assets

This sample follows the same lifecycle as the framework notebooks:

1. Run `00_env_config`.
2. Seed/create the sample source table (`minimal_source`) from generated rows in notebook code.
3. Run `02_ex_agreement_topic` with `USE_SAMPLE_DATA = True`.
   - In sample mode, the notebook seeds (or refreshes) `minimal_source` in the configured source lakehouse table.
   - `02_ex` creates the approved source-input contract and writes it to Fabric metadata.
4. Run `03_pc_agreement_source_to_target` with `USE_SAMPLE_DATA = True`.
   - `03_pc` reads the same `minimal_source` table and enforces the approved contract from step 3.

Notes:
- There is no checked-in `minimal_source.csv` fixture and no pre-seeded contract file.
- Local metadata fallback is optional for local-only runs. Set `USE_LOCAL_SAMPLE_METADATA = True` in both notebooks to read/write local sample metadata under `samples/end_to_end/_output/metadata`.
