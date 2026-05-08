# Notebook responsibilities

## `03_pc` is the executable contract

In FabricOps, the pipeline contract starts in the notebook. The `03_pc` notebook is the executable contract: it contains source/output expectations, quality rules, approved classification metadata to enforce, transformation logic, runtime checks, and evidence writing.

Metadata tables do not replace the notebook. They make notebook contract content queryable, reviewable, AI-readable, and auditable.

| Contract view | Meaning |
| --- | --- |
| `03_pc` notebook | Executable contract and enforcement logic |
| Metadata tables | Queryable contract records and run evidence |
| Handover document | Human narrative explaining why the pipeline exists and how to take over |
| Generated contract summary | Human- and AI-readable summary of approved contract state |

## `02_ex` and `03_pc` together

FabricOps extends a metadata-logger pattern into contract operations:

1. `02_ex` profiles a table and drafts metadata candidates.
2. Approved DQ and classification controls are attached to profiled columns.
3. `03_pc` enforces approved expectations in runtime.
4. The run stores quality results, schema snapshots, and runtime evidence.
5. Contract summaries and handover evidence are generated from stored metadata.

## Data contract vs handover document

A data contract and a handover document are related but not identical.

| Artifact | What it answers | Main reader | Stored as |
| --- | --- | --- | --- |
| Data contract | What must this dataset contain, what is approved, and what must be enforced? | Data engineer, steward, pipeline, AI assistant | Contract metadata records |
| Handover document | Why was the pipeline built this way, and how should a human take over? | Engineer, analyst, steward | Markdown or generated documentation |
| Metadata evidence | What happened during each run, and did the contract pass? | Pipeline owner, governance reviewer, AI assistant | Run, quality, and schema evidence tables |

Put simply: the handover document tells the story; `03_pc` executes the contract; and the data contract captures the enforceable metadata summary.
