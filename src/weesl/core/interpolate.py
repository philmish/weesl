import os
from typing import Any, Dict


def interpolate_placeholder_str(target: str, prefix: str, kv: Dict[str, Any]) -> Any:
    if not isinstance(target, str):
        return target
    for k, v in kv.items():
        var = f"{prefix}{k}"
        if target == var:
            return v
        if f"{prefix}{k}" in target:
            target = target.replace(f"{prefix}{k}", f"{v}")
    return target

def interpolate_env(var: Any) -> Any:
    if isinstance(var, str) and var.startswith("ENV:"):
        parts = var.split(":")
        default = ""
        if len(parts) > 2:
            default = parts[2]
        return os.getenv(parts[1], default)
    return var




