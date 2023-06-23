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



class TestParseTitles:
    def test_title_name_1(self):
        assert PARSED_TITLE_16.name == "Criminal Proceedings"

    def test_title_name_2(self):
        assert PARSED_TITLE_4.name == "Uniform Commercial Code"


    def test_title_url_1(self):
        assert (
            PARSED_TITLE_16.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-16.pdf"
        )

    def test_title_url_2(self):
        assert (
            PARSED_TITLE_4.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-04.pdf"
        )


    def test_title_number_1(self):
        assert PARSED_TITLE_16.number == "16"

    def test_title_number_2(self):
        assert PARSED_TITLE_4.number == "4"



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



class TestParseArticles:
    def test_correct_number_of_articles_in_a_division_1(self):
        # Title 16 contains eight Divisions.
        #   The first Division is _Code of Criminal Procedure_
        #       This Division contains 22 Articles.
        div_1_code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])

        assert div_1_code_of_crim_pro.name          == "Code of Criminal Procedure"
        assert len(div_1_code_of_crim_pro.articles) == 22

    def test_correct_number_of_articles_in_a_division_2(self):
        division_2 = cast(Division, PARSED_TITLE_16.children[1])
        
        assert division_2.name          == "Uniform Mandatory Disposition of Detainers Act"
        assert len(division_2.articles) == 1


    def test_article_number_1(self):
        code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])
        article_1        = code_of_crim_pro.articles[0]

        assert article_1.number == "1"

    def test_article_name_1(self):
        code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])
        article_1        = code_of_crim_pro.articles[0]

        assert article_1.name == "General Provisions"

    def test_article_url_1(self):
        code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])
        article_1        = code_of_crim_pro.articles[0]

        assert article_1.source_url == "https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-16.pdf"


class TestParseSection:
    def test_article_has_sections_1(self):
        code_of_crim_pro   = cast(Division, PARSED_TITLE_16.children[0])
        general_provisions = code_of_crim_pro.articles[0]

        assert len(general_provisions.sections) == 10


    def test_section_number_1(self):
        code_of_crim_pro   = cast(Division, PARSED_TITLE_16.children[0])
        general_provisions = code_of_crim_pro.articles[0]
        first_section      = general_provisions.sections[0]

        assert first_section.number == "16-1-101"


    def test_section_name_1(self):
        code_of_crim_pro   = cast(Division, PARSED_TITLE_16.children[0])
        general_provisions = code_of_crim_pro.articles[0]
        first_section      = general_provisions.sections[0]

        assert first_section.name == "Short Title"


    # def we_can_get_a_div_editors_note(self):
    #     div_1 = PARSED_TITLE_16.children[0]

    #     assert (
    #         div_1.editors_note
    #         == "Articles 1 to 13 of this title (excluding articles 2.5, 2.7, 8.5, 11.3, 11.5, 11.7, 11.8, and 11.9) were numbered as articles 1 to 13 of chapter 39, C.R.S. 1963. The provisions of those articles were repealed and reenacted in 1972, resulting in the addition, relocation, and elimination of sections as well as subject matter. For amendments to those articles prior to 1972, consult the Colorado statutory research explanatory note beginning on page vii in the front of this volume. For a detailed comparison of those articles, see the comparative tables located in the back of the index."
    #     )

    # def test_article_has_correct_number_of_sections
