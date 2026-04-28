# Framework Architecture

This architecture describes a reusable delivery system for Microsoft Fabric projects, not only a set of coding snippets.

## High-level components

- **Metadata templates**
  - Table registry, column dictionary, DQ rule registry, and contracts.
- **AI-assisted metadata generation**
  - AI drafts metadata and rule ideas from requirements and source profiling.
- **Validation engine**
  - Executes approved quality and contract checks in notebook/pipeline runtime.
- **Drift detection**
  - Detects schema drift and data drift against expected baselines.
- **Governance labeling**
  - Applies and audits sensitivity or governance classifications.
- **Pipeline enforcement**
  - Pipelines enforce approved checks before publishing curated outputs.
- **Central validation log**
  - Stores pass/fail outcomes, thresholds, and alert context.
- **Documentation generation**
  - Produces handover packs and operational docs from metadata + logs.

```mermaid
flowchart TB
    subgraph Inputs
        A[Business Requirements]
        B[Source Tables]
        C[Previous Reports]
        D[Stakeholder Notes]
    end

    subgraph AI_Assisted_Layer[AI-Assisted Layer]
        E[Metadata Drafting]
        F[DQ Rule Suggestion]
        G[Business Rule Translation]
        H[Documentation Drafting]
    end

    subgraph Human_Control[Human Control]
        I[Review Metadata]
        J[Approve Rules]
        K[Sign Off Contracts]
    end

    subgraph Metadata_Registry[Metadata Registry]
        L[Table Registry]
        M[Column Dictionary]
        N[DQ Rule Registry]
        O[Data Contract]
        P[Pipeline Contract]
    end

    subgraph Fabric_Runtime[Fabric Runtime]
        Q[Notebook Template]
        R[Pipeline Template]
        S[Validation Engine]
        T[Drift Detection]
    end

    subgraph Outputs
        U[Curated Data Product]
        V[Central Validation Log]
        W[Monitoring Dashboard]
        X[Generated Handover Pack]
    end

    A --> E
    B --> E
    B --> F
    C --> G
    D --> G

    E --> I
    F --> J
    G --> J
    H --> X

    I --> L
    I --> M
    J --> N
    K --> O
    K --> P

    L --> Q
    M --> Q
    N --> S
    O --> S
    P --> R

    Q --> R
    R --> S
    S --> T
    T --> U
    S --> V
    V --> W
    L --> X
    M --> X
    N --> X
    O --> X
    P --> X
```
