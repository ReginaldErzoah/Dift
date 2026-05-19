from pathlib import Path

import pytest

from dift.core.comparator import compare_datasets
from dift.io.readers import DatasetReadError, read_dataset
from dift.reports.html_report import render_html
from dift.reports.json_report import render_json

duckdb = pytest.importorskip("duckdb")
sqlalchemy = pytest.importorskip("sqlalchemy")


def _write_csv(path: Path) -> None:
    path.write_text(
        "customer_id,name,revenue\n"
        "1,Ama,100\n"
        "2,Kojo,200\n",
        encoding="utf-8",
    )


def _create_sqlite_db(path: Path, table_name: str, rows: list[tuple[int, str, int]]) -> None:
    engine = sqlalchemy.create_engine(f"sqlite:///{path}")

    with engine.begin() as conn:
        conn.exec_driver_sql(
            f"""
            CREATE TABLE {table_name} (
                customer_id INTEGER,
                name TEXT,
                revenue INTEGER
            )
            """
        )

        for row in rows:
            conn.exec_driver_sql(
                f"INSERT INTO {table_name} VALUES (?, ?, ?)",
                row,
            )


def _create_duckdb(path: Path) -> None:
    conn = duckdb.connect(str(path))

    conn.execute("CREATE TABLE customers_old (customer_id INTEGER, name VARCHAR, revenue INTEGER)")
    conn.execute("INSERT INTO customers_old VALUES (1, 'Ama', 100), (2, 'Kojo', 200)")

    conn.execute("CREATE TABLE customers_new (customer_id INTEGER, name VARCHAR, revenue INTEGER)")
    conn.execute(
        "INSERT INTO customers_new VALUES "
        "(1, 'Ama', 150), "
        "(2, 'Kojo', 200), "
        "(3, 'Yaw', 300)"
    )

    conn.close()


def test_sqlite_connector_to_connector_comparison(tmp_path):
    old_db = tmp_path / "old.db"
    new_db = tmp_path / "new.db"

    _create_sqlite_db(
        old_db,
        "customers_old",
        [
            (1, "Ama", 100),
            (2, "Kojo", 200),
        ],
    )
    _create_sqlite_db(
        new_db,
        "customers_new",
        [
            (1, "Ama", 150),
            (2, "Kojo", 200),
            (3, "Yaw", 300),
        ],
    )

    report = compare_datasets(
        f"sqlite:///{old_db}:customers_old",
        f"sqlite:///{new_db}:customers_new",
        key="customer_id",
    )

    assert report.summary.old_rows == 2
    assert report.summary.new_rows == 3
    assert report.summary.row_delta == 1
    assert report.row_diff.added_rows == 1
    assert report.summary.risk_level in {"low", "medium", "high"}


def test_sqlite_connector_to_file_comparison(tmp_path):
    old_db = tmp_path / "old.db"
    new_csv = tmp_path / "new.csv"

    _create_sqlite_db(
        old_db,
        "customers_old",
        [
            (1, "Ama", 100),
            (2, "Kojo", 200),
        ],
    )
    _write_csv(new_csv)

    report = compare_datasets(
        f"sqlite:///{old_db}:customers_old",
        str(new_csv),
        key="customer_id",
    )

    assert report.summary.old_rows == 2
    assert report.summary.new_rows == 2
    assert report.row_diff.unchanged_rows >= 1


def test_duckdb_connector_to_connector_comparison(tmp_path):
    db_path = tmp_path / "warehouse.duckdb"
    _create_duckdb(db_path)

    report = compare_datasets(
        f"duckdb:///{db_path}:customers_old",
        f"duckdb:///{db_path}:customers_new",
        key="customer_id",
    )

    assert report.summary.old_rows == 2
    assert report.summary.new_rows == 3
    assert report.row_diff.added_rows == 1
    assert report.summary.risk_level in {"low", "medium", "high"}


def test_connector_report_generation_compatibility(tmp_path):
    old_db = tmp_path / "old.db"
    new_db = tmp_path / "new.db"

    _create_sqlite_db(
        old_db,
        "customers_old",
        [
            (1, "Ama", 100),
            (2, "Kojo", 200),
        ],
    )
    _create_sqlite_db(
        new_db,
        "customers_new",
        [
            (1, "Ama", 150),
            (2, "Kojo", 200),
            (3, "Yaw", 300),
        ],
    )

    report = compare_datasets(
        f"sqlite:///{old_db}:customers_old",
        f"sqlite:///{new_db}:customers_new",
        key="customer_id",
    )

    json_payload = render_json(report)
    html_path = render_html(report, output=str(tmp_path / "connector_report.html"))

    assert "summary" in json_payload
    assert html_path.exists()
    assert "Dift Dataset Diff Report" in html_path.read_text(encoding="utf-8")


def test_sql_connector_invalid_table_error(tmp_path):
    db_path = tmp_path / "customers.db"

    _create_sqlite_db(
        db_path,
        "customers",
        [
            (1, "Ama", 100),
        ],
    )

    with pytest.raises(DatasetReadError):
        read_dataset(f"sqlite:///{db_path}:missing_table")


def test_external_warehouse_uri_routing_errors_are_clear():
    with pytest.raises(DatasetReadError):
        read_dataset(
            "snowflake://user:password@account/db/schema?"
            "warehouse=compute_wh:orders"
        )


def test_bigquery_uri_routing_errors_are_clear():
    with pytest.raises(DatasetReadError):
        read_dataset("bigquery://project.dataset.table")