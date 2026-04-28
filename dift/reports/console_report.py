from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dift.reports.models import DiffReport


def render_console(report: DiffReport) -> None:
    """Render a compact terminal report."""
    console = Console()
    risk = report.summary.risk_level.upper()

    risk_color = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red"}.get(risk, "white")

    console.print(Panel.fit(
        f"[bold]Dift Dataset Comparison[/bold]\nRisk Level: [bold {risk_color}]{risk}[/bold {risk_color}]"
    ))

    summary = Table(title="Summary")
    summary.add_column("Metric")
    summary.add_column("Value", justify="right")
    summary.add_row("Old rows", str(report.summary.old_
