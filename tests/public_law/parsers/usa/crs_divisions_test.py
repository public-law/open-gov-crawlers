from typing import cast

from scrapy.selector.unified import Selector

from public_law.parsers.usa.colorado.crs import parse_title
from public_law.items.crs import Division


def fixture(filename: str) -> str:
    return open(f"tests/fixtures/usa/crs/{filename}", encoding="utf8").read()


# A Title with no Divisions.
TITLE_4 = Selector(text=fixture("title04.xml"))
PARSED_TITLE_4 = parse_title(TITLE_4)

# A Title which uses Divisions.
TITLE_16 = Selector(text=fixture("title16.xml"))
PARSED_TITLE_16 = parse_title(TITLE_16)



class TestParseDivisions:
    def test_correct_number_of_divisions_1(self):
        assert len(PARSED_TITLE_16.children) == 8

    def test_correct_number_of_divisions_2(self):
        assert len(PARSED_TITLE_4.children) == 0


    def test_first_division_retrieved(self):
        divs = PARSED_TITLE_16.children

        assert divs[0].name == "Code of Criminal Procedure"

    def test_last_division_retrieved(self):
        divs = PARSED_TITLE_16.children

        assert divs[-1].name == "Offenders - Registration"


    def test_division_source_url(self):
        last_division = PARSED_TITLE_16.children[-1]

        assert (
            last_division.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-16.pdf"
        )
