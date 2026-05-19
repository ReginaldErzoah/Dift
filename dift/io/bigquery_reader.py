from __future__ import annotations

from typing import Final

import polars as pl

from dift.io.base_reader import BaseReader

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None


BIGQUERY_PREFIX: Final[str] = "bigquery://"


def _require_bigquery() -> None:
    """Ensure BigQuery dependencies are installed."""
    if bigquery is None:
        raise ImportError(
            "BigQuery support requires the Google BigQuery client.\n"
            "Install it with:\n"
            "  pip install google-cloud-bigquery db-dtypes"
        )


class BigQueryReader(BaseReader):
    """BigQuery dataset reader."""

    name = "bigquery"

    supports_tables = True
    supports_queries = True
    supports_streaming = False

    def can_handle(self, source: str) -> bool:
        return is_bigquery_uri(source)

    def read(self, source: str) -> pl.DataFrame:
        return read_bigquery_table(source)


def is_bigquery_uri(value: str) -> bool:
    """Return True if the value is a BigQuery URI."""
    return value.startswith(BIGQUERY_PREFIX)


def parse_bigquery_uri(uri: str) -> tuple[str, str, str]:
    """
    Parse a BigQuery URI.

    Expected format:
        bigquery://project.dataset.table

    Returns:
        tuple(project, dataset, table)
    """

    if not is_bigquery_uri(uri):
        raise ValueError(
            "Invalid BigQuery URI.\n"
            "Expected format:\n"
            "  bigquery://project.dataset.table"
        )

    identifier = uri.removeprefix(BIGQUERY_PREFIX)

    parts = identifier.split(".")

    if len(parts) != 3:
        raise ValueError(
            "Invalid BigQuery URI format.\n"
            "Expected format:\n"
            "  bigquery://project.dataset.table"
        )

    project, dataset, table = parts

    if not project:
        raise ValueError("Invalid BigQuery URI. Project is missing.")

    if not dataset:
        raise ValueError("Invalid BigQuery URI. Dataset is missing.")

    if not table:
        raise ValueError("Invalid BigQuery URI. Table is missing.")

    return project, dataset, table


def read_bigquery_table(uri: str) -> pl.DataFrame:
    """
    Read a BigQuery table into a Polars DataFrame.

    Example:
        bigquery://my-project.analytics.customers
    """

    _require_bigquery()

    project, dataset, table = parse_bigquery_uri(uri)

    table_id = f"{project}.{dataset}.{table}"

    try:
        client = bigquery.Client(project=project)

        query = f"SELECT * FROM `{table_id}`"

        dataframe = client.query(query).to_dataframe()

        return pl.from_pandas(dataframe)

    except Exception as exc:
        raise ValueError(
            f"Failed to read BigQuery table '{table_id}'.\n"
            "Check:\n"
            "  - Google Cloud authentication\n"
            "  - project, dataset, and table names\n"
            "  - BigQuery permissions\n"
            "  - query billing/project configuration"
        ) from exc


def read_bigquery_query(
    query: str,
    project: str | None = None,
) -> pl.DataFrame:
    """
    Execute a BigQuery SQL query and return a Polars DataFrame.
    """

    _require_bigquery()

    try:
        client = bigquery.Client(project=project)

        dataframe = client.query(query).to_dataframe()

        return pl.from_pandas(dataframe)

    except Exception as exc:
        raise ValueError(
            "Failed to execute BigQuery query.\n"
            "Check:\n"
            "  - SQL query syntax\n"
            "  - Google Cloud authentication\n"
            "  - BigQuery permissions\n"
            "  - query billing/project configuration"
        ) from exc