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
            f"Unsupported HTML template '{template}'. "
            f"Supported templates: {supported}"
        )

    output_path = Path(output or "dift_report.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html = _build_html(report, template=template)
    output_path.write_text(html, encoding="utf-8")

    return output_path


def _build_html(report: DiffReport, template: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
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
      <div class="risk-badge">Risk: {_safe(report.summary.risk_level)}</div>
    </header>

    {_summary_section(report)}
    {_schema_section(report)}
    {_row_section(report)}
    {_quality_section(report)}

  </main>
</body>
</html>
"""


def _summary_section(report: DiffReport) -> str:
    return f"""
    <section class="card">
      <h2>Summary</h2>
      <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Old rows</td><td>{report.summary.old_rows}</td></tr>
        <tr><td>New rows</td><td>{report.summary.new_rows}</td></tr>
        <tr><td>Row delta</td><td>{report.summary.row_delta}</td></tr>
        <tr><td>Old columns</td><td>{report.summary.old_columns}</td></tr>
        <tr><td>New columns</td><td>{report.summary.new_columns}</td></tr>
        <tr><td>Column delta</td><td>{report.summary.column_delta}</td></tr>
        <tr><td>Risk level</td><td>{_safe(report.summary.risk_level)}</td></tr>
      </table>
    </section>
    """


def _schema_section(report: DiffReport) -> str:
    type_rows = ""

    for change in report.schema_diff.type_changes:
        type_rows += (
            "<tr>"
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
        <tr><td>Columns added</td><td>{_safe_list(report.schema_diff.columns_added)}</td></tr>
        <tr><td>Columns removed</td><td>{_safe_list(report.schema_diff.columns_removed)}</td></tr>
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
        <tr><td>Added rows</td><td>{_safe(row_diff.added_rows)}</td></tr>
        <tr><td>Removed rows</td><td>{_safe(row_diff.removed_rows)}</td></tr>
        <tr><td>Changed rows</td><td>{_safe(row_diff.changed_rows)}</td></tr>
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
        null_rows += (
            "<tr>"
            f"<td>{_safe(item.column)}</td>"
            f"<td>{item.old_nulls}</td>"
            f"<td>{item.new_nulls}</td>"
            f"<td>{item.old_null_pct:.2f}%</td>"
            f"<td>{item.new_null_pct:.2f}%</td>"
            f"<td>{item.delta_null_pct:.2f}%</td>"
            f"<td>{'Yes' if item.is_spike else 'No'}</td>"
            f"<td>{_safe(item.severity)}</td>"
            "</tr>"
        )

    if not null_rows:
        null_rows = '<tr><td colspan="8">No null changes detected.</td></tr>'

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
        <tr><td>Delta duplicates</td><td>{duplicate.delta_duplicates}</td></tr>
        <tr><td>Old duplicate %</td><td>{duplicate.old_duplicate_pct:.2f}%</td></tr>
        <tr><td>New duplicate %</td><td>{duplicate.new_duplicate_pct:.2f}%</td></tr>
        <tr><td>Delta duplicate %</td><td>{duplicate.delta_duplicate_pct:.2f}%</td></tr>
        <tr><td>Duplicate basis</td><td>{_safe(duplicate.duplicate_basis)}</td></tr>
        <tr><td>Spike</td><td>{"Yes" if duplicate.is_spike else "No"}</td></tr>
        <tr><td>Severity</td><td>{_safe(duplicate.severity)}</td></tr>
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
      font-family: Arial, sans-serif;
      line-height: 1.5;
    }

    main {
      max-width: 1120px;
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
      font-size: 32px;
    }

    h2 {
      margin-top: 0;
    }

    h3 {
      margin-top: 24px;
      margin-bottom: 8px;
    }

    .eyebrow {
      margin: 0 0 4px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 12px;
      font-weight: bold;
    }

    .muted {
      margin: 4px 0 0;
      font-size: 14px;
    }

    .risk-badge {
      border-radius: 999px;
      padding: 8px 14px;
      font-weight: bold;
      white-space: nowrap;
    }

    .card {
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }

    th,
    td {
      text-align: left;
      padding: 10px;
      vertical-align: top;
    }
    """

    themes = {
        "default": """
        body {
          background: #f9fafb;
          color: #111827;
        }

        .card {
          background: #ffffff;
          border: 1px solid #e5e7eb;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
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
          color: #6b7280;
        }

        .risk-badge {
          background: #fef3c7;
          color: #92400e;
        }
        """,
        "clean": """
        body {
          background: #ffffff;
          color: #111827;
        }

        main {
          max-width: 1040px;
        }

        .card {
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

        .risk-badge {
          background: #eef2ff;
          color: #3730a3;
        }
        """,
        "compact": """
        body {
          background: #ffffff;
          color: #111827;
          font-size: 14px;
        }

        main {
          max-width: 980px;
          padding: 20px;
        }

        h1 {
          font-size: 24px;
        }

        h2 {
          font-size: 18px;
        }

        h3 {
          font-size: 15px;
          margin-top: 16px;
        }

        .card {
          border-radius: 0;
          padding: 12px;
          margin-bottom: 12px;
          border: 1px solid #e5e7eb;
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

        .risk-badge {
          background: #f3f4f6;
          color: #111827;
          padding: 6px 10px;
        }
        """,
        "enterprise": """
        body {
          background: #eef2f7;
          color: #172033;
          font-family: "Segoe UI", Arial, sans-serif;
        }

        main {
          max-width: 1180px;
        }

        .report-header {
          background: linear-gradient(135deg, #0f172a, #1e3a8a);
          color: #ffffff;
          border-radius: 16px;
          padding: 24px;
        }

        .card {
          background: #ffffff;
          border: 1px solid #dbe3ef;
          box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        }

        th {
          background: #1e3a8a;
          color: #ffffff;
        }

        td {
          border-bottom: 1px solid #e5e7eb;
        }

        .muted,
        .eyebrow {
          color: #cbd5e1;
        }

        .risk-badge {
          background: #ffffff;
          color: #1e3a8a;
        }
        """,
        "dark": """
        body {
          background: #020617;
          color: #e5e7eb;
        }

        .card {
          background: #0f172a;
          border: 1px solid #1e293b;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }

        th {
          background: #334155;
          color: #f8fafc;
        }

        td {
          border-bottom: 1px solid #1e293b;
        }

        .muted,
        .eyebrow {
          color: #94a3b8;
        }

        .risk-badge {
          background: #7f1d1d;
          color: #fecaca;
        }
        """,
    }

    return base + themes[template]


def _safe(value: Any) -> str:
    if value is None:
        return ""
    return escape(str(value))


def _safe_list(values: list[Any]) -> str:
    if not values:
        return ""
    return ", ".join(_safe(value) for value in values)