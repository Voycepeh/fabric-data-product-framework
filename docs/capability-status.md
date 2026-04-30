# Capability Status

This page is the canonical status view for framework capabilities, gaps, and next priorities.

## Module capability status (MVP)

| Capability area | Current status | What exists now | What is missing | Build next |
|---|---|---|---|---|
| Product definition + run configuration | Implemented (core) | Notebook/runtime helpers, Fabric config loading, naming/runtime guardrails. | Rich policy packs for steward/usage approval workflows. | Add explicit policy templates for product sign-off and publish constraints. |
| Source contract declaration | Implemented (core) | Contract schema + validation helpers and example contract assets. | Stronger contract versioning/change-log helpers. | Add contract version diff utility and release note generator. |
| Ingest + profiling metadata | Implemented (core) | pandas/Spark-aware profiling and metadata record generation. | Profile registry/history querying helpers. | Add profile history compare API and baseline retrieval helpers. |
| AI-suggested DQ rules | Implemented (MVP) | AI prompt/parse helpers for DQ candidate generation and normalisation. | First-class approval registry API and scoring/rationale persistence. | Add approval-state model and reviewer audit metadata helpers. |
| Human-reviewed DQ contract | Pattern/template | Documented review pattern and rule compiler integration. | Opinionated workflow tooling for approve/edit/reject lifecycle. | Add lightweight approval workflow notebook utilities. |
| DQ execution gates | Implemented (core) | Rule execution, gate summaries, and run summary integration. | Wider rule-type coverage and richer exception routing. | Expand rules + quarantine patterns and add policy presets. |
| Schema drift checks | Implemented (core) | Schema snapshot and diff helpers with gate-ready output. | Automated mitigation playbooks and remediation recommendations. | Add drift action hints and configurable response policies. |
| Data drift + incremental safety | Implemented (core) | Incremental helpers and safety comparisons for runtime checks. | Broader statistical drift detectors and seasonal baseline handling. | Extend drift metrics and threshold templates by domain pattern. |
| Sensitivity/governance classification | Partial | Governance module scaffolding and metadata structures. | Full AI suggestion + human approval + enforcement pipeline. | Implement sensitivity suggestion helpers and governance gate checks. |
| Transform & explain | Partial | AI transformation summary workflow and run artefact capture. | Structured transformation rationale schema enforcement. | Add rationale schema validator + publish-ready summary formatter. |
| Standardise & write output | Implemented (core) | Technical/audit column helpers and Fabric write patterns. | More built-in partition strategy templates. | Add partition strategy presets and validation checks. |
| Validate output + handover pack | Implemented (core) | Run summary, lineage record builders, handover package guidance. | One-command handover bundle export utilities. | Add packaged export helper for summaries, lineage, DQ, governance notes. |
| Promote / consume readiness | Partial | Lifecycle docs and run artefacts that support promotion review. | Explicit promotion checklist automation and release gate scoring. | Add promotion-readiness checklist utility with pass/warn/fail scoring. |

## Notes
- “Implemented” means callable framework utilities are available in `src/`.
- “Partial” means some building blocks exist, but end-to-end workflow automation is incomplete.
- “Pattern/template” means the approach is documented, but not fully productised in code yet.

Implementation-oriented detail remains in [framework-status.md](framework-status.md).
