from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_SCHEDULES_PATH = Path(".dift") / "schedules.json"


def _schedule_path(path: str | None = None) -> Path:
    return Path(path) if path else DEFAULT_SCHEDULES_PATH


def load_schedules(path: str | None = None) -> dict[str, dict[str, Any]]:
    schedule_path = _schedule_path(path)

    if not schedule_path.exists():
        return {}

    return json.loads(schedule_path.read_text(encoding="utf-8"))


def save_schedules(
    schedules: dict[str, dict[str, Any]],
    path: str | None = None,
) -> Path:
    schedule_path = _schedule_path(path)
    schedule_path.parent.mkdir(parents=True, exist_ok=True)
    schedule_path.write_text(json.dumps(schedules, indent=2), encoding="utf-8")
    return schedule_path


def create_schedule(
    name: str,
    profile: str,
    cron: str,
    history: bool = True,
    strict_exit_codes: bool = True,
    path: str | None = None,
    overwrite: bool = False,
) -> Path:
    schedules = load_schedules(path)

    if name in schedules and not overwrite:
        raise ValueError(
            f"Schedule '{name}' already exists. Use --overwrite to replace it."
        )

    schedules[name] = {
        "profile": profile,
        "cron": cron,
        "history": history,
        "strict_exit_codes": strict_exit_codes,
    }

    return save_schedules(schedules, path)


def get_schedule(name: str, path: str | None = None) -> dict[str, Any]:
    schedules = load_schedules(path)

    if name not in schedules:
        raise ValueError(f"Schedule '{name}' not found.")

    return schedules[name]


def delete_schedule(name: str, path: str | None = None) -> Path:
    schedules = load_schedules(path)

    if name not in schedules:
        raise ValueError(f"Schedule '{name}' not found.")

    del schedules[name]
    return save_schedules(schedules, path)


def list_schedule_names(path: str | None = None) -> list[str]:
    return sorted(load_schedules(path))


def build_profile_command(
    profile: str,
    history: bool = True,
    strict_exit_codes: bool = True,
) -> str:
    parts = ["dift", "profile", "run", profile]

    if history:
        parts.append("--history")

    if strict_exit_codes:
        parts.append("--strict-exit-codes")

    return " ".join(parts)