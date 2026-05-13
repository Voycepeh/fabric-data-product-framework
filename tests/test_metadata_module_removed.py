from pathlib import Path
import json


def test_manifest_includes_discovered_metadata_alias_module() -> None:
    manifest = json.loads(Path("docs/reference/manifest.json").read_text(encoding="utf-8"))
    modules = {m["module_name"] for m in manifest.get("modules", [])}
    assert "data_product_metadata" in modules
    assert Path("docs/api/modules/data_product_metadata.md").exists()
