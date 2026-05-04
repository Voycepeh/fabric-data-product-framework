# Lifecycle Operating Model

![FabricOps Starter Kit canonical lifecycle workflow](assets/mvp-flow.png)

FabricOps Starter Kit turns a Fabric data product workflow into a repeatable operating model: governance first, reusable engineering checks, AI-assisted data quality/classification/lineage, and handover documentation.

## How to use this page

Use this page as the control map for the full workflow:

1. Start from the lifecycle stage.
2. Open the matching notebook section.
3. Run the supporting function.
4. Produce the expected artefact.
5. Move only when the exit criteria are met.

## Lifecycle at a glance

| Step | Stage | Owner | Main output | Exit criteria |
|---|---|---|---|---|
| 1 | Governance | Governance | Purpose, approved usage, ownership | Use case and governance owner are clear |
| 2 | Runtime config | Starter kit | Environment config | Paths, workspace rules, prompts, and prefixes are configured |
| 3 | Source contract | Starter kit | Source contract and ingested source data | Expected schema, keys, freshness, and volume rules are declared |
| 4 | Source validation | Starter kit | Source profile, metadata, and drift validation result | Source is accepted or drift is flagged before transformation |
| 5 | Exploration | Analyst / data scientist | Exploration rationale | Transformation and DQ decisions are documented |
| 6 | Production transform | Data engineer | Target table/output | Production output is written with repeatable logic |
| 7 | Target validation | Starter kit | Target metadata and validation result | Output is profiled and validated for downstream use |
| 8 | AI-assisted DQ | AI + human review | Draft DQ rules and reviewed configuration | Human-reviewed DQ rules are ready to run |
| 9 | AI-assisted classification | AI + human review | Classification suggestions and reviewed sensitivity decisions | Sensitivity decisions are reviewed for enforcement or documentation |
| 10 | AI-assisted handover | AI + human review | Lineage summary and handover documentation | Product can be handed over or released |

## Step-by-step operating model

### 1. Define purpose, approved usage, and governance ownership

This guardrail step records why the data product exists, who owns it, what usage is approved, and which governance constraints apply.

**Output**
- Data product purpose
- Approved usage
- Governance owner
- Access or sensitivity notes

**Done when**
- The product has a clear business purpose
- The owner is known
- The team knows what the data can and cannot be used for

### 2. Configure runtime, environment, and path rules

This step standardizes how notebooks read, write, validate, and store metadata across environments. Configuration covers path rules, notebook prefixes, environment naming, and reusable prompt templates where needed.

**Output**
- Environment config
- Path and storage rules
- Notebook naming/prefix rules
- Reusable prompt templates

**Done when**
- The same workflow runs consistently across dev/prod-style environments
- Notebook naming and path conventions are reusable

### 3. Declare source contract and ingest source data

The source contract defines what the source should look like before downstream logic depends on it.

**Output**
- Source contract
- Ingested source data

**Done when**
- Expected schema, keys, freshness, volume, and key value rules are declared

### 4. Validate source against contract and capture metadata

The source profile captures what actually arrived. Drift validation compares contract expectations with profile observations before transformation.

**Output**
- Source profile
- Source metadata
- Drift validation result

**Done when**
- Schema, freshness, key, volume, and value drift are passed or flagged before transformation

### 5. Explore data and capture transformation / DQ rationale

Exploration helps analysts and data scientists test assumptions and explain why specific transformations and quality checks are required.

**Output**
- Exploration notes
- Transformation rationale
- DQ rationale

**Done when**
- The team can explain transformation logic and quality concerns before productionizing them

### 6. Build production transformation and write target output

This step converts exploration decisions into repeatable production transformation logic.

**Output**
- Production transformation notebook section
- Target table/output

**Done when**
- Output is written to the intended target using repeatable logic

### 7. Validate output and persist target metadata

The produced output is profiled and validated so downstream users know what was published and how it was checked.

**Output**
- Target profile
- Target validation result
- Persisted target metadata

**Done when**
- Output checks pass or are flagged, and metadata is stored for audit, lineage, and comparison

### 8. Generate, review, and configure DQ rules

AI assists by drafting DQ rules from contracts, profiles, and context. Humans review and approve before rule execution.

**Output**
- Draft DQ rules
- Reviewed DQ rule configuration

**Done when**
- AI-generated rules are reviewed and ready for execution

### 9. Generate and review classification / sensitivity suggestions

AI assists by proposing classification and sensitivity labels. Humans remain accountable for final decisions.

**Output**
- Classification suggestions
- Reviewed sensitivity decisions

**Done when**
- Sensitive fields and governance classifications are reviewed and ready for enforcement or documentation

### 10. Generate data lineage and handover documentation

AI assists by turning contracts, profiles, validations, and notebook context into handover-ready lineage and delivery documentation.

**Output**
- Data lineage summary
- Handover documentation

**Done when**
- Another team can understand source-to-target flow, checks, governance decisions, and operating handover expectations

## Source contract powers drift validation

- **Source contract** is the **expectation layer**.
- **Source profile** is the **observation layer**.
- **Drift validation** is the **comparison layer**.

Together they detect schema, freshness, key, volume, and value drift before downstream publication.

## Related pages

- [Quick Start](quick-start.md): run the workflow end to end.
- [Notebook Structure](notebook-structure.md): follow the notebook sequence.
- [Functions (`src/README.md`)](../src/README.md): inspect reusable callable utilities.
- [Architecture](architecture.md): understand environments, storage patterns, and platform flow.
