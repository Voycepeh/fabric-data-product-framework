# FabricOps Starter Kit

A practical starter kit for building governed, quality-checked, AI-ready notebooks in Microsoft Fabric.

Quick Start and list of functions
[https://voycepeh.github.io/fabricops-kit/  ](https://voycepeh.github.io/FabricOps-Starter-Kit/)

FabricOps Starter Kit helps teams structure Microsoft Fabric notebooks with reusable configuration, runtime validation, profiling, quality checks, lineage, metadata logging, and handover patterns.

## Why this starter kit exists

![Before vs after using the starter kit](docs/assets/before-after.png)

Fabric notebooks often begin as analysis work, then slowly become recurring operational work. FabricOps Starter Kit gives that transition a clearer structure: reusable configuration, checks, governance review, lineage, and handover.

## What users get

![Benefits of the FabricOps Starter Kit](docs/assets/framework-benefits.png)

Governance and engineering work often gets repeated across every notebook: configuration, profiling, quality checks, sensitivity review, lineage, and handover. FabricOps Starter Kit turns those repeated steps into reusable patterns, with AI helping to draft the tedious parts while humans review the decisions that matter.

## How it fits into a Fabric data platform

![Generic data platform architecture](docs/assets/data-platform-architecture.png)

Fabric work often spans dev and prod environments, plus multiple lakehouses and warehouses. Since a Fabric notebook only has one default attached data store through the UI, the starter kit uses reusable configuration and code-based paths to make cross-store notebook work clearer and repeatable.

## Notebook operating model

![Workspace notebook setup](docs/assets/notebook-structure.png)

The notebooks share upstream context instead of standing alone. One environment config can support many agreements and notebooks, while one data sharing agreement can branch into many exploration and pipeline contract notebooks.

## Canonical lifecycle workflow

![FabricOps Starter Kit canonical lifecycle workflow](docs/assets/mvp-flow.png)

FabricOps Starter Kit uses a canonical **10-step lifecycle** with governance first, reusable starter-kit engineering steps in the middle, and AI-assisted enhancements at the end. Detailed step guidance lives in [Lifecycle Operating Model](docs/lifecycle-operating-model.md).

- Governance owns purpose, approved usage, and accountability first.
- Starter kit patterns handle repeated runtime, contract, validation, and metadata engineering work.
- AI-assisted steps help draft DQ rules, classification/sensitivity suggestions, and lineage/handover documentation, with human review of governance and DQ decisions.

## What problems it aims to solve?

| Problem | Starter kit response |
|---|---|
| Repetitive notebook setup and Fabric path handling | Reusable runtime/config and notebook workflow structure. |
| Profiling results are not reusable metadata | Profiling artifacts are captured as reusable metadata outputs. |
| Manual DQ rule writing is slow | AI-assisted and deterministic DQ candidate generation with human approval. |
| Schema drift, data drift, and incremental refresh risk | Drift/safety checks are integrated into the notebook workflow path. |
| Governance and sensitivity review are disconnected from execution | Governance suggestions and approval artifacts are included in the same workflow. |
| Handover is hard when logic lives only in notebooks | Lineage, run summaries, and handover pack artifacts are assembled for transfer. |

## DQX-inspired, Fabric-native
This starter kit takes inspiration from [Databricks Labs DQX](https://databrickslabs.github.io/dqx/docs/guide/ai_assisted_quality_checks_generation/) patterns (profiling, quality rule generation, quality check storage, check execution, and quarantine/summary metrics).

This repository adapts that pattern to Microsoft Fabric notebooks, Lakehouse/Warehouse, Fabric AI functions, and Copilot-style workflows.

## How does AI come into play?
AI helps draft DQ rules, sensitivity labels, lineage, transformation summaries, and handover notes.
We do it via creating functions within this starter kit that allow us to prompt the native [AI function](https://learn.microsoft.com/en-us/fabric/data-science/ai-functions/overview?tabs=pandas-pyspark%2Cpandas) or standardize prompts that we manually generate and paste into copilot.

### Microsoft Fabric AI Functions prerequisites
Fabric AI Functions are used as an optional AI in the loop layer for generating candidate metadata, quality rules, governance suggestions, and handover summaries from profiling evidence. They are not required for the deterministic core pipeline to run.

Requirements:
- Fabric Runtime 1.3 or later.
- Paid Fabric capacity F2 or higher, or P capacity.
- Tenant switch for Copilot / Azure OpenAI powered features enabled.
- See Microsoft Learn: [AI Functions overview](https://learn.microsoft.com/en-us/fabric/data-science/ai-functions/overview).

Dependency notes (runtime and DataFrame-type dependent):
- Pandas with Python runtime: install `synapseml_internal` and `synapseml_core` wheel dependencies plus `openai`.
- Pandas with PySpark runtime: install `openai`.
- PySpark DataFrame with PySpark runtime: no installation required.

Use the Microsoft Learn installation commands for your environment rather than pinning local versions unless Microsoft documentation requires specific versions.

The starter kit supports native Fabric AI Functions when available.
When Fabric AI Functions are unavailable, you can generate the same standardized prompts and manually paste them into Copilot or another LLM.
Human-reviewed outputs should then be stored back into starter-kit metadata or rules tables.
