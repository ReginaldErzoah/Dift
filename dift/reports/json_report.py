from __future__ import annotations

from pathlib import Path

from dift.reports.models import DiffReport


def render_json(report: DiffReport, output: str | None = None) -> str:
    """Render and optionally write a JSON report."""
    payload = report.model_dump_json(indent=2)
    if output:
        Path(output).write_text(payload, encoding="utf-8")
    return payload
