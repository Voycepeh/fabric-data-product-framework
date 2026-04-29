# AGENTS.md

## Purpose

Guide agent/Codex contributions for this repository so changes stay reusable, public-safe, and easy to hand over.

## Repo working rules

- Pull requests must target `main`.
- Treat GitHub as the source of truth.
- Treat Microsoft Fabric as the execution environment.
- Keep an AI-in-the-loop workflow and optimize for junior-friendly handover.
- Prefer small, focused PRs over large restructures.

## Public safety rules

- Keep the framework generic and public-safe.
- Do not include real data, NUS-specific secrets, tenant details, workspace identifiers, internal URLs, or production screenshots.

## Documentation placement rules

- Keep root `README.md` concise as the entry point only.
- Put lifecycle/operating behavior in `docs/`.
- Put callable API reference in `src/README.md`.
- Update `docs/` when lifecycle or architecture behavior changes.
- Update `src/README.md` when public APIs in `src/` change.
- Keep examples in `examples/` runnable and teachable for Python users.
- Use links to detailed docs instead of duplicating long explanations across multiple files.

## PR expectations

- If a PR adds or changes a public function in `src/`, update `src/README.md` with:
  - function name
  - purpose
  - minimal usage example
  - expected input/output behavior
  - Fabric-specific assumptions
- Update root `README.md` only for top-level journey/navigation changes.

## Testing expectations

- Run `python -m compileall src tests`.
- Run `PYTHONPATH=src pytest -q`.
