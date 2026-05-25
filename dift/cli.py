from __future__ import annotations

import os
import sys
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from time import perf_counter

import click
import typer
from rich.console import Console

from dift.batch import find_dataset_pairs
from dift.core.comparator import compare_datasets
from dift.history import clear_history, load_history, save_history_record
from dift.io.bigquery_reader import is_bigquery_uri
from dift.io.config_loader import load_config
from dift.io.duckdb_reader import is_duckdb_uri, parse_duckdb_uri
from dift.io.sql_reader import is_sql_uri, parse_sql_table_uri
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
from dift.schedules import (
    build_profile_command,
    create_schedule,
    delete_schedule,
    get_schedule,
    list_schedule_names,
    load_schedules,
)
from dift.thresholds import resolve_threshold_config
from dift.utils.validation import (
    ValidationError,
    validate_config_path,
    validate_html_template,
    validate_output_options,
)


class CustomUsageCommand(typer.core.TyperCommand):
    """Customize the main help usage line for beginner-friendly CLI docs."""

    def format_usage(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        formatter.write_usage(
            ctx.command_path,
            "[OLD_DATASET] [NEW_DATASET] [OPTIONS]",
        )


compare_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "Compare datasets, databases, and warehouse tables for schema changes, "
        "row changes, quality issues, drift, and risk."
    ),
)


profile_app = typer.Typer(help="Manage saved comparison profiles.")
batch_app = typer.Typer(help="Run batch dataset comparisons.")
history_app = typer.Typer(help="Manage comparison history.")
schedule_app = typer.Typer(help="Manage scheduled comparison workflows.")

console = Console()
QUIET_MODE = False


def configure_output(quiet: bool = False, no_color: bool = False) -> None:
    global console
    global QUIET_MODE

    QUIET_MODE = quiet
    console = Console(no_color=no_color)


def success(msg: str) -> None:
    if not QUIET_MODE:
        console.print(f"[green]{msg}[/green]")


def progress(msg: str, verbose: bool = False) -> None:
    if verbose and not QUIET_MODE:
        console.print(f"[cyan]{msg}[/cyan]")


def warning(msg: str) -> None:
    if not QUIET_MODE:
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

LOW_RISK_EXIT_CODE = 0
MEDIUM_RISK_EXIT_CODE = 1
HIGH_RISK_EXIT_CODE = 2
ERROR_EXIT_CODE = 3


def risk_exit_code(risk_level: str) -> int:
    risk = risk_level.lower()

    if risk == "low":
        return LOW_RISK_EXIT_CODE

    if risk == "medium":
        return MEDIUM_RISK_EXIT_CODE

    if risk == "high":
        return HIGH_RISK_EXIT_CODE

    return ERROR_EXIT_CODE


def _resolve_chunk_size(
    cli_chunk_size: int | None,
    config_data: dict,
) -> int | None:
    chunk_size = cli_chunk_size

    if chunk_size is None:
        config_chunk_size = config_data.get("chunk_size")
        if config_chunk_size is not None:
            chunk_size = int(config_chunk_size)

    if chunk_size is not None and chunk_size <= 0:
        raise ValidationError("--chunk-size must be a positive integer.")

    return chunk_size


def run_comparison(
    old_dataset: str | None,
    new_dataset: str | None,
    key: str | None,
    threshold: float,
    report: ReportFormat,
    output: str | None,
    output_dir: str | None,
    template: str,
    config: str | None = None,
    env: str | None = None,
    save_history: bool = False,
    history_dir: str | None = None,
    strict_exit_codes: bool = False,
    quiet: bool = False,
    no_color: bool = False,
    verbose: bool = False,
    chunk_size: int | None = None,
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    progress("Validating inputs...", verbose=verbose)

    try:
        validate_config_path(config)

    except ValidationError as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc

    try:
        if config:
            progress(f"Loading config file: {config}", verbose=verbose)

        config_data = load_config(config, env=env) if config else {}

    except Exception as exc:
        error(f"Error: Failed to load config file '{config}'.")
        warning("Tip:")
        warning("Check that the config file exists, is valid, and matches the expected format.")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc

    try:
        chunk_size = _resolve_chunk_size(chunk_size, config_data)

    except ValidationError as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc

    threshold_config = resolve_threshold_config(
        config_data=config_data,
        cli_threshold=threshold,
        default_threshold=DEFAULT_THRESHOLD,
    )
    numeric_threshold = threshold_config.numeric

    if key is None:
        key = config_data.get("key", key)

    if report == DEFAULT_REPORT:
        report_str = config_data.get("report")
        if report_str:
            try:
                report = ReportFormat(report_str)
            except ValueError as exc:
                error(
                    f"Error: Invalid report format '{report_str}' in config.\n"
                    "Supported report formats: console, json, csv, excel, html"
                )
                raise typer.Exit(code=ERROR_EXIT_CODE) from exc

    if output is None:
        output = config_data.get("output")

    if output_dir is None:
        output_dir = config_data.get("output_dir")

    if template == DEFAULT_TEMPLATE:
        template = config_data.get("template", template)

    try:
        validate_output_options(output, output_dir)

        if report == ReportFormat.html:
            validate_html_template(template)

    except ValidationError as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc

    old_dataset = old_dataset or config_data.get("old_dataset")
    new_dataset = new_dataset or config_data.get("new_dataset")

    progress("Checking dataset sources...", verbose=verbose)

    if not old_dataset or not new_dataset:
        error("Error: Missing dataset paths.")
        console.print("Please provide paths as arguments or via a config file.")
        warning("\nExample:")
        warning("  dift old.csv new.csv")
        warning("  dift --config config.yaml")
        raise typer.Exit(code=ERROR_EXIT_CODE)

    missing_files: list[str] = []

    for dataset in [old_dataset, new_dataset]:
        if dataset is None:
            continue

        if is_duckdb_uri(dataset):
            try:
                database_path, _ = parse_duckdb_uri(dataset)

                if not os.path.exists(database_path):
                    missing_files.append(database_path)

            except ValueError:
                missing_files.append(dataset)

        elif is_bigquery_uri(dataset):
            continue

        elif is_sql_uri(dataset):
            try:
                connection_string, _ = parse_sql_table_uri(dataset)

                if connection_string.startswith("sqlite:///"):
                    sqlite_path = connection_string.removeprefix("sqlite:///")

                    if not os.path.exists(sqlite_path):
                        missing_files.append(sqlite_path)

            except ValueError:
                missing_files.append(dataset)

        elif not os.path.exists(dataset):
            missing_files.append(dataset)

    if missing_files:
        for file in missing_files:
            name = os.path.basename(file)
            error(f"Error: File not found: {file}")
            warning("Tip:")
            warning(f"Use examples/{name} or provide a full path.\n")

        raise typer.Exit(code=ERROR_EXIT_CODE)

    if output:
        output_parent = os.path.dirname(output)

        if output_parent:
            os.makedirs(output_parent, exist_ok=True)

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

    started_at = perf_counter()
    generated_at = datetime.now(UTC).isoformat()

    if chunk_size is not None:
        progress(
            f"Loading datasets in chunks of {chunk_size} rows and running comparison...",
            verbose=verbose,
        )
    else:
        progress("Loading datasets and running comparison...", verbose=verbose)

    diff_report = compare_datasets(
        old_dataset,
        new_dataset,
        key=key,
        threshold=numeric_threshold,
        threshold_config=threshold_config,
        chunk_size=chunk_size,
    )

    runtime_seconds = round(perf_counter() - started_at, 4)

    progress("Comparison completed.", verbose=verbose)

    diff_report.metadata.generated_at = generated_at
    diff_report.metadata.old_source = old_dataset
    diff_report.metadata.new_source = new_dataset
    diff_report.metadata.key = key
    diff_report.metadata.threshold = numeric_threshold
    diff_report.metadata.report_format = report.value
    diff_report.metadata.template = template if report == ReportFormat.html else None
    diff_report.metadata.runtime_seconds = runtime_seconds

    progress(f"Generating {report.value} report...", verbose=verbose)

    if save_history:
        history_path = save_history_record(
            report=diff_report,
            old_dataset=old_dataset,
            new_dataset=new_dataset,
            key=key,
            threshold=numeric_threshold,
            report_format=report.value,
            history_dir=history_dir,
        )
        success(f"Saved comparison history to {history_path}")

    if report == ReportFormat.json:
        payload = render_json(diff_report, output=output)

        if output is None and not quiet:
            console.print(payload)
        elif output is not None:
            success(f"Wrote JSON report to {output}")

    elif report == ReportFormat.csv:
        payload = render_csv(diff_report, output=output)

        if output is None and not quiet:
            console.print(payload)
        elif output is not None:
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
        if not quiet:
            render_console(diff_report)

    progress("Report generation completed.", verbose=verbose)

    if strict_exit_codes:
        raise typer.Exit(code=risk_exit_code(diff_report.summary.risk_level))


@compare_app.command(
    cls=CustomUsageCommand,
    help="""
Compare datasets, databases, and warehouse tables.

Examples:

  Compare CSV files:
    dift old.csv new.csv --key customer_id

  Compare CSV files with chunked loading:
    dift old.csv new.csv --key customer_id --chunk-size 50000

  Generate JSON report:
    dift old.csv new.csv --report json --output report.json

  Generate HTML report:
    dift old.csv new.csv --report html --template dark --output report.html

  Compare DuckDB tables:
    dift duckdb:///examples/warehouse.duckdb:customers_old \\
         duckdb:///examples/warehouse.duckdb:customers_new \\
         --key customer_id

  Compare SQL tables:
    dift sqlite:///examples/old.db:customers_old \\
         sqlite:///examples/new.db:customers_new \\
         --key customer_id

  Use config file:
    dift --config config.yaml --env production
""",
)
def main(
    old_dataset: str | None = typer.Argument(
        None,
        help="Original dataset, table, or connector URI.",
    ),
    new_dataset: str | None = typer.Argument(
        None,
        help="New dataset, table, or connector URI.",
    ),
    key: str | None = typer.Option(
        None,
        "--key",
        "-k",
        help="Column used to match rows across datasets, for example customer_id.",
    ),
    threshold: float = typer.Option(
        DEFAULT_THRESHOLD,
        "--threshold",
        "-t",
        help="Drift sensitivity threshold. Lower values are more sensitive.",
    ),
    report: ReportFormat = typer.Option(
        DEFAULT_REPORT,
        "--report",
        "-r",
        help="Report output format.",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write report to a specific file path.",
    ),
    output_dir: str | None = typer.Option(
        None,
        "--output-dir",
        help="Write report to a directory with an auto-generated filename.",
    ),
    config: str | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to a JSON, YAML, or TOML config file.",
    ),
    env: str | None = typer.Option(
        None,
        "--env",
        help="Environment name to load from config file.",
    ),
    template: str = typer.Option(
        DEFAULT_TEMPLATE,
        "--template",
        help="HTML template to use: default, clean, compact, enterprise, or dark.",
    ),
    save_history: bool = typer.Option(
        False,
        "--history",
        help="Save comparison history.",
    ),
    history_dir: str | None = typer.Option(
        None,
        "--history-dir",
        help="Directory to save comparison history.",
    ),
    strict_exit_codes: bool = typer.Option(
        False,
        "--strict-exit-codes",
        help="Exit with risk-based codes: 0 low, 1 medium, 2 high, 3 error.",
    ),
    chunk_size: int | None = typer.Option(
        None,
        "--chunk-size",
        help="Read supported datasets in chunks of N rows. Currently supports local CSV files.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        help="Suppress non-error output for automation workflows.",
    ),
    no_color: bool = typer.Option(
        False,
        "--no-color",
        help="Disable colored terminal output.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show progress messages for loading, comparison, and report generation.",
    ),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

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
            config=config,
            env=env,
            save_history=save_history,
            history_dir=history_dir,
            strict_exit_codes=strict_exit_codes,
            quiet=quiet,
            no_color=no_color,
            verbose=verbose,
            chunk_size=chunk_size,
        )

    except typer.Exit:
        raise

    except Exception as exc:
        error(f"Error: {repr(exc)}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


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
    save_history: bool = typer.Option(
        False,
        "--history",
        help="Save comparison history.",
    ),
    history_dir: str | None = typer.Option(
        None,
        "--history-dir",
        help="Directory to save comparison history.",
    ),
    strict_exit_codes: bool = typer.Option(
        False,
        "--strict-exit-codes",
        help="Exit with risk-based codes during batch comparisons.",
    ),
    chunk_size: int | None = typer.Option(
        None,
        "--chunk-size",
        help="Read supported datasets in chunks of N rows. Currently supports local CSV files.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        help="Suppress non-error output for automation workflows.",
    ),
    no_color: bool = typer.Option(
        False,
        "--no-color",
        help="Disable colored terminal output.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show progress messages for each batch comparison.",
    ),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        pairs = find_dataset_pairs(old_dir, new_dir)

        if not pairs:
            warning("No matching dataset files found.")
            raise typer.Exit(code=ERROR_EXIT_CODE)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        success(f"Found {len(pairs)} dataset pair(s).")

        failures = 0

        for old_file, new_file in pairs:
            dataset_name = old_file.stem
            success(f"Comparing {old_file.name}")

            pair_output_dir = None
            pair_history_dir = history_dir

            if output_dir:
                pair_output_dir = str(Path(output_dir) / dataset_name)

            if history_dir:
                pair_history_dir = str(Path(history_dir) / dataset_name)

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
                    save_history=save_history,
                    history_dir=pair_history_dir,
                    strict_exit_codes=strict_exit_codes,
                    quiet=quiet,
                    no_color=no_color,
                    verbose=verbose,
                    chunk_size=chunk_size,
                )

            except typer.Exit as exc:
                if exc.exit_code in {
                    MEDIUM_RISK_EXIT_CODE,
                    HIGH_RISK_EXIT_CODE,
                } and strict_exit_codes:
                    raise

                failures += 1
                error(f"Failed comparison for {old_file.name}: exit code {exc.exit_code}")

                if not continue_on_error:
                    raise typer.Exit(code=ERROR_EXIT_CODE) from exc

            except Exception as exc:
                failures += 1
                error(f"Failed comparison for {old_file.name}: {exc}")

                if not continue_on_error:
                    raise typer.Exit(code=ERROR_EXIT_CODE) from exc

        if failures:
            error(f"Batch completed with {failures} failure(s).")
            raise typer.Exit(code=ERROR_EXIT_CODE)

        success("Batch comparison completed successfully.")

    except typer.Exit:
        raise

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@history_app.command("list")
def history_list(
    history_dir: str | None = typer.Option(None, "--history-dir"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    records = load_history(history_dir)

    if not records:
        warning("No comparison history found.")
        return

    if quiet:
        return

    for index, record in enumerate(records, start=1):
        console.print(
            f"{index}. {record['timestamp']} | "
            f"risk={record['risk_level']} | "
            f"{record['old_dataset']} -> {record['new_dataset']}"
        )


@history_app.command("show")
def history_show(
    index: int = typer.Argument(..., help="History record number."),
    history_dir: str | None = typer.Option(None, "--history-dir"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    records = load_history(history_dir)

    if index < 1 or index > len(records):
        error("Error: History record not found.")
        raise typer.Exit(code=ERROR_EXIT_CODE)

    if not quiet:
        console.print_json(data=records[index - 1])


@history_app.command("clear")
def history_clear(
    history_dir: str | None = typer.Option(None, "--history-dir"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    path = clear_history(history_dir)
    success(f"Cleared comparison history at {path}")


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
    chunk_size: int | None = typer.Option(
        None,
        "--chunk-size",
        help="Read supported datasets in chunks of N rows. Currently supports local CSV files.",
    ),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
    overwrite: bool = typer.Option(False, "--overwrite"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        if chunk_size is not None and chunk_size <= 0:
            raise ValueError("--chunk-size must be a positive integer.")

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
                "chunk_size": chunk_size,
            },
            path=profiles_file,
            overwrite=overwrite,
        )
        success(f"Created profile '{name}'.")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@profile_app.command("list")
def profile_list(
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        names = list_profile_names(profiles_file)

        if not names:
            warning("No profiles found.")
            return

        if quiet:
            return

        for name in names:
            console.print(f"- {name}")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@profile_app.command("show")
def profile_show(
    name: str = typer.Argument(..., help="Profile name."),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        profile = get_profile(name, profiles_file)

        if not quiet:
            console.print_json(data=profile)

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@profile_app.command("delete")
def profile_delete(
    name: str = typer.Argument(..., help="Profile name."),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        delete_profile(name, profiles_file)
        success(f"Deleted profile '{name}'.")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@profile_app.command("run")
def profile_run(
    name: str = typer.Argument(..., help="Profile name."),
    key: str | None = typer.Option(None, "--key", "-k"),
    threshold: float | None = typer.Option(None, "--threshold", "-t"),
    report: ReportFormat | None = typer.Option(None, "--report", "-r"),
    output: str | None = typer.Option(None, "--output", "-o"),
    output_dir: str | None = typer.Option(None, "--output-dir"),
    template: str | None = typer.Option(None, "--template"),
    chunk_size: int | None = typer.Option(
        None,
        "--chunk-size",
        help="Override profile chunk size for supported datasets.",
    ),
    profiles_file: str | None = typer.Option(None, "--profiles-file"),
    save_history: bool = typer.Option(
        False,
        "--history",
        help="Save comparison history.",
    ),
    history_dir: str | None = typer.Option(
        None,
        "--history-dir",
        help="Directory to save comparison history.",
    ),
    strict_exit_codes: bool = typer.Option(
        False,
        "--strict-exit-codes",
        help="Exit with risk-based codes: 0 low, 1 medium, 2 high, 3 error.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        help="Suppress non-error output for automation workflows.",
    ),
    no_color: bool = typer.Option(
        False,
        "--no-color",
        help="Disable colored terminal output.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show progress messages for the profile comparison.",
    ),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        profile = get_profile(name, profiles_file)

        old_dataset = profile.get("old_dataset")
        new_dataset = profile.get("new_dataset")

        if not old_dataset or not new_dataset:
            error("Error: Profile must define old_dataset and new_dataset.")
            raise typer.Exit(code=ERROR_EXIT_CODE)

        profile_report = profile.get("report", DEFAULT_REPORT.value)

        profile_chunk_size = profile.get("chunk_size")
        resolved_chunk_size = (
            chunk_size
            if chunk_size is not None
            else int(profile_chunk_size)
            if profile_chunk_size is not None
            else None
        )

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
            save_history=save_history,
            history_dir=history_dir,
            strict_exit_codes=strict_exit_codes,
            quiet=quiet,
            no_color=no_color,
            verbose=verbose,
            chunk_size=resolved_chunk_size,
        )

    except typer.Exit:
        raise

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@schedule_app.command("create")
def schedule_create(
    name: str = typer.Argument(..., help="Schedule name."),
    profile: str = typer.Option(..., "--profile", help="Saved profile to run."),
    cron: str = typer.Option(..., "--cron", help="Cron expression."),
    history: bool = typer.Option(
        True,
        "--history/--no-history",
        help="Include --history when running the scheduled profile.",
    ),
    strict_exit_codes: bool = typer.Option(
        True,
        "--strict-exit-codes/--no-strict-exit-codes",
        help="Include --strict-exit-codes when running the scheduled profile.",
    ),
    quiet_schedule: bool = typer.Option(
        True,
        "--quiet/--no-quiet",
        help="Include --quiet in the scheduled command.",
    ),
    no_color_schedule: bool = typer.Option(
        True,
        "--no-color/--color",
        help="Include --no-color in the scheduled command.",
    ),
    schedules_file: str | None = typer.Option(None, "--schedules-file"),
    overwrite: bool = typer.Option(False, "--overwrite"),
) -> None:
    try:
        path = create_schedule(
            name=name,
            profile=profile,
            cron=cron,
            history=history,
            strict_exit_codes=strict_exit_codes,
            quiet=quiet_schedule,
            no_color=no_color_schedule,
            path=schedules_file,
            overwrite=overwrite,
        )
        success(f"Created schedule '{name}' at {path}")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@schedule_app.command("list")
def schedule_list(
    schedules_file: str | None = typer.Option(None, "--schedules-file"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    names = list_schedule_names(schedules_file)

    if not names:
        warning("No schedules found.")
        return

    if quiet:
        return

    schedules = load_schedules(schedules_file)

    for name in names:
        schedule = schedules[name]
        command = build_profile_command(
            profile=schedule["profile"],
            history=bool(schedule.get("history", True)),
            strict_exit_codes=bool(schedule.get("strict_exit_codes", True)),
            quiet=bool(schedule.get("quiet", True)),
            no_color=bool(schedule.get("no_color", True)),
        )
        console.print(f"- {name}: {schedule['cron']} -> {command}")


@schedule_app.command("show")
def schedule_show(
    name: str = typer.Argument(..., help="Schedule name."),
    schedules_file: str | None = typer.Option(None, "--schedules-file"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        schedule = get_schedule(name, schedules_file)

        if not quiet:
            console.print_json(data=schedule)

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@schedule_app.command("delete")
def schedule_delete(
    name: str = typer.Argument(..., help="Schedule name."),
    schedules_file: str | None = typer.Option(None, "--schedules-file"),
    quiet: bool = typer.Option(False, "--quiet"),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    configure_output(quiet=quiet, no_color=no_color)

    try:
        delete_schedule(name, schedules_file)
        success(f"Deleted schedule '{name}'.")

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@schedule_app.command("run")
def schedule_run(
    name: str = typer.Argument(..., help="Schedule name."),
    schedules_file: str | None = typer.Option(None, "--schedules-file"),
    quiet: bool | None = typer.Option(None, "--quiet/--no-quiet"),
    no_color: bool | None = typer.Option(None, "--no-color/--color"),
) -> None:
    try:
        schedule = get_schedule(name, schedules_file)

        profile_run(
            name=schedule["profile"],
            key=None,
            threshold=None,
            report=None,
            output=None,
            output_dir=None,
            template=None,
            chunk_size=None,
            profiles_file=None,
            save_history=bool(schedule.get("history", True)),
            history_dir=None,
            strict_exit_codes=bool(schedule.get("strict_exit_codes", True)),
            quiet=bool(schedule.get("quiet", True)) if quiet is None else quiet,
            no_color=bool(schedule.get("no_color", True)) if no_color is None else no_color,
            verbose=False,
        )

    except typer.Exit:
        raise

    except Exception as exc:
        error(f"Error: {exc}")
        raise typer.Exit(code=ERROR_EXIT_CODE) from exc


@schedule_app.command("cron")
def schedule_cron(
    profile_name: str = typer.Argument(..., help="Saved profile name to schedule."),
    hour: int = typer.Option(2, "--hour", help="Hour to run, 0-23."),
    minute: int = typer.Option(0, "--minute", help="Minute to run, 0-59."),
    history: bool = typer.Option(True, "--history/--no-history"),
    strict_exit_codes: bool = typer.Option(
        True,
        "--strict-exit-codes/--no-strict-exit-codes",
    ),
    quiet: bool = typer.Option(True, "--quiet/--no-quiet"),
    no_color: bool = typer.Option(True, "--no-color/--color"),
) -> None:
    if hour < 0 or hour > 23:
        error("Error: --hour must be between 0 and 23.")
        raise typer.Exit(code=ERROR_EXIT_CODE)

    if minute < 0 or minute > 59:
        error("Error: --minute must be between 0 and 59.")
        raise typer.Exit(code=ERROR_EXIT_CODE)

    command = build_profile_command(
        profile=profile_name,
        history=history,
        strict_exit_codes=strict_exit_codes,
        quiet=quiet,
        no_color=no_color,
    )
    console.print(f"{minute} {hour} * * * {command}")


@schedule_app.command("examples")
def schedule_examples(
    profile_name: str = typer.Argument(..., help="Saved profile name to schedule."),
) -> None:
    command = build_profile_command(profile_name)

    console.print("Daily at 2:00 AM:")
    console.print(f"0 2 * * * {command}")

    console.print("\nEvery Monday at 6:00 AM:")
    console.print(f"0 6 * * 1 {command}")

    console.print("\nEvery 6 hours:")
    console.print(f"0 */6 * * * {command}")


def app() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        sys.argv.pop(1)
        profile_app()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        sys.argv.pop(1)
        batch_app()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "history":
        sys.argv.pop(1)
        history_app()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "schedule":
        sys.argv.pop(1)
        schedule_app()
        return

    compare_app()


if __name__ == "__main__":
    app()