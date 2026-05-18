from dift.reports.html_report import render_html
from dift.reports.models import (
    CategoricalDiff,
    DiffReport,
    DuplicateDiff,
    NullDiff,
    NumericDiff,
    OutlierDiff,
    QualityDiff,
    RowDiff,
    SchemaDiff,
    Summary,
)


def _sample_report() -> DiffReport:
    return DiffReport(
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
            changed_rows=1,
            unchanged_rows=9,
            compared_columns=["name", "email"],
        ),
        quality_diff=QualityDiff(
            null_diffs=[
                NullDiff(
                    column="email",
                    old_nulls=0,
                    new_nulls=3,
                    old_null_pct=0.0,
                    new_null_pct=27.27,
                    delta_null_pct=27.27,
                    is_spike=True,
                    severity="high",
                )
            ],
            duplicate_diff=DuplicateDiff(
                old_duplicates=0,
                new_duplicates=2,
                delta_duplicates=2,
                old_duplicate_pct=0.0,
                new_duplicate_pct=18.18,
                delta_duplicate_pct=18.18,
                duplicate_basis="all_columns",
                is_spike=True,
                severity="medium",
            ),
        ),
        numeric_diff=[
            NumericDiff(
                column="revenue",
                old_mean=100.0,
                new_mean=250.0,
                delta_mean=150.0,
                mean_shift_pct=1.5,
                old_std=10.0,
                new_std=40.0,
                delta_std=30.0,
                std_shift_pct=3.0,
                delta_range=100.0,
                range_shift_pct=1.0,
                drift_threshold=0.1,
                is_drifted=True,
                severity="high",
            )
        ],
        outlier_diff=[
            OutlierDiff(
                column="revenue",
                method="iqr",
                old_outliers=0,
                new_outliers=2,
                delta_outliers=2,
                old_outlier_pct=0.0,
                new_outlier_pct=18.18,
                delta_outlier_pct=18.18,
                lower_bound=10.0,
                upper_bound=300.0,
                is_spike=True,
                severity="high",
            )
        ],
        categorical_diff=[
            CategoricalDiff(
                column="segment",
                values_added=["enterprise"],
                values_removed=[],
                old_top_values={"retail": 8},
                new_top_values={"enterprise": 6},
                frequency_shifts={"enterprise": 0.6},
                max_frequency_shift=0.6,
                is_shifted=True,
                severity="high",
            )
        ],
    )


def test_render_html_writes_file(tmp_path):
    output_path = tmp_path / "report.html"
    report = _sample_report()

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


def test_html_report_renders_visual_summary_cards(tmp_path):
    output_path = tmp_path / "visual.html"
    report = _sample_report()

    render_html(report, output=str(output_path))

    html = output_path.read_text(encoding="utf-8")

    assert "Visual Summary" in html
    assert "Key Findings" in html
    assert "summary-grid" in html
    assert "summary-card" in html
    assert "Risk Level" in html
    assert "Row Delta" in html
    assert "Column Delta" in html
    assert "Null Spikes" in html
    assert "Duplicate Spikes" in html
    assert "Numeric Drift Columns" in html
    assert "Outlier Spikes" in html
    assert "Categorical Shifts" in html


def test_html_report_renders_risk_and_severity_badges(tmp_path):
    output_path = tmp_path / "badges.html"
    report = _sample_report()

    render_html(report, output=str(output_path))

    html = output_path.read_text(encoding="utf-8")

    assert "risk-badge risk-medium" in html
    assert "severity-badge severity-high" in html
    assert "severity-badge severity-medium" in html
    assert "yes-no-badge yes-no-yes" in html


def test_html_report_highlights_findings(tmp_path):
    output_path = tmp_path / "highlights.html"
    report = _sample_report()

    render_html(report, output=str(output_path))

    html = output_path.read_text(encoding="utf-8")

    assert "row-alert" in html
    assert "has-findings" in html
    assert "changed" in html
    assert "<strong>revenue</strong>" in html
    assert "<strong>segment</strong>" in html


def test_html_report_dark_template_is_supported(tmp_path):
    output_path = tmp_path / "dark.html"
    report = _sample_report()

    render_html(report, output=str(output_path), template="dark")

    html = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert "background: #020617" in html
    assert "Visual Summary" in html
    assert "risk-medium" in html


def test_html_report_contains_responsive_css(tmp_path):
    output_path = tmp_path / "responsive.html"
    report = _sample_report()

    render_html(report, output=str(output_path))

    html = output_path.read_text(encoding="utf-8")

    assert '@media (max-width: 900px)' in html
    assert '@media (max-width: 560px)' in html