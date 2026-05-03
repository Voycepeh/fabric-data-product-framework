"""Microsoft Fabric AI Functions helpers for optional AI-in-the-loop workflows."""

from __future__ import annotations

import importlib.util
from typing import Any


def check_fabric_ai_functions_available() -> dict:
    """Check whether Microsoft Fabric AI Functions appear available.

    Returns
    -------
    dict
        Status dictionary with keys ``available``, ``runtime``, and ``message``.

    Notes
    -----
    Fabric notebook runtime required. This is a best-effort import check and does
    not guarantee tenant switch, capacity, or deployment configuration.
    """
    try:
        import synapse.ml.spark.aifunc as _aifunc  # noqa: F401
        return {"available": True, "runtime": "fabric_pyspark", "message": "Microsoft Fabric AI Functions import check passed."}
    except Exception as exc:  # pragma: no cover - runtime dependent
        return {
            "available": False,
            "runtime": "local_or_unknown",
            "message": (
                "Microsoft Fabric AI Functions are unavailable in this environment. "
                "They require Fabric PySpark runtime and Microsoft Fabric AI feature availability. "
                f"Import error: {exc}"
            ),
        }


def configure_fabric_ai_functions(deployment_name: str | None = None, temperature: float = 0.0) -> dict:
    """Configure Fabric AI Functions default settings when available.

    Parameters
    ----------
    deployment_name : str | None, optional
        Optional deployment name passed to ``aifunc.default_conf.set_deployment_name``.
    temperature : float, default=0.0
        Temperature value passed to ``aifunc.default_conf.set_temperature`` when supported.
    """
    try:
        import synapse.ml.spark.aifunc as aifunc
    except Exception as exc:  # pragma: no cover - runtime dependent
        return {
            "available": False,
            "configured": False,
            "message": (
                "Microsoft Fabric AI Functions are unavailable in this environment. "
                "They require Fabric PySpark runtime and Microsoft Fabric AI feature availability. "
                f"Import error: {exc}"
            ),
        }

    conf = getattr(aifunc, "default_conf", None)
    if conf is None:
        return {"available": True, "configured": False, "message": "aifunc.default_conf is not available in this runtime."}

    if deployment_name and hasattr(conf, "set_deployment_name"):
        conf.set_deployment_name(deployment_name)
    if hasattr(conf, "set_temperature"):
        conf.set_temperature(float(temperature))

    return {
        "available": True,
        "configured": True,
        "message": "Microsoft Fabric AI Functions default configuration applied.",
        "deployment_name": deployment_name,
        "temperature": float(temperature),
    }


def _fabric_ai_dependencies_available() -> bool:
    return importlib.util.find_spec("openai") is not None and importlib.util.find_spec("pydantic") is not None


def _extract_fabric_ai_response_payload(ai_response: Any):
    import pandas as pd

    if isinstance(ai_response, (str, list)):
        return ai_response
    if isinstance(ai_response, dict):
        return ai_response.get("response") or ai_response.get("generated_response") or ai_response.get("text") or ai_response
    if isinstance(ai_response, pd.DataFrame):
        if ai_response.empty:
            return "[]"
        row = ai_response.iloc[0].to_dict()
        for key in ("response", "generated_response", "text"):
            val = row.get(key)
            if isinstance(val, (str, list, dict)):
                return val
        for val in row.values():
            if isinstance(val, (str, list)):
                return val
        return row
    return ai_response


def generate_dq_rule_candidates_with_fabric_ai(profile, contract=None, business_context=None, dataset_name=None, table_name=None, response_format=None) -> list[dict]:
    """Generate DQ candidate rules using Fabric AI Functions.

    This helper only returns candidate suggestions and does not enforce pipeline
    outcomes directly.
    """
    import pandas as pd
    from .quality import build_quality_rule_generation_prompt, normalize_dq_rule, parse_ai_quality_rule_candidates

    if not _fabric_ai_dependencies_available():
        raise RuntimeError(
            "Fabric AI candidate generation requires Microsoft Fabric AI functions plus openai/pydantic runtime dependencies. "
            "Install the fabric-ai extra or run %pip install openai pydantic in the Fabric notebook."
        )

    prompt = build_quality_rule_generation_prompt(
        profile=profile,
        contract=contract,
        business_context=business_context,
        table_name=table_name,
        dataset_name=dataset_name,
    )
    prompt_df = pd.DataFrame([{"prompt": prompt}])
    ai = getattr(prompt_df, "ai", None)
    if ai is None or not hasattr(ai, "generate_response"):
        raise RuntimeError(
            "Fabric AI candidate generation requires Microsoft Fabric AI functions plus openai/pydantic runtime dependencies. "
            "Install the fabric-ai extra or run %pip install openai pydantic in the Fabric notebook."
        )

    kwargs = {"prompt": prompt}
    if response_format is not None:
        kwargs["response_format"] = response_format
    raw_response = _extract_fabric_ai_response_payload(ai.generate_response(**kwargs))
    parsed = parse_ai_quality_rule_candidates(raw_response)

    out = []
    for c in parsed.get("candidates", []):
        rule = {
            "rule_id": c.get("rule_id") or c.get("name"),
            "table_name": table_name,
            "column": c.get("column"),
            "columns": c.get("columns"),
            "rule_type": c.get("rule_type"),
            "severity": c.get("severity", "warning"),
            "description": c.get("layman_rule") or c.get("reason"),
            "generated_by": "fabric_ai",
            "status": "candidate",
        }
        cfg = c.get("rule_config") or {}
        if isinstance(cfg, dict):
            rule.update(cfg)
        out.append(normalize_dq_rule(rule))
    return out
