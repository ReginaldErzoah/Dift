from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dift.reports.models import DiffReport


def render_console(report: DiffReport) -> None:
    """Render a compact terminal report."""
    console = Console()
    risk = report.summary.risk_level.upper()

    console.print(Panel.fit(f"[bold]Dift Dataset Comparison[/bold]\nRisk Level: [bold]{risk}[/bold]"))

    summary = Table(title="Summary")
    summary.add_column("Metric")
    summary.add_column("Value", justify="right")
    summary.add_row("Old rows", str(report.summary.old_rows))
    summary.add_row("New rows", str(report.summary.new_rows))
    summary.add_row("Row delta", str(report.summary.row_delta))
    summary.add_row("Old columns", str(report.summary.old_columns))
    summary.add_row("New columns", str(report.summary.new_columns))
    summary.add_row("Column delta", str(report.summary.column_delta))
    console.print(summary)

    schema = Table(title="Schema Diff")
    schema.add_column("Change")
    schema.add_column("Value")
    schema.add_row("Columns added", ", ".join(report.schema_diff.columns_added) or "None")
    schema.add_row("Columns removed", ", ".join(report.schema_diff.columns_removed) or "None")
    schema.add_row("Type changes", str(len(report.schema_diff.type_changes)))
    console.print(schema)

    if report.row_diff.key:
        rows = Table(title=f"Row Diff by key: {report.row_diff.key}")
        rows.add_column("Metric")
        rows.add_column("Value", justify="right")
        rows.add_row("Added rows", str(report.row_diff.added_rows))
        rows.add_row("Removed rows", str(report.row_diff.removed_rows))
        rows.add_row("Changed rows", str(report.row_diff.changed_rows))
        rows.add_row("Unchanged rows", str(report.row_diff.unchanged_rows))
        console.print(rows)
    elif report.row_diff.note:
        console.print(f"[dim]{report.row_diff.note}[/dim]")
