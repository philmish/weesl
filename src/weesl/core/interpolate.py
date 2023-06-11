import os
import re
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

def _resolve_env_placeholder(placeholder: str) -> str:
    if placeholder.endswith(":"):
        placeholder = placeholder[:-1]
    parts = placeholder.split(":")
    if len(parts) < 2:
        raise Exception
    var = parts[1]
    default = ""
    if ";" in var:
        var_parts = var.split(";")
        var = var_parts[0]
        default = var_parts[1]
    return get_from_env(var, default)

def get_from_env(var: str, default: str = "") -> str:
    try:
        return os.environ[var]
    except KeyError:
        return default

def interpolate_env(var: Any) -> Any:
    if isinstance(var, str):
        pattern = re.compile(r"(ENV:[a-zA-Z]+(;[ -~]+)?:)")
        matches = re.findall(pattern, var)
        for match in matches:
            placeholder = match[0]
            var = var.replace(
                placeholder, 
                _resolve_env_placeholder(placeholder)
            )
    return var




