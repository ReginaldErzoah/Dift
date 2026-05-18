from __future__ import annotations

from pathlib import Path

import polars as pl

from dift.io.bigquery_reader import is_bigquery_uri, read_bigquery_table
from dift.io.duckdb_reader import (
    is_duckdb_uri,
    parse_duckdb_uri,
    read_duckdb_table,
)

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".parquet",
    ".xlsx",
    ".xls",
    ".json",
}

SUPPORTED_SOURCE_TYPES = sorted(
    list(SUPPORTED_EXTENSIONS)
    + [
        "duckdb:///database.duckdb:table",
        "bigquery://project.dataset.table",
    ]
)


class DatasetReadError(ValueError):
    """Raised when Dift cannot read a dataset."""


def read_dataset(path: str | Path) -> pl.DataFrame:
    """Read a local dataset, DuckDB table, or BigQuery table into a Polars DataFrame."""
    path_str = str(path)

    if is_duckdb_uri(path_str):
        try:
            database_path, table_name = parse_duckdb_uri(path_str)
            return read_duckdb_table(database_path, table_name)

        except Exception as exc:
            raise DatasetReadError(f"Failed to read DuckDB dataset: {path_str}") from exc

    if is_bigquery_uri(path_str):
        try:
            return read_bigquery_table(path_str)

        except Exception as exc:
            raise DatasetReadError(f"Failed to read BigQuery dataset: {path_str}") from exc

    dataset_path = Path(path)

    if not dataset_path.exists():
        raise DatasetReadError(f"Dataset not found: {dataset_path}")

    suffix = dataset_path.suffix.lower()

    if suffix == ".csv":
        return pl.read_csv(dataset_path)

    if suffix == ".parquet":
        return pl.read_parquet(dataset_path)

    if suffix in {".xlsx", ".xls"}:
        return pl.read_excel(dataset_path, engine="fastexcel")

    if suffix == ".json":
        return pl.read_json(dataset_path)

    raise DatasetReadError(
        f"Unsupported dataset type '{suffix}'. "
        f"Supported types: {SUPPORTED_SOURCE_TYPES}"
    )