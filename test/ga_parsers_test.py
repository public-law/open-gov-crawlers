import pytest

from typing import Any, IO


def fixture(filename: str) -> IO[Any]:
    return open(f"test/fixtures/{filename}")
