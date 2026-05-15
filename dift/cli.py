from __future__ import annotations

import os
import sys
from enum import Enum
from pathlib import Path

import typer
from rich.console import Console

from dift.batch import find_dataset_pairs
from dift.core.comparator import compare_datasets
from dift.io.config_loader import load_config
from dift.profiles import (
    create_profile,
    delete_profile,
    get_profile,
    list_profile_names,
)
from dift.reports.console_report import render_console
from dift.reports.csv_report import render_csv
from dift.reports.excel_report import render_excel
from dift.reports.html_report import render_html
from dift.reports.json_report import render_json

compare_app = typer.Typer(
    no_args_is_help=True,
    help="Dift - data comparison & quality check tool for datasets.",
)

profile_app = typer.Typer(help="Manage saved comparison profiles.")
batch_app = typer.Typer(help="Run batch dataset comparisons.")

console = Console()


def success(msg: str) -> None:
    console.print(f"[green]{msg}[/green]")


def warning(msg: str) -> None:
    console.print(f"[yellow]{msg}[/yellow]")


def error(msg: str) -> None:
    console.print(f"[red]{msg}[/red]")


class ReportFormat(str, Enum):
    console = "console"
    json = "json"
    csv = "csv"
    excel = "excel"
    html = "html"


DEFAULT_THRESHOLD = 0.1
DEFAULT_REPORT = ReportFormat.console
DEFAULT_TEMPLATE = "default"


def run_comparison(
    old_dataset: str,
    new_dataset: str,
    key: str | None,
    threshold: float,
    report: ReportFormat,
    output: str | None,
    output_dir: str | None,
    template: str,
) -> None:
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

    if output and output_dir:
        error("Error: Use either --output or --output-dir, not both.")
        raise typer.Exit(code=1)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        extension_map = {
            ReportFormat.json: "json",
            ReportFormat.csv: "csv",
            ReportFormat.excel: "xlsx",
            ReportFormat.html: "html",
        }

        if report in extension_map:
            extension = extension_map[report]
            output = os.path.join(output_dir, f"dift_report.{extension}")

    diff_report = compare_datasets(
        old_dataset,
        new_dataset,
        key=key,
        threshold=threshold,
    )

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
        output_path = render_html(
            diff_report,
            output=output,
            template=template,
        )
        success(f"Wrote HTML report to {output_path}")

    else:
        render_console(diff_report)


@compare_app.command()
def main(
    old_dataset: str = typer.Argument(..., help="Path to the old dataset."),
    new_dataset: str = typer.Argument(..., help="Path to the new dataset."),
    key: str | None = typer.Option(None, "--key", "-k"),
    threshold: float = typer.Option(DEFAULT_THRESHOLD, "--threshold", "-t"),
    report: ReportFormat = typer.Option(DEFAULT_REPORT, "--report", "-r"),
    output: str | None = typer.Option(None, "--output", "-o"),
    output_dir: str | None = typer.Option(None, "--output-dir"),
    config: str | None = typer.Option(None, "--config", "-c"),
    template: str = typer.Option(DEFAULT_TEMPLATE, "--template"),
) -> None:
    config_data = load_config(config) if config else {}

    if key is None:
        key = config_data.get("key")

    if threshold == DEFAULT_THRESHOLD:
        threshold = float(config_data.get("threshold", threshold))

    if report == DEFAULT_REPORT:
        report_str = config_data.get("report")

        if report_str:
            try:
                report = ReportFormat(report_str)
            except ValueError:
                warning(f"Invalid report format '{report_str}' in config. Keeping default.")

    if output is None:
        output = config_data.get("output")

    if output_dir is None:
        output_dir = config_data.get("output_dir")

    if template == DEFAULT_TEMPLATE:
        template = config_data.get("template", template)

    try:
        run_comparison(
            old_dataset=old_dataset,
            new_dataset=new_dataset,
            key=key,
            threshold=threshold,
            report=report,
            output=output,
            output_dir=output_dir,
            template=template,
        )

    except typer.Exit:
        raise

    except Exception as exc:
        error(f"Error: {repr(exc)}")
        raise typer.Exit(code=1) from exc


@batch_app.callback(invoke_without_command=True)
def batch_run(
    old_dir: str = typer.Option(..., "--old-dir", help="Directory with old datasets."),
    new_dir: str = typer.Option(..., "--new-dir", help="Directory with new datasets."),
    key: str | None = typer.Option(None, "--key", "-k"),
    threshold: float = typer.Option(DEFAULT_THRESHOLD, "--threshold", "-t"),
    report: ReportFormat = typer.Option(DEFAULT_REPORT, "--report", "-r"),
    output_dir: str | None = typer.Option(None, "--output-dir"),
    template: str = typer.Option(DEFAULT_TEMPLATE, "--template"),
    continue_on_error: bool = typer.Option(
        True,
        "--continue-on-error/--stop-on-error",
        help="Continue running other comparisons if one fails.",
    ),
) -> None:
    try:
        pairs = find_dataset_pairs(old_dir, new_dir)

        if not pairs:
            warning("No matching dataset files found.")
            raise typer.Exit(code=1)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        success(f"Found {len(pairs)} dataset pair(s).")

        failures = 0

        for old_file, new_file in pairs:
            dataset_name = old_file.stem
            success(f"Comparing {old_file.name}")

            pair_output_dir = None

            if output_dir:
                pair_output_dir = str(Path(output_dir) / dataset_name)

            try:
                run_comparison(
                    old_dataset=str(old_file),
                    new_dataset=str(new_file),
                    key=key,
                    threshold=threshold,
                    report=report,
                    output=None,
                    output_dir=pair_output_dir,
                    template=template,
                )

            except Exception as exc:
                failures += 1
                error(f"Failed comparison for {old_file.name}: {exc}")

                if not continue_on_error:
                    raise typer.Exit(code=1) from exc

        if failures:
            error(f"Batch completed with {failures} failure(s).")
            raise typer.Exit(code=1)

        success("Batch comparison completed successfully.")

    except typer.Exit:
        raise

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=1) from exc


@profile_app.command("create")
def profile_create(
    name: str = typer.Argument(..., help="Profile name."),
    old_dataset: str = typer.Option(..., "--old", help="Old dataset path."),
    new_dataset: str = typer.Option(..., "--new", help="New dataset path."),
    key: str | None = typer.Option(None, "--key", "-k"),
    threshold: float = typer.Option(DEFAULT_THRESHOLD, "--threshold", "-t"),
    report: ReportFormat = typer.Option(DEFAULT_REPORT, "--report", "-r"),
    output: str | None = typer.Option(None, "--output", "-o"),
    output_dir: str | None = typer.Option(None, "--output-dir"),
    template: str = typer.Option(DEFAULT_TEMPLATE, "--template"),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
    overwrite: bool = typer.Option(False, "--overwrite"),
) -> None:
    try:
        create_profile(
            name=name,
            profile={
                "old_dataset": old_dataset,
                "new_dataset": new_dataset,
                "key": key,
                "threshold": threshold,
                "report": report.value,
                "output": output,
                "output_dir": output_dir,
                "template": template,
            },
            path=profiles_file,
            overwrite=overwrite,
        )
        success(f"Created profile '{name}'.")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=1) from exc


@profile_app.command("list")
def profile_list(
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
) -> None:
    try:
        names = list_profile_names(profiles_file)

        if not names:
            warning("No profiles found.")
            return

        for name in names:
            console.print(f"- {name}")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=1) from exc


@profile_app.command("show")
def profile_show(
    name: str = typer.Argument(..., help="Profile name."),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
) -> None:
    try:
        profile = get_profile(name, profiles_file)
        console.print_json(data=profile)

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=1) from exc


@profile_app.command("delete")
def profile_delete(
    name: str = typer.Argument(..., help="Profile name."),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
) -> None:
    try:
        delete_profile(name, profiles_file)
        success(f"Deleted profile '{name}'.")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=1) from exc


@profile_app.command("run")
def profile_run(
    name: str = typer.Argument(..., help="Profile name."),
    key: str | None = typer.Option(None, "--key", "-k"),
    threshold: float | None = typer.Option(None, "--threshold", "-t"),
    report: ReportFormat | None = typer.Option(None, "--report", "-r"),
    output: str | None = typer.Option(None, "--output", "-o"),
    output_dir: str | None = typer.Option(None, "--output-dir"),
    template: str | None = typer.Option(None, "--template"),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
) -> None:
    try:
        profile = get_profile(name, profiles_file)

        old_dataset = profile.get("old_dataset")
        new_dataset = profile.get("new_dataset")

        if not old_dataset or not new_dataset:
            error("Error: Profile must define old_dataset and new_dataset.")
            raise typer.Exit(code=1)

        profile_report = profile.get("report", DEFAULT_REPORT.value)

        run_comparison(
            old_dataset=old_dataset,
            new_dataset=new_dataset,
            key=key if key is not None else profile.get("key"),
            threshold=(
                threshold
                if threshold is not None
                else float(profile.get("threshold", DEFAULT_THRESHOLD))
            ),
            report=report if report is not None else ReportFormat(profile_report),
            output=output if output is not None else profile.get("output"),
            output_dir=(
                output_dir
                if output_dir is not None
                else profile.get("output_dir")
            ),
            template=(
                template
                if template is not None
                else profile.get("template", DEFAULT_TEMPLATE)
            ),
        )

    except typer.Exit:
        raise

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=1) from exc


def app() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        sys.argv.pop(1)
        profile_app()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        sys.argv.pop(1)
        batch_app()
        return

    compare_app()


if __name__ == "__main__":
    app()