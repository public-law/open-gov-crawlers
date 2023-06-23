from scrapy.selector.unified import Selector

from public_law.test_util import fixture
from public_law.parsers.usa.colorado.crs import parse_sections


# A Title which uses Divisions.
TITLE_16 = Selector(text = fixture('usa', 'crs', "title16.xml"))
TITLE_16_SECTIONS = parse_sections(TITLE_16)


class TestParseSection:
    def test_article_has_correct_number_of_sections_1(self):
        """The parsing strategy is JSON lines. And so there isn't a
        direct API for this.
        """

        art_1_sections = [s for s in TITLE_16_SECTIONS if s.article_number == "1"]

        assert len(art_1_sections) == 10


    # def test_section_number_1(self):
    #     code_of_crim_pro   = cast(Division, PARSED_TITLE_16.children[0])
    #     general_provisions = code_of_crim_pro.articles[0]
    #     first_section      = general_provisions.sections[0]

    #     assert first_section.number == "16-1-101"


    # def test_section_name_1(self):
    #     code_of_crim_pro   = cast(Division, PARSED_TITLE_16.children[0])
    #     general_provisions = code_of_crim_pro.articles[0]
    #     first_section      = general_provisions.sections[0]

    #     assert first_section.name == "Short Title"
