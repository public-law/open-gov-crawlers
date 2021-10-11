from scrapy.selector.unified import Selector
from public_law.items.crs import Title

from public_law.parsers.us.colorado.crs import parse_title


def fixture(filename: str) -> str:
    return open(f"./test/fixtures/{filename}", encoding="utf8").read()


# A Title with no Divisions.
TITLE_4 = Selector(text=fixture("crs/title04.xml"))
PARSED_TITLE_4 = parse_title(TITLE_4)

# A Title which uses Divisions.
TITLE_16 = Selector(text=fixture("crs/title16.xml"))
PARSED_TITLE_16 = parse_title(TITLE_16)


class TestParseTitle:
    def test_title_16_name(self):
        assert PARSED_TITLE_16.name == "Criminal Proceedings"

    def test_title_16_url(self):
        assert (
            PARSED_TITLE_16.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2021-title-16.pdf"
        )

    def test_title_4_url(self):
        assert (
            PARSED_TITLE_4.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2021-title-04.pdf"
        )

    def test_title_4_name(self):
        assert PARSED_TITLE_4.name == "Uniform Commercial Code"

    def test_title_16_number(self):
        assert PARSED_TITLE_16.number == "16"

    def test_title_4_number(self):
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

    def test_correct_number_of_articles_in_division(self):
        code_of_crim_pro = PARSED_TITLE_16.divisions[0]
        # Verify we have the correct Division.
        assert code_of_crim_pro.name == "Code of Criminal Procedure"

        assert len(code_of_crim_pro.articles) == 21

    # def we_can_get_a_div_editors_note(self):
    #     div_1 = PARSED_TITLE_16.divisions[0]

    #     assert (
    #         div_1.editors_note
    #         == "Articles 1 to 13 of this title (excluding articles 2.5, 2.7, 8.5, 11.3, 11.5, 11.7, 11.8, and 11.9) were numbered as articles 1 to 13 of chapter 39, C.R.S. 1963. The provisions of those articles were repealed and reenacted in 1972, resulting in the addition, relocation, and elimination of sections as well as subject matter. For amendments to those articles prior to 1972, consult the Colorado statutory research explanatory note beginning on page vii in the front of this volume. For a detailed comparison of those articles, see the comparative tables located in the back of the index."
    #     )
