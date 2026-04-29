# Lifecycle Operating Model

This framework is an operating model and reusable notebook framework for building governed, quality-checked, handover-ready data products in Microsoft Fabric.

## Four actors

### Functional People
Business owners, data stewards, process owners, domain SMEs, and report consumers.
They own business meaning, usage, definitions, caveats, governance approval, and handover acceptance.

### Technical People
Data analysts, data scientists, data engineers, and Fabric developers.
They own source declaration, profiling interpretation, EDA, transformation logic, data contracts, DQ rules, and exception review.

### AI
Copilot / Fabric AI / ChatGPT-style assistant.
AI drafts, summarizes, recommends, explains, and generates candidate rules, labels, lineage, and handover context.
AI does not approve, govern, or sign off production readiness.

### Framework
Reusable notebooks, utilities, metadata tables, gates, and templates.
The framework runs profiling, logs metadata, executes drift checks, applies write patterns, validates contracts, executes DQ rules, and exports handover context.

Functional people define meaning. Technical people turn meaning into data products. AI accelerates documentation and reasoning. The framework makes the process repeatable, validated, and handover-ready.

## 15-step lifecycle

| Step | Stage | Primary actor | Where it happens |
|---:|---|---|---|
| 1 | Dataset purpose and steward agreement | Functional People | Governance doc / metadata table |
| 2 | Business metadata entry | Functional People | Metadata table / form |
| 3 | Governance labeling and usage controls | Functional People | Governance doc / metadata table |
| 4 | Data contract draft | Technical People | Contract file / notebook |
| 5 | Notebook parameters and source declaration | Technical People | Main pipeline notebook |
| 6 | Source profiling | Framework | Profiling notebook / utility |
| 7 | Source metadata logging | Framework | Metadata table |
| 8 | EDA notes and data nuance explanation | Technical People | Separate EDA notebook |
| 9 | Schema drift, data drift, and incremental safety checks | Framework | Checks notebook / reusable gate |
| 10 | Transformation pipeline | Technical People | Main pipeline notebook |
| 11 | Technical columns and write pattern | Framework | Main pipeline notebook |
| 12 | Output profiling | Framework | Profiling utility / metadata table |
| 13 | DQ rules and contract validation | Technical People + Framework | Checks notebook / pipeline gate |
| 14 | Lineage and transformation summary | Framework + AI + Technical People | Handover notebook |
| 15 | Handover package and AI context export | Framework + AI, accepted by Functional People | Handover notebook |

## Lifecycle flow

```mermaid
flowchart TD

subgraph FUNC["Functional People"]
    F1["1. Dataset purpose and steward agreement"]
    F2["2. Business metadata entry<br/>Definitions, metric meaning, usage examples, caveats"]
    F3["3. Governance labeling and usage controls"]
    F4["15. Accept handover package"]
end

subgraph TECH["Technical People"]
    T1["4. Data contract draft"]
    T2["5. Notebook parameters and source declaration"]
    T3["8. EDA notes and data nuance explanation<br/>Separate EDA notebook"]
    T4["10. Transformation pipeline<br/>Main pipeline notebook"]
    T5["13. Approve DQ rules and review exceptions"]
    T6["14. Review lineage and transformation summary"]
end

subgraph AI["AI"]
    A1["Assist purpose and metadata drafting"]
    A2["Recommend labels and contract expectations"]
    A3["Summarise source profile and EDA notes"]
    A4["Suggest DQ rules from profiles and metadata"]
    A5["Generate lineage explanation and handover narrative"]
end

subgraph FW["Framework"]
    W1["6. Run source profiling"]
    W2["7. Log source metadata"]
    W3["9. Run schema drift, data drift, and incremental safety checks"]
    W4["11. Apply technical columns and write pattern"]
    W5["12. Run output profiling"]
    W6["13. Execute DQ rules and contract validation"]
    W7["14. Capture lineage metadata"]
    W8["15. Export run summary and AI context package"]
end

F1 --> A1 --> F2
F2 --> A2 --> F3
F3 --> T1
T1 --> T2
T2 --> W1 --> W2
W2 --> A3 --> T3
T3 --> W3
W3 --> T4
T4 --> W4 --> W5
W5 --> A4 --> T5
T5 --> W6
W6 --> W7 --> A5 --> T6
T6 --> W8 --> F4

W3 -. "If drift or incremental risk is found" .-> T3
W6 -. "If DQ or contract validation fails" .-> T5
T6 -. "If lineage is unclear" .-> T4
F4 -. "If business context is incomplete" .-> F2
```

## Where work happens

- **Governance doc / metadata table** for purpose, steward, business metadata, labels, and business signoff.
- **Profiling notebook** for source profiling and source metadata logging.
- **Separate EDA notebook** for analyst interpretation, caveats, and assumptions.
- **Main pipeline notebook** for parameter setup, source declaration, transformation logic, technical columns, and write pattern.
- **Checks notebook / reusable gates** for drift checks, incremental safety, DQ rules, and contract validation.
- **Handover notebook** for lineage summary, run summary, AI context export, and final handover package.
