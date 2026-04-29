# Lifecycle Operating Model

This is the canonical lifecycle guide for how work moves between people, framework code, and Fabric runtime.

## Six-phase flow

1. **Outside Fabric preparation**
   - Confirm product purpose, steward, approved usage, caveats, and business context.
   - Prepare supporting inputs (mapping/reference files, assumptions, known exclusions).
2. **Inside Fabric human-guided setup and interpretation**
   - Set notebook parameters, load contract intent, declare source/target tables.
   - Review source profile outputs and capture EDA/data nuance notes.
3. **Framework-run checks and logging**
   - Execute deterministic profiling, schema drift, data drift/incremental safety, and metadata logging.
4. **AI-assisted drafting and summarisation**
   - Use evidence-based AI prompts to draft DQ candidates or transformation summaries.
   - Keep AI output as reviewable artifacts; do not treat chat history as a system of record.
5. **Human approval**
   - Approve/reject DQ candidates, review exceptions, and confirm release readiness.
6. **Framework enforcement and run artifacts**
   - Enforce quality and contract gates, apply technical columns/write pattern, and publish run outputs.

## Notebook journey mapped to lifecycle

| Notebook activity | Primary lane | Lifecycle phase |
|---|---|---|
| Purpose and approved usage section | Outside Fabric + Human-guided | 1, 2 |
| Notebook parameters | Human-guided | 2 |
| Source declaration | Human-guided | 2 |
| Source profiling | Framework-run | 3 |
| Schema drift / data drift / incremental safety | Framework-run | 3 |
| EDA notes and nuance explanation | Human-guided | 2, 5 |
| Transformation logic | Human-guided | 2 |
| Technical columns and write pattern | Framework-run | 6 |
| Output profiling | Framework-run | 3, 6 |
| DQ checks | Framework-run + Human-guided | 3, 5, 6 |
| Governance labels (where implemented) | Human-guided + Framework-run | 5, 6 |
| Contracts | Framework-run + Human-guided | 3, 5, 6 |
| Lineage | Framework-run + Human-guided | 6 |
| Run summary + AI context export | Framework-run + Human-guided | 6 |

## What the framework does automatically
- Profiles source/output datasets and formats metadata records.
- Runs schema drift and incremental safety gates.
- Runs quality rules and contract checks.
- Builds lineage, run summaries, and handover-ready structured artifacts.

## What humans still provide
- Business purpose, approved usage, caveats, and data interpretation.
- Dataset-specific transformation logic.
- Approval decisions for AI suggestions, exceptions, and release gating.

## AI role in this lifecycle
Use AI only as a bounded assistant within explicit artifacts.

- Canonical AI behavior and guardrails: [workflows/ai-generated-dq-rules.md](workflows/ai-generated-dq-rules.md)
- Transformation-summary workflow: [workflows/ai-transformation-summary.md](workflows/ai-transformation-summary.md)

**Boundary:** AI proposes. Humans approve. The framework validates and records.
