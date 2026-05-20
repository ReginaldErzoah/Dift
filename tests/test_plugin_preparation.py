import polars as pl

from dift.io.base_reader import BaseReader
from dift.io.plugins import load_plugin_readers, register_plugin_readers
from dift.io.registry import ReaderRegistry


class FakePluginReader(BaseReader):
    name = "fake_plugin"

    supports_tables = True
    supports_queries = False
    supports_streaming = False

    def can_handle(self, source: str) -> bool:
        return source.startswith("fake://")

    def read(self, source: str) -> pl.DataFrame:
        return pl.DataFrame({"source": [source]})


def test_load_plugin_readers_returns_list():
    readers = load_plugin_readers()

    assert isinstance(readers, list)


def test_register_plugin_readers_adds_reader_to_registry():
    registry = ReaderRegistry()

    register_plugin_readers(
        registry=registry,
        readers=[FakePluginReader()],
    )

    reader = registry.get_reader("fake://dataset")

    assert reader is not None
    assert reader.name == "fake_plugin"


def test_plugin_reader_can_read_dataset():
    registry = ReaderRegistry()

    register_plugin_readers(
        registry=registry,
        readers=[FakePluginReader()],
    )

    reader = registry.get_reader("fake://dataset")

    assert reader is not None

    df = reader.read("fake://dataset")

    assert df.height == 1
    assert df["source"][0] == "fake://dataset"