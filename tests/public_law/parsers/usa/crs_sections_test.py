from scrapy.selector.unified import Selector

from public_law.test_util import fixture
from public_law.parsers.usa.colorado.crs import parse_sections


# A Title which uses Divisions.
TITLE_16 = Selector(text = fixture('usa', 'crs', "title16.xml"))
TITLE_16_SECTIONS = parse_sections(TITLE_16)
ARTICLE_1_SECTIONS = [s for s in TITLE_16_SECTIONS if s.article_number == "1"]


class TestParseSection:
    def test_article_has_correct_number_of_sections_1(self):
        """The parsing strategy is JSON lines. And so there isn't a
        direct API for this.
        """
        assert len(ARTICLE_1_SECTIONS) == 10


    def test_section_number_1(self):
        first_section  = ARTICLE_1_SECTIONS[0]

        assert first_section.number == "16-1-101"


    def test_section_name_1(self):
        first_section  = ARTICLE_1_SECTIONS[0]

        assert first_section.name == "Short title"
