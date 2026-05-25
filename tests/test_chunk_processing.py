from __future__ import annotations

import json
import subprocess
import sys

import polars as pl
import pytest

from dift.core.comparator import compare_datasets
from dift.io.readers import DatasetReadError, read_dataset_chunks


def test_read_dataset_chunks_reads_csv_in_chunks(tmp_path):
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n"
        "2,Kojo,200\n"
        "3,Esi,300\n"
        "4,Yaw,400\n"
        "5,Abena,500\n",
        encoding="utf-8",
    )

    chunks = list(read_dataset_chunks(csv_path, chunk_size=2))

    assert len(chunks) >= 2
    assert all(isinstance(chunk, pl.DataFrame) for chunk in chunks)
    assert sum(chunk.height for chunk in chunks) == 5
    assert chunks[0].columns == ["customer_id", "name", "revenue"]


def test_read_dataset_chunks_rejects_invalid_chunk_size(tmp_path):
    csv_path = tmp_path / "customers.csv"
    csv_path.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n",
        encoding="utf-8",
    )

    with pytest.raises(DatasetReadError, match="positive integer"):
        list(read_dataset_chunks(csv_path, chunk_size=0))


def test_read_dataset_chunks_rejects_non_csv_files(tmp_path):
    json_path = tmp_path / "customers.json"
    json_path.write_text(
        json.dumps(
            [
                {"customer_id": 1, "name": "Ama", "revenue": 100},
                {"customer_id": 2, "name": "Kojo", "revenue": 200},
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(DatasetReadError, match="Chunked reading is not supported"):
        list(read_dataset_chunks(json_path, chunk_size=2))


def test_compare_datasets_supports_chunk_size(tmp_path):
    old_csv = tmp_path / "old.csv"
    new_csv = tmp_path / "new.csv"

    old_csv.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n"
        "2,Kojo,200\n"
        "3,Esi,300\n",
        encoding="utf-8",
    )

    new_csv.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n"
        "2,Kojo,250\n"
        "4,Yaw,400\n",
        encoding="utf-8",
    )

    report = compare_datasets(
        str(old_csv),
        str(new_csv),
        key="customer_id",
        chunk_size=2,
    )

    assert report.summary.old_rows == 3
    assert report.summary.new_rows == 3
    assert report.row_diff.added_rows == 1
    assert report.row_diff.removed_rows == 1
    assert report.row_diff.changed_rows == 1


def test_cli_accepts_chunk_size_option(tmp_path):
    old_csv = tmp_path / "old.csv"
    new_csv = tmp_path / "new.csv"

    old_csv.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n"
        "2,Kojo,200\n",
        encoding="utf-8",
    )

    new_csv.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n"
        "2,Kojo,250\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
            "--chunk-size",
            "1",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() or result.stderr.strip()


def test_cli_rejects_invalid_chunk_size(tmp_path):
    old_csv = tmp_path / "old.csv"
    new_csv = tmp_path / "new.csv"

    old_csv.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n",
        encoding="utf-8",
    )

    new_csv.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
            "--chunk-size",
            "0",
        ],
        capture_output=True,
        text=True,
    )

    combined_output = result.stdout + result.stderr

    assert result.returncode != 0
    assert "chunk-size" in combined_output.lower()
    assert "positive integer" in combined_output.lower()