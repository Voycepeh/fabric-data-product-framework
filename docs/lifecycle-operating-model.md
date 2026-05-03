# Lifecycle Operating Model

![FabricOps Starter Kit canonical lifecycle workflow](assets/mvp-flow.png)

FabricOps Starter Kit uses one canonical 10-step lifecycle workflow across docs, templates, and execution guidance.

## 3-row lifecycle framing

- **Row 1: Setup (Steps 1 to 4)**
- **Row 2: Core work (Steps 5 to 7)**
- **Row 3: AI enhancements (Steps 8 to 10)**

Actor colors used in the workflow image:

- **Grey = Human-led**
- **Blue = Starter kit / engineering**
- **Green = AI-assisted**

## Canonical 10-step lifecycle

1. **Define purpose, approved usage & governance ownership**  
   Actor: **Governance**
2. **Configure runtime, environment & path rules**  
   Actor: **Starter kit**
3. **Declare source contract & ingest source data**  
   Actor: **Starter kit**
4. **Validate source against contract & capture metadata**  
   Actor: **Starter kit**
5. **Explore data & capture transformation / DQ rationale**  
   Actor: **Analyst / Data scientist notebook**
6. **Build production transformation & write target output**  
   Actor: **Data engineer notebook**
7. **Validate output & persist target metadata**  
   Actor: **Starter kit**
8. **Generate, review & configure DQ rules**  
   Actor: **AI-assisted + human review**
9. **Generate & review classification / sensitivity suggestions**  
   Actor: **AI-assisted + human review**
10. **Generate data lineage and handover documentation**  
    Actor: **AI-assisted handover document generation**

## Source contract powers drift validation

The source contract is the expectation layer. It defines expected schema, keys, refresh pattern, freshness, volume, and acceptable values.

The source profile is the observation layer. It captures what actually arrived in the current run.

Drift validation is the comparison layer. It checks expectation (contract) versus reality (profile) and flags schema, freshness, key, volume, and value drift before downstream publication.

## Operating principles

- **Governance first:** purpose, approved usage, and ownership are defined before transformation work.
- **Starter kit handles repeated engineering work:** runtime setup, contract checks, profiling, validation, and metadata capture are standardized.
- **AI enhances, humans decide:** AI drafts DQ, classification, lineage, and handover outputs; human reviewers approve governance and DQ decisions.

## Related pages

- [Quick Start](quick-start.md)
- [Architecture](architecture.md)
- [Notebook template workflow](workflows/fabric-notebook-template.md)
