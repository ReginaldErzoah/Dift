from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTENSIONS = {".csv", ".parquet", ".xlsx", ".xls", ".json"}


def find_dataset_pairs(old_dir: str, new_dir: str) -> list[tuple[Path, Path]]:
    """Find matching dataset files by filename in old and new directories."""
    old_path = Path(old_dir)
    new_path = Path(new_dir)

    if not old_path.exists():
        raise ValueError(f"Old directory does not exist: {old_dir}")

    if not new_path.exists():
        raise ValueError(f"New directory does not exist: {new_dir}")

    old_files = {
        file.name: file
        for file in old_path.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    }

    new_files = {
        file.name: file
        for file in new_path.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    }

    shared_names = sorted(set(old_files) & set(new_files))

    return [(old_files[name], new_files[name]) for name in shared_names]