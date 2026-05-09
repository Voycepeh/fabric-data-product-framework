# Notebook templates

This folder contains the only supported user-facing templates for FabricOps Starter Kit in Microsoft Fabric.

## Supported lifecycle starters

- `00_env_config.ipynb`: environment and runtime setup starter (configuration, startup checks, and execution readiness).
- `02_ex_agreement_topic.ipynb`: exploration starter for profiling, AI-assisted suggestions, and human review/approval decisions.
- `03_pc_agreement_source_to_target.ipynb`: pipeline contract starter for enforcing approved deterministic rules, running DQ checks, writing outputs, and capturing metadata/lineage handover evidence.

These three notebooks are the plug-and-play lifecycle entry points. No additional template folders or placeholder files are required.

## AI boundary (required)

- Exploration (`02_ex`) may use AI for suggestions and analyst support.
- Pipeline enforcement (`03_pc`) must apply only approved deterministic rules and contract checks.
- AI should not make runtime production decisions inside enforcement execution.

## Usage sequence

1. Run `00_env_config.ipynb` to initialize runtime configuration and environment checks.
2. Use `02_ex_agreement_topic.ipynb` to explore source data and document human-approved decisions.
3. Promote approved rules/contracts into `03_pc_agreement_source_to_target.ipynb` for governed execution.

Contracts, DQ rules, classifications, lineage, and handover evidence should be stored through the framework metadata workflow, not maintained as separate static template files.
