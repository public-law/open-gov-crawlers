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
