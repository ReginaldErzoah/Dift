from __future__ import annotations

from typing import Final

import polars as pl

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None

BIGQUERY_PREFIX: Final[str] = "bigquery://"


def _require_bigquery() -> None:
    """Ensure BigQuery dependencies are installed."""
    if bigquery is None:
        raise ImportError(
            "BigQuery support requires the Google BigQuery client. "
            "Install it with: "
            "pip install google-cloud-bigquery db-dtypes"
        )


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
        raise ValueError("Invalid BigQuery URI.")

    identifier = uri.removeprefix(BIGQUERY_PREFIX)

    parts = identifier.split(".")

    if len(parts) != 3:
        raise ValueError(
            "Invalid BigQuery URI format. "
            "Expected: bigquery://project.dataset.table"
        )

    project, dataset, table = parts

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
            f"Failed to read BigQuery table '{table_id}'."
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
        raise ValueError("Failed to execute BigQuery query.") from exc