import subprocess
import sys


def test_default_behavior_returns_zero_for_medium_or_high_risk(sample_csv_files):
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


def test_strict_exit_codes_low_risk(sample_csv_files):
    old_csv, _ = sample_csv_files

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(old_csv),
            "--key",
            "customer_id",
            "--strict-exit-codes",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0


def test_strict_exit_codes_medium_or_high_risk(sample_csv_files):
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
            "--strict-exit-codes",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode in {1, 2}


def test_strict_exit_codes_missing_file_returns_error_code(sample_csv_files):
    _, new_csv = sample_csv_files

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            "missing.csv",
            str(new_csv),
            "--strict-exit-codes",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 3


def test_output_and_output_dir_conflict_returns_error_code(sample_csv_files, tmp_path):
    old_csv, new_csv = sample_csv_files

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--output",
            str(tmp_path / "report.json"),
            "--output-dir",
            str(tmp_path / "reports"),
            "--strict-exit-codes",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 3