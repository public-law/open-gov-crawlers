from typing import cast

from scrapy.selector.unified import Selector

from public_law.test_util import fixture
from public_law.parsers.usa.colorado.crs import parse_title
from public_law.items.crs import Division


# A Title with no Divisions.
# TITLE_4 = Selector(text = fixture('usa', 'crs', "title04.xml"))
# PARSED_TITLE_4 = parse_title(TITLE_4)

# A Title which uses Divisions.
TITLE_16 = Selector(text = fixture('usa', 'crs', "title16.xml"))
PARSED_TITLE_16 = parse_title(TITLE_16)



class TestParseSection:
    def test_article_has_correct_number_of_sections_1(self):
        code_of_crim_pro   = cast(Division, PARSED_TITLE_16.children[0])
        general_provisions = code_of_crim_pro.articles[0]

        assert len(general_provisions.sections) == 10


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
