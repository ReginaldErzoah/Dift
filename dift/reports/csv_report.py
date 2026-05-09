from __future__ import annotations

from pathlib import Path

from dift.reports.models import DiffReport


def render_csv(report: DiffReport, output: str | None = None) -> str:
    """Render and optionally write a CSV summary report."""

    null_spikes = sum(1 for diff in report.quality_diff.null_diffs if diff.is_spike)

    rows = [
        "metric,value",
        f"old_rows,{report.summary.old_rows}",
        f"new_rows,{report.summary.new_rows}",
        f"row_delta,{report.summary.row_delta}",
        f"old_columns,{report.summary.old_columns}",
        f"new_columns,{report.summary.new_columns}",
        f"column_delta,{report.summary.column_delta}",
        f"columns_added,{len(report.schema_diff.columns_added)}",
        f"columns_removed,{len(report.schema_diff.columns_removed)}",
        f"type_changes,{len(report.schema_diff.type_changes)}",
        f"added_rows,{report.row_diff.added_rows or 0}",
        f"removed_rows,{report.row_diff.removed_rows or 0}",
        f"changed_rows,{report.row_diff.changed_rows or 0}",
        f"unchanged_rows,{report.row_diff.unchanged_rows or 0}",
        f"null_spikes,{null_spikes}",
        f"duplicate_delta,{report.quality_diff.duplicate_diff.delta_duplicates}",
        f"old_duplicate_pct,{report.quality_diff.duplicate_diff.old_duplicate_pct}",
        f"new_duplicate_pct,{report.quality_diff.duplicate_diff.new_duplicate_pct}",
        f"delta_duplicate_pct,{report.quality_diff.duplicate_diff.delta_duplicate_pct}",
        f"duplicate_spike,{report.quality_diff.duplicate_diff.is_spike}",
        f"duplicate_severity,{report.quality_diff.duplicate_diff.severity}",
        f"numeric_drift_columns,{len(report.numeric_diff)}",
        f"categorical_drift_columns,{len(report.categorical_diff)}",
        f"risk_level,{report.summary.risk_level}",
    ]

    payload = "\n".join(rows) + "\n"

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")

    return payload