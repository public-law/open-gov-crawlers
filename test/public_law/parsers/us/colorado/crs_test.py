from scrapy.selector.unified import Selector

from public_law.parsers.us.colorado.crs import parse_title


def fixture(filename: str) -> str:
    return open(f"test/fixtures/{filename}", encoding="utf8").read()


# A Title with no Divisions.
TITLE_4 = Selector(text=fixture("crs/title04.txt"))
PARSED_TITLE_4 = parse_title(TITLE_4)

# A Title which uses Divisions.
TITLE_16 = Selector(text=fixture("crs/title16.txt"))
PARSED_TITLE_16 = parse_title(TITLE_16)


class TestParseTitle:
    def test_name_of_title_16(self):
        assert PARSED_TITLE_16.name == "Criminal Proceedings"

    def test_url_of_title_16(self):
        assert (
            PARSED_TITLE_16.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2021-title-16.pdf"
        )

    def test_url_of_title_4(self):
        assert (
            PARSED_TITLE_4.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2021-title-04.pdf"
        )

    def test_name_of_title_4(self):
        assert PARSED_TITLE_4.name == "Uniform Commercial Code"

    def test_title_number_16(self):
        assert PARSED_TITLE_16.number == "16"

    def test_title_number_4(self):
        assert PARSED_TITLE_4.number == "4"

    def test_division_count(self):
        assert len(PARSED_TITLE_16.divisions) == 8

    def test_first_division_retrieved(self):
        divs = PARSED_TITLE_16.divisions

        assert divs[0].name == "Code of Criminal Procedure"

    def test_last_division_retrieved(self):
        divs = PARSED_TITLE_16.divisions

        assert divs[-1].name == "Offenders - Registration"

    def test_url_of_title_16_last_division(self):
        last_division = PARSED_TITLE_16.divisions[-1]

        assert (
            last_division.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2021-title-16.pdf"
        )

    def test_no_divisions(self):
        divs = PARSED_TITLE_4.divisions

        assert len(divs) == 0
