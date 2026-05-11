from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "src" / "fabricops_kit"
PACKAGE_NAME = "fabricops_kit"
INIT_PATH = PKG_DIR / "__init__.py"
DOCS_METADATA_PATH = PKG_DIR / "docs_metadata.py"
REFERENCE_PATH = ROOT / "docs" / "reference" / "index.md"
NOTEBOOK_STRUCTURE_DIR = ROOT / "docs" / "notebook-structure"
MODULE_DIR = ROOT / "docs" / "api" / "modules"

PUBLIC_MODULE_PREFERRED_NAMES = {
    "config": "environment_config",
    "runtime": "runtime_context",
    "fabric_io": "fabric_input_output",
    "profiling": "data_profiling",
    "contracts": "data_contracts",
    "dq": "data_quality",
    "drift": "data_drift",
    "governance": "data_governance",
    "metadata": "data_product_metadata",
    "lineage": "data_lineage",
    "run_summary": "handover_documentation",
    "technical_columns": "technical_audit_columns",
}
VISIBLE_PUBLIC_MODULES = [
    "environment_config",
    "fabric_input_output",
    "data_profiling",
    "data_contracts",
    "data_quality",
    "data_governance",
    "data_lineage",
]
HIDDEN_SUPPORTING_MODULES = [
    "runtime_context",
    "data_drift",
    "data_product_metadata",
    "handover_documentation",
    "technical_audit_columns",
]
RECOMMENDED_ENTRYPOINTS = {
    "environment_config": {
        "validate_framework_config",
        "load_fabric_config",
        "get_path",
        "bootstrap_fabric_env",
    },
    "fabric_input_output": {"Housepath", "lakehouse_table_read", "lakehouse_table_write", "warehouse_read", "warehouse_write"},
    "data_profiling": {"generate_metadata_profile", "profile_dataframe_to_metadata", "build_ai_quality_context"},
    "data_contracts": {
        "load_latest_approved_contract",
        "normalize_contract_dict",
        "validate_contract_dict",
        "get_executable_quality_rules",
        "write_contract_to_lakehouse",
        "build_contract_summary",
    },
    "data_quality": {"validate_dq_rules", "run_dq_rules", "assert_dq_passed", "split_valid_and_quarantine", "suggest_dq_rules_prompt"},
    "data_governance": {"classify_columns", "summarize_governance_classifications", "build_governance_classification_records"},
    "data_lineage": {"build_lineage_from_notebook_code"},
}

STEP_FALLBACK_NOTES = {
    "5": "No public callable is currently mapped to this step. Use exploration notebook prompts to capture transformation rationale before pipeline enforcement.",
}

@dataclass
class Symbol:
    name: str
    actual_module: str
    public_module: str
    obj_type: str
    summary: str
    importance: str = "Optional"
    purpose: str = ""


def first_sentence(doc: str | None) -> str:
    if not doc:
        return ""
    line = doc.strip().splitlines()[0].strip()
    return line.split(".")[0].strip() + ("." if "." in line else "")


def _assert_non_placeholder_summary(symbol_name: str, field_name: str, text: str) -> None:
    """Fail fast when placeholder-style summary text is detected."""
    normalized = text.strip()
    if normalized.startswith("Execute the `"):
        raise RuntimeError(f"{symbol_name} has placeholder {field_name}: {normalized}")
    if "Input parameter `" in normalized:
        raise RuntimeError(f"{symbol_name} has placeholder {field_name}: {normalized}")


def parse_module(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions: dict[str, str] = {}
    classes: dict[str, str] = {}
    constants: dict[str, str] = {}
    calls: dict[str, set[str]] = {}
    used_by: dict[str, set[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = first_sentence(ast.get_docstring(node))
            called = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        called.add(child.func.id)
                    elif isinstance(child.func, ast.Attribute):
                        called.add(child.func.attr)
            calls[node.name] = called
        elif isinstance(node, ast.ClassDef):
            classes[node.name] = first_sentence(ast.get_docstring(node))
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    constants[target.id] = ""
    names = set(functions) | set(classes)
    for caller, callees in calls.items():
        for callee in names:
            if callee in callees:
                used_by.setdefault(callee, set()).add(caller)
    return {"functions": functions, "classes": classes, "constants": constants, "calls": calls, "used_by": used_by}


def parse_public_exports() -> list[str]:
    tree = ast.parse(INIT_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            if isinstance(node.value, ast.List):
                return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant) and isinstance(elt.value, str)]
    raise RuntimeError("Could not parse __all__ from __init__.py")


def parse_step_registry() -> list[dict[str, Any]]:
    tree = ast.parse((PKG_DIR / "handover.py").read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "MVP_STEP_REGISTRY" for t in node.targets)
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "MVP_STEP_REGISTRY"
        if is_assign or is_annassign:
            if node.value is None:
                continue
            reg = ast.literal_eval(node.value)
            return [
                {
                    "step_number": item["step_number"],
                    "step_name": item["step_name"],
                    "canonical_modules": [m.replace(".py", "") for m in item.get("canonical_modules", [])],
                }
                for item in reg
            ]
    return []


def parse_docs_metadata() -> dict[str, dict[str, Any]]:
    tree = ast.parse(DOCS_METADATA_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "PUBLIC_SYMBOL_DOCS" for t in node.targets
        )
        is_annassign = (
            isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "PUBLIC_SYMBOL_DOCS"
        )
        if (is_assign or is_annassign) and node.value is not None:
            rows = ast.literal_eval(node.value)
            return {row["symbol_name"]: row for row in rows}
    raise RuntimeError("Could not parse PUBLIC_SYMBOL_DOCS from docs_metadata.py")


def parse_workflow_step_docs() -> list[dict[str, Any]]:
    tree = ast.parse(DOCS_METADATA_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "WORKFLOW_STEP_DOCS" for t in node.targets
        )
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "WORKFLOW_STEP_DOCS"
        if (is_assign or is_annassign) and node.value is not None:
            return ast.literal_eval(node.value)
    raise RuntimeError("Could not parse WORKFLOW_STEP_DOCS from docs_metadata.py")


def parse_template_flow_docs() -> list[dict[str, Any]]:
    tree = ast.parse(DOCS_METADATA_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "TEMPLATE_FLOW_DOCS" for t in node.targets
        )
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "TEMPLATE_FLOW_DOCS"
        if (is_assign or is_annassign) and node.value is not None:
            return ast.literal_eval(node.value)
    raise RuntimeError("Could not parse TEMPLATE_FLOW_DOCS from docs_metadata.py")


def internal_helper_link(actual_module: str, helper: str) -> str:
    """Return docs-relative link target for an internal helper page."""
    return f"../../reference/internal/{actual_module}/{helper}.md"


def public_reference_link(symbol: str, docs_metadata: dict[str, dict[str, Any]], step_slugs: dict[str, str]) -> str:
    """Return docs-relative link target for a public callable reference page."""
    if symbol not in docs_metadata:
        raise RuntimeError(f"Missing PUBLIC_SYMBOL_DOCS entry for exported symbol: {symbol}")
    step = docs_metadata[symbol].get("workflow_step")
    if step is None:
        raise RuntimeError(f"Missing workflow_step metadata for exported symbol: {symbol}")
    step_slug = step_slugs.get(str(step))
    if not step_slug:
        raise RuntimeError(f"Missing WORKFLOW_STEP_DOCS slug mapping for workflow step {step} ({symbol})")
    return f"../../reference/{step_slug}/{symbol}.md"


def callable_docs_link(
    symbol_name: str, module: str, docs_metadata: dict[str, dict[str, Any]], step_slugs: dict[str, str]
) -> str:
    """Return a safe docs link for a public callable."""
    workflow_step = docs_metadata[symbol_name].get("workflow_step")
    if workflow_step is not None:
        return public_reference_link(symbol_name, docs_metadata, step_slugs)
    return f"../modules/{module}/#{symbol_name}"


def resolve_preferred_actual_module(preferred_module: str) -> str:
    """Return the likely source module that owns callable implementations."""
    return next((actual for actual, public_name in PUBLIC_MODULE_PREFERRED_NAMES.items() if public_name == preferred_module), preferred_module)


def main() -> None:
    public = parse_public_exports()
    module_data = {p.stem: parse_module(p) for p in PKG_DIR.glob("*.py") if p.name != "__init__.py"}

    docs_metadata = parse_docs_metadata()
    step_docs = parse_workflow_step_docs()
    step_slugs = {str(step["number"]): step["slug"] for step in step_docs}
    template_flow_docs = parse_template_flow_docs()

    missing_metadata = sorted(name for name in public if name not in docs_metadata)
    if missing_metadata:
        raise RuntimeError("Missing PUBLIC_SYMBOL_DOCS entries for exported symbols: " + ", ".join(missing_metadata))

    unknown_metadata = sorted(name for name in docs_metadata if name not in public)
    if unknown_metadata:
        raise RuntimeError("PUBLIC_SYMBOL_DOCS contains symbols not exported in __all__: " + ", ".join(unknown_metadata))

    symbol_map: dict[str, Symbol] = {}
    for name in public:
        preferred_module = docs_metadata[name]["module"]
        preferred_actual_module = resolve_preferred_actual_module(preferred_module)
        modules_to_check = [preferred_actual_module] + [m for m in module_data if m != preferred_actual_module]
        for module in modules_to_check:
            info = module_data[module]
            if name in info["functions"]:
                symbol_map[name] = Symbol(name, module, preferred_module, "function", info["functions"][name])
                break
            if name in info["classes"]:
                symbol_map[name] = Symbol(name, module, preferred_module, "class", info["classes"][name])
                break
            if name in info["constants"]:
                symbol_map[name] = Symbol(name, module, preferred_module, "constant", info["constants"][name])
                break
        if name not in symbol_map:
            raise RuntimeError(f"Could not resolve exported symbol {name} to a module-level function/class.")

    for symbol in symbol_map.values():
        meta = docs_metadata[symbol.name]
        if meta["kind"] != symbol.obj_type:
            raise RuntimeError(f"Metadata kind mismatch for {symbol.name}: expected {symbol.obj_type}, found {meta['kind']}")
        step = meta.get("workflow_step")
        step_key = str(step) if step is not None else None
        if step_key is not None and step_key not in step_slugs:
            raise RuntimeError(f"Invalid workflow_step {step} for {symbol.name}; expected one of {sorted(step_slugs)}")
        symbol.summary = meta.get("summary_override") or symbol.summary
        symbol.purpose = meta.get("purpose") or symbol.summary or "—"
        enforce_placeholder_guard = symbol.actual_module in {"config", "ai"}
        if enforce_placeholder_guard and symbol.summary:
            _assert_non_placeholder_summary(symbol.name, "summary", symbol.summary)
        if enforce_placeholder_guard and symbol.purpose and symbol.purpose != "—":
            _assert_non_placeholder_summary(symbol.name, "purpose", symbol.purpose)
        step_rank = int(str(step).split("A")[0].split("B")[0].split("C")[0].split("D")[0]) if step is not None else 99
        symbol.importance = meta.get("importance") or ("Essential" if step is not None and step_rank <= 7 else "Optional")
        if symbol.importance not in {"Essential", "Optional"}:
            raise RuntimeError(f"Invalid importance {symbol.importance!r} for {symbol.name}; expected Essential or Optional")
    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    module_index_lines = ["# Module API Catalogue", "", "Function Reference/workflow pages are the primary entrypoint. Module pages below are secondary technical references.", "", "Short-form modules remain import-compatible aliases but are intentionally hidden from this user-facing catalogue.", ""]
    all_doc_modules = sorted(set(VISIBLE_PUBLIC_MODULES + HIDDEN_SUPPORTING_MODULES))
    for module in all_doc_modules:
        actual_module = next((k for k,v in PUBLIC_MODULE_PREFERRED_NAMES.items() if v==module), module)
        info = module_data[actual_module]
        module_data[module] = info
        info = module_data[module]
        module_md = MODULE_DIR / f"{module}.md"
        public_in_module = [s for s in symbol_map.values() if s.public_module == module]
        is_internal_only = not public_in_module
        title = f"# `{module}` module" if not is_internal_only else f"# `{module}` module (internal)"
        if is_internal_only:
            status_banner = (
                '<div class="api-status-block">\n'
                '  <span class="api-chip api-chip-internal">Internal-only module</span>\n'
                '  <div class="api-chip-subtitle">Not intended as a primary user-facing API surface.</div>\n'
                '</div>'
            )
        elif module in HIDDEN_SUPPORTING_MODULES:
            status_banner = (
                '<div class="api-status-block">\n'
                '  <span class="api-chip api-chip-internal">Advanced supporting module</span>\n'
                '  <div class="api-chip-subtitle">Used by workflow references but not promoted as a primary notebook module.</div>\n'
                '</div>'
            )
        else:
            status_banner = '<div class="api-status-block">\n  <span class="api-chip api-chip-module">Module overview</span>\n</div>'
        lines = [title, "", status_banner, ""]
        if public_in_module:
            recommended_names = RECOMMENDED_ENTRYPOINTS.get(module, set())
            recommended = sorted([s for s in public_in_module if s.name in recommended_names], key=lambda x: x.name.lower())
            advanced = sorted([s for s in public_in_module if s.name not in recommended_names], key=lambda x: x.name.lower())
            lines.extend(["## Recommended notebook entrypoints", ""])
            lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
            for s in recommended:
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                callable_link = callable_docs_link(s.name, module, docs_metadata, step_slugs)
                lines.append(
                    f"| [`{s.name}`]({callable_link}) | {s.obj_type} | {s.summary or '—'} | "
                    f"{', '.join(f'[`{r}`]({internal_helper_link(s.actual_module, r)}) (internal)' for r in related) or '—'} |"
                )
            if not recommended:
                lines.append("| — | — | No recommended entrypoints configured. | — |")

            lines.extend(["", "## Advanced helpers", ""])
            if advanced:
                lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
                for s in advanced:
                    related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                    callable_link = callable_docs_link(s.name, module, docs_metadata, step_slugs)
                    lines.append(
                        f"| [`{s.name}`]({callable_link}) | {s.obj_type} | {s.summary or '—'} | "
                        f"{', '.join(f'[`{r}`]({internal_helper_link(s.actual_module, r)}) (internal)' for r in related) or '—'} |"
                    )
            else:
                lines.append("No advanced helpers listed for this module.")
        else:
            lines.extend(["## Recommended notebook entrypoints", "", "No public exports in this module.", "", "## Advanced helpers", "", "No advanced helpers listed for this module."])
        lines.extend(["", "## Internal helpers", ""])
        internal_fns = sorted([f for f in info["functions"] if f.startswith("_")])
        if internal_fns:
            lines.extend(["| Helper | Related public callables |", "|---|---|"])
            for helper in internal_fns:
                users = sorted([u for u in info["used_by"].get(helper, set()) if u in {p.name for p in public_in_module}])
                users_links = ", ".join(
                    f"[`{u}`]({callable_docs_link(u, module, docs_metadata, step_slugs)})" for u in users
                ) or "—"
                lines.append(f"| [`{helper}`]({internal_helper_link(actual_module, helper)}) | {users_links} |")
        else:
            lines.append("No module-level internal helpers detected.")

        if public_in_module:
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                expected_target = callable_docs_link(s.name, module, docs_metadata, step_slugs)
                expected_link = f"[`{s.name}`]({expected_target})"
                if not any(expected_link in line for line in lines):
                    raise RuntimeError(f"Missing callable table link for {module}.{s.name}")
                if f"../../reference/{module}/{s.name}.md" in "\n".join(lines):
                    raise RuntimeError(
                        f"Found deprecated module-path public link for {module}.{s.name}; expected workflow-step slug path."
                    )
        for helper in internal_fns:
            expected_helper_link = f"[`{helper}`]({internal_helper_link(actual_module, helper)})"
            if not any(expected_helper_link in line for line in lines):
                raise RuntimeError(f"Missing internal helper link for {module}.{helper}")
        if any("## Public callable details" in line for line in lines):
            raise RuntimeError(f"Public callable details section should not be rendered for {module}")
        if any("## Full module API" in line for line in lines):
            raise RuntimeError(f"Full module API section should not be rendered for {module}")
        if any(line.strip().startswith("::: fabricops_kit.") for line in lines):
            raise RuntimeError(f"Mkdocstrings directives should not be rendered on module page for {module}")
        module_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        if module in VISIBLE_PUBLIC_MODULES:
            module_index_lines.append(f"- [`{module}`]({module}.md)")

    (MODULE_DIR / "index.md").write_text("\n".join(module_index_lines) + "\n", encoding="utf-8", newline="\n")

    starter_symbol_to_notebooks: dict[str, set[str]] = {}
    for flow in template_flow_docs:
        notebook_key = flow["notebook_key"]
        for segment in flow["segments"]:
            for symbol in segment["symbols"]:
                if symbol not in symbol_map:
                    raise RuntimeError(f"TEMPLATE_FLOW_DOCS references unknown symbol: {symbol}")
                starter_symbol_to_notebooks.setdefault(symbol, set()).add(notebook_key)

    def _esc(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def _html_table(
        table_class: str,
        headers: list[str],
        rows: list[list[str]],
        *,
        row_attrs: list[dict[str, str]] | None = None,
    ) -> list[str]:
        lines = [f'<table class="{table_class}">', "  <thead>", "    <tr>"]
        for header in headers:
            lines.append(f"      <th>{_esc(header)}</th>")
        lines.extend(["    </tr>", "  </thead>", "  <tbody>"])
        for row_index, row in enumerate(rows):
            attr_text = ""
            if row_attrs and row_index < len(row_attrs):
                attrs = row_attrs[row_index]
                attr_text = "".join(f' {key}="{_esc(value)}"' for key, value in attrs.items())
            lines.append(f"    <tr{attr_text}>")
            for idx, cell in enumerate(row):
                lines.append(f'      <td data-label="{_esc(headers[idx])}">{cell}</td>')
            lines.append("    </tr>")
        lines.extend(["  </tbody>", "</table>"])
        return lines

    def _anchor(href: str, text: str, *, code: bool = False) -> str:
        content = f"<code>{_esc(text)}</code>" if code else _esc(text)
        return f'<a href="{_esc(href)}">{content}</a>'

    def _module_link(module: str, *, base_prefix: str = "../") -> str:
        return (
            f'<a class="reference-module-link" href="{_esc(base_prefix)}api/modules/{_esc(module)}/" '
            f'title="Open {module} module page" aria-label="Open {module} module page">{_esc(module)}</a>'
        )

    def _strip_backticks(label: str) -> str:
        return label[1:-1] if label.startswith("`") and label.endswith("`") else label

    notebook_page_files = {
        "00_env_config": "00-env-config.md",
        "02_ex": "02-exploration.md",
        "03_pc": "03-pipeline-contract.md",
    }
    notebook_boundary_notes = {
        "00_env_config": "`00_env_config` is shared setup.",
        "02_ex": "`02_ex` is AI-assisted exploration and human review.",
        "03_pc": "`03_pc` is deterministic pipeline enforcement.",
    }

    NOTEBOOK_STRUCTURE_DIR.mkdir(parents=True, exist_ok=True)
    for flow in template_flow_docs:
        notebook_key = flow["notebook_key"]
        page_name = notebook_page_files.get(notebook_key)
        if not page_name:
            continue
        notebook_path = ROOT / flow["template_path"]
        notebook_link = (
            _anchor(f"https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/{flow['template_path']}", "Open template notebook")
            if notebook_path.exists()
            else "—"
        )
        notebook_lines = [
            f"# {flow['notebook_label']}",
            "",
            flow["segment_intro"],
            "",
            f"> {notebook_link}",
            "",
            f"> {notebook_boundary_notes[notebook_key]}",
            "",
        ]
        for segment in flow["segments"]:
            notebook_lines.append(f"## {segment['title']}")
            notebook_lines.append("")
            segment_text = str(segment.get("text", "")).strip()
            if segment_text:
                notebook_lines.append(segment_text)
                notebook_lines.append("")
            segment_rows: list[list[str]] = []
            for symbol_name in segment["symbols"]:
                s = symbol_map[symbol_name]
                info = module_data[s.actual_module]
                step_slug = step_slugs.get(str(docs_metadata[s.name]["workflow_step"]))
                symbol_link = f"../../reference/{step_slug}/{s.name}/" if step_slug else f"../../api/modules/{s.public_module}/#{s.name}"
                segment_rows.append([
                    _anchor(symbol_link, s.name, code=True),
                    _module_link(s.public_module, base_prefix="../../"),
                    s.purpose or "—",
                ])
            if segment_rows:
                notebook_lines.extend(
                    _html_table(
                        "reference-function-table notebook-structure-function-table",
                        ["Function / class", "Module", "Purpose"],
                        segment_rows,
                    )
                )
                notebook_lines.append("")
        (NOTEBOOK_STRUCTURE_DIR / page_name).write_text("\n".join(notebook_lines) + "\n", encoding="utf-8", newline="\n")

    ref = [
        "# Function Reference",
        "",
        "Use this page as an API lookup after you understand the notebook flow.",
        "",
        "## Start from the templates",
        "",
    ]
    notebook_structure_links = {
        "00_env_config": "../notebook-structure/00-env-config/",
        "02_ex": "../notebook-structure/02-exploration/",
        "03_pc": "../notebook-structure/03-pipeline-contract/",
    }

    template_rows: list[list[str]] = []
    for row in template_flow_docs:
        template_path = ROOT / row["template_path"]
        if template_path.exists():
            template_link = _anchor(
                f"https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/{row['template_path']}",
                "Open notebook",
            )
        else:
            template_link = "—"
        guided_link = notebook_structure_links.get(row["notebook_key"], "")
        guided_usage = row["segment_intro"]
        if guided_link:
            guided_usage = f"{guided_usage}<br><a href=\"{_esc(guided_link)}\">View guided structure</a>"
        template_rows.append([f"<code>{_esc(_strip_backticks(row['notebook_label']))}</code>", guided_usage, template_link])
    ref.extend(_html_table("reference-template-table", ["Notebook", "Guided usage", "Full template"], template_rows))

    ref.extend([
        "",
        "## What runs where",
        "",
        "- `00_env_config` is shared setup.",
        "- `02_ex` is AI-assisted exploration and human review.",
        "- `03_pc` is deterministic pipeline enforcement.",
        "",
        "AI functions are advisory. Approved contracts and pipeline notebooks are the enforcement point.",
        "",
    ])

    ref.extend(
        [
            "## Find a callable",
            "",
            "Use the finder below to look up public callables.",
            "",
            '<div class="callable-finder" data-callable-finder>',
            '  <label class="callable-finder-label" for="callable-finder-input">Search callables</label>',
            '  <input id="callable-finder-input" class="callable-finder-input" type="search" placeholder="Search callables" aria-describedby="callable-finder-help callable-finder-status callable-finder-examples" autocomplete="off">',
            '  <p id="callable-finder-help" class="callable-finder-help">Search by function name, module, or what the function does.</p>',
            '  <p id="callable-finder-examples" class="callable-finder-examples">Try: <span class="callable-finder-chip">csv</span> <span class="callable-finder-chip">data_quality</span> <span class="callable-finder-chip">quarantine</span></p>',
            '  <p id="callable-finder-status" class="callable-finder-status" aria-live="polite">Showing all callables.</p>',
            '  <p class="callable-finder-empty" data-callable-finder-empty hidden>No callables match your search.</p>',
            "</div>",
            "",
            "## All public functions",
            "",
        ]
    )
    all_rows: list[list[str]] = []
    all_row_attrs: list[dict[str, str]] = []
    for s in sorted(symbol_map.values(), key=lambda x: x.name.lower()):
        step_slug = step_slugs.get(str(docs_metadata[s.name]["workflow_step"]))
        symbol_link = f"./{step_slug}/{s.name}/" if step_slug else f"../api/modules/{s.public_module}/#{s.name}"
        starter_path = ", ".join(sorted(starter_symbol_to_notebooks.get(s.name, set()))) or "—"
        all_rows.append([
            _anchor(symbol_link, s.name, code=True),
            _module_link(s.public_module),
            starter_path,
            s.importance,
            s.purpose or s.summary or "—",
        ])
        all_row_attrs.append(
            {
                "data-callable-row": "true",
                "data-callable-name": s.name,
                "data-callable-module": s.public_module,
                "data-callable-starter-path": starter_path,
                "data-callable-importance": s.importance,
                "data-callable-purpose": s.purpose or s.summary or "—",
            }
        )
    ref.extend(
        _html_table(
            "reference-catalogue-table",
            ["Function / class", "Module", "Starter path", "Importance", "Purpose"],
            all_rows,
            row_attrs=all_row_attrs,
        )
    )

    ref.append("")
    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text("\n".join(ref) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
