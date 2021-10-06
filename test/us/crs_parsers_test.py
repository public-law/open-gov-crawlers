from scrapy.selector.unified import Selector

from public_law.parsers.us.colorado.crs import parse_title


def fixture(filename: str) -> str:
    return open(f"test/fixtures/{filename}", encoding="utf8").read()


TITLE_16 = Selector(text=fixture("crs/title16.txt"))


class TestParseTitle:
    def test_name_of_title(self):
        assert parse_title(TITLE_16)["name"] == "Criminal Proceedings"

    def test_division_count(self):
        assert len(parse_title(TITLE_16)["divisions"]) == 8

    def test_divisions_retrieved(self):
        divs = parse_title(TITLE_16)["divisions"]

        assert divs[0] == "Code of Criminal Procedure"
