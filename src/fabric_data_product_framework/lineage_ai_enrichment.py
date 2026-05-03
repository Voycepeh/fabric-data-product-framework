"""AI enrichment layer for deterministic lineage steps."""
from __future__ import annotations
from typing import Any


def fallback_copilot_lineage_prompt(lineage_steps: list[dict[str, Any]]) -> str:
    return (
        "Review deterministic lineage steps below and improve reason/handover notes only. "
        "Do not change source/target structure. Mark uncertain cases for human review.\n"
        f"steps={lineage_steps}"
    )


def enrich_lineage_steps_with_ai(lineage_steps: list[dict[str, Any]], ai_helper: Any | None = None) -> dict[str, Any]:
    """Optionally enrich lineage steps with AI explanations while keeping structure unchanged."""
    if ai_helper is None:
        return {
            "steps": lineage_steps,
            "ai_used": False,
            "fallback_prompt": fallback_copilot_lineage_prompt(lineage_steps),
            "notes": "AI helper unavailable; Copilot fallback prompt generated.",
        }
    enriched = ai_helper(lineage_steps)
    return {"steps": enriched or lineage_steps, "ai_used": True, "fallback_prompt": "", "notes": "AI enrichment applied."}
