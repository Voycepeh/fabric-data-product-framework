from __future__ import annotations

import os
import subprocess
import sys


def test_mvp_template_executes_in_dry_run_mode():
    env = dict(os.environ)
    env["PYTHONPATH"] = "src"
    result = subprocess.run(
        [sys.executable, "templates/notebooks/fabric_data_product_mvp.py"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "FINAL STATUS:" in result.stdout
