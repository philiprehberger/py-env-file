""".env file parser with interpolation and multi-file support."""

from __future__ import annotations

import os
import re
from pathlib import Path


__all__ = [
    "load_env",
    "parse_env_file",
]

_INTERPOLATION_RE = re.compile(r"\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def load_env(
    *paths: str,
    override: bool = True,
) -> dict[str, str]:
    """Load one or more .env files into ``os.environ``.

    Files are loaded in order; later files override earlier ones.
    If no paths are given, defaults to ``".env"``.

    Args:
        *paths: Paths to .env files.
        override: If False, existing environment variables are not overwritten.

    Returns:
        Dict of all variables loaded across all files.
    """
    if not paths:
        paths = (".env",)

    all_vars: dict[str, str] = {}

    for path in paths:
        file_path = Path(path)
        if not file_path.is_file():
            continue

        parsed = parse_env_file(str(file_path))
        all_vars.update(parsed)

    for key, value in all_vars.items():
        if override or key not in os.environ:
            os.environ[key] = value

    return all_vars


def parse_env_file(path: str) -> dict[str, str]:
    """Parse a .env file without modifying ``os.environ``.

    Supports:
        - ``KEY=value`` assignments
        - ``export KEY=value`` prefix
        - Single and double quoted values
        - ``#`` comments (full line and inline for unquoted values)
        - Variable interpolation: ``${VAR}`` and ``$VAR``
        - Empty values: ``KEY=``

    Args:
        path: Path to the .env file.

    Returns:
        Dict of parsed key-value pairs.
    """
    env: dict[str, str] = {}
    file_path = Path(path)

    if not file_path.is_file():
        msg = f"File not found: {path}"
        raise FileNotFoundError(msg)

    text = file_path.read_text(encoding="utf-8")

    for line in text.splitlines():
        result = _parse_line(line, env)
        if result is not None:
            key, value = result
            env[key] = value

    return env


def _parse_line(line: str, env: dict[str, str]) -> tuple[str, str] | None:
    stripped = line.strip()

    if not stripped or stripped.startswith("#"):
        return None

    if stripped.startswith("export "):
        stripped = stripped[7:].strip()

    if "=" not in stripped:
        return None

    key, _, raw_value = stripped.partition("=")
    key = key.strip()

    if not key or not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
        return None

    raw_value = raw_value.strip()

    if raw_value.startswith('"') and raw_value.endswith('"') and len(raw_value) >= 2:
        value = raw_value[1:-1]
        value = value.replace('\\"', '"').replace("\\n", "\n").replace("\\t", "\t")
    elif raw_value.startswith("'") and raw_value.endswith("'") and len(raw_value) >= 2:
        value = raw_value[1:-1]
    else:
        comment_idx = raw_value.find(" #")
        if comment_idx >= 0:
            raw_value = raw_value[:comment_idx]
        value = raw_value.strip()

    value = _interpolate(value, env)

    return key, value


def _interpolate(value: str, env: dict[str, str]) -> str:
    def replace_match(match: re.Match[str]) -> str:
        var_name = match.group(1) or match.group(2)
        if var_name in env:
            return env[var_name]
        return os.environ.get(var_name, match.group(0))

    return _INTERPOLATION_RE.sub(replace_match, value)
