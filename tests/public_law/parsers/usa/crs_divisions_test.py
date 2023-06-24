from scrapy.http.response.xml import XmlResponse

from public_law.test_util import fixture
from public_law.parsers.usa.colorado.crs import parse_title_bang


# Divisions aren't parsing correctly.
TITLE_1 =  XmlResponse(body = fixture('usa', 'crs', "title01.xml"), url = "title01.xml", encoding = "utf-8")
PARSED_TITLE_1 = parse_title_bang(TITLE_1)

# A Title with no Divisions.
TITLE_4 =  XmlResponse(body = fixture('usa', 'crs', "title04.xml"), url = "title04.xml", encoding = "utf-8")
PARSED_TITLE_4 = parse_title_bang(TITLE_4)

# A Title which uses Divisions.
TITLE_16 = XmlResponse(body = fixture('usa', 'crs', "title16.xml"), url = "title16.xml", encoding = "utf-8")
PARSED_TITLE_16 = parse_title_bang(TITLE_16)


class TestParseErrors:
    def test_name(self):
        divs = PARSED_TITLE_1.children
        assert divs[0].name == "General, Primary, Recall, and Congressional Vacancy Elections"


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

    # def we_can_get_a_div_editors_note(self):
    #     div_1 = PARSED_TITLE_16.children[0]

    #     assert (
    #         div_1.editors_note
    #         == "Articles 1 to 13 of this title (excluding articles 2.5, 2.7, 8.5, 11.3, 11.5, 11.7, 11.8, and 11.9) were numbered as articles 1 to 13 of chapter 39, C.R.S. 1963. The provisions of those articles were repealed and reenacted in 1972, resulting in the addition, relocation, and elimination of sections as well as subject matter. For amendments to those articles prior to 1972, consult the Colorado statutory research explanatory note beginning on page vii in the front of this volume. For a detailed comparison of those articles, see the comparative tables located in the back of the index."
    #     )
