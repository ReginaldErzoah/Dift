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
        f"[bold]Dift Dataset Comparison[/bold]\n"
        f"Risk Level: [bold {risk_color}]{risk}[/bold {risk_color}]"
    ))

    summary = Table(title="Summary")
    summary.add_column("Metric")
    summary.add_column("Value", justify="right")

    summary.add_row("Old rows",      str(report.summary.old_rows))
    summary.add_row("New rows",      str(report.summary.new_rows))
    summary.add_row("Added rows",    str(report.summary.added_rows))
    summary.add_row("Removed rows",  str(report.summary.removed_rows))
    summary.add_row("Changed rows",  str(report.summary.changed_rows))
    summary.add_row("Schema changes",str(report.summary.schema_changes))
    summary.add_row("Null spikes",   str(report.summary.null_spikes))

    console.print(summary)

