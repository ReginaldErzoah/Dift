import pytest

from dift.io.base_reader import BaseReader


def test_base_reader_requires_can_handle_and_read():
    with pytest.raises(TypeError):
        BaseReader()