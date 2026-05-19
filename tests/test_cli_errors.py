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

    combined_output = result.stdout + result.stderr

    assert result.returncode != 0
    assert "File not found" in combined_output
    assert "provide a full path" in combined_output


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

    combined_output = result.stdout + result.stderr

    assert result.returncode != 0
    assert "not_a_real_key" in combined_output or "key" in combined_output.lower()


def test_cli_fails_for_missing_dataset_paths():
    result = subprocess.run(
        [sys.executable, "-m", "dift.cli"],
        capture_output=True,
        text=True,
    )

    combined_output = result.stdout + result.stderr

    assert result.returncode != 0
    assert "Missing dataset paths" in combined_output
    assert "dift old.csv new.csv" in combined_output


def test_cli_rejects_output_and_output_dir_together(sample_csv_files, tmp_path):
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
            "--output",
            str(tmp_path / "report.json"),
            "--output-dir",
            str(tmp_path / "reports"),
        ],
        capture_output=True,
        text=True,
    )

    combined_output = result.stdout + result.stderr

    assert result.returncode != 0
    assert "Use either --output or --output-dir" in combined_output


def test_cli_unsupported_file_type_has_helpful_message(tmp_path):
    old_txt = tmp_path / "old.txt"
    new_txt = tmp_path / "new.txt"

    old_txt.write_text("id,name\n1,Ama\n", encoding="utf-8")
    new_txt.write_text("id,name\n1,Ama\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_txt),
            str(new_txt),
        ],
        capture_output=True,
        text=True,
    )

    combined_output = result.stdout + result.stderr

    assert result.returncode != 0
    assert "Unsupported dataset type" in combined_output
    assert "Supported local file" in combined_output
    assert "types" in combined_output
    assert "Supported connector examples" in combined_output