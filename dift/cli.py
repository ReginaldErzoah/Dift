from __future__ import annotations

import os
from enum import Enum

import typer
from rich.console import Console

from dift.core.comparator import compare_datasets
from dift.reports.console_report import render_console
from dift.reports.json_report import render_json
from dift.reports.csv_report import render_csv
from dift.reports.excel_report import render_excel
from dift.reports.html_report import render_html

app = typer.Typer(
    no_args_is_help=True,
    help="Dift — Git diff for datasets.",
)
console = Console()


def success(msg: str) -> None:
    """Display success messages in green."""
    console.print(f"[green]{msg}[/green]")


def warning(msg: str) -> None:
    """Display warnings and tips in yellow."""
    console.print(f"[yellow]{msg}[/yellow]")


def error(msg: str) -> None:
    """Display errors and high-risk messages in red."""
    console.print(f"[red]{msg}[/red]")


class ReportFormat(str, Enum):
    console = "console"
    json = "json"
    csv = "csv"
    excel = "excel"
    html = "html"


@app.command()
def main(
    old_dataset: str = typer.Argument(..., help="Path to the old dataset."),
    new_dataset: str = typer.Argument(..., help="Path to the new dataset."),
    key: str | None = typer.Option(
        None,
        "--key",
        "-k",
        help="Primary key column for row comparison.",
    ),
    report: ReportFormat = typer.Option(
        ReportFormat.console,
        "--report",
        "-r",
        help="Report format.",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write report to a file.",
    ),
) -> None:
    """
    Compare two datasets and instantly detect:
    • row changes
    • schema changes
    • null spikes
    • duplicates
    • risk level

    Install:
      pip install dift-cli

    Upgrade:
      pip install --upgrade dift-cli

    Quick Start:
      dift old.csv new.csv
      dift old.csv new.csv --key customer_id
      dift old.csv new.csv --report json --output report.json
      dift old.csv new.csv --report csv --output report.csv
      dift old.csv new.csv --report excel --output report.xlsx
      dift old.csv new.csv --report html --output report.html
    """

    missing_files: list[str] = []

    if not os.path.exists(old_dataset):
        missing_files.append(old_dataset)

    if not os.path.exists(new_dataset):
        missing_files.append(new_dataset)

    if missing_files:
        for file in missing_files:
            name = os.path.basename(file)

            error(f"Error: File not found: {file}")
            warning("Tip:")
            warning(f"Use examples/{name} or provide a full path.\n")

        raise typer.Exit(code=1)

    try:
        diff_report = compare_datasets(old_dataset, new_dataset, key=key)

        if report == ReportFormat.json:
            payload = render_json(diff_report, output=output)

            if output is None:
                console.print(payload)
            else:
                success(f"Wrote JSON report to {output}")

        elif report == ReportFormat.csv:
            payload = render_csv(diff_report, output=output)

            if output is None:
                console.print(payload)
            else:
                success(f"Wrote CSV report to {output}")

        elif report == ReportFormat.excel:
            output_path = render_excel(diff_report, output=output)
            success(f"Wrote Excel report to {output_path}")
        
        elif report == ReportFormat.html:
            output_path = render_html(diff_report, output=output)
            success(f"Wrote HTML report to {output_path}")

        else:
            render_console(diff_report)


    except Exception as exc:
        error(f"Error: {repr(exc)}")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
