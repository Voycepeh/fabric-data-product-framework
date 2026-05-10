# Metadata and Contracts

This section is the landing page for how FabricOps assembles a governed data contract.

A data contract is the agreed expectation for a dataset: what it is, how it may be used, what quality must pass, and what evidence proves it ran safely.

A FabricOps data contract is assembled from:

- environment configuration,
- approved usage,
- source/profile metadata,
- approved DQ rules,
- approved sensitivity/classification metadata,
- transformation logic,
- runtime evidence.

Use the pages below for details:

- [Contract model](metadata-and-contracts/contract-model.md)
- [Metadata tables](metadata-and-contracts/metadata-tables.md)
- [Notebook Structure](notebook-structure.md)
- [Data Quality Rules System](data-quality-rules-system.md)

## Storage and metadata scope

- Source, Unified, and Product stores hold business data.
- The metadata target holds framework evidence such as contracts, approved rules, profiling outputs, run evidence, and handover records.
- Metadata is environment-local, so dev and prod metadata remain separate.
