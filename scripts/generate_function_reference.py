from __future__ import annotations

import ast
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "src" / "fabricops_kit"
PACKAGE_NAME = "fabricops_kit"
INIT_PATH = PKG_DIR / "__init__.py"
DOCS_METADATA_PATH = PKG_DIR / "docs_metadata.py"
REFERENCE_PATH = ROOT / "docs" / "reference" / "index.md"
FUNCTION_USAGE_GUIDE_PATH = ROOT / "docs" / "reference" / "function-usage-guide.md"
NOTEBOOK_STRUCTURE_DIR = ROOT / "docs" / "notebook-structure"
MODULE_DIR = ROOT / "docs" / "api" / "modules"
MKDOCS_PATH = ROOT / "mkdocs.yml"
MANIFEST_PATH = ROOT / "docs" / "reference" / "manifest.json"
CALLABLE_MAP_PATH = ROOT / "docs" / "reference" / "callable-map.md"
CALLABLE_MAP_JSON_PATH = ROOT / "docs" / "reference" / "callable-map.json"
CALLABLE_MAP_HTML_PATH = ROOT / "docs" / "assets" / "callable-map.html"

PUBLIC_MODULE_PREFERRED_NAMES = {
    "config": "config",
    "fabric_input_output": "fabric_input_output",
    "data_profiling": "data_profiling",
    "data_quality": "data_quality",
    "drift": "drift",
    "data_governance": "data_governance",
    "metadata": "metadata",
    "data_lineage": "data_lineage",
    "handover": "handover",
    "technical_columns": "technical_columns",
    "business_context": "business_context",
    "data_agreement": "data_agreement",
}
INTERNAL_MODULE_BLACKLIST = {"_utils"}
INTERNAL_ALIAS_MODULES = {}
@dataclass
class Symbol:
    name: str
    actual_module: str
    public_module: str
    obj_type: str
    summary: str
    role: str = "optional"
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
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id.isupper():
                constants[target.id] = ""
    names = set(functions) | set(classes)
    for caller, callees in calls.items():
        for callee in names:
            if callee in callees:
                used_by.setdefault(callee, set()).add(caller)
    return {"functions": functions, "classes": classes, "constants": constants, "calls": calls, "used_by": used_by}


def parse_import_aliases(nodes: list[ast.stmt]) -> tuple[dict[str, str], dict[str, str]]:
    module_aliases: dict[str, str] = {}
    symbol_aliases: dict[str, str] = {}
    for node in nodes:
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name
                module_aliases[name] = alias.name
        elif isinstance(node, ast.ImportFrom):
            if not node.module:
                continue
            for alias in node.names:
                if alias.name == "*":
                    continue
                name = alias.asname or alias.name
                symbol_aliases[name] = f"{node.module}.{alias.name}"
    return module_aliases, symbol_aliases


def collect_function_calls(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, str]]:
    calls: list[dict[str, str]] = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        call_target = ""
        call_type = "unknown"
        if isinstance(child.func, ast.Name):
            call_target = child.func.id
            call_type = "name"
        elif isinstance(child.func, ast.Attribute):
            attr = child.func.attr
            if isinstance(child.func.value, ast.Name):
                call_target = f"{child.func.value.id}.{attr}"
            else:
                call_target = attr
            call_type = "attribute"
        if call_target:
            calls.append({"raw_name": call_target, "call_type": call_type})
    return calls


def resolve_call_target(
    module: str,
    raw_name: str,
    module_aliases: dict[str, str],
    symbol_aliases: dict[str, str],
    same_module_names: set[str],
    exported_symbol_map: dict[str, Symbol],
    package_module_names: set[str],
) -> tuple[str | None, str, str]:
    def _classify_callee(module_name: str, symbol_name: str) -> str:
        mapped = exported_symbol_map.get(symbol_name)
        if mapped and mapped.actual_module == module_name:
            return "public_export"
        if symbol_name.startswith("_"):
            return "internal_helper"
        return "internal_callable"
    # same-module callable/class names are always safe to resolve first
    if raw_name in same_module_names:
        return f"{PACKAGE_NAME}.{module}.{raw_name}", "same_module", _classify_callee(module, raw_name)

    # explicit import alias from "from x import y as z"
    if raw_name in symbol_aliases:
        imported = symbol_aliases[raw_name]
        imported_short = imported.split(".")
        if len(imported_short) >= 2 and (imported.startswith(PACKAGE_NAME) or imported_short[-2] in package_module_names):
            resolved_module = imported_short[-2]
            resolved_symbol = imported_short[-1]
            callee_kind = _classify_callee(resolved_module, resolved_symbol)
            return (
                f"{PACKAGE_NAME}.{resolved_module}.{resolved_symbol}",
                "cross_module" if resolved_module != module else "same_module",
                callee_kind,
            )

    # module/alias call like alias.func() or module.func()
    if "." in raw_name:
        owner, member = raw_name.split(".", 1)
        mapped_owner = module_aliases.get(owner, owner)
        short_owner = mapped_owner.split(".")[-1]
        if mapped_owner.startswith(PACKAGE_NAME) or short_owner in package_module_names:
            resolved_module = short_owner if short_owner in package_module_names else mapped_owner.rsplit(".", 1)[-1]
            callee_kind = _classify_callee(resolved_module, member)
            return f"{PACKAGE_NAME}.{resolved_module}.{member}", "cross_module" if resolved_module != module else "same_module", callee_kind
        return None, "unresolved", "unresolved"

    # public exported symbol map fallback (bare-name cross-module only for exported mapping)
    exported = exported_symbol_map.get(raw_name)
    if exported and exported.actual_module != module:
        callee_kind = _classify_callee(exported.actual_module, raw_name)
        return f"{PACKAGE_NAME}.{exported.actual_module}.{raw_name}", "cross_module", callee_kind

    return None, "unresolved", "unresolved"


def build_callable_graph(
    module_data: dict[str, dict[str, Any]],
    symbol_map: dict[str, Symbol],
    public_exports: list[str],
    docs_metadata: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    package_modules = {m for m in module_data if m not in {"docs_metadata"}}
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    node_keys: set[tuple[str, str]] = set()
    module_summaries: list[dict[str, Any]] = []
    calls_modules: dict[str, set[str]] = {m: set() for m in package_modules}
    called_by_modules: dict[str, set[str]] = {m: set() for m in package_modules}

    for module, info in module_data.items():
        module_tree = ast.parse((PKG_DIR / f"{module}.py").read_text(encoding="utf-8"))
        module_aliases, symbol_aliases = parse_import_aliases(list(getattr(module_tree, "body", [])))
        functions = info.get("functions", {})
        classes = info.get("classes", {})
        exported_names = {name for name, sym in symbol_map.items() if sym.actual_module == module}
        same_module_names = set(functions) | set(classes)
        for callable_name in sorted(set(functions) | set(classes)):
            role = str(docs_metadata.get(callable_name, {}).get("role", "internal")).lower()
            exported = callable_name in exported_names
            if not exported and role not in {"essential", "optional", "internal"}:
                role = "internal"
            qualified_name = f"{PACKAGE_NAME}.{module}.{callable_name}"
            key = (module, callable_name)
            if key not in node_keys:
                node_keys.add(key)
                nodes.append(
                    {
                        "callable_name": callable_name,
                        "module_name": module,
                        "qualified_name": qualified_name,
                        "role": role if exported else "internal",
                        "exported": exported,
                        "is_underscore": callable_name.startswith("_"),
                    }
                )

        for node in module_tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            caller_qn = f"{PACKAGE_NAME}.{module}.{node.name}"
            local_module_aliases, local_symbol_aliases = parse_import_aliases(
                [n for n in ast.walk(node) if isinstance(n, (ast.Import, ast.ImportFrom))]
            )
            merged_module_aliases = {**module_aliases, **local_module_aliases}
            merged_symbol_aliases = {**symbol_aliases, **local_symbol_aliases}
            for call in collect_function_calls(node):
                raw_name = call["raw_name"]
                resolved_qn, edge_type, callee_kind = resolve_call_target(
                    module, raw_name, merged_module_aliases, merged_symbol_aliases, same_module_names, symbol_map, package_modules
                )
                edge = {
                    "caller_qualified_name": caller_qn,
                    "callee_qualified_name": resolved_qn,
                    "callee_raw_name": raw_name if resolved_qn is None else None,
                    "edge_type": edge_type,
                    "callee_kind": callee_kind,
                }
                edges.append(edge)
                if resolved_qn and edge_type in {"same_module", "cross_module"}:
                    callee_module = resolved_qn.split(".")[-2]
                    if callee_module != module:
                        calls_modules[module].add(callee_module)
                        called_by_modules[callee_module].add(module)

        public_count = len([name for name in exported_names if not name.startswith("_")])
        helper_count = len([name for name in functions if name.startswith("_")])
        module_summaries.append(
            {
                "module": module,
                "calls_modules": sorted(calls_modules.get(module, set())),
                "called_by_modules": sorted(called_by_modules.get(module, set())),
                "public_callable_count": public_count,
                "internal_helper_count": helper_count,
            }
        )
    return nodes, edges, sorted(module_summaries, key=lambda x: x["module"])


def parse_public_exports() -> list[str]:
    tree = ast.parse(INIT_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            if isinstance(node.value, ast.List):
                return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant) and isinstance(elt.value, str)]
    raise RuntimeError("Could not parse __all__ from __init__.py")



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
            seen = set()
            out = {}
            for row in rows:
                name = row["symbol_name"]
                if name in seen:
                    raise RuntimeError(f"Duplicate PUBLIC_SYMBOL_DOCS symbol_name detected: {name}")
                seen.add(name)
                out[name] = row
            return out
    raise RuntimeError("Could not parse PUBLIC_SYMBOL_DOCS from docs_metadata.py")


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


def parse_module_docs_metadata() -> list[dict[str, Any]]:
    tree = ast.parse(DOCS_METADATA_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "MODULE_DOCS_METADATA" for t in node.targets
        )
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "MODULE_DOCS_METADATA"
        if (is_assign or is_annassign) and node.value is not None:
            return ast.literal_eval(node.value)
    raise RuntimeError("Could not parse MODULE_DOCS_METADATA from docs_metadata.py")


def internal_helper_link(actual_module: str, helper: str) -> str:
    """Return module-page-relative link target for an internal helper page."""
    return f"../../reference/internal/{actual_module}/{helper}/"


def public_reference_link(
    symbol: str,
    docs_metadata: dict[str, dict[str, Any]],
    *,
    context: str = "module",
) -> str:
    """Return context-relative link target for a public callable page."""
    if symbol not in docs_metadata:
        raise RuntimeError(f"Missing PUBLIC_SYMBOL_DOCS entry for exported symbol: {symbol}")
    if context == "module":
        return f"../../reference/{symbol}/"
    if context == "reference":
        return f"../api/reference/{symbol}/"
    if context == "notebook":
        return f"../../api/reference/{symbol}/"
    raise RuntimeError(f"Unknown link context: {context}")


def callable_docs_link(
    symbol_name: str, module: str, docs_metadata: dict[str, dict[str, Any]], *, context: str = "module"
) -> str:
    """Return a safe docs link for a public callable."""
    if symbol_name in docs_metadata:
        return public_reference_link(symbol_name, docs_metadata, context=context)
    return f"../modules/{module}/#{symbol_name}"


def resolve_preferred_actual_module(preferred_module: str) -> str:
    """Return the likely source module that owns callable implementations."""
    return next((actual for actual, public_name in PUBLIC_MODULE_PREFERRED_NAMES.items() if public_name == preferred_module), preferred_module)


def canonical_public_module(module_name: str) -> str:
    """Return the canonical docs/public module name for metadata and manifests."""
    return PUBLIC_MODULE_PREFERRED_NAMES.get(module_name, module_name)


def render_callable_map_page() -> str:
    return "\n".join([
        "# Callable Dependency Map",
        "",
        '!!! note "Maintainer diagnostic page"',
        "    This page is generated from source code and is intended for maintainers.",
        "    For normal usage, start with the Function Usage Guide or Function Reference.",
        "",
        '<iframe src="../../assets/callable-map.html" title="Callable lineage explorer" style="width:100%;height:78vh;min-height:640px;border:1px solid #2a2f3a;border-radius:8px;"></iframe>',
        "",
    ])


def render_callable_map_html() -> str:
    return """<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<style>body{margin:0;font:14px system-ui;background:#0b1020;color:#d7deff}#app{display:flex;min-height:100vh}.title{font-size:16px;font-weight:700;margin-bottom:8px}#left{flex:1;padding:12px}#graphWrap{position:relative;overflow:hidden;border:1px solid #25304a;border-radius:8px;background:#0f1730}#right{width:34%;min-width:280px;border-left:1px solid #25304a;padding:12px;overflow:auto}input,select,button{background:#121a31;color:#d7deff;border:1px solid #2f3a58;border-radius:6px;padding:6px}button{cursor:pointer}svg{width:100%;height:72vh;touch-action:none}.node{cursor:pointer}.edge{stroke:#5a6a95;stroke-opacity:.24}.edge.hl{stroke:#ffd166;stroke-opacity:.95;stroke-width:2.2}.muted{opacity:.14}.legend span{display:inline-block;margin-right:8px}.pill{display:inline-block;padding:2px 7px;border-radius:999px;border:1px solid #2f3a58;background:#121a31;margin-right:5px}.empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#b9c4e8;font-weight:600}.controls{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}@media(max-width:900px){#app{flex-direction:column}#right{width:auto;min-width:0;border-left:none;border-top:1px solid #25304a}svg{height:56vh}}</style></head>
<body><div id='app'><section id='left'><div class='title'>Callable Dependency Explorer</div><div class='controls'><input id='q' placeholder='Search callable'><select id='m'><option value=''>All modules</option></select><select id='r'><option value=''>All roles</option></select><button id='reset'>Reset view</button></div><div id='graphWrap'><svg id='g'></svg><div id='empty' class='empty' style='display:none'>No callables match the current filters.</div></div><div class='legend'><span>● public</span><span>● internal helper</span><span>● internal callable</span></div></section><aside id='right'><h3>Callable Inspector</h3><div id='ins'>Select a node.</div></aside></div>
<script>
const color=n=>n.exported?'#66d9ef':(n.is_underscore?'#ff6b6b':'#c792ea');
fetch('../reference/callable-map.json').then(r=>r.json()).then(data=>{
const qEl=document.getElementById('q'),mEl=document.getElementById('m'),rEl=document.getElementById('r'),ins=document.getElementById('ins');
const svg=document.getElementById('g'),empty=document.getElementById('empty'),resetBtn=document.getElementById('reset');
const nodes=data.nodes, edges=data.edges.filter(e=>e.callee_qualified_name), byQ=Object.fromEntries(nodes.map(n=>[n.qualified_name,n]));
[...new Set(nodes.map(n=>n.module_name))].sort().forEach(m=>mEl.innerHTML+=`<option>${m}</option>`);
[...new Set(nodes.map(n=>n.role))].sort().forEach(r=>rEl.innerHTML+=`<option>${r}</option>`);
let sel=null, visNodes=[], visEdges=[], pos={}, camera={x:0,y:0,w:100,h:100};
let pinchDist=0;
const related=(q)=>{const up=new Set(),down=new Set();let ch=true;while(ch){ch=false;for(const e of visEdges){if(e.callee_qualified_name===q||up.has(e.callee_qualified_name)){if(!up.has(e.caller_qualified_name)){up.add(e.caller_qualified_name);ch=true}} if(e.caller_qualified_name===q||down.has(e.caller_qualified_name)){if(!down.has(e.callee_qualified_name)){down.add(e.callee_qualified_name);ch=true}}}}return{up,down}};
const layout=()=>{const groups=new Map();for(const n of visNodes){if(!groups.has(n.module_name))groups.set(n.module_name,[]);groups.get(n.module_name).push(n)};const modules=[...groups.keys()].sort();const rowH=34,colGap=120,colPad=36;let x=0;pos={};for(const m of modules){const arr=groups.get(m).sort((a,b)=>a.callable_name.localeCompare(b.callable_name));const h=Math.max(100,arr.length*rowH+44);for(let i=0;i<arr.length;i++)pos[arr[i].qualified_name]={x:x+70,y:i*rowH+42-h/2};x+=Math.max(200,Math.min(320,140+arr.length*7))+colGap}if(modules.length===1){for(const k in pos)pos[k].x-=x/2}};
const bounds=(keys)=>{const pts=keys.map(k=>pos[k]).filter(Boolean);if(!pts.length)return null;let minX=1e9,minY=1e9,maxX=-1e9,maxY=-1e9;for(const p of pts){minX=Math.min(minX,p.x);maxX=Math.max(maxX,p.x+140);minY=Math.min(minY,p.y-18);maxY=Math.max(maxY,p.y+18)}return{minX,minY,maxX,maxY}};
const fit=(targetKeys)=>{const b=bounds(targetKeys||visNodes.map(n=>n.qualified_name));if(!b){camera={x:-50,y:-50,w:100,h:100};svg.setAttribute('viewBox',`${camera.x} ${camera.y} ${camera.w} ${camera.h}`);return;}const pad=48;const w=Math.max(260,b.maxX-b.minX+pad*2),h=Math.max(200,b.maxY-b.minY+pad*2);camera={x:b.minX-pad,y:b.minY-pad,w,h};svg.setAttribute('viewBox',`${camera.x} ${camera.y} ${camera.w} ${camera.h}`)};
const draw=()=>{svg.innerHTML='';empty.style.display=visNodes.length?'none':'flex';if(!visNodes.length){ins.textContent='No callables match the current filters.';return;}layout();const rel=sel?related(sel):{up:new Set(),down:new Set()};for(const e of visEdges){const a=pos[e.caller_qualified_name],b=pos[e.callee_qualified_name];if(!a||!b)continue;const keep=!sel||(e.caller_qualified_name===sel||e.callee_qualified_name===sel||rel.up.has(e.caller_qualified_name)&&rel.up.has(e.callee_qualified_name)||rel.down.has(e.caller_qualified_name)&&rel.down.has(e.callee_qualified_name)||rel.up.has(e.caller_qualified_name)&&e.callee_qualified_name===sel||e.caller_qualified_name===sel&&rel.down.has(e.callee_qualified_name));svg.insertAdjacentHTML('beforeend',`<line class='edge ${keep&&sel?'hl':''} ${sel&&!keep?'muted':''}' x1='${a.x}' y1='${a.y}' x2='${b.x}' y2='${b.y}'/>`);}for(const n of visNodes){const p=pos[n.qualified_name];const keep=!sel||n.qualified_name===sel||rel.up.has(n.qualified_name)||rel.down.has(n.qualified_name);const stroke=n.qualified_name===sel?'#ffd166':'#1b2542';svg.insertAdjacentHTML('beforeend',`<g class='node ${keep?'':'muted'}' data-q='${n.qualified_name}'><circle cx='${p.x}' cy='${p.y}' r='8' fill='${color(n)}' stroke='${stroke}' stroke-width='2'/><text x='${p.x+12}' y='${p.y+4}' fill='#d7deff' font-size='12'>${n.callable_name}</text></g>`);}svg.querySelectorAll('.node').forEach(el=>el.onclick=()=>select(el.dataset.q));if(sel&&pos[sel]){const relKeys=[sel,...rel.up,...rel.down];fit(relKeys)}else fit();};
function render(){const q=qEl.value.toLowerCase(),mf=mEl.value,rf=rEl.value;visNodes=nodes.filter(n=>(!q||n.callable_name.toLowerCase().includes(q)||n.qualified_name.toLowerCase().includes(q))&&(!mf||n.module_name===mf)&&(!rf||n.role===rf));const set=new Set(visNodes.map(n=>n.qualified_name));visEdges=edges.filter(e=>set.has(e.caller_qualified_name)&&set.has(e.callee_qualified_name));if(sel&&!set.has(sel))sel=null;draw();}
function select(qn){sel=qn;const n=byQ[qn];const upstream=[...new Set(visEdges.filter(e=>e.callee_qualified_name===qn).map(e=>e.caller_qualified_name.split('.').slice(-2).join('.')))].sort();const downstream=[...new Set(visEdges.filter(e=>e.caller_qualified_name===qn).map(e=>e.callee_qualified_name.split('.').slice(-2).join('.')))].sort();const ctype=n.exported?'public callable':(n.is_underscore?'private helper':'internal callable');ins.innerHTML=`<div class='pill'>module: ${n.module_name}</div><div class='pill'>role: ${n.role}</div><div class='pill'>type: ${ctype}</div><h4 style='margin:10px 0 4px'>${n.callable_name}</h4><b>Upstream callers</b><br>${upstream.join('<br>')||'—'}<br><br><b>Downstream calls</b><br>${downstream.join('<br>')||'—'}`;draw();}
[qEl,mEl,rEl].forEach(x=>x.oninput=render);resetBtn.onclick=()=>{sel=null;render()};
svg.addEventListener('wheel',e=>{if(!visNodes.length)return;e.preventDefault();const f=e.deltaY<0?0.9:1.1;camera.w*=f;camera.h*=f;svg.setAttribute('viewBox',`${camera.x} ${camera.y} ${camera.w} ${camera.h}`)},{passive:false});
let dragging=false,sx=0,sy=0;svg.addEventListener('pointerdown',e=>{dragging=true;sx=e.clientX;sy=e.clientY;svg.setPointerCapture(e.pointerId)});svg.addEventListener('pointermove',e=>{if(!dragging)return;const dx=(e.clientX-sx)*(camera.w/svg.clientWidth),dy=(e.clientY-sy)*(camera.h/svg.clientHeight);camera.x-=dx;camera.y-=dy;sx=e.clientX;sy=e.clientY;svg.setAttribute('viewBox',`${camera.x} ${camera.y} ${camera.w} ${camera.h}`)});svg.addEventListener('pointerup',()=>dragging=false);
svg.addEventListener('touchstart',e=>{if(e.touches.length===2){const[a,b]=e.touches;pinchDist=Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY)}if(e.touches.length===1&&e.detail===2){sel=null;render()}},{passive:true});svg.addEventListener('touchmove',e=>{if(e.touches.length!==2||!pinchDist)return;const[a,b]=e.touches;const d=Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY);const f=pinchDist/d;camera.w*=f;camera.h*=f;pinchDist=d;svg.setAttribute('viewBox',`${camera.x} ${camera.y} ${camera.w} ${camera.h}`)},{passive:true});
render();
});
</script></body></html>"""


def write_callable_map_manifest(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], module_summary: list[dict[str, Any]]) -> None:
    CALLABLE_MAP_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    CALLABLE_MAP_JSON_PATH.write_text(
        json.dumps({"nodes": nodes, "edges": edges, "module_summary": module_summary}, indent=2) + "\n",
        encoding="utf-8",
    )
    CALLABLE_MAP_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    CALLABLE_MAP_HTML_PATH.write_text(render_callable_map_html(), encoding="utf-8")


def main() -> None:
    public = parse_public_exports()
    module_data = {p.stem: parse_module(p) for p in PKG_DIR.glob("*.py") if p.name != "__init__.py"}

    discovered_modules = sorted(
        p.stem
        for p in PKG_DIR.glob("*.py")
        if p.name not in {"__init__.py", "docs_metadata.py"} and p.stem not in INTERNAL_MODULE_BLACKLIST
    )

    docs_metadata = parse_docs_metadata()
    template_flow_docs = parse_template_flow_docs()
    module_docs_metadata = parse_module_docs_metadata()

    missing_metadata = sorted(name for name in public if name not in docs_metadata)
    if missing_metadata:
        raise RuntimeError("Missing PUBLIC_SYMBOL_DOCS entries for exported symbols: " + ", ".join(missing_metadata))

    unknown_metadata = sorted(name for name in docs_metadata if name not in public)
    if unknown_metadata:
        raise RuntimeError("PUBLIC_SYMBOL_DOCS contains symbols not exported in __all__: " + ", ".join(unknown_metadata))

    symbol_map: dict[str, Symbol] = {}
    function_symbol_map: dict[str, Symbol] = {}
    for name in public:
        preferred_module = canonical_public_module(docs_metadata[name]["module"])
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
        symbol.summary = meta.get("summary_override") or symbol.summary
        symbol.purpose = meta.get("purpose") or symbol.summary or "—"
        enforce_placeholder_guard = symbol.actual_module in {"config", "ai"}
        if enforce_placeholder_guard and symbol.summary:
            _assert_non_placeholder_summary(symbol.name, "summary", symbol.summary)
        if enforce_placeholder_guard and symbol.purpose and symbol.purpose != "—":
            _assert_non_placeholder_summary(symbol.name, "purpose", symbol.purpose)
        symbol_role = meta.get("role")
        if not symbol_role:
            raise RuntimeError(f"Missing explicit role for {symbol.name} in PUBLIC_SYMBOL_DOCS")
        symbol.role = str(symbol_role).lower()
        if symbol.role not in {"essential", "optional", "internal"}:
            raise RuntimeError(f"Invalid role {symbol.role!r} for {symbol.name}; expected essential/optional/internal")
        if symbol.role == "internal" and not symbol.name.startswith("_"):
            raise RuntimeError(f"Non-underscore callable cannot be internal: {symbol.name}")
        if symbol.role in {"essential", "optional"} and symbol.name.startswith("_"):
            raise RuntimeError(f"Underscore callable cannot be public role: {symbol.name}")

    function_symbol_map = {name: symbol for name, symbol in symbol_map.items() if symbol.obj_type == "function"}
    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    module_manifest = {row["module_name"]: row for row in module_docs_metadata}
    discovered_doc_modules = [INTERNAL_ALIAS_MODULES.get(module, module) for module in discovered_modules]
    module_index_lines = ["# Module API Catalogue", "", "Function Reference/workflow pages are the primary entrypoint. Module pages below are secondary technical references.", "", "Short-form modules remain import-compatible aliases but are intentionally hidden from this user-facing catalogue.", ""]
    all_doc_modules = discovered_doc_modules
    for module in all_doc_modules:
        actual_module = next((k for k,v in PUBLIC_MODULE_PREFERRED_NAMES.items() if v==module), module)
        info = module_data[actual_module]
        module_data[module] = info
        info = module_data[module]
        module_md = MODULE_DIR / f"{module}.md"
        public_in_module = [s for s in function_symbol_map.values() if s.public_module == module]
        is_internal_only = not public_in_module
        title = f"# `{module}` module" if not is_internal_only else f"# `{module}` module (internal)"
        module_visibility = module_manifest.get(module, {}).get("visibility", "public")
        if module_visibility == "public":
            status_banner = '<div class="api-status-block">\n  <span class="api-chip api-chip-module">Module overview</span>\n</div>'
        elif public_in_module:
            status_banner = (
                '<div class="api-status-block">\n'
                '  <span class="api-chip api-chip-internal">Advanced supporting module</span>\n'
                '  <div class="api-chip-subtitle">Used by workflow references but not promoted as a primary notebook module.</div>\n'
                '</div>'
            )
        elif is_internal_only:
            status_banner = (
                '<div class="api-status-block">\n'
                '  <span class="api-chip api-chip-internal">Internal-only module</span>\n'
                '  <div class="api-chip-subtitle">Not intended as a primary user-facing API surface.</div>\n'
                '</div>'
            )
        else:
            status_banner = (
                '<div class="api-status-block">\n'
                '  <span class="api-chip api-chip-internal">Internal-only module</span>\n'
                '</div>'
            )
        lines = [title, "", status_banner, ""]
        if module == "data_product_metadata":
            lines.extend(
                [
                    "## Module boundary",
                    "",
                    "This module stores and retrieves metadata evidence. It does not own governance approval logic. Agreement approval, classification, sensitivity, and PII review remain in `data_governance.py` and the `01_da_<agreement>` notebook.",
                    "",
                ]
            )
        if public_in_module:
            recommended = sorted([s for s in public_in_module if s.role == "essential"], key=lambda x: x.name.lower())
            advanced = sorted([s for s in public_in_module if s.role == "optional"], key=lambda x: x.name.lower())
            lines.extend(["## Essential callables", ""])
            lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
            for s in recommended:
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                callable_link = callable_docs_link(s.name, module, docs_metadata)
                lines.append(
                    f"| [`{s.name}`]({callable_link}) | {s.obj_type} | {s.summary or '—'} | "
                    f"{', '.join(f'[`{r}`]({internal_helper_link(s.actual_module, r)}) (internal)' for r in related) or '—'} |"
                )
            if not recommended:
                lines.append("| — | — | No recommended entrypoints configured. | — |")
            if module == "data_quality":
                lines.extend(
                    [
                        "",
                        "Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.",
                    ]
                )

            lines.extend(["", "## Optional callables", ""])
            if advanced:
                lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
                for s in advanced:
                    related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                    callable_link = callable_docs_link(s.name, module, docs_metadata)
                    lines.append(
                        f"| [`{s.name}`]({callable_link}) | {s.obj_type} | {s.summary or '—'} | "
                        f"{', '.join(f'[`{r}`]({internal_helper_link(s.actual_module, r)}) (internal)' for r in related) or '—'} |"
                    )
            else:
                lines.append("No advanced helpers listed for this module.")
        else:
            lines.extend(["## Essential callables", "", "No public exports in this module.", "", "## Optional callables", "", "No advanced helpers listed for this module."])
        lines.extend(["", "## Related internal helpers", ""])
        internal_fns = sorted([f for f in info["functions"] if f.startswith("_")])
        if internal_fns:
            lines.extend(["| Helper | Related public callables |", "|---|---|"])
            for helper in internal_fns:
                users = sorted([u for u in info["used_by"].get(helper, set()) if u in {p.name for p in public_in_module}])
                users_links = ", ".join(
                    f"[`{u}`]({callable_docs_link(u, module, docs_metadata)})" for u in users
                ) or "—"
                lines.append(f"| [`{helper}`]({internal_helper_link(actual_module, helper)}) | {users_links} |")
        else:
            lines.append("No module-level internal helpers detected.")

        if public_in_module:
            for s in sorted([x for x in public_in_module if x.role in {"essential", "optional"}], key=lambda x: x.name.lower()):
                expected_target = callable_docs_link(s.name, module, docs_metadata)
                expected_link = f"[`{s.name}`]({expected_target})"
                if not any(expected_link in line for line in lines):
                    raise RuntimeError(f"Missing callable table link for {module}.{s.name}")
                if f"../../api/reference/{module}/{s.name}.md" in "\n".join(lines):
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
        module_index_lines.append(f"- [`{module}`]({module}.md)")

    (MODULE_DIR / "index.md").write_text("\n".join(module_index_lines) + "\n", encoding="utf-8", newline="\n")
    discovered_set = set(discovered_doc_modules)
    workflow_sidebar_rows = [row for row in module_docs_metadata if row.get("sidebar_include")]
    workflow_sidebar_groups: dict[str, list[str]] = {}
    for row in workflow_sidebar_rows:
        module_name = row["module_name"]
        if module_name not in discovered_set:
            raise RuntimeError(f"Workflow sidebar module is missing in src/fabricops_kit: {module_name}")
        workflow_sidebar_groups.setdefault(row["sidebar_group"], []).append(module_name)

    mkdocs_text = MKDOCS_PATH.read_text(encoding="utf-8")
    start_marker = "      # AUTO-GENERATED-MODULES-START"
    end_marker = "      # AUTO-GENERATED-MODULES-END"
    if start_marker in mkdocs_text and end_marker in mkdocs_text:
        generated_lines = []
        for modules in workflow_sidebar_groups.values():
            for module in modules:
                generated_lines.append(f"          - {module}: api/modules/{module}.md")
        generated = "\n".join(generated_lines)
        before, rest = mkdocs_text.split(start_marker, 1)
        middle, after = rest.split(end_marker, 1)
        mkdocs_text = before + start_marker + "\n" + generated + "\n" + end_marker + after
        MKDOCS_PATH.write_text(mkdocs_text, encoding="utf-8", newline="\n")

    manifest_rows = []
    known_modules = set(discovered_doc_modules)
    for s in sorted(function_symbol_map.values(), key=lambda x: x.name.lower()):
        canonical_module = canonical_public_module(s.public_module)
        if canonical_module not in known_modules:
            raise RuntimeError(f"Callable {s.name} resolved to module_name without generated page: {canonical_module!r}.")
        module_meta = module_manifest.get(canonical_module, {"visibility": "public", "sidebar_include": True, "module_summary": "", "sidebar_group": "Modules"})
        callable_role = s.role
        manifest_rows.append(
            {
                "module_name": canonical_module,
                "visibility": module_meta["visibility"],
                "module_summary": module_meta["module_summary"],
                "sidebar_group": module_meta["sidebar_group"],
                "sidebar_include": module_meta["sidebar_include"],
                "callable_name": s.name,
                "callable_visibility": module_meta["visibility"],
                "callable_role": callable_role,
                "template_notebook": docs_metadata[s.name].get("template_notebook"),
                "template_segment": docs_metadata[s.name].get("template_segment"),
            }
        )
    manifest_modules = []
    for module in discovered_doc_modules:
        meta = module_manifest.get(module, {})
        manifest_modules.append({
            "module_name": module,
            "visibility": meta.get("visibility", "public"),
            "module_summary": meta.get("module_summary", ""),
            "sidebar_group": meta.get("sidebar_group", "Modules"),
            "sidebar_include": meta.get("sidebar_include", True),
        })
    MANIFEST_PATH.write_text(json.dumps({"modules": manifest_modules, "callables": manifest_rows}, indent=2) + "\n", encoding="utf-8")
    nodes, edges, module_summary = build_callable_graph(module_data, symbol_map, public, docs_metadata)
    CALLABLE_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    CALLABLE_MAP_PATH.write_text(
        render_callable_map_page(),
        encoding="utf-8",
        newline="\n",
    )
    write_callable_map_manifest(nodes, edges, module_summary)

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
        "02_ex": "`02_ex` proposes evidence and AI-assisted suggestions.",
        "03_pc": "`03_pc` loads approved metadata and enforces controls.",
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
            "Use this page to understand the purpose and segment flow of this notebook template. Each segment shows the typical callables commonly used there.",
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
                symbol_link = public_reference_link(s.name, docs_metadata, context="notebook")
                segment_rows.append([
                    _anchor(symbol_link, s.name, code=True),
                    _module_link(s.public_module, base_prefix="../../"),
                    s.purpose or "—",
                ])
            if segment_rows:
                notebook_lines.extend(
                    _html_table(
                        "reference-function-table notebook-structure-function-table",
                        ["Callable", "Module", "Why it is commonly used here"],
                        segment_rows,
                    )
                )
                notebook_lines.append("")
        (NOTEBOOK_STRUCTURE_DIR / page_name).write_text("\n".join(notebook_lines) + "\n", encoding="utf-8", newline="\n")

    usage_guide = [
        "# Function Usage Guide",
        "",
        "Use this page to understand how notebook templates map to the main public callables.",
        "",
        "## Start from the templates",
        "",
    ]
    notebook_structure_links = {
        "00_env_config": "../notebook-structure/00-env-config/",
        "01_data_agreement": "../notebook-structure/01-data-sharing-agreement/",
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
    usage_guide.extend(_html_table("reference-template-table", ["Notebook", "Guided usage", "Full template"], template_rows))

    usage_guide.extend([
        "",
        "## What runs where",
        "",
        "- `00_env_config` is shared setup.",
        "- `01_data_sharing_agreement` is the governance source of truth.",
        "- `02_ex` proposes evidence and AI-assisted suggestions.",
        "- `03_pc` loads approved metadata and enforces controls.",
        "",
        "AI functions are advisory. Approved contracts and pipeline notebooks are the enforcement point.",
        "",
    ])
    FUNCTION_USAGE_GUIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FUNCTION_USAGE_GUIDE_PATH.write_text("\n".join(usage_guide) + "\n", encoding="utf-8", newline="\n")

    ref = [
        "# Function Reference",
        "",
        "Use this page as a callable lookup after you understand the notebook flow.",
        "",
    ]

    ref.extend(
        [
            "## Find a callable",
            "",
            "Use the finder below to look up public callable functions.",
            "",
            '<div class="callable-finder" data-callable-finder>',
            '  <label class="callable-finder-label" for="callable-finder-input">Search callable functions</label>',
            '  <input id="callable-finder-input" class="callable-finder-input" type="search" placeholder="Search callable functions" aria-describedby="callable-finder-help callable-finder-status callable-finder-examples" autocomplete="off">',
            '  <p id="callable-finder-help" class="callable-finder-help">Search by function name, module, role, starter path, or what the public function does.</p>',
            '  <p id="callable-finder-examples" class="callable-finder-examples">Try: <span class="callable-finder-chip">csv</span> <span class="callable-finder-chip">data_quality</span> <span class="callable-finder-chip">quarantine</span></p>',
            '  <p id="callable-finder-status" class="callable-finder-status" aria-live="polite">Showing all public callables.</p>',
            '  <fieldset class="callable-role-filters">',
            '    <legend>Role filters</legend>',
            '    <label><input type="checkbox" data-role-filter="essential" checked> Essential</label>',
            '    <p class="callable-role-note"><strong>Essential</strong>: Core functions used in the starter notebook flow.</p>',
            '    <label><input type="checkbox" data-role-filter="optional" checked> Optional</label>',
            '    <p class="callable-role-note"><strong>Optional</strong>: Extra helper functions for advanced or situational use.</p>',
            '  </fieldset>',
            '  <p class="callable-finder-empty" data-callable-finder-empty hidden>No callables match your search.</p>',
            "</div>",
            "",
            "## Function catalogue",
            "",
            "## All public functions",
            "",
        ]
    )
    all_items: list[str] = []
    for s in sorted(function_symbol_map.values(), key=lambda x: x.name.lower()):
        symbol_link = public_reference_link(s.name, docs_metadata, context="reference")
        starter_path = ", ".join(sorted(starter_symbol_to_notebooks.get(s.name, set()))) or "—"
        purpose = s.purpose or s.summary or "—"
        all_items.extend(
            [
                (
                    f'<article id="{_esc(s.name)}" class="reference-catalogue-item" '
                    f'data-callable-row="true" data-callable-name="{_esc(s.name)}" '
                    f'data-callable-module="{_esc(s.public_module)}" '
                    f'data-callable-starter-path="{_esc(starter_path)}" '
                    f'data-role="{_esc(s.role)}" '
                    f'data-callable-purpose="{_esc(purpose)}">'
                ),
                f'  <h3 class="reference-catalogue-item-name">{_anchor(symbol_link, s.name, code=True)}</h3>',
                (
                    '  <p class="reference-catalogue-item-meta">'
                    f'{_module_link(s.public_module)}'
                    f' <span class="reference-catalogue-separator">·</span> <span>{_esc(s.role)}</span>'
                    f' <span class="reference-catalogue-separator">·</span> <span>{_esc(starter_path)}</span>'
                    "</p>"
                ),
                f'  <p class="reference-catalogue-item-purpose">{_esc(purpose)}</p>',
                "</article>",
            ]
        )
    ref.extend(['<div class="reference-catalogue-list">', *all_items, "</div>"])

    ref.append("")
    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text("\n".join(ref) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
