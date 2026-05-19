from __future__ import annotations

from typing import Final

import polars as pl

from dift.io.base_reader import BaseReader

try:
    import sqlalchemy as sa
except ImportError:
    sa = None


SQL_URI_PREFIXES: Final[tuple[str, ...]] = (
    "sqlite:///",
    "postgres://",
    "postgresql://",
    "postgresql+psycopg://",
    "postgresql+psycopg2://",
    "mysql://",
    "mysql+pymysql://",
    "redshift+psycopg2://",
    "redshift+redshift_connector://",
    "snowflake://",
    "snowflake+snowflake://",
    "mssql://",
)


def _require_sqlalchemy() -> None:
    if sa is None:
        raise ImportError(
            "SQL database support requires SQLAlchemy.\n"
            "Install it with:\n"
            "  pip install sqlalchemy"
        )


class SQLReader(BaseReader):
    """SQLAlchemy-compatible dataset reader."""

    name = "sql"

    supports_tables = True
    supports_queries = True
    supports_streaming = False

    def can_handle(self, source: str) -> bool:
        return is_sql_uri(source)

    def read(self, source: str) -> pl.DataFrame:
        connection_string, table_name = parse_sql_table_uri(source)
        return read_sql_table(connection_string, table_name)


def is_sql_uri(value: str) -> bool:
    """Return True if the value looks like a supported SQL connector URI."""
    return value.startswith(SQL_URI_PREFIXES)


def parse_sql_table_uri(uri: str) -> tuple[str, str]:
    """
    Parse a SQL table URI.

    Expected format:
        sqlite:///path/to/database.db:table_name
        postgresql://user:pass@host:5432/dbname:table_name
        postgres://user:pass@host:5432/dbname:table_name
        mysql+pymysql://user:pass@host:3306/dbname:table_name
        redshift+redshift_connector://user:pass@host:5439/dbname:table_name
        snowflake://user:pass@account/db/schema?warehouse=compute_wh:table_name

    Returns:
        tuple(connection_string, table_name)
    """

    if not is_sql_uri(uri):
        raise ValueError(
            "Invalid SQL URI.\n"
            "Expected examples:\n"
            "  sqlite:///database.db:table\n"
            "  postgresql://user:password@host:5432/database:table\n"
            "  mysql+pymysql://user:password@host:3306/database:table"
        )

    if ":" not in uri:
        raise ValueError(
            "Invalid SQL table URI.\n"
            "Expected format:\n"
            "  connection_string:table_name\n"
            "Examples:\n"
            "  sqlite:///database.db:customers\n"
            "  postgresql://user:password@host:5432/sales:orders"
        )

    connection_string, table_name = uri.rsplit(":", 1)

    if not connection_string:
        raise ValueError(
            "Invalid SQL table URI. Connection string is missing.\n"
            "Expected format:\n"
            "  connection_string:table_name"
        )

    if not table_name:
        raise ValueError(
            "Invalid SQL table URI. Table name is missing.\n"
            "Expected format:\n"
            "  connection_string:table_name\n"
            "Example:\n"
            "  sqlite:///database.db:customers"
        )

    return connection_string, table_name


def read_sql_table(connection_string: str, table_name: str) -> pl.DataFrame:
    """Read an SQL table into a Polars DataFrame."""
    _require_sqlalchemy()

    query = f"SELECT * FROM {_quote_table_name(table_name)}"

    try:
        engine = sa.create_engine(connection_string)

        with engine.connect() as connection:
            return pl.read_database(query, connection)

    except ModuleNotFoundError as exc:
        raise ImportError(_driver_help(connection_string)) from exc

    except Exception as exc:
        raise ValueError(
            f"Failed to read SQL table '{table_name}' "
            f"using connection '{connection_string}'.\n"
            "Check:\n"
            "  - database credentials\n"
            "  - connection string format\n"
            "  - table existence\n"
            "  - database server availability"
        ) from exc


def read_sql_query(connection_string: str, query: str) -> pl.DataFrame:
    """Read SQL query results into a Polars DataFrame."""
    _require_sqlalchemy()

    try:
        engine = sa.create_engine(connection_string)

        with engine.connect() as connection:
            return pl.read_database(query, connection)

    except ModuleNotFoundError as exc:
        raise ImportError(_driver_help(connection_string)) from exc

    except Exception as exc:
        raise ValueError(
            f"Failed to execute SQL query using connection '{connection_string}'.\n"
            "Check:\n"
            "  - SQL query syntax\n"
            "  - table existence\n"
            "  - database credentials\n"
            "  - database server availability"
        ) from exc


def _quote_table_name(table_name: str) -> str:
    """
    Quote table names safely.

    Supports:
        customers
        public.customers
        analytics.public.customers
    """
    return ".".join(_quote_identifier(part) for part in table_name.split("."))


def _quote_identifier(identifier: str) -> str:
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


def _driver_help(connection_string: str) -> str:
    if connection_string.startswith(("postgres://", "postgresql://")):
        return (
            "PostgreSQL support requires a PostgreSQL driver.\n"
            "Install one with:\n"
            "  pip install psycopg2-binary"
        )

    if connection_string.startswith("postgresql+psycopg://"):
        return (
            "PostgreSQL support requires psycopg.\n"
            "Install it with:\n"
            "  pip install psycopg"
        )

    if connection_string.startswith("postgresql+psycopg2://"):
        return (
            "PostgreSQL support requires psycopg2.\n"
            "Install it with:\n"
            "  pip install psycopg2-binary"
        )

    if connection_string.startswith(("mysql://", "mysql+pymysql://")):
        return (
            "MySQL support requires a MySQL driver.\n"
            "Install it with:\n"
            "  pip install pymysql"
        )

    if connection_string.startswith(
        ("redshift+psycopg2://", "redshift+redshift_connector://")
    ):
        return (
            "Redshift support requires a Redshift-compatible SQLAlchemy driver.\n"
            "Install one with:\n"
            "  pip install sqlalchemy-redshift redshift-connector"
        )

    if connection_string.startswith(("snowflake://", "snowflake+snowflake://")):
        return (
            "Snowflake support requires the Snowflake SQLAlchemy driver.\n"
            "Install it with:\n"
            "  pip install snowflake-sqlalchemy"
        )

    return (
        "This SQL database requires a compatible SQLAlchemy driver.\n"
        "Install the appropriate database driver and try again."
    )