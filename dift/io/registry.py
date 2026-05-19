from __future__ import annotations

from pathlib import Path

from dift.io.base_reader import BaseReader


class ReaderRegistry:
    """Registry for dataset readers."""

    def __init__(self) -> None:
        self._readers: list[BaseReader] = []

    def register(self, reader: BaseReader) -> None:
        """Register a dataset reader."""
        self._readers.append(reader)

    def get_reader(self, source: str | Path) -> BaseReader | None:
        """Return the first reader that can handle the source."""
        source_str = str(source)

        for reader in self._readers:
            if reader.can_handle(source_str):
                return reader

        return None

    def list_readers(self) -> list[str]:
        """Return registered reader names."""
        return [reader.name for reader in self._readers]