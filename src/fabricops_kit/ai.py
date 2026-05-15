"""Internal helpers for optional Microsoft Fabric AI runtime integration."""
from __future__ import annotations


def _check_fabric_ai_functions_available() -> dict:
    """Check whether Fabric AI Functions can be imported in the current runtime."""
    try:
        import synapse.ml.spark.aifunc as _aifunc  # noqa: F401
        return {
            "available": True,
            "runtime": "fabric_pyspark",
            "message": "Microsoft Fabric AI Functions import check passed.",
        }
    except Exception as exc:  # pragma: no cover
        return {
            "available": False,
            "runtime": "local_or_unknown",
            "message": (
                "Microsoft Fabric AI Functions are unavailable. "
                "Require Fabric PySpark runtime and feature enablement. "
                f"Import error: {exc}"
            ),
        }


def _configure_fabric_ai_functions(
    deployment_name: str | None = None,
    temperature: float = 0.0,
) -> dict:
    """Apply optional default Fabric AI Function configuration."""
    try:
        import synapse.ml.spark.aifunc as aifunc
    except Exception as exc:  # pragma: no cover
        return {
            "available": False,
            "configured": False,
            "message": f"Microsoft Fabric AI Functions are unavailable. Import error: {exc}",
        }

    conf = getattr(aifunc, "default_conf", None)
    if conf is None:
        return {
            "available": True,
            "configured": False,
            "message": "aifunc.default_conf is not available in this runtime.",
        }
    if deployment_name and hasattr(conf, "set_deployment_name"):
        conf.set_deployment_name(deployment_name)
    if hasattr(conf, "set_temperature"):
        conf.set_temperature(float(temperature))
    return {
        "available": True,
        "configured": True,
        "message": "Microsoft Fabric AI Functions default configuration applied.",
    }
