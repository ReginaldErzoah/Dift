from __future__ import annotations

from pathlib import Path

import polars as pl

SUPPORTED_EXTENSIONS = {".csv", ".parquet", ".xlsx", ".xls"}


class DatasetReadError(ValueError):
    """Raised when Dift cannot read a dataset."""


def read_dataset(path: str | Path) -> pl.DataFrame:
    """Read a local CSV or Parquet dataset into a Polars DataFrame."""
    dataset_path = Path(path)

    if not dataset_path.exists():
        raise DatasetReadError(f"Dataset not found: {dataset_path}")

    suffix = dataset_path.suffix.lower()

    if suffix == ".csv":
        return pl.read_csv(dataset_path)

    if suffix == ".parquet":
        return pl.read_parquet(dataset_path)
    
    if suffix in {".xlsx", ".xls"}:
        return pl.read_excel(dataset_path)

    raise DatasetReadError(
        f"Unsupported dataset type '{suffix}'. Supported types: {sorted(SUPPORTED_EXTENSIONS)}"
    )
