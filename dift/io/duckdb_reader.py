from __future__ import annotations

from pathlib import Path

import polars as pl

try:
    import duckdb
except ImportError:
    duckdb = None


def _require_duckdb() -> None:
    if duckdb is None:
        raise ImportError(
            "DuckDB support requires the 'duckdb' package. "
            "Install it with: pip install duckdb"
        )


def read_duckdb_table(database_path: str, table_name: str) -> pl.DataFrame:
    """Read a DuckDB table into a Polars DataFrame."""
    _require_duckdb()

    db_path = Path(database_path)

    if not db_path.exists():
        raise FileNotFoundError(f"DuckDB database not found: {database_path}")

    query = f"SELECT * FROM {_quote_identifier(table_name)}"

    try:
        with duckdb.connect(str(db_path), read_only=True) as conn:
            return conn.execute(query).pl()
    except Exception as exc:
        raise ValueError(
            f"Failed to read DuckDB table '{table_name}' from '{database_path}'."
        ) from exc


def read_duckdb_query(
    query: str,
    database_path: str | None = None,
) -> pl.DataFrame:
    """Read DuckDB query results into a Polars DataFrame."""
    _require_duckdb()

    try:
        if database_path:
            db_path = Path(database_path)

            if not db_path.exists():
                raise FileNotFoundError(f"DuckDB database not found: {database_path}")

            with duckdb.connect(str(db_path), read_only=True) as conn:
                return conn.execute(query).pl()

        with duckdb.connect(":memory:") as conn:
            return conn.execute(query).pl()

    except FileNotFoundError:
        raise

    except Exception as exc:
        raise ValueError("Failed to execute DuckDB query.") from exc


def parse_duckdb_uri(uri: str) -> tuple[str, str]:
    """
    Parse a DuckDB URI.

    Expected format:
        duckdb:///path/to/database.duckdb:table_name

    Example:
        duckdb:///data/warehouse.duckdb:customers
    """
    prefix = "duckdb:///"

    if not uri.startswith(prefix):
        raise ValueError(
            "Invalid DuckDB URI. Expected format: "
            "duckdb:///path/to/database.duckdb:table_name"
        )

    raw = uri[len(prefix) :]

    if ":" not in raw:
        raise ValueError(
            "Invalid DuckDB URI. Missing table name. Expected format: "
            "duckdb:///path/to/database.duckdb:table_name"
        )

    database_path, table_name = raw.rsplit(":", 1)

    if not database_path:
        raise ValueError("Invalid DuckDB URI. Database path is missing.")

    if not table_name:
        raise ValueError("Invalid DuckDB URI. Table name is missing.")

    return database_path, table_name


def is_duckdb_uri(value: str) -> bool:
    return value.startswith("duckdb:///")


def _quote_identifier(identifier: str) -> str:
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'