from __future__ import annotations

from collections.abc import Iterable

from dift.io.base_reader import BaseReader
from dift.io.registry import ReaderRegistry


def register_plugin_readers(
    registry: ReaderRegistry,
    readers: Iterable[BaseReader],
) -> None:
    """
    Register plugin-provided readers.

    This is the internal hook that future external connector packages can use.
    """
    for reader in readers:
        registry.register(reader)


def load_plugin_readers() -> list[BaseReader]:
    """
    Load plugin readers.

    Placeholder for future plugin discovery using package entry points.
    """
    return []