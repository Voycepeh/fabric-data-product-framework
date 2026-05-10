# Minimal end-to-end sample assets

1. Run `00_env_config`.
2. Run `02_ex_agreement_topic` with `USE_SAMPLE_DATA = True`.
   This creates the approved contract and writes it to metadata or local sample metadata.
3. Run `03_pc_agreement_source_to_target` with `USE_SAMPLE_DATA = True`.
   This loads the approved contract from metadata (or local sample metadata fallback), not from a static fixture.
