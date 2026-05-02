from __future__ import annotations

import os
import subprocess
import sys

from fabric_data_product_framework.mvp_steps import get_mvp_step_registry


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
        "MVP ARTIFACT VALIDATION",
    ]
    for marker in required:
        assert marker in text


def test_template_contains_all_expected_artifact_names():
    text = open("templates/notebooks/fabric_data_product_mvp.py", encoding="utf-8").read()
    expected = sorted({a for s in get_mvp_step_registry() for a in s["expected_artifacts"]})
    for artifact_name in expected:
        assert artifact_name in text


def test_mvp_template_sample_mode_runs_and_artifacts_validate():
    result = _run_template()
    assert result.returncode == 0, result.stderr
    assert '"valid": true' in result.stdout.lower()
    assert "FINAL STATUS: NOT_READY" in result.stdout
