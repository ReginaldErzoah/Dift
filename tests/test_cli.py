import json
import subprocess
import sys

from typer.testing import CliRunner

from dift.cli import compare_app

runner = CliRunner()


def test_cli_help_runs():
    result = runner.invoke(compare_app, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "[OLD_DATASET] [NEW_DATASET] [OPTIONS]" in result.output


def test_cli_help_contains_examples():
    result = runner.invoke(compare_app, ["--help"])

    assert result.exit_code == 0

    assert "Compare CSV files" in result.output
    assert "Generate JSON report" in result.output
    assert "Compare DuckDB tables" in result.output
    assert "Compare SQL tables" in result.output
    assert "Use config file" in result.output


def test_cli_help_has_clear_option_descriptions():
    result = runner.invoke(compare_app, ["--help"])

    assert result.exit_code == 0

    assert "Compare CSV files" in result.output
    assert "Generate JSON report" in result.output
    assert "Compare DuckDB tables" in result.output
    assert "Compare SQL tables" in result.output
    assert "Use config file" in result.output

def test_cli_subprocess_help_runs():
    result = subprocess.run(
        [sys.executable, "-m", "dift.cli", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Usage" in result.stdout
    assert "[OLD_DATASET] [NEW_DATASET] [OPTIONS]" in result.stdout


def test_cli_console_report_runs(sample_csv_files):
    old_csv, new_csv = sample_csv_files

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip()


def test_cli_json_report_writes_file(sample_csv_files, tmp_path):
    old_csv, new_csv = sample_csv_files
    output_path = tmp_path / "report.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
            "--report",
            "json",
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_path.exists()

    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert isinstance(report, dict)

    assert "metadata" in report
    assert "summary" in report
    assert "schema" in report
    assert "rows" in report
    assert "quality" in report
    assert "numeric" in report
    assert "categorical" in report

    assert "schema_diff" not in report
    assert "row_diff" not in report
    assert "quality_diff" not in report
    assert "numeric_diff" not in report
    assert "categorical_diff" not in report

    assert report["metadata"]["tool"] == "dift"
    assert report["metadata"]["version"] == "0.5.0"
    assert report["metadata"]["report_type"] == "dataset_diff"


def test_cli_json_report_writes_to_output_dir(sample_csv_files, tmp_path):
    old_csv, new_csv = sample_csv_files
    output_dir = tmp_path / "reports"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
            "--report",
            "json",
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_dir.exists()
    assert (output_dir / "dift_report.json").exists()


def test_cli_csv_report_writes_to_output_dir(sample_csv_files, tmp_path):
    old_csv, new_csv = sample_csv_files
    output_dir = tmp_path / "reports"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
            "--report",
            "csv",
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_dir.exists()
    assert (output_dir / "dift_report.csv").exists()


def test_cli_rejects_output_and_output_dir_together(sample_csv_files, tmp_path):
    old_csv, new_csv = sample_csv_files
    output_dir = tmp_path / "reports"
    output_path = tmp_path / "report.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
            "--report",
            "json",
            "--output",
            str(output_path),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0

    combined_output = result.stdout + result.stderr

    assert "--output" in combined_output
    assert "--output-dir" in combined_output