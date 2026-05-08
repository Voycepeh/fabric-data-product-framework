# FabricOps Starter Kit

A practical starter kit for building governed, quality-checked, AI-ready notebooks in Microsoft Fabric.

<div align="center">

[![Open Documentation](https://img.shields.io/badge/Open%20Documentation-FabricOps%20Starter%20Kit-blue?style=for-the-badge)](https://voycepeh.github.io/FabricOps-Starter-Kit/)
.
.
</div>

## Why this starter kit exists

![Before vs after using the starter kit](docs/assets/before-after.png)

Fabric notebooks often begin as analysis work and then become recurring operations. This starter kit gives that transition a reusable structure for configuration, checks, governance review, lineage, and handover.

Read more: [Quick Start](https://voycepeh.github.io/FabricOps-Starter-Kit/quick-start/) · [Lifecycle Operating Model](https://voycepeh.github.io/FabricOps-Starter-Kit/lifecycle-operating-model/) · [Function Reference](https://voycepeh.github.io/FabricOps-Starter-Kit/reference/) · [Data contracts](https://voycepeh.github.io/FabricOps-Starter-Kit/metadata-and-contracts/)

## Design choices

### Fabric-first

FabricOps Starter Kit is inspired by open data contracts, DQX-style data quality checks, metadata registries, and lineage patterns, but adapts those ideas to Microsoft Fabric realities.

In Fabric, teams must operate across Lakehouses, Warehouses, OneLake paths, workspace separation, dev-to-prod promotion, and cross-store or cross-workspace movement that often needs explicit notebook code.

### Notebook-first

Many Fabric data products begin as notebooks. This kit does not try to replace notebooks with a full orchestration, governance, or data platform product; it makes notebooks more repeatable, reviewable, and handover-ready.

The model separates exploration notebooks that capture profiling, reasoning, and AI-assisted suggestions from pipeline notebooks that enforce approved logic, quality checks, classifications, and output contracts.

### Contract-first and metadata-first

Contracts are not standalone documents only. In this kit, contracts connect to notebook naming, approved usage, schema expectations, data quality rules, sensitivity review, metadata profiling, and output registration.

This pattern is inspired by open data contract approaches, adapted to Fabric-native storage and execution.

### DQX-inspired, Fabric-native quality checks

The quality-check model is inspired by DQX-style reusable rule definitions and rule application, but implemented for Fabric notebooks, Spark DataFrames, and metadata tables.

AI may help suggest rules, humans approve them, and pipeline notebooks enforce them.

### AI-in-the-loop

AI helps with repeated governance and engineering work such as metadata summaries, DQ rule suggestions, sensitivity classification suggestions, lineage drafting, and handover notes.

AI does not replace approval. Governance owners, data stewards, and engineers remain responsible for approved usage, classifications, quality rules, and production release decisions.

### Handover-first

The goal is not only to make one notebook run. The goal is to make the data product understandable to the next engineer, analyst, reviewer, or owner.

## What users get

![Benefits of the FabricOps Starter Kit](docs/assets/framework-benefits.png)

Reusable templates and callable functions for building governed Fabric notebook pipelines without rebuilding the same setup, profiling, quality, contract, lineage, and handover patterns each time.

<div align="center">

[![Runtime Config Template](https://img.shields.io/badge/Template-Runtime%20Config-blue?style=for-the-badge)](https://github.com/Voycepeh/FabricOps-Starter-Kit/tree/main/templates/notebooks/00_env_config.ipynb)
[![Pipeline Contract Template](https://img.shields.io/badge/Template-Pipeline%20Contract-blue?style=for-the-badge)](https://github.com/Voycepeh/FabricOps-Starter-Kit/tree/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb)
[![Exploration Notebook Template](https://img.shields.io/badge/Template-Exploration%20Notebook-blue?style=for-the-badge)](https://github.com/Voycepeh/FabricOps-Starter-Kit/tree/main/templates/notebooks/02_ex_agreement_topic.ipynb)

[![Function Reference](https://img.shields.io/badge/Reference-Callable%20Functions-purple?style=for-the-badge)](https://voycepeh.github.io/FabricOps-Starter-Kit/reference/)
</div>

These patterns are inspired by open data contracts and DQX, but intentionally adapted to Fabric.

## Scope

This is a Fabric-first notebook starter kit.
It is not a full data platform, orchestration system, or governance product.
