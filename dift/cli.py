from __future__ import annotations

from enum import Enum

import typer
from rich.console import Console

from dift.core.comparator import compare_datasets
from dift.reports.console_report import render_console
from dift.reports.json_report import render_json
import os 

app = typer.Typer(help="Dift: Git diff for datasets.")
console = Console()


class ReportFormat(str, Enum):
    console = "console"
    json = "json"


@app.command()
def main(
    old_dataset: str = typer.Argument(..., help="Path to the old dataset."),
    new_dataset: str = typer.Argument(..., help="Path to the new dataset."),
    key: str | None = typer.Option(None, "--key", "-k", help="Primary key column for row comparison."),
    report: ReportFormat = typer.Option(ReportFormat.console, "--report", "-r", help="Report format."),
    output: str | None = typer.Option(None, "--output", "-o", help="Write report to a file."),
) -> None:


    """Compare two datasets and explain what changed."""
 # Input data Validation
    missing_files=[] #list to store the missing files
    if not os.path.exists(old_dataset): # To check if full path of old_dataset exists
        missing_files.append(old_dataset) # if full path of old_dataset does not exist then add it to missing files list
    if not os.path.exists(new_dataset): # To check if full path of new_dataset exists
        missing_files.append(new_dataset) # if full path of new_dataset does not exist then add it to missing files list

    if missing_files: # To check whether the missing_files empty or not
        names=[] # List to store names of files whose path have not been specified
        for file in missing_files: # take the contents of missing_files and display error the exact error message
            name=os.path.basename(file) # to find the path of the file
            names.append(name) # adding file with missing path to names
            console.print(f"[bold red]Error: File not found: {file}[/bold red]") # Error Message
        console.print("[bold red]Tip:[/bold red]") # Message to prompt to the user to take necessary action
        console.print(f"Use examples/{",".join(names)} or provide a full path") # Message to give expected input to user
        raise typer.Exit(code=1)
    try:
        diff_report = compare_datasets(old_dataset, new_dataset, key=key)
    except Exception as exc:# noqa: BLE001 - CLI should show readable errors
        console.print(f"[bold red] Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    if report == ReportFormat.json:
        payload = render_json(diff_report, output=output)
        if output is None:
            console.print(payload)
        else:
            console.print(f"Wrote JSON report to {output}")
    else:
        render_console(diff_report)


if __name__ == "__main__":
    app()
