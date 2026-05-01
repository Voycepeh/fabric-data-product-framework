# Capability Status (aligned to MVP workflow)

| MVP step | Status | Notes |
|---|---|---|
| Define data product | Partial | Pattern exists in docs/templates; no strict contract-capture orchestrator yet. |
| Setup config and environment | Implemented | Runtime/context/config helpers are available in `src/`. |
| Declare source and ingest data | Implemented | Core table read and source declaration patterns exist. |
| Profile source and capture metadata | Implemented | Profiling and metadata flatten/write helpers are callable. |
| Explore data | Pattern only | Human-driven notebook pattern; no enforced framework API. |
| Explain transformation logic | Partial | Transformation summary helpers exist; rationale enforcement is light. |
| Build transformation pipeline | Pattern only | Framework helpers exist, but transformation logic remains user-authored. |
| AI generate DQ rules from metadata, profile, and context | Implemented | MVP AI DQ candidate callables exist with parser/normalizer flow. |
| Human review DQ rules | Partial | Review workflow documented; approval registry is not fully productized. |
| AI suggest sensitivity labels | Partial | Governance classification scaffolding exists; full AI suggestion flow is incomplete. |
| Human review and governance gate | Partial | Review/gate pattern exists; strict workflow automation is limited. |
| AI generated lineage and transformation summary | Partial | Lineage and summary builders exist; full AI-assisted auto-capture is still evolving. |
| Handover framework pack | Partial | Core records/builders exist; one-command export bundle is still partial. |

## Status legend
- **Implemented**: callable and usable now.
- **Partial**: some callable support exists, but not fully end-to-end.
- **Pattern only**: documented notebook pattern, little/no packaged callable orchestration.
- **Not implemented**: currently unavailable.
