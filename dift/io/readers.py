from __future__ import annotations

from pathlib import Path

import polars as pl

from dift.io.base_reader import BaseReader
from dift.io.bigquery_reader import BigQueryReader, is_bigquery_uri
from dift.io.duckdb_reader import DuckDBReader, is_duckdb_uri
from dift.io.plugins import load_plugin_readers, register_plugin_readers
from dift.io.registry import ReaderRegistry
from dift.io.sql_reader import SQLReader, is_sql_uri

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


class LocalFileReader(BaseReader):
    """Read local dataset files."""

    name = "local_file"

    supports_tables = False
    supports_queries = False
    supports_streaming = False

    def can_handle(self, source: str) -> bool:
        return not (
            is_duckdb_uri(source)
            or is_bigquery_uri(source)
            or is_sql_uri(source)
        )

    def read(self, source: str) -> pl.DataFrame:
        dataset_path = Path(source)

        if not dataset_path.exists():
            raise DatasetReadError(
                f"Dataset not found: {dataset_path}\n"
                "Check that the file path is correct.\n"
                "Example:\n"
                "  dift examples/old.csv examples/new.csv"
            )

        suffix = dataset_path.suffix.lower()

        if suffix == ".csv":
            return pl.read_csv(dataset_path)

        if suffix == ".parquet":
            return pl.read_parquet(dataset_path)

        if suffix in {".xlsx", ".xls"}:
            return pl.read_excel(dataset_path, engine="calamine")

        if suffix == ".json":
            return pl.read_json(dataset_path)

        raise DatasetReadError(
            f"Unsupported dataset type '{suffix}'.\n"
            f"Supported local file types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}\n"
            "Supported connector examples:\n"
            "  duckdb:///database.duckdb:table\n"
            "  sqlite:///database.db:table\n"
            "  postgresql://user:password@host:5432/database:table\n"
            "  mysql+pymysql://user:password@host:3306/database:table\n"
            "  redshift+redshift_connector://user:password@host:5439/database:table\n"
            "  snowflake://user:password@account/database/schema?warehouse=name:table\n"
            "  bigquery://project.dataset.table\n"
            "For database inputs, use a supported connector URI."
        )


def create_default_registry() -> ReaderRegistry:
    """Create the default Dift reader registry."""
    registry = ReaderRegistry()

    registry.register(DuckDBReader())
    registry.register(BigQueryReader())
    registry.register(SQLReader())
    registry.register(LocalFileReader())

    register_plugin_readers(
        registry=registry,
        readers=load_plugin_readers(),
    )

    return registry


DEFAULT_READER_REGISTRY = create_default_registry()


def get_reader(source: str | Path) -> BaseReader:
    """Return the first reader that can handle the source."""
    reader = DEFAULT_READER_REGISTRY.get_reader(source)

    if reader is not None:
        return reader

    raise DatasetReadError(
        f"No reader found for source: {source}\n"
        f"Supported source types: {SUPPORTED_SOURCE_TYPES}"
    )


def read_dataset(path: str | Path) -> pl.DataFrame:
    """Read a dataset source into a Polars DataFrame."""
    source = str(path)
    reader = get_reader(source)

    try:
        return reader.read(source)

    except DatasetReadError:
        raise

    except ImportError as exc:
        raise DatasetReadError(str(exc)) from exc

    except ValueError as exc:
        raise DatasetReadError(str(exc)) from exc

    except Exception as exc:
        raise DatasetReadError(
            f"Failed to read dataset source '{source}'. {exc}"
        ) from exc