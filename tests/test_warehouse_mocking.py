from unittest.mock import MagicMock, patch

import pytest

from dift.io.bigquery_reader import (
    parse_bigquery_uri,
    read_bigquery_query,
    read_bigquery_table,
)
from dift.io.readers import DatasetReadError, read_dataset
from dift.io.sql_reader import (
    parse_sql_table_uri,
    read_sql_query,
    read_sql_table,
)

# =========================================================
# Snowflake Mock Tests
# =========================================================


def test_snowflake_uri_parsing():
    connection_string, table_name = parse_sql_table_uri(
        "snowflake://user:password@account/db/schema?"
        "warehouse=compute_wh:orders"
    )

    assert connection_string.startswith("snowflake://")
    assert table_name == "orders"


@patch("dift.io.sql_reader.sa.create_engine")
def test_snowflake_authentication_failure(mock_create_engine):
    mock_engine = MagicMock()

    mock_engine.connect.side_effect = Exception(
        "Snowflake authentication failed"
    )

    mock_create_engine.return_value = mock_engine

    with pytest.raises(ValueError):
        read_sql_table(
            (
                "snowflake://user:password@account/db/schema"
                "?warehouse=compute_wh"
            ),
            "orders",
        )


@patch("dift.io.sql_reader.sa.create_engine")
def test_snowflake_query_failure(mock_create_engine):
    mock_connection = MagicMock()

    mock_connection.__enter__.return_value = mock_connection

    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_connection

    mock_create_engine.return_value = mock_engine

    with patch(
        "polars.read_database",
        side_effect=Exception("Invalid Snowflake query"),
    ):
        with pytest.raises(ValueError):
            read_sql_query(
                (
                    "snowflake://user:password@account/db/schema"
                    "?warehouse=compute_wh"
                ),
                "SELECT * FROM missing_table",
            )


def test_snowflake_missing_driver_error():
    with pytest.raises(DatasetReadError):
        read_dataset(
            
                "snowflake://user:password@account/db/schema"
                "?warehouse=compute_wh:orders"
            
        )


# =========================================================
# Redshift Mock Tests
# =========================================================


def test_redshift_uri_parsing():
    connection_string, table_name = parse_sql_table_uri(
        
            "redshift+redshift_connector://"
            "user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders"
        
    )

    assert connection_string.startswith("redshift+")
    assert table_name == "orders"


@patch("dift.io.sql_reader.sa.create_engine")
def test_redshift_connection_failure(mock_create_engine):
    mock_create_engine.side_effect = Exception(
        "Redshift cluster unavailable"
    )

    with pytest.raises(ValueError):
        read_sql_table(
            (
                "redshift+redshift_connector://"
                "user:password@cluster.region.redshift.amazonaws.com:5439/dev"
            ),
            "orders",
        )


def test_redshift_missing_driver_error():
    with pytest.raises(DatasetReadError):
        read_dataset(
            
                "redshift+redshift_connector://"
                "user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders"
            
        )


# =========================================================
# BigQuery Mock Tests
# =========================================================


def test_bigquery_uri_parsing():
    project, dataset, table = parse_bigquery_uri(
        "bigquery://analytics.sales.customers"
    )

    assert project == "analytics"
    assert dataset == "sales"
    assert table == "customers"


@patch("dift.io.bigquery_reader.bigquery")
def test_bigquery_authentication_failure(mock_bigquery):
    mock_client = MagicMock()

    mock_client.query.side_effect = Exception(
        "BigQuery authentication failed"
    )

    mock_bigquery.Client.return_value = mock_client

    with pytest.raises(ValueError):
        read_bigquery_table(
            "bigquery://analytics.sales.customers"
        )


@patch("dift.io.bigquery_reader.bigquery")
def test_bigquery_query_failure(mock_bigquery):
    mock_client = MagicMock()

    mock_client.query.side_effect = Exception(
        "Invalid BigQuery query"
    )

    mock_bigquery.Client.return_value = mock_client

    with pytest.raises(ValueError):
        read_bigquery_query(
            "SELECT * FROM missing_table",
            project="analytics",
        )


def test_bigquery_missing_dependency_error():
    with pytest.raises(DatasetReadError):
        read_dataset("bigquery://analytics.sales.customers")



# General Warehouse Routing Tests


@pytest.mark.parametrize(
    "uri",
    [
        (
            "snowflake://user:password@account/db/schema"
            "?warehouse=compute_wh:orders"
        ),
        (
            "redshift+redshift_connector://"
            "user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders"
        ),
        "bigquery://analytics.sales.customers",
    ],
)
def test_warehouse_connector_routing_errors(uri):
    with pytest.raises(DatasetReadError):
        read_dataset(uri)