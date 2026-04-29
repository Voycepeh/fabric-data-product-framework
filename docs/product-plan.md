# Product Plan

## Vision

Build a lightweight, notebook-first framework for Microsoft Fabric that helps teams produce trusted, documented, and governed data products with a repeatable structure.

## Problem Statement

Many Fabric projects duplicate the same lifecycle work (profiling, drift checks, quality rules, lineage notes, and run reporting) in ad hoc notebooks. This leads to inconsistency, poor traceability, and slower delivery.

## Product Principles

1. Data First before AI First.
2. GitHub is the source of truth; Fabric is the execution environment.
3. Standardize the common 80% and preserve flexibility for the remaining 20%.
4. Make governance and documentation part of the notebook workflow, not an afterthought.
5. Prefer transparent, Python-first workflows.
6. Keep public artifacts synthetic and safe.

## Target Users

- Analytics engineers building reusable dataset pipelines
- Data engineers developing governed notebook workflows in Fabric
- Data scientists who need structured handoffs from exploration to productionized data products

## The 80/20 Reusable Framework Concept

- **80% reusable:** lifecycle scaffolding, metadata capture, quality/drift hooks, lineage and governance structure, and run summarization.
- **20% project-specific:** business logic, feature engineering, domain-specific transformations, exploratory nuance, and analytical judgement.

## Key Modules

- Dataset purpose and steward agreement
- Notebook environment setup
- Source profiling
- EDA notes
- Transformation pipeline
- Technical columns
- Output profiling
- Schema drift checks
- Data drift checks
- Incremental refresh safety checks
- Data quality rule engine
- Governance labeling
- Data contracts
- Lineage logging
- AI prompt pack and AI context export

## MVP Definition

The MVP provides:

- Public documentation for product direction and notebook lifecycle
- Initial architecture and metadata model proposal
- Synthetic dataset contract example
- Minimal Python package scaffold and placeholder modules

## Non-goals

- Full profiler implementation
- Production-grade drift engine implementation
- Complete rule execution engine
- Purview replacement
- Fabric deployment automation
- End-to-end catalog system

## Future Roadmap

1. Define dataset contract schema and validation
2. Implement basic source/output profiling
3. Write metadata output helpers for Lakehouse tables
4. Add technical columns helper utilities
5. Add schema drift, data drift, and incremental safety checks
6. Add quality rule execution engine and contract validation
7. Add observability integration and AI context refinement


## Engine-aware guidance

- Use pandas for small/local synthetic data, CSV/Excel prototyping, and unit tests.
- Use Spark for Fabric lakehouse-scale production workloads.
- Public dataframe APIs should accept `engine="auto" | "pandas" | "spark"`.
- Do not auto-convert Spark DataFrames to pandas.
