from __future__ import annotations

from typing import Final

import polars as pl

try:
    import sqlalchemy as sa
except ImportError:
    sa = None


SQL_URI_PREFIXES: Final[tuple[str, ...]] = (
    "sqlite:///",
    "postgresql://",
    "postgresql+psycopg://",
    "postgresql+psycopg2://",
    "mysql://",
    "mysql+pymysql://",
    "mssql://",
)


def _require_sqlalchemy() -> None:
    if sa is None:
        raise ImportError(
            "SQL database support requires SQLAlchemy. "
            "Install it with: pip install sqlalchemy"
        )


def is_sql_uri(value: str) -> bool:
    return value.startswith(SQL_URI_PREFIXES)


def parse_sql_table_uri(uri: str) -> tuple[str, str]:
    """
    Parse a SQL table URI.

    Expected format:
        sqlite:///path/to/database.db:table_name
        postgresql://user:pass@host:5432/dbname:table_name

    Returns:
        tuple(connection_string, table_name)
    """

    if not is_sql_uri(uri):
        raise ValueError("Invalid SQL URI.")

    if ":" not in uri:
        raise ValueError(
            "Invalid SQL table URI. Expected format: "
            "connection_string:table_name"
        )

    connection_string, table_name = uri.rsplit(":", 1)

    if not connection_string:
        raise ValueError("Invalid SQL table URI. Connection string is missing.")

    if not table_name:
        raise ValueError("Invalid SQL table URI. Table name is missing.")

    return connection_string, table_name


def read_sql_table(connection_string: str, table_name: str) -> pl.DataFrame:
    """Read an SQL table into a Polars DataFrame."""
    _require_sqlalchemy()

    query = f"SELECT * FROM {_quote_identifier(table_name)}"

    try:
        engine = sa.create_engine(connection_string)

        with engine.connect() as connection:
            return pl.read_database(query, connection)

    except Exception as exc:
        raise ValueError(
            f"Failed to read SQL table '{table_name}' "
            f"using connection '{connection_string}'."
        ) from exc


def read_sql_query(connection_string: str, query: str) -> pl.DataFrame:
    """Read SQL query results into a Polars DataFrame."""
    _require_sqlalchemy()

    try:
        engine = sa.create_engine(connection_string)

        with engine.connect() as connection:
            return pl.read_database(query, connection)

    except Exception as exc:
        raise ValueError("Failed to execute SQL query.") from exc


def _quote_identifier(identifier: str) -> str:
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'