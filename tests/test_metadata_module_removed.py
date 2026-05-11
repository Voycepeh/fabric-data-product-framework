from pathlib import Path
import json
import ast

def test_metadata_module_removed() -> None:
    assert not Path("src/fabricops_kit/metadata.py").exists()

def test_manifest_and_docs_exclude_metadata_module() -> None:
    manifest = json.loads(Path("docs/reference/manifest.json").read_text(encoding="utf-8"))
    assert "data_product_metadata" not in {m["module_name"] for m in manifest.get("modules", [])}
    assert "data_product_metadata" not in {c["module_name"] for c in manifest.get("callables", [])}
    text = Path("src/fabricops_kit/docs_metadata.py").read_text(encoding="utf-8")
    tree = ast.parse(text)
    modules = []
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "MODULE_DOCS_METADATA":
            modules = ast.literal_eval(node.value)
    assert "data_product_metadata" not in {m["module_name"] for m in modules}
    assert not Path("docs/api/modules/data_product_metadata.md").exists()
