from __future__ import annotations

from abc import ABC, abstractmethod

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