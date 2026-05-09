# Data quality architecture (DQX-inspired, Fabric-native)

## Purpose

This page is the conceptual architecture source of truth for data quality in FabricOps Starter Kit.

FabricOps follows a DQX-inspired operating approach, implemented with Fabric-native notebooks, metadata, and runtime patterns.

## Core operating principle

- **AI suggests** candidate quality rules and supporting context.
- **Humans approve** (edit/reject/accept) before promotion.
- **Pipelines enforce** only approved rules during `03_pc` execution.

## Architecture responsibilities

### Design-time (human-led with AI assistance)

- Profile source data and gather business context.
- Generate candidate DQ rules.
- Perform steward/owner review and approvals.
- Persist approved rule metadata for execution.

### Run-time (pipeline enforcement)

- Load approved rule metadata.
- Execute checks deterministically in run-all-safe pipeline notebooks.
- Persist DQ results and failed-row/quarantine evidence.
- Persist summary metrics for monitoring, governance, and handover.

## Fabric-native persistence model

The architecture persists contract and quality evidence so it is queryable and auditable:

- approved rule metadata,
- per-run DQ results,
- failed-row/quarantine outputs,
- aggregated quality metrics and run summaries.

## Relationship to implementation guides

- Use [Data Quality Rules System](../workflows/data-quality-rules-system.md) for practical notebook usage.
- Use [Contract model](../metadata-and-contracts/contract-model.md) for conceptual contract scope.
- Use [Notebook Structure](../notebook-structure.md) for notebook role boundaries.
