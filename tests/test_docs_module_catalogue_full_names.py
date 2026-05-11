from pathlib import Path
import json

def test_runtime_module_removed_from_manifest_and_source() -> None:
    assert not Path("src/fabricops_kit/runtime.py").exists()
    manifest = json.loads(Path("docs/reference/manifest.json").read_text(encoding="utf-8"))
    modules = {m["module_name"] for m in manifest.get("modules", [])}
    assert "runtime_context" not in modules
