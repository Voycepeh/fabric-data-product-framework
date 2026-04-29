from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "templates" / "fabric_adapters.py"
SPEC = spec_from_file_location("fabric_adapters", MODULE_PATH)
MODULE = module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_stringify_nested_metadata_fields_converts_nested_values():
    records = [{"a": 1, "b": {"x": 2}, "c": [1, 2]}]
    out = MODULE._stringify_nested_metadata_fields(records)
    assert out[0]["a"] == 1
    assert out[0]["b"] == '{"x": 2}'
    assert out[0]["c"] == '[1, 2]'


def test_stringify_nested_metadata_fields_empty_records_returns_empty_list():
    assert MODULE._stringify_nested_metadata_fields([]) == []


def test_stringify_nested_metadata_fields_flat_records_unchanged():
    records = [{"a": "v", "b": 2}]
    assert MODULE._stringify_nested_metadata_fields(records) == records
