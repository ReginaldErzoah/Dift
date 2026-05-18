from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from dift.reports.models import DiffReport

SUPPORTED_TEMPLATES = {
    "default",
    "clean",
    "compact",
    "enterprise",
    "dark",
}


def render_html(
    report: DiffReport,
    output: str | None = None,
    template: str = "default",
) -> Path:
    """Render and write an HTML report."""

    if template not in SUPPORTED_TEMPLATES:
        supported = ", ".join(sorted(SUPPORTED_TEMPLATES))
        raise ValueError(
            f"Unsupported HTML template '{template}'. Supported templates: {supported}"
        )

    output_path = Path(output or "dift_report.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html = _build_html(report, template=template)
    output_path.write_text(html, encoding="utf-8")

    return output_path


def _build_html(report: DiffReport, template: str) -> str:
    risk = _safe(report.summary.risk_level).lower()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dift Report</title>
  <style>
    {_template_css(template)}
  </style>
</head>
<body>
  <main>
    <header class="report-header">
      <div>
        <p class="eyebrow">Dift Report</p>
        <h1>Dift Dataset Diff Report</h1>
        <p class="muted">Template: {_safe(template)}</p>
      </div>
      <div class="risk-badge risk-{risk}">Risk: {_safe(report.summary.risk_level)}</div>
    </header>

    {_visual_summary_section(report)}
    {_summary_section(report)}
    {_metadata_section(report)}
    {_schema_section(report)}
    {_row_section(report)}
    {_quality_section(report)}
    {_numeric_section(report)}
    {_outlier_section(report)}
    {_categorical_section(report)}

  </main>
</body>
</html>
"""


def _visual_summary_section(report: DiffReport) -> str:
    duplicate = report.quality_diff.duplicate_diff

    null_spikes = sum(1 for item in report.quality_diff.null_diffs if item.is_spike)
    numeric_drift_columns = sum(1 for item in report.numeric_diff if item.is_drifted)
    outlier_spikes = sum(1 for item in report.outlier_diff if item.is_spike)
    categorical_shifts = sum(
        1 for item in report.categorical_diff if item.is_shifted
    )

    duplicate_spikes = 1 if duplicate.is_spike else 0

    cards = [
        ("Risk Level", report.summary.risk_level, f"risk-{report.summary.risk_level}"),
        ("Row Delta", report.summary.row_delta, _delta_class(report.summary.row_delta)),
        (
            "Column Delta",
            report.summary.column_delta,
            _delta_class(report.summary.column_delta),
        ),
        ("Null Spikes", null_spikes, _count_class(null_spikes)),
        ("Duplicate Spikes", duplicate_spikes, _count_class(duplicate_spikes)),
        (
            "Numeric Drift Columns",
            numeric_drift_columns,
            _count_class(numeric_drift_columns),
        ),
        ("Outlier Spikes", outlier_spikes, _count_class(outlier_spikes)),
        ("Categorical Shifts", categorical_shifts, _count_class(categorical_shifts)),
    ]

    card_html = ""

    for label, value, class_name in cards:
        card_html += f"""
        <div class="summary-card {class_name}">
          <span>{_safe(label)}</span>
          <strong>{_safe(value)}</strong>
        </div>
        """

    return f"""
    <section class="visual-summary">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Key Findings</p>
          <h2>Visual Summary</h2>
        </div>
        <p class="muted">Important changes are highlighted for quick review.</p>
      </div>
      <div class="summary-grid">
        {card_html}
      </div>
    </section>
    """


def _summary_section(report: DiffReport) -> str:
    risk = _safe(report.summary.risk_level).lower()

    return f"""
    <section class="card">
      <h2>Summary</h2>
      <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Old rows</td><td>{report.summary.old_rows}</td></tr>
        <tr><td>New rows</td><td>{report.summary.new_rows}</td></tr>
        <tr class="{_delta_class(report.summary.row_delta)}"><td>Row delta</td><td>{report.summary.row_delta}</td></tr>
        <tr><td>Old columns</td><td>{report.summary.old_columns}</td></tr>
        <tr><td>New columns</td><td>{report.summary.new_columns}</td></tr>
        <tr class="{_delta_class(report.summary.column_delta)}"><td>Column delta</td><td>{report.summary.column_delta}</td></tr>
        <tr><td>Risk level</td><td><span class="pill risk-{risk}">{_safe(report.summary.risk_level)}</span></td></tr>
      </table>
    </section>
    """


def _metadata_section(report: DiffReport) -> str:
    metadata = report.metadata

    return f"""
    <section class="card">
      <h2>Report Metadata</h2>
      <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Tool</td><td>{_safe(metadata.tool)}</td></tr>
        <tr><td>Version</td><td>{_safe(metadata.version)}</td></tr>
        <tr><td>Report type</td><td>{_safe(metadata.report_type)}</td></tr>
        <tr><td>Generated at</td><td>{_safe(metadata.generated_at)}</td></tr>
        <tr><td>Old source</td><td>{_safe(metadata.old_source)}</td></tr>
        <tr><td>New source</td><td>{_safe(metadata.new_source)}</td></tr>
        <tr><td>Key</td><td>{_safe(metadata.key)}</td></tr>
        <tr><td>Threshold</td><td>{_safe(metadata.threshold)}</td></tr>
        <tr><td>Report format</td><td>{_safe(metadata.report_format)}</td></tr>
        <tr><td>Template</td><td>{_safe(metadata.template)}</td></tr>
        <tr><td>Runtime seconds</td><td>{_safe(metadata.runtime_seconds)}</td></tr>
      </table>
    </section>
    """


def _schema_section(report: DiffReport) -> str:
    type_rows = ""

    for change in report.schema_diff.type_changes:
        type_rows += (
            '<tr class="row-highlight">'
            f"<td>{_safe(change.column)}</td>"
            f"<td>{_safe(change.old_type)}</td>"
            f"<td>{_safe(change.new_type)}</td>"
            "</tr>"
        )

    if not type_rows:
        type_rows = '<tr><td colspan="3">No type changes detected.</td></tr>'

    return f"""
    <section class="card">
      <h2>Schema Diff</h2>
      <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr class="{_count_class(len(report.schema_diff.columns_added))}"><td>Columns added</td><td>{_safe_list(report.schema_diff.columns_added)}</td></tr>
        <tr class="{_count_class(len(report.schema_diff.columns_removed))}"><td>Columns removed</td><td>{_safe_list(report.schema_diff.columns_removed)}</td></tr>
        <tr><td>Shared columns</td><td>{_safe_list(report.schema_diff.shared_columns)}</td></tr>
      </table>

      <h3>Type Changes</h3>
      <table>
        <tr><th>Column</th><th>Old Type</th><th>New Type</th></tr>
        {type_rows}
      </table>
    </section>
    """


def _row_section(report: DiffReport) -> str:
    row_diff = report.row_diff

    return f"""
    <section class="card">
      <h2>Row Diff</h2>
      <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Key</td><td>{_safe(row_diff.key)}</td></tr>
        <tr class="{_count_class(row_diff.added_rows)}"><td>Added rows</td><td>{_safe(row_diff.added_rows)}</td></tr>
        <tr class="{_count_class(row_diff.removed_rows)}"><td>Removed rows</td><td>{_safe(row_diff.removed_rows)}</td></tr>
        <tr class="{_count_class(row_diff.changed_rows)}"><td>Changed rows</td><td>{_safe(row_diff.changed_rows)}</td></tr>
        <tr><td>Unchanged rows</td><td>{_safe(row_diff.unchanged_rows)}</td></tr>
        <tr><td>Compared columns</td><td>{_safe_list(row_diff.compared_columns)}</td></tr>
        <tr><td>Note</td><td>{_safe(row_diff.note)}</td></tr>
      </table>
    </section>
    """


def _quality_section(report: DiffReport) -> str:
    duplicate = report.quality_diff.duplicate_diff
    null_rows = ""

    for item in report.quality_diff.null_diffs:
        row_class = "row-alert" if item.is_spike else ""
        null_rows += (
            f'<tr class="{row_class}">'
            f"<td>{_safe(item.column)}</td>"
            f"<td>{item.old_nulls}</td>"
            f"<td>{item.new_nulls}</td>"
            f"<td>{item.old_null_pct:.2f}%</td>"
            f"<td>{item.new_null_pct:.2f}%</td>"
            f"<td>{item.delta_null_pct:.2f}%</td>"
            f"<td>{_yes_no_badge(item.is_spike)}</td>"
            f"<td>{_severity_badge(item.severity)}</td>"
            "</tr>"
        )

    if not null_rows:
        null_rows = '<tr><td colspan="8">No null changes detected.</td></tr>'

    duplicate_class = "row-alert" if duplicate.is_spike else ""

    return f"""
    <section class="card">
      <h2>Quality Diff</h2>

      <h3>Null Changes</h3>
      <table>
        <tr>
          <th>Column</th>
          <th>Old Nulls</th>
          <th>New Nulls</th>
          <th>Old Null %</th>
          <th>New Null %</th>
          <th>Delta Null %</th>
          <th>Spike</th>
          <th>Severity</th>
        </tr>
        {null_rows}
      </table>

      <h3>Duplicate Changes</h3>
      <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Old duplicates</td><td>{duplicate.old_duplicates}</td></tr>
        <tr><td>New duplicates</td><td>{duplicate.new_duplicates}</td></tr>
        <tr class="{_delta_class(duplicate.delta_duplicates)}"><td>Delta duplicates</td><td>{duplicate.delta_duplicates}</td></tr>
        <tr><td>Old duplicate %</td><td>{duplicate.old_duplicate_pct:.2f}%</td></tr>
        <tr><td>New duplicate %</td><td>{duplicate.new_duplicate_pct:.2f}%</td></tr>
        <tr class="{_delta_class(duplicate.delta_duplicate_pct)}"><td>Delta duplicate %</td><td>{duplicate.delta_duplicate_pct:.2f}%</td></tr>
        <tr><td>Duplicate basis</td><td>{_safe(duplicate.duplicate_basis)}</td></tr>
        <tr class="{duplicate_class}"><td>Spike</td><td>{_yes_no_badge(duplicate.is_spike)}</td></tr>
        <tr><td>Severity</td><td>{_severity_badge(duplicate.severity)}</td></tr>
      </table>
    </section>
    """


def _numeric_section(report: DiffReport) -> str:
    rows = ""

    for item in report.numeric_diff:
        row_class = "row-alert" if item.is_drifted else ""
        rows += (
            f'<tr class="{row_class}">'
            f"<td><strong>{_safe(item.column)}</strong></td>"
            f"<td>{_safe(item.old_mean)}</td>"
            f"<td>{_safe(item.new_mean)}</td>"
            f"<td>{_safe(item.delta_mean)}</td>"
            f"<td>{_safe_pct(item.mean_shift_pct)}</td>"
            f"<td>{_safe(item.old_std)}</td>"
            f"<td>{_safe(item.new_std)}</td>"
            f"<td>{_safe(item.delta_std)}</td>"
            f"<td>{_safe_pct(item.std_shift_pct)}</td>"
            f"<td>{_safe(item.delta_range)}</td>"
            f"<td>{_safe_pct(item.range_shift_pct)}</td>"
            f"<td>{_safe(item.drift_threshold)}</td>"
            f"<td>{_yes_no_badge(item.is_drifted)}</td>"
            f"<td>{_severity_badge(item.severity)}</td>"
            "</tr>"
        )

    if not rows:
        rows = '<tr><td colspan="14">No numeric drift detected.</td></tr>'

    return f"""
    <section class="card">
      <h2>Numeric Drift</h2>
      <table>
        <tr>
          <th>Column</th>
          <th>Old Mean</th>
          <th>New Mean</th>
          <th>Delta Mean</th>
          <th>Mean Shift %</th>
          <th>Old Std</th>
          <th>New Std</th>
          <th>Delta Std</th>
          <th>Std Shift %</th>
          <th>Delta Range</th>
          <th>Range Shift %</th>
          <th>Threshold</th>
          <th>Drifted</th>
          <th>Severity</th>
        </tr>
        {rows}
      </table>
    </section>
    """


def _outlier_section(report: DiffReport) -> str:
    rows = ""

    for item in report.outlier_diff:
        row_class = "row-alert" if item.is_spike else ""
        rows += (
            f'<tr class="{row_class}">'
            f"<td><strong>{_safe(item.column)}</strong></td>"
            f"<td>{_safe(item.method)}</td>"
            f"<td>{item.old_outliers}</td>"
            f"<td>{item.new_outliers}</td>"
            f"<td>{item.delta_outliers}</td>"
            f"<td>{item.old_outlier_pct:.2f}%</td>"
            f"<td>{item.new_outlier_pct:.2f}%</td>"
            f"<td>{item.delta_outlier_pct:.2f}%</td>"
            f"<td>{_safe(item.lower_bound)}</td>"
            f"<td>{_safe(item.upper_bound)}</td>"
            f"<td>{_yes_no_badge(item.is_spike)}</td>"
            f"<td>{_severity_badge(item.severity)}</td>"
            "</tr>"
        )

    if not rows:
        rows = '<tr><td colspan="12">No outlier changes detected.</td></tr>'

    return f"""
    <section class="card">
      <h2>Outlier Diff</h2>
      <table>
        <tr>
          <th>Column</th>
          <th>Method</th>
          <th>Old Outliers</th>
          <th>New Outliers</th>
          <th>Delta Outliers</th>
          <th>Old Outlier %</th>
          <th>New Outlier %</th>
          <th>Delta Outlier %</th>
          <th>Lower Bound</th>
          <th>Upper Bound</th>
          <th>Spike</th>
          <th>Severity</th>
        </tr>
        {rows}
      </table>
    </section>
    """


def _categorical_section(report: DiffReport) -> str:
    rows = ""

    for item in report.categorical_diff:
        row_class = "row-alert" if item.is_shifted else ""
        rows += (
            f'<tr class="{row_class}">'
            f"<td><strong>{_safe(item.column)}</strong></td>"
            f"<td>{_safe_list(item.values_added)}</td>"
            f"<td>{_safe_list(item.values_removed)}</td>"
            f"<td>{_safe_frequency_shifts(item.frequency_shifts)}</td>"
            f"<td>{item.max_frequency_shift:.2%}</td>"
            f"<td>{_yes_no_badge(item.is_shifted)}</td>"
            f"<td>{_severity_badge(item.severity)}</td>"
            "</tr>"
        )

    if not rows:
        rows = '<tr><td colspan="7">No categorical changes detected.</td></tr>'

    return f"""
    <section class="card">
      <h2>Categorical Diff</h2>
      <table>
        <tr>
          <th>Column</th>
          <th>Values Added</th>
          <th>Values Removed</th>
          <th>Frequency Shifts</th>
          <th>Max Frequency Shift</th>
          <th>Shifted</th>
          <th>Severity</th>
        </tr>
        {rows}
      </table>
    </section>
    """


def _template_css(template: str) -> str:
    base = """
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;
      line-height: 1.5;
    }

    main {
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px;
    }

    .report-header {
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: flex-start;
      margin-bottom: 24px;
    }

    h1 {
      margin: 0;
      font-size: clamp(28px, 4vw, 42px);
      line-height: 1.1;
      letter-spacing: -0.04em;
    }

    h2 {
      margin: 0;
      font-size: 22px;
      letter-spacing: -0.02em;
    }

    h3 {
      margin-top: 28px;
      margin-bottom: 10px;
      font-size: 16px;
    }

    .eyebrow {
      margin: 0 0 6px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 12px;
      font-weight: 800;
    }

    .muted {
      margin: 6px 0 0;
      font-size: 14px;
    }

    .section-heading {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-end;
      margin-bottom: 16px;
    }

    .visual-summary {
      margin-bottom: 24px;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }

    .summary-card {
      border-radius: 16px;
      padding: 18px;
      min-height: 104px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border: 1px solid transparent;
    }

    .summary-card span {
      font-size: 13px;
      font-weight: 700;
      opacity: 0.82;
    }

    .summary-card strong {
      font-size: 30px;
      line-height: 1;
      letter-spacing: -0.04em;
      text-transform: capitalize;
    }

    .risk-badge,
    .pill,
    .severity-badge,
    .yes-no-badge {
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      font-weight: 800;
      white-space: nowrap;
      line-height: 1;
    }

    .risk-badge {
      padding: 10px 16px;
      font-size: 14px;
      text-transform: capitalize;
    }

    .pill,
    .severity-badge,
    .yes-no-badge {
      padding: 6px 10px;
      font-size: 12px;
      text-transform: capitalize;
    }

    .card {
      border-radius: 16px;
      padding: 22px;
      margin-bottom: 24px;
      overflow-x: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      min-width: 760px;
    }

    th,
    td {
      text-align: left;
      padding: 11px 12px;
      vertical-align: top;
      font-size: 14px;
    }

    th {
      position: sticky;
      top: 0;
      z-index: 1;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .risk-low,
    .severity-low,
    .summary-card.low {
      background: #dcfce7;
      color: #166534;
      border-color: #86efac;
    }

    .risk-medium,
    .severity-medium,
    .summary-card.medium {
      background: #fef3c7;
      color: #92400e;
      border-color: #fcd34d;
    }

    .risk-high,
    .severity-high,
    .summary-card.high,
    .summary-card.has-findings {
      background: #fee2e2;
      color: #991b1b;
      border-color: #fca5a5;
    }

    .summary-card.no-findings {
      background: #ecfdf5;
      color: #047857;
      border-color: #a7f3d0;
    }

    .summary-card.changed,
    .row-highlight {
      background: rgba(245, 158, 11, 0.13);
    }

    .row-alert {
      background: rgba(239, 68, 68, 0.12);
    }

    .yes-no-yes {
      background: #fee2e2;
      color: #991b1b;
    }

    .yes-no-no {
      background: #e0f2fe;
      color: #075985;
    }

    @media (max-width: 900px) {
      main {
        padding: 20px;
      }

      .report-header,
      .section-heading {
        flex-direction: column;
        align-items: flex-start;
      }

      .summary-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 560px) {
      .summary-grid {
        grid-template-columns: 1fr;
      }

      .summary-card {
        min-height: 90px;
      }
    }
    """

    themes = {
        "default": """
        body {
          background: #f8fafc;
          color: #111827;
        }

        .card,
        .summary-card {
          background-color: #ffffff;
        }

        .card {
          border: 1px solid #e5e7eb;
          box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }

        th {
          background: #1f2937;
          color: #ffffff;
        }

        td {
          border-bottom: 1px solid #e5e7eb;
        }

        .muted,
        .eyebrow {
          color: #64748b;
        }
        """,
        "clean": """
        body {
          background: #ffffff;
          color: #111827;
        }

        main {
          max-width: 1080px;
        }

        .card,
        .summary-card {
          background: #ffffff;
          border: 1px solid #e5e7eb;
        }

        th {
          background: #f3f4f6;
          color: #111827;
        }

        td {
          border-bottom: 1px solid #f3f4f6;
        }

        .muted,
        .eyebrow {
          color: #6b7280;
        }
        """,
        "compact": """
        body {
          background: #ffffff;
          color: #111827;
          font-size: 14px;
        }

        main {
          max-width: 1000px;
          padding: 20px;
        }

        h1 {
          font-size: 26px;
        }

        h2 {
          font-size: 18px;
        }

        h3 {
          font-size: 15px;
          margin-top: 16px;
        }

        .card {
          border-radius: 8px;
          padding: 12px;
          margin-bottom: 12px;
          border: 1px solid #e5e7eb;
        }

        .summary-grid {
          gap: 8px;
        }

        .summary-card {
          border-radius: 8px;
          padding: 12px;
          min-height: 82px;
        }

        .summary-card strong {
          font-size: 22px;
        }

        th,
        td {
          padding: 6px;
        }

        th {
          background: #f3f4f6;
          color: #111827;
        }

        td {
          border-bottom: 1px solid #e5e7eb;
        }

        .muted,
        .eyebrow {
          color: #6b7280;
        }
        """,
        "enterprise": """
        body {
          background: #eef2f7;
          color: #172033;
          font-family: "Segoe UI", Arial, sans-serif;
        }

        main {
          max-width: 1220px;
        }

        .report-header {
          background: linear-gradient(135deg, #0f172a, #1e3a8a);
          color: #ffffff;
          border-radius: 18px;
          padding: 26px;
          box-shadow: 0 14px 40px rgba(15, 23, 42, 0.18);
        }

        .card,
        .summary-card {
          background: #ffffff;
          border: 1px solid #dbe3ef;
          box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        }

        th {
          background: #1e3a8a;
          color: #ffffff;
        }

        td {
          border-bottom: 1px solid #e5e7eb;
        }

        .report-header .muted,
        .report-header .eyebrow {
          color: #cbd5e1;
        }

        .muted,
        .eyebrow {
          color: #64748b;
        }
        """,
        "dark": """
        body {
          background: #020617;
          color: #e5e7eb;
        }

        .card,
        .summary-card {
          background: #0f172a;
          border: 1px solid #1e293b;
          box-shadow: 0 12px 34px rgba(0, 0, 0, 0.35);
        }

        th {
          background: #1e293b;
          color: #f8fafc;
        }

        td {
          border-bottom: 1px solid #1e293b;
          color: #e2e8f0;
        }

        .muted,
        .eyebrow {
          color: #94a3b8;
        }

        .risk-low,
        .severity-low,
        .summary-card.low,
        .summary-card.no-findings {
          background: rgba(34, 197, 94, 0.18);
          color: #bbf7d0;
          border-color: rgba(74, 222, 128, 0.38);
        }

        .risk-medium,
        .severity-medium,
        .summary-card.medium,
        .summary-card.changed {
          background: rgba(245, 158, 11, 0.18);
          color: #fde68a;
          border-color: rgba(251, 191, 36, 0.38);
        }

        .risk-high,
        .severity-high,
        .summary-card.high,
        .summary-card.has-findings,
        .row-alert {
          background: rgba(239, 68, 68, 0.18);
          color: #fecaca;
          border-color: rgba(248, 113, 113, 0.38);
        }

        .row-highlight {
          background: rgba(245, 158, 11, 0.14);
        }

        .yes-no-yes {
          background: rgba(239, 68, 68, 0.22);
          color: #fecaca;
        }

        .yes-no-no {
          background: rgba(14, 165, 233, 0.18);
          color: #bae6fd;
        }
        """,
    }

    return base + themes[template]


def _severity_badge(severity: str | None) -> str:
    safe_severity = _safe(severity or "low").lower()
    return (
        f'<span class="severity-badge severity-{safe_severity}">'
        f"{_safe(severity or 'low')}"
        "</span>"
    )


def _yes_no_badge(value: bool) -> str:
    label = "Yes" if value else "No"
    class_name = "yes-no-yes" if value else "yes-no-no"
    return f'<span class="yes-no-badge {class_name}">{label}</span>'


def _delta_class(value: int | float | None) -> str:
    if value is None:
        return ""

    return "changed" if value != 0 else ""


def _count_class(value: int | float | None) -> str:
    if value is None:
        return "no-findings"

    return "has-findings" if value > 0 else "no-findings"


def _safe_frequency_shifts(shifts: dict[str, float]) -> str:
    if not shifts:
        return ""

    return ", ".join(f"{_safe(value)}: {shift:.2%}" for value, shift in shifts.items())


def _safe_pct(value: float | None) -> str:
    if value is None:
        return ""

    return f"{value:.2%}"


def _safe(value: Any) -> str:
    if value is None:
        return ""
    return escape(str(value))


def _safe_list(values: list[Any]) -> str:
    if not values:
        return ""
    return ", ".join(_safe(value) for value in values)