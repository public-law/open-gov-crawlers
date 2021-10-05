from scrapy.selector import Selector
from typing import Any, IO
from public_law.parsers.us.colorado import parse_division


def fixture(filename: str) -> IO[Any]:
    return open(f"test/fixtures/{filename}")
