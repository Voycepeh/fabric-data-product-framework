# Notebook Templates

This folder stores reusable Microsoft Fabric notebook templates that consume approved metadata and contracts.

## Included starter
- `fabric_data_product_mvp.py`: copy-pasteable Fabric MVP notebook starter aligned to the 13-step workflow.
- `fabric_data_product_mvp.md`: usage guide for the starter with safety and customization notes.

## MVP starter guarantees
- Starts with a clear parameter block.
- Defaults to `DRY_RUN = True` to avoid accidental production writes.
- Includes local/Fabric-safe synthetic sample branch for first execution.
- Includes explicit marker where users replace transformation logic.
- Keeps the sequence: profile → DQ → governance → lineage → handover.
- Provides concrete Copilot prompt blocks for DQ, governance, lineage, and handover.
- Ends with a final run summary cell.
- Clarifies “human fills this in” vs “framework generates this.”

Use metadata-driven parameters so notebook behavior stays consistent across domains.
