from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

import polars as pl


class BaseReader(ABC):
    """Base interface for all Dift dataset readers."""

    name: str

    @abstractmethod
    def can_handle(self, source: str) -> bool:
        """Return True if this reader can read the source."""

    @abstractmethod
    def read(self, source: str) -> pl.DataFrame:
        """Read source into a Polars DataFrame."""

    def supports_chunks(self, source: str) -> bool:
        """
        Return True if this reader supports chunked reading for the source.

        Readers can override this when they support incremental loading.
        """
        return False

    def read_chunks(self, source: str, chunk_size: int) -> Iterator[pl.DataFrame]:
        """
        Read source incrementally as Polars DataFrame chunks.

        Readers that support chunked loading should override this method.
        """
        raise NotImplementedError(
            f"{self.name} reader does not support chunked reading for source: {source}"
        )