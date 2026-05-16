from __future__ import annotations

import polars as pl
import sqlalchemy as sa


def read_sql_table(connection_string: str, table_name: str) -> pl.DataFrame:
    """Read an SQL table into a Polars DataFrame."""
    engine = sa.create_engine(connection_string)

    try:
        query = f"SELECT * FROM {table_name}"
        return pl.read_database(query, engine)
    except Exception as exc:
        raise ValueError(
            f"Failed to read table '{table_name}' from database."
        ) from exc


def read_sql_query(connection_string: str, query: str) -> pl.DataFrame:
    """Read SQL query results into a Polars DataFrame."""
    engine = sa.create_engine(connection_string)

    try:
        return pl.read_database(query, engine)
    except Exception as exc:
        raise ValueError("Failed to execute SQL query.") from exc
