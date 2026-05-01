from __future__ import annotations

from pathlib import Path

from dift.reports.models import DiffReport


def render_csv(report: DiffReport, output: str | None = None) -> str:
    """
    Render and optionally write a CSV summary report.

    Example:
    metric,value
    old_rows,10
    new_rows,11
    row_delta,1
    risk_level,high
    """

    rows = [
        "metric,value",
        f"old_rows,{report.summary.old_rows}",
        f"new_rows,{report.summary.new_rows}",
        f"row_delta,{report.summary.row_delta}",
        f"risk_level,{report.summary.risk_level}",
    ]

    payload = "\n".join(rows)

    if output:
        Path(output).write_text(payload, encoding="utf-8")

    return payload
