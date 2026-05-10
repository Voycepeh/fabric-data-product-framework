# AGENTS.md

## Purpose

Guide agent/Codex contributions for this repository so changes stay reusable, public-safe, and easy to hand over.

## Repo working rules

- Pull requests must target `main`.
- Treat GitHub as the source of truth.
- Treat Microsoft Fabric as the execution environment.
- Keep an AI-in-the-loop workflow and optimize for junior-friendly handover.
- Prefer small, focused PRs over large restructures.
- Prefer updating existing modules over creating new files; only add new `.py`, `.md`, or other repo files when clearly justified by a separate user-facing concept or when extending an existing file would materially hurt readability. Avoid thin wrapper modules and unnecessary feature fragmentation.

## Public safety rules

- Keep the framework generic and public-safe.
- Do not include real data, NUS-specific secrets, tenant details, workspace identifiers, internal URLs, or production screenshots.

## Documentation placement rules

- Keep root `README.md` concise as the entry point only.
- Put lifecycle/operating behavior in `docs/`.
- Put callable API reference in `src/README.md`.
- Update `docs/` when lifecycle or architecture behavior changes.
- Keep examples in `examples/` runnable and teachable for Python users.
- Use links to detailed docs instead of duplicating long explanations across multiple files.
- Docstrings in `src/fabricops_kit/` are the source of truth for generated API docs under `docs/api/`.
- Do not create or maintain duplicate manual function/member lists in `README.md`, `src/README.md`, or `docs/api/`.


## Public callable catalogue and workflow mapping rules

- Add a symbol to `src/fabricops_kit/__init__.py::__all__` only when it is intentionally user-facing.
- Every public callable in `__all__` must have a complete NumPy-style docstring with a meaningful first sentence.
- Public callables must be assignable to a 13-step workflow category through the central registry (`get_mvp_step_registry` / `MVP_STEP_REGISTRY`) consumed by the reference generator.
- If a public callable depends on important internal helpers, keep those helpers documented enough that generated relationship lists remain useful.
- Do not maintain manual duplicate function/member lists across docs. Regenerate the callable catalogue instead.
- PRs that add/remove/rename public callables must run `PYTHONPATH=src python scripts/generate_function_reference.py` and include generated docs updates in the same PR.
- New public callables must be added to `__all__`, mapped to the 13-step reference flow (or intentionally placed under Other Utilities), and documented with useful non-placeholder docstrings.
- Internal-only modules should not appear as public modules in the module API catalogue unless clearly labeled as internal-only.
- Deprecated callables must not be promoted as the recommended path when a replacement callable exists.
- If `__all__`, module names, public callable mappings, or docstrings change, regenerate the reference and module catalogue docs in the same PR.

## Docs and API reference generation

- GitHub Pages may auto-deploy after merge, but deployment only publishes what was built; it does not discover new Python callables unless API/reference pages are regenerated in the docs build workflow.
- When changing public functions, module boundaries, `__all__`, docstrings, or module ownership, always verify whether generated docs/reference files must be refreshed.
- For edits under `src/fabricops_kit/*.py`, confirm affected pages in `docs/api/modules/` and `docs/reference/` are updated, or confirm CI regenerates them during `mkdocs build`.
- If a module page is generated from `__all__`, ensure new public callables are exported in `__all__` and visible in the generated module table.
- New public functions must be discoverable from the relevant module page and, where appropriate, the step-based reference page.
- Run the docs generation command when available. If no explicit generator is documented, inspect `scripts/`, `mkdocs.yml`, and docs tooling before assuming `mkdocs build` alone is enough.
- Run `mkdocs build` after docs/reference generation changes when possible.
- Do not assume GitHub Pages will fix stale generated docs on its own.
- `docs/reference/index.md` is generated output.
- Do not manually patch `docs/reference/index.md` as the only source of truth.
- Update `scripts/generate_function_reference.py` first, then regenerate `docs/reference/index.md`.
- Keep `/reference/` template-first.

Example (PR-132-style):
- If you add `bootstrap_fabric_env`, `run_config_smoke_tests`, `check_fabric_ai_functions_available`, or add `get_path` to `config`, also update/regenerate the config API/module page so those callables appear.

## Docstring requirements for public APIs

For every new or modified public API under `src/fabricops_kit/` (public function, class, dataclass, and important public method):

- Include a NumPy-style docstring.
- Use NumPy-style sections:
  - `Parameters`
  - `Returns`
  - `Raises`, where applicable
  - `See Also`, where helpful
  - `Notes`, where helpful
  - `Examples`, where helpful
- Docstrings must describe actual behavior, not intended behavior.
- Do not use placeholder text such as:
  - `"Description of x"`
  - `"Returned value"`
  - `"Documentation for API-reference generation"`
- Do not leave duplicate adjacent triple-quoted strings.
- Do not mix Google-style `Args`/`Returns` with NumPy-style `Parameters`/`Returns`.
- Keep examples generic and safe.
- Do not include private workspace IDs, lakehouse IDs, NUS-specific paths, or internal dataset names.

For Fabric-specific functions, clearly state runtime assumptions in `Notes`:

- Fabric notebook runtime required
- PySpark DataFrame expected
- local Python compatible
- optional Fabric dependency required

### NumPy-style docstring template

```python
def api_name(param1: str, param2: int = 0) -> bool:
    """Short summary sentence.

    Parameters
    ----------
    param1 : str
        Meaningful description of `param1`.
    param2 : int, default=0
        Meaningful description of `param2`.

    Returns
    -------
    bool
        What is returned and under which conditions.

    Raises
    ------
    ValueError
        When inputs fail validation.

    See Also
    --------
    related_api : Brief relationship.

    Notes
    -----
    Include Fabric/runtime assumptions when relevant.

    Examples
    --------
    >>> api_name("example", 1)
    True
    """
```

## PR expectations

- Keep PRs focused and ensure docs impact is handled in the same PR.
- When public APIs change, update their NumPy-style docstrings first; only add high-level navigation updates to `README.md`/`src/README.md`/`docs/` where needed.
- Update root `README.md` only for top-level journey/navigation changes.

## Review checklist (required before PR completion)

- [ ] New/modified public APIs in `src/fabricops_kit/` include complete NumPy-style docstrings.
- [ ] Docstrings describe actual behavior and avoid placeholders.
- [ ] No duplicate adjacent docstrings exist.
- [ ] No mixed Google-style and NumPy-style section headers.
- [ ] Examples are generic/public-safe and contain no sensitive/internal identifiers.
- [ ] Fabric-specific assumptions are documented in `Notes` where applicable.

Recommended duplicate-docstring check:

```bash
python - <<'PY'
import ast
from pathlib import Path

bad = []
for path in Path("src/fabricops_kit").glob("*.py"):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if len(body) >= 2:
                first = isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)
                second = isinstance(body[1], ast.Expr) and isinstance(body[1].value, ast.Constant) and isinstance(body[1].value.value, str)
                if first and second:
                    bad.append(f"{path}:{node.lineno} {node.name} has duplicate adjacent docstrings")
if bad:
    raise SystemExit("\n".join(bad))
print("No duplicate adjacent docstrings found.")
PY
```

## Testing expectations

- Run `uv run python -m compileall src tests`.
- Run `uv run python -m pytest -q`.
- Run `uv run mkdocs build`.


## Branding guidance

- Public brand name is **FabricOps Starter Kit**.
- Preferred wording: **governed, quality-checked, AI-ready notebooks in Microsoft Fabric**.
- Avoid reintroducing **FabricOps Starter Kit** as the public-facing brand.
- Do not position the project as a full data product platform.
