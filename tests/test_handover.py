import json

from fabricops_kit.handover import build_handover, build_handover_record, render_handover_markdown


def _ctx():
    return {"run_id": "r1", "dataset_name": "sales", "environment": "dev", "source_table": "a", "target_table": "b", "started_at_utc": "2026-01-01T00:00:00Z"}


def test_build_summary_pass_warning_fail_and_markdown_record():
    summary = build_handover(runtime_context=_ctx(), quality_result={"status": "passed", "can_continue": True})
    assert summary["overall_status"] == "passed"
    warn = build_handover(runtime_context=_ctx(), quality_result={"status": "warning", "can_continue": True})
    assert warn["overall_status"] == "warning"
    fail = build_handover(runtime_context=_ctx(), quality_result={"status": "failed", "can_continue": False})
    assert fail["overall_status"] == "failed"
    md = render_handover_markdown(fail)
    assert "Run ID" in md and "failed" in md
    record = build_handover_record(fail)
    json.dumps(record)


def test_missing_sections_do_not_crash_and_are_explicit():
    summary = build_handover(runtime_context=_ctx())
    assert summary["sections"]["quality"] is None
    assert "quality" in summary["not_provided_sections"]
    md = render_handover_markdown(summary)
    assert "Not Provided Sections" in md
