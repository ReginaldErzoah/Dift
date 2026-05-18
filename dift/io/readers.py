from __future__ import annotations

from pathlib import Path

import polars as pl

from dift.io.bigquery_reader import is_bigquery_uri, read_bigquery_table
from dift.io.duckdb_reader import (
    is_duckdb_uri,
    parse_duckdb_uri,
    read_duckdb_table,
)
from dift.io.sql_reader import (
    is_sql_uri,
    parse_sql_table_uri,
    read_sql_table,
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
        "sqlite:///database.db:table",
        "postgresql://user:password@host:5432/database:table",
        "mysql+pymysql://user:password@host:3306/database:table",
        "redshift+redshift_connector://user:password@host:5439/database:table",
        "snowflake://user:password@account/database/schema?warehouse=name:table",
    ]
)


class DatasetReadError(ValueError):
    """Raised when Dift cannot read a dataset."""


def read_dataset(path: str | Path) -> pl.DataFrame:
    """
    Read a local dataset, DuckDB table,
    BigQuery table, or SQL table into a Polars DataFrame.
    """

    path_str = str(path)

    if is_duckdb_uri(path_str):
        try:
            database_path, table_name = parse_duckdb_uri(path_str)
            return read_duckdb_table(database_path, table_name)

        except ImportError as exc:
            raise DatasetReadError(str(exc)) from exc

        except Exception as exc:
            raise DatasetReadError(
                f"Failed to read DuckDB dataset: {path_str}"
            ) from exc

    if is_bigquery_uri(path_str):
        try:
            return read_bigquery_table(path_str)

        except ImportError as exc:
            raise DatasetReadError(str(exc)) from exc

        except Exception as exc:
            raise DatasetReadError(
                f"Failed to read BigQuery dataset: {path_str}"
            ) from exc

    if is_sql_uri(path_str):
        try:
            connection_string, table_name = parse_sql_table_uri(path_str)
            return read_sql_table(connection_string, table_name)

        except ImportError as exc:
            raise DatasetReadError(str(exc)) from exc

        except ValueError as exc:
            message = str(exc)

            if "support requires" in message or "Install" in message:
                raise DatasetReadError(message) from exc

            raise DatasetReadError(
                f"Failed to read SQL dataset: {path_str}. {message}"
            ) from exc

        except Exception as exc:
            raise DatasetReadError(
                f"Failed to read SQL dataset: {path_str}. {exc}"
            ) from exc

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