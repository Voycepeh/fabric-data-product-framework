# AGENTS.md

## Project purpose

Build and maintain a **reusable Microsoft Fabric data product framework** that is portable, scaffold-friendly, and safe to share publicly.

## Preferred workflow

- Pull requests should target the `main` branch.
- Treat GitHub as the source of truth and Microsoft Fabric as the execution environment.

## Delivery emphasis

- Keep an **AI-in-the-loop** workflow so generated artifacts can be reviewed, explained, and improved by humans.
- Design for **reusable onboarding** across teams and projects.
- Optimize for **junior-friendly handover** with clear structure, conventions, and practical examples.

## Development commands

- `python -m compileall src tests`
- `PYTHONPATH=src pytest -q`

## Guardrails

- Keep the framework generic and public-safe.
- Do **not** include NUS-specific secrets, data, workspace names, tenant details, or internal URLs.
- Do not add real organizational data, secrets, tenant/workspace identifiers, or internal URLs.
- Keep module files lightweight unless a PR explicitly introduces engine logic.

## Documentation and change expectations

- Prefer concise documentation.
- Use Mermaid diagrams where useful.
- Favor implementation patterns that are teachable to Python users who may not be Fabric/PySpark experts.
- For schema or configuration changes, update **examples, tests, and README together**.
- Prioritize synthetic examples and public-safe content.
- Prefer clear documentation and notebook lifecycle consistency over premature optimization.

## Current intent and roadmap context

- Keep implementation minimal while standards and lifecycle are being defined.

Near-term roadmap:

1. Dataset contract schema and validation.
2. Basic profiling and metadata writers.
3. Drift and incremental safety checks.
4. Quality rules, contracts, lineage, and AI context enhancements.
