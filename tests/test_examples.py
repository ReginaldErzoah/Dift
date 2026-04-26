import subprocess
import sys
from pathlib import Path


def test_example_csv_files_exist():
    assert Path("examples/old.csv").exists()
    assert Path("examples/new.csv").exists()


def test_example_parquet_files_exist():
    assert Path("examples/old.parquet").exists()
    assert Path("examples/new.parquet").exists()


def test_examples_run_successfully():
    if not Path("examples/old.csv").exists() or not Path("examples/new.csv").exists():
        return

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            "examples/old.csv",
            "examples/new.csv",
            "--key",
            "customer_id",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
