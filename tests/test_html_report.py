from dift.reports.html_report import render_html
from dift.reports.models import (
    DiffReport,
    DuplicateDiff,
    QualityDiff,
    RowDiff,
    SchemaDiff,
    Summary,
)


def test_render_html_writes_file(tmp_path):
    output_path = tmp_path / "report.html"

    report = DiffReport(
        summary=Summary(
            old_rows=10,
            new_rows=11,
            row_delta=1,
            old_columns=4,
            new_columns=5,
            column_delta=1,
            risk_level="medium",
        ),
        schema_diff=SchemaDiff(columns_added=["email"]),
        row_diff=RowDiff(
            key="customer_id",
            added_rows=1,
            removed_rows=0,
            changed_rows=0,
            unchanged_rows=10,
            compared_columns=["name", "email"],
        ),
        quality_diff=QualityDiff(
            null_diffs=[],
            duplicate_diff=DuplicateDiff(
                old_duplicates=0,
                new_duplicates=0,
                delta_duplicates=0,
                duplicate_basis="all_columns",
            ),
        ),
    )

    result = render_html(report, output=str(output_path))

    assert result == output_path
    assert output_path.exists()

    html = output_path.read_text(encoding="utf-8")

    assert "<!DOCTYPE html>" in html
    assert "Dift Dataset Diff Report" in html
    assert "Summary" in html
    assert "Schema Diff" in html
    assert "Row Diff" in html
    assert "Quality Diff" in html
    assert "email" in html