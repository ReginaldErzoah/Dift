from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from dift.reports.models import DiffReport


def render_html(report: DiffReport, output: str | None = None) -> Path:
    output_path = Path(output or "dift_report.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html = _build_html(report)
    output_path.write_text(html, encoding="utf-8")

    return output_path


def _build_html(report: DiffReport) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dift Report</title>
</head>
<body>
  <h1>Dift Dataset Diff Report</h1>

  <h2>Summary</h2>
  <table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>Old rows</td><td>{report.summary.old_rows}</td></tr>
    <tr><td>New rows</td><td>{report.summary.new_rows}</td></tr>
    <tr><td>Row delta</td><td>{report.summary.row_delta}</td></tr>
    <tr><td>Risk level</td><td>{_safe(report.summary.risk_level)}</td></tr>
  </table>

  <h2>Schema Diff</h2>
  <p>Columns added: {_safe_list(report.schema_diff.columns_added)}</p>

  <h2>Row Diff</h2>
  <p>Key: {_safe(report.row_diff.key)}</p>

  <h2>Quality Diff</h2>
  <p>Duplicate basis: {_safe(report.quality_diff.duplicate_diff.duplicate_basis)}</p>
</body>
</html>
"""


def _safe(value: Any) -> str:
    if value is None:
        return ""
    return escape(str(value))


def _safe_list(values: list[Any]) -> str:
    return ", ".join(_safe(value) for value in values)