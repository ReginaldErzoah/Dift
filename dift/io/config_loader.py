from __future__ import annotations

import json
import os
import pathlib
import re
import sys
from typing import Any, cast

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


ENV_PATTERN = re.compile(r"\$\{([A-ZA-Z0-9_]+)\}")


def load_config(
    file_path: str,
    env: str | None = None,
    expand_env_vars: bool = True,
) -> dict[str, Any]:
    path = pathlib.Path(file_path)

    if not path.exists():
        print(
            f"Warning: Configuration file '{file_path}' not found. Using defaults.",
            file=sys.stderr,
        )
        return {}

    suffix = path.suffix.lower()

    try:
        config_data = _read_config(path, suffix)

        if env:
            config_data = _select_environment_config(config_data, env)

        if expand_env_vars:
            config_data = _expand_env_vars(config_data)

        return config_data

    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return {}

    except Exception as exc:
        print(f"Failed to parse {suffix} config: {exc}", file=sys.stderr)
        return {}

    return {}


def _read_config(path: pathlib.Path, suffix: str) -> dict[str, Any]:
    if suffix == ".json":
        with path.open(encoding="utf-8") as file:
            return cast(dict[str, Any], json.load(file) or {})

    if suffix == ".toml":
        if tomllib:
            with path.open("rb") as file:
                return cast(dict[str, Any], tomllib.load(file) or {})

        print("Error: Install 'tomli' to use TOML configs.", file=sys.stderr)
        return {}

    if suffix in [".yaml", ".yml"]:
        try:
            import yaml

            with path.open(encoding="utf-8") as file:
                return cast(dict[str, Any], yaml.safe_load(file) or {})

        except ImportError:
            print("Error: Install 'PyYAML' to use YAML configs.", file=sys.stderr)
            return {}

    return {}


def _select_environment_config(
    config_data: dict[str, Any],
    env: str,
) -> dict[str, Any]:
    environments = config_data.get("environments")

    if not environments:
        return config_data

    if not isinstance(environments, dict):
        raise ValueError("'environments' must be a mapping/object.")

    if env not in environments:
        available = ", ".join(sorted(environments))
        raise ValueError(
            f"Environment '{env}' not found in config. "
            f"Available environments: {available}"
        )

    selected = environments[env]

    if not isinstance(selected, dict):
        raise ValueError(f"Environment '{env}' must be a mapping/object.")

    base_config = {
        key: value
        for key, value in config_data.items()
        if key != "environments"
    }

    return _deep_merge(base_config, selected)


def _deep_merge(
    base: dict[str, Any],
    override: dict[str, Any],
) -> dict[str, Any]:
    merged = dict(base)

    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = _deep_merge(
                cast(dict[str, Any], merged[key]),
                cast(dict[str, Any], value),
            )
        else:
            merged[key] = value

    return merged


def _expand_env_vars(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _expand_env_vars(nested_value)
            for key, nested_value in value.items()
        }

    if isinstance(value, list):
        return [_expand_env_vars(item) for item in value]

    if isinstance(value, str):
        return _replace_env_vars(value)

    return value


def _replace_env_vars(value: str) -> str:
    missing_vars: list[str] = []

    def replace(match: re.Match[str]) -> str:
        variable = match.group(1)

        if variable not in os.environ:
            missing_vars.append(variable)
            return match.group(0)

        return os.environ[variable]

    resolved = ENV_PATTERN.sub(replace, value)

    if missing_vars:
        missing = ", ".join(sorted(set(missing_vars)))
        raise ValueError(
            f"Missing environment variable(s): {missing}. "
            "Set them before running Dift."
        )

    return resolved