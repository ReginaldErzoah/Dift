from dift.core.risk import calculate_risk_score
from dift.reports.models import (
    CategoricalDiff,
    DiffReport,
    DuplicateDiff,
    NumericDiff,
    QualityDiff,
    RowDiff,
    SchemaDiff,
    Summary,
)


def make_report(**overrides):
    report = DiffReport(
        summary=Summary(
            old_rows=10,
            new_rows=10,
            row_delta=0,
            old_columns=3,
            new_columns=3,
            column_delta=0,
            risk_level="low",
        ),
        schema_diff=SchemaDiff(),
        row_diff=RowDiff(),
        quality_diff=QualityDiff(
            null_diffs=[],
            duplicate_diff=DuplicateDiff(
                old_duplicates=0,
                new_duplicates=0,
                delta_duplicates=0,
                duplicate_basis="entire_row",
            ),
        ),
    )

    for key, value in overrides.items():
        setattr(report, key, value)

    return report


def test_numeric_drift_adds_risk_score():
    report = make_report(
        numeric_diff=[
            NumericDiff(
                column="revenue",
                old_mean=100,
                new_mean=160,
                delta_mean=60,
                is_drifted=True,
            )
        ]
    )

    assert calculate_risk_score(report) >= 15


def test_categorical_drift_adds_risk_score():
    report = make_report(
        categorical_diff=[
            CategoricalDiff(
                column="segment",
                values_added=["enterprise", "startup"],
                values_removed=["legacy"],
            )
        ]
    )

    assert calculate_risk_score(report) >= 10