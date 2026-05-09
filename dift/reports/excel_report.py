from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from dift.reports.models import DiffReport


def render_excel(report: DiffReport, output: str | None = None) -> Path:
    """
    Render and write an Excel report.

    Excel reports should always be written to a file.
    """

    output_path = Path(output or "dift_report.xlsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"

    _add_summary_sheet(ws, report)
    _add_quality_sheet(wb, report)

    wb.save(output_path)
    return output_path


def _add_summary_sheet(ws, report: DiffReport) -> None:
    rows = [
        ["Metric", "Value"],
        ["old_rows", report.summary.old_rows],
        ["new_rows", report.summary.new_rows],
        ["row_delta", report.summary.row_delta],
        ["risk_level", report.summary.risk_level],
    ]

    for row in rows:
        ws.append(row)

    _style_header(ws)
    _auto_size_columns(ws)
    ws.freeze_panes = "A2"


def _add_quality_sheet(wb: Workbook, report: DiffReport) -> None:
    ws = wb.create_sheet("Quality Diff")

    rows = [
        [
            "Column",
            "Old Nulls",
            "New Nulls",
            "Old Null %",
            "New Null %",
            "Delta Null %",
            "Spike",
            "Severity",
        ]
    ]

    for item in report.quality_diff.null_diffs:
        rows.append(
            [
                item.column,
                item.old_nulls,
                item.new_nulls,
                item.old_null_pct,
                item.new_null_pct,
                item.delta_null_pct,
                "Yes" if item.is_spike else "No",
                item.severity,
            ]
        )

    duplicate = report.quality_diff.duplicate_diff

    rows.extend(
        [
            [],
            ["Duplicate Metric", "Value"],
            ["Old duplicates", duplicate.old_duplicates],
            ["New duplicates", duplicate.new_duplicates],
            ["Delta duplicates", duplicate.delta_duplicates],
            ["Old duplicate %", duplicate.old_duplicate_pct],
            ["New duplicate %", duplicate.new_duplicate_pct],
            ["Delta duplicate %", duplicate.delta_duplicate_pct],
            ["Duplicate basis", duplicate.duplicate_basis],
            ["Spike", "Yes" if duplicate.is_spike else "No"],
            ["Severity", duplicate.severity],
        ]
    )
    
    for row in rows:
        ws.append(row)

    _style_header(ws)
    _auto_size_columns(ws)
    ws.freeze_panes = "A2"


def _style_header(ws) -> None:
    header_fill = PatternFill("solid", fgColor="1F2937")
    header_font = Font(color="FFFFFF", bold=True)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font


def _auto_size_columns(ws) -> None:
    for column_cells in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column_cells[0].column)

        for cell in column_cells:
            value = "" if cell.value is None else str(cell.value)
            max_length = max(max_length, len(value))

        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)