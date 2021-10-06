from scrapy.selector.unified import Selector

from public_law.parsers.us.colorado.crs import parse_title


def fixture(filename: str) -> str:
    return open(f"test/fixtures/{filename}", encoding="utf8").read()


# A title with no Divisions.
TITLE_4 = Selector(text=fixture("crs/title04.txt"))

# A title which does use Divisions.
TITLE_16 = Selector(text=fixture("crs/title16.txt"))


class TestParseTitle:
    def test_name_of_title_1(self):
        assert parse_title(TITLE_16)["name"] == "Criminal Proceedings"

    def test_name_of_title_2(self):
        assert parse_title(TITLE_4)["name"] == "Uniform Commercial Code"

    def test_division_count(self):
        assert len(parse_title(TITLE_16)["divisions"]) == 8

    def test_first_division_retrieved(self):
        divs = parse_title(TITLE_16)["divisions"]

        assert divs[0] == "Code of Criminal Procedure"

    def test_last_division_retrieved(self):
        divs = parse_title(TITLE_16)["divisions"]

        assert divs[-1] == "Offenders - Registration"

    def test_no_divisions(self):
        divs = parse_title(TITLE_4)["divisions"]

        assert len(divs) == 0
