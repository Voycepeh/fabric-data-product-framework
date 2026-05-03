"""Deterministic notebook/code scanner for structural dataframe lineage."""
from __future__ import annotations
import ast
from typing import Any

READ_HELPERS = {"lakehouse_table_read": "lakehouse_table", "warehouse_read": "warehouse_table", "lakehouse_csv_read": "file", "lakehouse_excel_read_as_spark": "file", "lakehouse_parquet_read_as_spark": "file"}
WRITE_HELPERS = {"lakehouse_table_write": "lakehouse_table", "warehouse_write": "warehouse_table"}
OPS = {"select","selectExpr","filter","where","withColumn","drop","withColumnRenamed","groupBy","agg","join","union","unionByName","distinct","dropDuplicates","orderBy","sort","fillna","dropna"}


def _name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    return None

def _call_name(call: ast.Call) -> str:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return "unknown"

def _flatten_chain(node: ast.AST) -> tuple[str | None, list[str]]:
    ops: list[str] = []
    cur = node
    while isinstance(cur, ast.Call) and isinstance(cur.func, ast.Attribute):
        ops.append(cur.func.attr)
        cur = cur.func.value
    return _name(cur), list(reversed(ops))

def _step(source:str,target:str,transformation:str,source_type:str,target_type:str,confidence:str,lineno:int,ops:list[str],notes:str="") -> dict[str, Any]:
    return {"source": source,"target": target,"transformation": transformation,"reason": "","source_type": source_type,"target_type": target_type,"confidence": confidence,"notes": notes,"operation_types": ops,"code_refs": [f"line:{lineno}"]}

def scan_notebook_lineage(code: str) -> list[dict[str, Any]]:
    """Scan Python notebook/code text and return deterministic lineage steps."""
    tree = ast.parse(code)
    steps: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets and isinstance(node.value, ast.Call):
            lhs = _name(node.targets[0])
            if not lhs:
                continue
            cname = _call_name(node.value)
            if cname in READ_HELPERS:
                steps.append(_step(cname, lhs, f"read via {cname}", READ_HELPERS[cname], "dataframe", "high", node.lineno, ["read"]))
                continue
            if cname == "read_csv" or cname == "read_parquet" or cname == "read_excel":
                steps.append(_step(cname, lhs, f"read via pandas.{cname}", "file", "dataframe", "high", node.lineno, ["read"]))
                continue
            src, ops = _flatten_chain(node.value)
            if ops:
                confidence = "high" if src else "medium"
                notes = "base dataframe could not be inferred" if not src else ""
                steps.append(_step(src or "unknown", lhs, " -> ".join(ops), "dataframe" if src else "unknown", "dataframe", confidence, node.lineno, ops, notes))

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            cname = _call_name(call)
            if cname in WRITE_HELPERS and call.args:
                src = _name(call.args[0]) or "unknown"
                conf = "high" if src != "unknown" else "medium"
                steps.append(_step(src, cname, f"write via {cname}", "dataframe" if src != "unknown" else "unknown", WRITE_HELPERS[cname], conf, node.lineno, ["write"]))
            if cname == "save" and isinstance(call.func, ast.Attribute):
                src, _ = _flatten_chain(call.func.value)
                steps.append(_step(src or "unknown", "external_target", "write via df.write", "dataframe" if src else "unknown", "unknown", "medium", node.lineno, ["write"], "target format/path not resolved"))
    return steps


def scan_notebook_cells(cells: list[str]) -> list[dict[str, Any]]:
    """Scan notebook cells deterministically and include cell references."""
    out: list[dict[str, Any]] = []
    for idx, cell in enumerate(cells):
        for step in scan_notebook_lineage(cell):
            step["code_refs"].append(f"cell:{idx}")
            out.append(step)
    return out
