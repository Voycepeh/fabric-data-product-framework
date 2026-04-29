# AGENTS.md

## Purpose

Guide agent/Codex contributions for this repository so changes stay reusable, public-safe, and easy to hand over.

## Repo working rules

- Pull requests must target `main`.
- Treat GitHub as the source of truth.
- Treat Microsoft Fabric as the execution environment.
- Keep an AI-in-the-loop workflow and optimize for junior-friendly handover.

## Public safety rules

- Keep the framework generic and public-safe.
- Do not include real data, NUS-specific secrets, tenant details, workspace identifiers, internal URLs, or production screenshots.

## Documentation placement rules

- Prefer concise documentation.
- Root `README.md` is for high-level overview, lifecycle, quick start, and navigation only.
- Do not add detailed function, helper, API, implementation, or utility notes to root `README.md`.
- Public functions, helpers, utilities, and callable APIs must be documented in `src/README.md`.
- Detailed lifecycle, governance, contract behavior, run summary behavior, AI context, and diagram explanations belong in `docs/`.
- Synthetic examples and walkthroughs belong in `examples/`.
- Use Mermaid diagrams where useful.
- Keep examples teachable for Python users who may not be Fabric/PySpark experts.

For runtime contract behavior, see `docs/contract-enforcement.md`.
For run summary behavior, see `docs/run-summary.md`.
For callable utility usage, see `src/README.md`.

## PR expectations

- If a PR adds or changes a public function in `src/`, update `src/README.md` with:
  - function name
  - purpose
  - minimal usage example
  - expected input/output behavior
  - Fabric-specific assumptions
- Update root `README.md` only when top-level user journey, lifecycle, installation, quick start, or navigation changes.
- Prefer links to `docs/` and `src/README.md` over long implementation details.

## Testing expectations

- Run `python -m compileall src tests`.
- Run `PYTHONPATH=src pytest -q`.
