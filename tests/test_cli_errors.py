import subprocess
import sys


def test_cli_fails_for_missing_dataset(sample_csv_files):
    old_csv, _ = sample_csv_files

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            "missing.csv",
            "--key",
            "customer_id",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    combined_output = result.stdout + result.stderr
    assert (
        "not found" in combined_output.lower() or "missing" in combined_output.lower()
    )


def test_cli_fails_for_missing_key(sample_csv_files):
    old_csv, new_csv = sample_csv_files

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "not_a_real_key",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
