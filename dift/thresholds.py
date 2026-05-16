from __future__ import annotations

from pydantic import BaseModel, Field


class ColumnThresholds(BaseModel):
    numeric: float | None = None
    categorical: float | None = None
    outlier: float | None = None


class ThresholdConfig(BaseModel):
    numeric: float = 0.1
    categorical: float = 0.1
    outlier: float = 0.1
    columns: dict[str, ColumnThresholds] = Field(default_factory=dict)

    def numeric_for(self, column: str) -> float:
        override = self.columns.get(column)
        if override and override.numeric is not None:
            return override.numeric
        return self.numeric

    def categorical_for(self, column: str) -> float:
        override = self.columns.get(column)
        if override and override.categorical is not None:
            return override.categorical
        return self.categorical

    def outlier_for(self, column: str) -> float:
        override = self.columns.get(column)
        if override and override.outlier is not None:
            return override.outlier
        return self.outlier


def resolve_threshold_config(
    config_data: dict[str, object],
    cli_threshold: float,
    default_threshold: float,
) -> ThresholdConfig:
    raw_thresholds = config_data.get("thresholds", {})

    base_threshold = float(config_data.get("threshold", default_threshold))

    numeric = float(raw_thresholds.get("numeric", base_threshold))
    categorical = float(raw_thresholds.get("categorical", base_threshold))
    outlier = float(raw_thresholds.get("outlier", base_threshold))

    # CLI threshold remains backward-compatible and overrides default numeric threshold.
    if cli_threshold != default_threshold:
        numeric = cli_threshold

    return ThresholdConfig(
        numeric=numeric,
        categorical=categorical,
        outlier=outlier,
        columns=raw_thresholds.get("columns", {}),
    )