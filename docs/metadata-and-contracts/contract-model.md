# Contract model

## Page purpose

This page defines what a data contract means in FabricOps and how to reason about it during design and review.

## What is a data contract?

A data contract is the agreement that makes a dataset safe to use. It defines what the data should contain, how it may be used, which quality checks must pass, who approved it, and what downstream users or pipelines can rely on.

| Question | Why it matters |
| --- | --- |
| What dataset are we using or producing? | Identifies the exact source or output table. |
| What is the approved usage? | Prevents reuse outside the approved purpose. |
| What columns should exist? | Catches schema changes early. |
| Which columns are required? | Prevents silent missing critical fields. |
| What are the business keys and grain? | Makes joins, deduplication, and row meaning clear. |
| What data quality rules must pass? | Stops bad data from flowing downstream unnoticed. |
| Which columns are sensitive? | Supports classification, masking, and governance review. |
| Who approved the contract? | Gives ownership and accountability. |
| What happened during the run? | Supports audit, lineage, troubleshooting, and handover. |

## Open Data Contract Standard (ODCS) and FabricOps

The Open Data Contract Standard (ODCS) is a structured way to describe data contracts, commonly as YAML or JSON. It covers schema definitions, quality expectations, ownership, governance metadata, and contract versioning.

FabricOps uses ODCS as design inspiration for interoperability and governance clarity, but not as a YAML-first runtime requirement. FabricOps follows the spirit of ODCS while using a table-first operational model so contracts can be reviewed, queried, governed, and enforced inside Microsoft Fabric.

## Why FabricOps is not YAML-first

YAML is useful for Git-based workflows and portability. A YAML or JSON version of the contract can be added as an interoperability layer.

FabricOps does not make YAML the primary runtime editing model because many Fabric teams operate through notebooks, Spark DataFrames, Lakehouse tables, Warehouse tables, and Power BI stewardship views.

FabricOps therefore uses a Fabric-native flow:

1. Exploration notebooks profile data and draft contract candidates.
2. Humans review and approve the contract content.
3. Approved contract metadata is stored in Fabric metadata tables.
4. Pipeline notebooks load approved metadata and enforce it.
5. YAML or JSON export can be added later when cross-platform exchange is needed.

## One contract model, two perspectives

FabricOps uses one contract model with two perspectives.

| Perspective | What it means | Examples |
| --- | --- | --- |
| Input expectations | What the pipeline expects from the source before it can run safely | Source object, required columns, business keys, freshness, minimum quality thresholds |
| Output expectations | What the pipeline promises to produce for downstream users | Target object, output schema, descriptions, classifications, approved DQ rules, consumer-facing metadata |

> **One contract model, two perspectives.** Input expectations protect the pipeline. Output expectations protect downstream consumers.
