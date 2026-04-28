# Agent Notes

This repository is currently scaffold-first and documentation-heavy.

## Current intent

- Keep implementation minimal while standards and lifecycle are being defined.
- Prioritize synthetic examples and public-safe content.
- Treat GitHub as the source of truth and Fabric as the execution environment.

## Guardrails for changes

- Do not add real organizational data, secrets, tenant/workspace identifiers, or internal URLs.
- Keep module files lightweight unless a PR explicitly introduces engine logic.
- Prefer clear documentation and notebook lifecycle consistency over premature optimization.

## Near-term roadmap

1. Dataset contract schema and validation.
2. Basic profiling and metadata writers.
3. Drift and incremental safety checks.
4. Quality rules, contracts, lineage, and AI context enhancements.
