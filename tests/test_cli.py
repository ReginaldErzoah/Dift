import json
import subprocess
import sys


def test_cli_help_runs():
    result = subprocess.run(
        [sys.executable, "-m", "dift.cli", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Usage" in result.stdout or "usage" in result.stdout.lower()


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
    assert report["metadata"]["version"] == "0.3.0"
    assert report["metadata"]["report_type"] == "dataset_diff"