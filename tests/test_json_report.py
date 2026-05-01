import json

from dift.reports.json_report import render_json
from dift.reports.models import (
    DiffReport,
    DuplicateDiff,
    QualityDiff,
    RowDiff,
    SchemaDiff,
    Summary,
)


def test_render_json_structure():
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

    payload = render_json(report)
    data = json.loads(payload)

    #New structure (aliases)
    assert "metadata" in data
    assert "summary" in data
    assert "schema" in data
    assert "rows" in data
    assert "quality" in data
    assert "numeric" in data
    assert "categorical" in data

    #Old names should NOT appear
    assert "schema_diff" not in data
    assert "row_diff" not in data
    assert "quality_diff" not in data
    assert "numeric_diff" not in data
    assert "categorical_diff" not in data

    # Metadata sanity check
    assert data["metadata"]["tool"] == "dift"
    assert data["metadata"]["version"] == "0.3.0"