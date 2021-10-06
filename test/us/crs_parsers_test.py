from scrapy.selector import Selector

from public_law.parsers.us.colorado import parse_title


def fixture(filename: str) -> str:
    return open(f"test/fixtures/{filename}", encoding="utf8").read()


class TestParseTitle:
    def test_title_of_title(self):
        assert parse_title(TITLE_16)["name"] == "Criminal Proceedings"
