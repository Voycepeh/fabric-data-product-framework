import json
import sys
import types
from pathlib import Path

import fabricops_kit.metadata as metadata


class JavaMapLike:
    def __init__(self, values):
        self.values = values

    def get(self, key):
        if key == "explode":
            raise RuntimeError("boom")
        return self.values.get(key)


class FakeSpark:
    def __init__(self):
        self.rows = None

    def createDataFrame(self, rows):
        self.rows = rows
        return rows


def test_runtime_context_reads_javamap_keys(monkeypatch):
    context = JavaMapLike(
        {
            "currentNotebookName": "01_data_agreement_template",
            "currentNotebookId": "nb-1",
            "currentWorkspaceName": "ws",
            "currentWorkspaceId": "wid",
            "userName": "alice",
            "userId": "u1",
        }
    )
    notebookutils = types.SimpleNamespace(runtime=types.SimpleNamespace(context=context))
    monkeypatch.setitem(sys.modules, "notebookutils", notebookutils)

    out = metadata._runtime_context()
    assert out["currentNotebookName"] == "01_data_agreement_template"
    assert out["currentNotebookId"] == "nb-1"
    assert out["currentWorkspaceName"] == "ws"
    assert out["currentWorkspaceId"] == "wid"
    assert out["userName"] == "alice"
    assert out["userId"] == "u1"


def test_runtime_context_reads_dict_keys(monkeypatch):
    context = {
        "currentNotebookName": "01_data_agreement_template",
        "currentNotebookId": "nb-1",
        "currentWorkspaceName": "ws",
        "currentWorkspaceId": "wid",
        "userName": "alice",
        "userId": "u1",
    }
    notebookutils = types.SimpleNamespace(runtime=types.SimpleNamespace(context=context))
    monkeypatch.setitem(sys.modules, "notebookutils", notebookutils)
    assert metadata._runtime_context()["currentWorkspaceId"] == "wid"


def test_context_get_supports_fallback_and_safe_lookup():
    context = JavaMapLike({"workspaceId": "wid-old", "explode": "ignored"})
    assert metadata._context_get(context, "explode", "workspaceId") == "wid-old"


def test_runtime_context_missing_returns_empty(monkeypatch):
    monkeypatch.delitem(sys.modules, "notebookutils", raising=False)
    assert metadata._runtime_context() == {}


def test_register_current_notebook_uses_current_and_fallback_keys(monkeypatch):
    captured = {}

    def fake_write(spark, rows, metadata_path, table_name, mode="append"):
        captured["row"] = rows[0]

    monkeypatch.setattr(metadata, "write_metadata_rows", fake_write)
    monkeypatch.setattr(
        metadata,
        "_runtime_context",
        lambda: {
            "currentWorkspaceId": "wid",
            "currentWorkspaceName": "ws",
            "currentNotebookId": "nbid",
            "currentNotebookName": "01_data_agreement_template",
            "userId": "u1",
            "userName": "alice",
        },
    )

    row = metadata.register_current_notebook(
        spark=FakeSpark(),
        metadata_path="/tmp/meta",
        agreement_id="A1",
        notebook_type="01",
        environment_name="Sandbox",
        dataset_name="d",
        table_name="t",
        topic="topic",
        pipeline_name="p",
    )

    expected_columns = {
        "agreement_id", "dataset_name", "environment_name", "notebook_id", "notebook_name",
        "notebook_type", "notebook_url", "pipeline_name", "registered_at", "table_name", "topic",
        "user_id", "user_name", "workspace_id", "workspace_name",
    }
    assert set(row) == expected_columns
    assert row["workspace_id"] == "wid"
    assert row["workspace_name"] == "ws"
    assert row["notebook_id"] == "nbid"
    assert row["notebook_name"] == "01_data_agreement_template"
    assert row["user_id"] == "u1"
    assert row["user_name"] == "alice"
    assert row["notebook_url"].endswith("/groups/wid/notebooks/nbid")
    assert captured["row"] == row


def test_register_current_notebook_handles_none_values(monkeypatch):
    captured = {}

    def fake_write(spark, rows, metadata_path, table_name, mode="append"):
        captured["row"] = rows[0]

    monkeypatch.setattr(metadata, "write_metadata_rows", fake_write)
    monkeypatch.setattr(
        metadata,
        "_runtime_context",
        lambda: {
            "currentWorkspaceId": None,
            "currentWorkspaceName": None,
            "currentNotebookId": None,
            "currentNotebookName": None,
            "userId": None,
            "userName": None,
        },
    )

    row = metadata.register_current_notebook(
        spark=FakeSpark(),
        metadata_path="/tmp/meta",
        agreement_id="A1",
        notebook_type="01",
    )
    assert row["workspace_id"] == ""
    assert row["workspace_name"] == ""
    assert row["notebook_id"] == ""
    assert row["user_id"] == ""
    assert row["user_name"] == ""
    assert row["environment_name"] == ""
    assert row["dataset_name"] == ""
    assert row["table_name"] == ""
    assert row["topic"] == ""
    assert row["pipeline_name"] == ""
    assert row["notebook_url"] == ""
    assert row["notebook_name"] == "unknown_notebook"
    assert all(isinstance(value, str) for value in row.values())
    assert captured["row"] == row


def test_templates_do_not_import_root_private_helpers():
    nb = Path("templates/notebooks/01_data_agreement_template.ipynb").read_text(encoding="utf-8")
    data = json.loads(nb)
    all_source = "\n".join("".join(cell.get("source", [])) for cell in data.get("cells", []))
    assert "from fabricops_kit import _" not in all_source
