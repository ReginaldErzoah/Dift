from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import tomllib
import yaml

DEFAULT_PROFILE_PATH = Path(".dift") / "profiles.yaml"


def load_profiles(path: str | None = None) -> dict[str, Any]:
    profile_path = Path(path) if path else DEFAULT_PROFILE_PATH

    if not profile_path.exists():
        return {}

    suffix = profile_path.suffix.lower()
    text = profile_path.read_text(encoding="utf-8")

    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text) or {}
    elif suffix == ".json":
        data = json.loads(text)
    elif suffix == ".toml":
        data = tomllib.loads(text)
    else:
        raise ValueError(f"Unsupported profile file format: {suffix}")

    if not isinstance(data, dict):
        raise ValueError("Profile file must contain a dictionary of profiles.")

    return data


def save_profiles(profiles: dict[str, Any], path: str | None = None) -> Path:
    profile_path = Path(path) if path else DEFAULT_PROFILE_PATH
    profile_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = profile_path.suffix.lower()

    if suffix in {".yaml", ".yml"}:
        payload = yaml.safe_dump(profiles, sort_keys=True)
    elif suffix == ".json":
        payload = json.dumps(profiles, indent=2)
    elif suffix == ".toml":
        payload = _to_toml(profiles)
    else:
        raise ValueError(f"Unsupported profile file format: {suffix}")

    profile_path.write_text(payload, encoding="utf-8")
    return profile_path


def create_profile(
    name: str,
    profile: dict[str, Any],
    path: str | None = None,
    overwrite: bool = False,
) -> Path:
    profiles = load_profiles(path)

    if name in profiles and not overwrite:
        raise ValueError(f"Profile '{name}' already exists.")

    profiles[name] = {key: value for key, value in profile.items() if value is not None}
    return save_profiles(profiles, path)


def get_profile(name: str, path: str | None = None) -> dict[str, Any]:
    profiles = load_profiles(path)

    if name not in profiles:
        raise ValueError(f"Profile '{name}' does not exist.")

    profile = profiles[name]

    if not isinstance(profile, dict):
        raise ValueError(f"Profile '{name}' is invalid.")

    return profile


def delete_profile(name: str, path: str | None = None) -> Path:
    profiles = load_profiles(path)

    if name not in profiles:
        raise ValueError(f"Profile '{name}' does not exist.")

    del profiles[name]
    return save_profiles(profiles, path)


def list_profile_names(path: str | None = None) -> list[str]:
    return sorted(load_profiles(path).keys())


def _to_toml(profiles: dict[str, Any]) -> str:
    lines: list[str] = []

    for name, profile in profiles.items():
        lines.append(f"[{name}]")

        for key, value in profile.items():
            if isinstance(value, str):
                lines.append(f'{key} = "{value}"')
            elif isinstance(value, bool):
                lines.append(f"{key} = {str(value).lower()}")
            else:
                lines.append(f"{key} = {value}")

        lines.append("")

    return "\n".join(lines)