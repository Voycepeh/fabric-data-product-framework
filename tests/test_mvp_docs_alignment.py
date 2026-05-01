from pathlib import Path

from fabric_data_product_framework.mvp_steps import MVP_STEPS


def test_capability_status_references_all_mvp_steps():
    text = Path("docs/capability-status.md").read_text(encoding="utf-8").lower()
    for step in MVP_STEPS:
        assert step["name"].lower() in text
