# Fabric Data Product Framework

A metadata-first, AI-in-the-loop, Fabric-first framework for building handover-ready data products.

AI proposes. Humans approve. The framework validates, logs, and packages artifacts for handover.

## MVP workflow

1. Define data product
2. Setup config and environment
3. Declare source and ingest data
4. Profile source and capture metadata
5. Explore data
6. Explain transformation logic
7. Build transformation pipeline
8. AI generate DQ rules from metadata, profile, and context
9. Human review DQ rules
10. AI suggest sensitivity labels
11. Human review and governance gate
12. AI generated lineage and transformation summary
13. Handover framework pack

### Role split
- **Human led:** 1, 5, 6, 9, 11
- **Framework led:** 2, 3, 4, 7, 13
- **AI assisted:** 8, 10, 12

> Steps 8, 10, and 12 are AI-assisted drafts and require human approval before production use.

## Start here
- Lifecycle model and flowchart: [docs/lifecycle-operating-model.md](docs/lifecycle-operating-model.md)
- Detailed step-by-step workflow: [docs/mvp-workflow.md](docs/mvp-workflow.md)
- Fabric executable checklist: [docs/fabric-smoke-test.md](docs/fabric-smoke-test.md)
- Capability implementation status: [docs/capability-status.md](docs/capability-status.md)
- Callable Function Reference: [src/README.md](src/README.md)
