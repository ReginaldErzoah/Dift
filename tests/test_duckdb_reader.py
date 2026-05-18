import pytest

from dift.io.duckdb_reader import (
    is_duckdb_uri,
    parse_duckdb_uri,
    read_duckdb_query,
    read_duckdb_table,
)

duckdb = pytest.importorskip("duckdb")


def test_parse_duckdb_uri():
    database_path, table_name = parse_duckdb_uri(
        "duckdb:///data/warehouse.duckdb:customers"
    )

    assert database_path == "data/warehouse.duckdb"
    assert table_name == "customers"


def test_parse_duckdb_uri_rejects_invalid_uri():
    with pytest.raises(ValueError):
        parse_duckdb_uri("warehouse.duckdb:customers")


def test_is_duckdb_uri():
    assert is_duckdb_uri("duckdb:///data/warehouse.duckdb:customers")
    assert not is_duckdb_uri("examples/old.csv")


def test_read_duckdb_table(tmp_path):
    db_path = tmp_path / "warehouse.duckdb"

    conn = duckdb.connect(str(db_path))
    conn.execute("CREATE TABLE customers (customer_id INTEGER, name VARCHAR)")
    conn.execute("INSERT INTO customers VALUES (1, 'Ama'), (2, 'Kojo')")
    conn.close()

    df = read_duckdb_table(str(db_path), "customers")

    assert df.height == 2
    assert df.columns == ["customer_id", "name"]


def test_read_duckdb_query_from_database(tmp_path):
    db_path = tmp_path / "warehouse.duckdb"

    conn = duckdb.connect(str(db_path))
    conn.execute("CREATE TABLE customers (customer_id INTEGER, revenue INTEGER)")
    conn.execute("INSERT INTO customers VALUES (1, 100), (2, 200)")
    conn.close()

    df = read_duckdb_query(
        "SELECT * FROM customers WHERE revenue > 100",
        database_path=str(db_path),
    )

    assert df.height == 1
    assert df["customer_id"][0] == 2


def test_read_duckdb_query_in_memory():
    df = read_duckdb_query("SELECT 1 AS customer_id, 'Ama' AS name")

    assert df.height == 1
    assert df["customer_id"][0] == 1
    assert df["name"][0] == "Ama"


def test_read_duckdb_table_missing_database(tmp_path):
    missing_db = tmp_path / "missing.duckdb"

    with pytest.raises(FileNotFoundError):
        read_duckdb_table(str(missing_db), "customers")