# Governance Operating Model

Governance is defined once, reused across environments, and improved through pipeline evidence.

## 1. What governance owns

Governance ownership includes:

- agreement
- approved usage
- business context
- ownership
- permissions
- restrictions
- classification
- sensitivity / PII
- approved DQ metadata

## 2. Where governance metadata lives

Governance metadata lives in a governance metadata lakehouse that is the source of truth for agreement-level metadata.

Sandbox, Dev/Test, and Prod environments read approved governance metadata from this source.

## 3. How environments use governance

- Environments load agreement context and approved metadata.
- Exploration notebooks propose metadata updates from profiling evidence.
- Pipeline contract notebooks load approved metadata and enforce it during execution.

## 4. AI in governance

- AI suggests classification, sensitivity, and PII candidates.
- Human governance stewards approve governance controls.
- AI does not approve governance controls.

## 5. Governance-engineering loop

Step 5 pipeline execution writes operational evidence.

That evidence feeds back to Step 2 governance metadata updates.

This Step 5 → Step 2 feedback is the core operational loop.

## 6. Related pages

- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Notebook Structure](notebook-structure.md)
- [Metadata and Data Contract Assembly](metadata-and-contracts.md)
- [Data Quality Rules System](data-quality-rules-system.md)
