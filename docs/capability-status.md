# Capability Status (MVP order)

Status values: **Implemented**, **Partial**, **Pattern only**, **Not implemented**.

| MVP step | Status | Notes |
|---|---|---|
| 1. Define data product | Pattern only | Driven by notebook/documentation pattern and context artifacts. |
| 2. Setup config and environment | Implemented | Runtime/context helpers and config loaders exist in `src/`. |
| 3. Declare source and ingest data | Implemented | Fabric adapter and ingest helpers are available. |
| 4. Profile source and capture metadata | Implemented | Profiling and metadata flatten/write helpers are available. |
| 5. Explore data | Pattern only | Human-led exploration notes pattern is documented. |
| 6. Explain transformation logic | Partial | Rationale/summary helpers exist; structured enforcement is limited. |
| 7. Build transformation pipeline | Pattern only | Notebook pattern + helpers; full opinionated pipeline module not packaged. |
| 8. AI generate DQ rules | Implemented | Candidate generation helpers exist, including Fabric AI-assisted path. |
| 9. Human review DQ rules | Pattern only | Review/approval flow documented; workflow tooling is lightweight. |
| 10. AI suggest sensitivity labels | Partial | Governance classification helpers exist but end-to-end AI review pipeline is incomplete. |
| 11. Human review and governance gate | Partial | Governance review artifacts/gates are possible but not fully productized. |
| 12. AI generated lineage and transformation summary | Partial | Lineage + transformation summary functions exist with human validation expected. |
| 13. Handover framework pack | Partial | Core summary/lineage artifacts exist; one-command full export remains partial. |
