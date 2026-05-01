import subprocess
import sys

from scripts.check_release_ready import get_init_version, get_pyproject_version


def test_repo_versions_match() -> None:
    from fabric_data_product_framework import __version__

    with open("pyproject.toml", "rb") as f:
        pyproject_bytes = f.read()

    if sys.version_info >= (3, 11):
        pyproject_text = pyproject_bytes.decode("utf-8")
    else:
        pyproject_text = pyproject_bytes.decode("utf-8")

    assert get_pyproject_version(pyproject_text) == __version__


def test_script_runs_from_repo_root() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_release_ready.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Release-ready version check passed" in result.stdout


def test_parsers_handle_mismatch_samples() -> None:
    pyproject_text = """
[project]
name = "fabric-data-product-framework"
version = "1.2.3"
"""
    init_text = '__version__ = "1.2.4"\n'

    assert get_pyproject_version(pyproject_text) == "1.2.3"
    assert get_init_version(init_text) == "1.2.4"
