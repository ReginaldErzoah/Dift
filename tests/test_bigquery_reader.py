from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from dift.io.bigquery_reader import (
    is_bigquery_uri,
    parse_bigquery_uri,
    read_bigquery_query,
    read_bigquery_table,
)


def test_is_bigquery_uri():
    assert is_bigquery_uri("bigquery://project.dataset.table")
    assert not is_bigquery_uri("examples/old.csv")


def test_parse_bigquery_uri():
    project, dataset, table = parse_bigquery_uri(
        "bigquery://my-project.analytics.customers"
    )

    assert project == "my-project"
    assert dataset == "analytics"
    assert table == "customers"


def test_parse_bigquery_uri_rejects_invalid_uri():
    with pytest.raises(ValueError):
        parse_bigquery_uri("bigquery://project.dataset")

    with pytest.raises(ValueError):
        parse_bigquery_uri("examples/old.csv")


@patch("dift.io.bigquery_reader.bigquery")
def test_read_bigquery_table(mock_bigquery):
    mock_client = MagicMock()
    mock_job = MagicMock()

    mock_job.to_dataframe.return_value = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "name": ["Ama", "Kojo"],
        }
    )

    mock_client.query.return_value = mock_job
    mock_bigquery.Client.return_value = mock_client

    df = read_bigquery_table("bigquery://my-project.analytics.customers")

    assert df.height == 2
    assert df.columns == ["customer_id", "name"]

    mock_bigquery.Client.assert_called_once_with(project="my-project")
    mock_client.query.assert_called_once_with(
        "SELECT * FROM `my-project.analytics.customers`"
    )


@patch("dift.io.bigquery_reader.bigquery")
def test_read_bigquery_query(mock_bigquery):
    mock_client = MagicMock()
    mock_job = MagicMock()

    mock_job.to_dataframe.return_value = pd.DataFrame(
        {
            "customer_id": [1],
            "revenue": [100],
        }
    )

    mock_client.query.return_value = mock_job
    mock_bigquery.Client.return_value = mock_client

    df = read_bigquery_query(
        "SELECT customer_id, revenue FROM `project.dataset.customers`",
        project="my-project",
    )

    assert df.height == 1
    assert df["customer_id"][0] == 1

    mock_bigquery.Client.assert_called_once_with(project="my-project")


@patch("dift.io.bigquery_reader.bigquery")
def test_read_bigquery_table_failure_raises_value_error(mock_bigquery):
    mock_client = MagicMock()
    mock_client.query.side_effect = RuntimeError("auth failed")
    mock_bigquery.Client.return_value = mock_client

    with pytest.raises(ValueError):
        read_bigquery_table("bigquery://my-project.analytics.customers")