# Metadata and Data Contract Assembly

![Data contract assembly from approved metadata evidence](assets/data-contract.png)

## 1. What it is

FabricOps does not treat the data contract as one manually maintained document.

The contract is assembled from approved metadata, pipeline evidence, quality results, lineage, and governance context.

## 2. Metadata-backed source of truth

The metadata/contract store is the source of truth:

- `contracts`
- `contract_columns`
- `contract_rules`
- `quality_results`
- `lineage_records`

## 3. Role ownership

| Role | Ownership |
| --- | --- |
| Governance steward | Approved usage, business context, classification, sensitivity/PII |
| Analyst / data scientist | Profiling interpretation and DQ rule validation |
| Data engineer | Deterministic pipeline enforcement and evidence writing |
| Handover / data contract | Generated from approved metadata-backed records |

## 4. AI touchpoints

- Governance metadata: AI suggests, human approves.
- DQ rules: AI applies/suggests candidates, human validates rule validity.
- Handover: AI generates from approved metadata and evidence; no human needed for generation.

## 5. Handover/export target

The assembled contract output is exportable to Open Data Contract-compatible YAML/JSON.

Recommended runtime entrypoints:

- `generate_handover_contract(...)` to assemble approved metadata-backed handover packages.
- `export_handover_contract(...)` to write reusable YAML/JSON handover exports.

## 6. Core operational loop

Step 5 → Step 2: pipeline execution produces evidence, and that evidence improves governance metadata and future agreement quality.

## 7. Related pages

- [Notebook Structure](notebook-structure.md)
- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Notebook Structure](notebook-structure.md)
- [Assembled Contract Model](metadata-and-contracts/contract-model.md)
- [Metadata Tables](metadata-and-contracts/metadata-tables.md)
