import json
from pathlib import Path

import pandas as pd
import pytest

from dift.core.comparator import compare_datasets
from dift.reports.csv_report import render_csv
from dift.reports.html_report import render_html
from dift.reports.json_report import render_json

duckdb = pytest.importorskip("duckdb")
sqlalchemy = pytest.importorskip("sqlalchemy")


OLD_ROWS = [
    {"customer_id": 1, "name": "Ama", "segment": "retail", "revenue": 100},
    {"customer_id": 2, "name": "Kojo", "segment": "retail", "revenue": 200},
    {"customer_id": 3, "name": "Esi", "segment": "business", "revenue": 300},
]

NEW_ROWS = [
    {"customer_id": 1, "name": "Ama", "segment": "retail", "revenue": 150},
    {"customer_id": 2, "name": "Kojo", "segment": "retail", "revenue": 200},
    {"customer_id": 4, "name": "Yaw", "segment": "enterprise", "revenue": 500},
]


def _write_csv(path: Path, rows: list[dict]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def _write_parquet(path: Path, rows: list[dict]) -> None:
    pd.DataFrame(rows).to_parquet(path, index=False)


def _write_excel(path: Path, rows: list[dict]) -> None:
    pd.DataFrame(rows).to_excel(path, index=False)


def _write_json(path: Path, rows: list[dict]) -> None:
    path.write_text(json.dumps(rows), encoding="utf-8")


def _write_sqlite(path: Path, table_name: str, rows: list[dict]) -> None:
    engine = sqlalchemy.create_engine(f"sqlite:///{path}")
    df = pd.DataFrame(rows)

    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)


def _write_duckdb(path: Path, table_name: str, rows: list[dict]) -> None:
    conn = duckdb.connect(str(path))
    df = pd.DataFrame(rows)

    conn.register("rows_df", df)
    conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM rows_df")
    conn.close()


def _core_result(report) -> dict:
    return {
        "old_rows": report.summary.old_rows,
        "new_rows": report.summary.new_rows,
        "row_delta": report.summary.row_delta,
        "old_columns": report.summary.old_columns,
        "new_columns": report.summary.new_columns,
        "column_delta": report.summary.column_delta,
        "risk_level": report.summary.risk_level,
        "added_rows": report.row_diff.added_rows,
        "removed_rows": report.row_diff.removed_rows,
        "changed_rows": report.row_diff.changed_rows,
        "unchanged_rows": report.row_diff.unchanged_rows,
        "columns_added": report.schema_diff.columns_added,
        "columns_removed": report.schema_diff.columns_removed,
        "numeric_diff_count": len(report.numeric_diff),
        "categorical_diff_count": len(report.categorical_diff),
        "outlier_diff_count": len(report.outlier_diff),
    }


@pytest.fixture
def equivalent_sources(tmp_path):
    old_csv = tmp_path / "old.csv"
    new_csv = tmp_path / "new.csv"

    old_parquet = tmp_path / "old.parquet"
    new_parquet = tmp_path / "new.parquet"

    old_excel = tmp_path / "old.xlsx"
    new_excel = tmp_path / "new.xlsx"

    old_json = tmp_path / "old.json"
    new_json = tmp_path / "new.json"

    old_sqlite = tmp_path / "old.db"
    new_sqlite = tmp_path / "new.db"

    duckdb_path = tmp_path / "warehouse.duckdb"

    _write_csv(old_csv, OLD_ROWS)
    _write_csv(new_csv, NEW_ROWS)

    _write_parquet(old_parquet, OLD_ROWS)
    _write_parquet(new_parquet, NEW_ROWS)

    _write_excel(old_excel, OLD_ROWS)
    _write_excel(new_excel, NEW_ROWS)

    _write_json(old_json, OLD_ROWS)
    _write_json(new_json, NEW_ROWS)

    _write_sqlite(old_sqlite, "customers_old", OLD_ROWS)
    _write_sqlite(new_sqlite, "customers_new", NEW_ROWS)

    _write_duckdb(duckdb_path, "customers_old", OLD_ROWS)
    _write_duckdb(duckdb_path, "customers_new", NEW_ROWS)

    return {
        "csv": (str(old_csv), str(new_csv)),
        "parquet": (str(old_parquet), str(new_parquet)),
        "excel": (str(old_excel), str(new_excel)),
        "json": (str(old_json), str(new_json)),
        "sqlite": (
            f"sqlite:///{old_sqlite}:customers_old",
            f"sqlite:///{new_sqlite}:customers_new",
        ),
        "duckdb": (
            f"duckdb:///{duckdb_path}:customers_old",
            f"duckdb:///{duckdb_path}:customers_new",
        ),
    }


@pytest.mark.parametrize(
    "format_name",
    ["parquet", "excel", "json", "sqlite", "duckdb"],
)
def test_cross_format_results_match_csv_baseline(equivalent_sources, format_name):
    old_csv, new_csv = equivalent_sources["csv"]
    old_other, new_other = equivalent_sources[format_name]

    csv_report = compare_datasets(old_csv, new_csv, key="customer_id")
    other_report = compare_datasets(old_other, new_other, key="customer_id")

    assert _core_result(other_report) == _core_result(csv_report)


def test_sql_vs_file_consistency(equivalent_sources):
    old_csv, new_csv = equivalent_sources["csv"]
    old_sqlite, new_sqlite = equivalent_sources["sqlite"]

    csv_report = compare_datasets(old_csv, new_csv, key="customer_id")
    sqlite_report = compare_datasets(old_sqlite, new_sqlite, key="customer_id")

    assert _core_result(sqlite_report) == _core_result(csv_report)


def test_duckdb_vs_parquet_consistency(equivalent_sources):
    old_parquet, new_parquet = equivalent_sources["parquet"]
    old_duckdb, new_duckdb = equivalent_sources["duckdb"]

    parquet_report = compare_datasets(old_parquet, new_parquet, key="customer_id")
    duckdb_report = compare_datasets(old_duckdb, new_duckdb, key="customer_id")

    assert _core_result(duckdb_report) == _core_result(parquet_report)


def test_report_generation_consistency(equivalent_sources, tmp_path):
    old_csv, new_csv = equivalent_sources["csv"]
    old_sqlite, new_sqlite = equivalent_sources["sqlite"]

    csv_report = compare_datasets(old_csv, new_csv, key="customer_id")
    sqlite_report = compare_datasets(old_sqlite, new_sqlite, key="customer_id")

    csv_json = json.loads(render_json(csv_report))
    sqlite_json = json.loads(render_json(sqlite_report))

    assert csv_json["summary"] == sqlite_json["summary"]
    assert csv_json["rows"] == sqlite_json["rows"]

    csv_summary = render_csv(csv_report)
    sqlite_summary = render_csv(sqlite_report)

    assert "risk_level" in csv_summary
    assert "risk_level" in sqlite_summary

    html_path = render_html(
        sqlite_report,
        output=str(tmp_path / "cross_format_report.html"),
    )

    assert html_path.exists()
    assert "Dift Dataset Diff Report" in html_path.read_text(encoding="utf-8")