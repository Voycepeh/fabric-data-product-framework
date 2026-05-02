from __future__ import annotations

import os
import subprocess
import sys


def _run_template() -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = "src"
    return subprocess.run(
        [sys.executable, "templates/notebooks/fabric_data_product_mvp.py"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_mvp_template_contains_required_sections_and_keys():
    text = open("templates/notebooks/fabric_data_product_mvp.py", encoding="utf-8").read()
    required = [
        "# 1) Package and runtime setup [Framework]",
        "# 13) Run summary and handover package [Framework]",
        "USE_SAMPLE_DATA = True",
        "ENABLE_FABRIC_WRITES = False",
        "RUN SUMMARY",
    ]
    for marker in required:
        assert marker in text

    run_summary_keys = [
        '"dataset_name"',
        '"run_id"',
        '"dq_status"',
        '"drift_status"',
        '"target_write_status"',
    ]
    for k in run_summary_keys:
        assert k in text


def test_mvp_template_default_gate_is_not_ready_in_safe_mode():
    result = _run_template()
    assert result.returncode == 0, result.stderr
    assert "FINAL STATUS: NOT_READY" in result.stdout
