from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dift.reports.models import DiffReport


def _risk_style(risk_level: str) -> str:
    """Return Rich style based on risk level."""
    risk = risk_level.lower()

    if risk == "low":
        return "bold green"
    if risk == "medium":
        return "bold yellow"
    if risk == "high":
        return "bold red"

    return "bold white"


def _section_title(title: str) -> str:
    """Return styled section title."""
    return f"[bold cyan]{title}[/bold cyan]"


def _format_delta(value: int) -> str:
    """Color positive, negative, and zero deltas."""
    if value > 0:
        return f"[yellow]+{value}[/yellow]"
    if value < 0:
        return f"[red]{value}[/red]"
    return f"[green]{value}[/green]"


def render_console(report: DiffReport) -> None:
    """Render a compact terminal report."""
    console = Console()

    risk = report.summary.risk_level.upper()
    risk_style = _risk_style(report.summary.risk_level)

    console.print(
        Panel.fit(
            f"[bold cyan]Dift Dataset Comparison[/bold cyan]\n"
            f"Risk Level: [{risk_style}]{risk}[/{risk_style}]"
        )
    )

    summary = Table(title=_section_title("Summary"))
    summary.add_column("Metric")
    summary.add_column("Value", justify="right")

    summary.add_row("Old rows", str(report.summary.old_rows))
    summary.add_row("New rows", str(report.summary.new_rows))
    summary.add_row("Row delta", _format_delta(report.summary.row_delta))
    summary.add_row("Old columns", str(report.summary.old_columns))
    summary.add_row("New columns", str(report.summary.new_columns))
    summary.add_row("Column delta", _format_delta(report.summary.column_delta))

    console.print(summary)

    schema = Table(title=_section_title("Schema Diff"))
    schema.add_column("Change")
    schema.add_column("Value")

    schema.add_row(
        "Columns added",
        ", ".join(report.schema_diff.columns_added) or "None",
    )
    schema.add_row(
        "Columns removed",
        ", ".join(report.schema_diff.columns_removed) or "None",
    )
    schema.add_row(
        "Type changes",
        str(len(report.schema_diff.type_changes)),
    )

    console.print(schema)

    if report.row_diff.key:
        rows = Table(title=_section_title(f"Row Diff by key: {report.row_diff.key}"))
        rows.add_column("Metric")
        rows.add_column("Value", justify="right")

        rows.add_row("Added rows", _format_delta(report.row_diff.added_rows or 0))
        rows.add_row("Removed rows", _format_delta(-(report.row_diff.removed_rows or 0)))
        rows.add_row("Changed rows", _format_delta(report.row_diff.changed_rows or 0))
        rows.add_row("Unchanged rows", str(report.row_diff.unchanged_rows))

        console.print(rows)

    elif report.row_diff.note:
        console.print(f"[dim]{report.row_diff.note}[/dim]")

    duplicate_delta = report.quality_diff.duplicate_diff.delta_duplicates

    if duplicate_delta > 0:
        console.print(
            f"[bold yellow]Warning:[/bold yellow] "
            f"Duplicates increased by {duplicate_delta}"
        )

    null_spikes = [
        diff
        for diff in report.quality_diff.null_diffs
        if diff.delta_null_pct >= 5
    ]

    for diff in null_spikes:
        console.print(
            f"[bold yellow]Warning:[/bold yellow] "
            f"Nulls increased in '{diff.column}' by {diff.delta_null_pct}%"
        )