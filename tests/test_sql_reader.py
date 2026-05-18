import pytest

from dift.io.sql_reader import (
    is_sql_uri,
    parse_sql_table_uri,
    read_sql_query,
    read_sql_table,
)

sqlalchemy = pytest.importorskip("sqlalchemy")


def test_is_sql_uri():
    assert is_sql_uri("sqlite:///examples/test.db:customers")
    assert is_sql_uri("postgresql://user:pass@localhost:5432/db:customers")
    assert is_sql_uri("mysql://user:pass@localhost:3306/db:customers")
    assert not is_sql_uri("examples/old.csv")


def test_parse_sql_table_uri():
    connection_string, table_name = parse_sql_table_uri(
        "sqlite:///examples/test.db:customers"
    )

    assert connection_string == "sqlite:///examples/test.db"
    assert table_name == "customers"


def test_parse_sql_table_uri_rejects_invalid_uri():
    with pytest.raises(ValueError):
        parse_sql_table_uri("examples/test.db:customers")


def test_read_sql_table_sqlite(tmp_path):
    db_path = tmp_path / "customers.db"
    connection_string = f"sqlite:///{db_path}"

    engine = sqlalchemy.create_engine(connection_string)

    with engine.begin() as conn:
        conn.exec_driver_sql(
            "CREATE TABLE customers (customer_id INTEGER, name TEXT, revenue INTEGER)"
        )
        conn.exec_driver_sql(
            "INSERT INTO customers VALUES (1, 'Ama', 100), (2, 'Kojo', 200)"
        )

    df = read_sql_table(connection_string, "customers")

    assert df.height == 2
    assert df.columns == ["customer_id", "name", "revenue"]


def test_read_sql_query_sqlite(tmp_path):
    db_path = tmp_path / "customers.db"
    connection_string = f"sqlite:///{db_path}"

    engine = sqlalchemy.create_engine(connection_string)

    with engine.begin() as conn:
        conn.exec_driver_sql(
            "CREATE TABLE customers (customer_id INTEGER, name TEXT, revenue INTEGER)"
        )
        conn.exec_driver_sql(
            "INSERT INTO customers VALUES (1, 'Ama', 100), (2, 'Kojo', 200)"
        )

    df = read_sql_query(
        connection_string,
        "SELECT * FROM customers WHERE revenue > 100",
    )

    assert df.height == 1
    assert df["customer_id"][0] == 2


def test_read_sql_table_invalid_table_raises(tmp_path):
    db_path = tmp_path / "customers.db"
    connection_string = f"sqlite:///{db_path}"

    engine = sqlalchemy.create_engine(connection_string)

    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE TABLE customers (customer_id INTEGER)")

    with pytest.raises(ValueError):
        read_sql_table(connection_string, "missing_table")